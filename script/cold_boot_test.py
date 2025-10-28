#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SmartThings + 시리얼 부팅 감지 + 사이클별 결과요약 
python3 cold_boot_test.py \
  --cli ./smartthings \
  --device-id "$SMARTTHINGS_DEVICEID" \
  --token "$SMARTTHINGS_TOKEN" \
  --cycles 100 \
  --off-hold 20 \
  --pre-on-min 10 \
  --pre-on-max 60 \
  --countdown-step 5 \
  --serial-port /dev/ttyUSB1 \
  --baudrate 115200 \
  --boot-timeout 120 \
  --boot-pattern "HDMI Init" \
  --log coldboot_results.csv
"""
import argparse
import csv
import json
import os
import random
import re
import signal
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

try:
    import serial  # pyserial 필요
except ImportError:
    print("pyserial이 필요합니다. 설치: pip install pyserial", file=sys.stderr)
    sys.exit(1)

STOP_REQUESTED = False

OK_STRINGS = ("Command executed successfully", "request completed")
PAT_TOO_MANY = re.compile(r"Too\s*Many\s*Requests", re.I)
PAT_429 = re.compile(r"\b429\b")

BOOT_DONE_PATTERNS = [
    re.compile(r"Boot animation end", re.I),
    re.compile(r"HDMI Init", re.I),
    re.compile(r"boot completed", re.I),
]

def now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def eprint(msg: str) -> None:
    sys.stderr.write(msg + "\n")
    sys.stderr.flush()

def run_cmd(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def is_rate_limited(out: str) -> bool:
    return bool(PAT_TOO_MANY.search(out) or PAT_429.search(out))

def smartthings_command(cli: str, dev: str, token: Optional[str], action: str,
                        max_retries: int = 5, base_sleep: float = 2.0) -> Tuple[bool, str]:
    """SmartThings on/off 명령 수행 및 결과 반환"""
    attempt = 0
    while True:
        if STOP_REQUESTED:
            return False, "Interrupted"
        base = [cli, "devices:commands", dev, f"switch:{action}"]
        if token:
            base += ["-t", token]
        cp = run_cmd(base)
        out = (cp.stdout or "") + (cp.stderr or "")
        ok = (cp.returncode == 0) and any(s in out for s in OK_STRINGS)
        if ok:
            return True, "OK"
        if attempt < max_retries and is_rate_limited(out):
            sleep_s = base_sleep * (2 ** attempt)
            eprint(f"[{now_str()}] 429 Too Many Requests → retry in {sleep_s:.1f}s ...")
            time.sleep(sleep_s)
            attempt += 1
            continue
        # 최종 실패
        err = out.strip().splitlines()[-1] if out.strip() else "unknown error"
        return False, err

def countdown(total: int, step: int, label="pre-on"):
    remain = total
    while remain > 0 and not STOP_REQUESTED:
        tick = min(step, remain)
        time.sleep(tick)
        remain -= tick
        print(f"[{now_str()}] {label} countdown: {remain}s remaining")

def monitor_serial_for_boot(port: str, baud: int, timeout_s: int, patterns) -> Tuple[bool, Optional[str], float]:
    """시리얼에서 부팅 완료 문자열 탐지."""
    try:
        ser = serial.Serial(port, baudrate=baud, timeout=1)
    except Exception as e:
        eprint(f"[{now_str()}] serial open failed: {e}")
        return False, None, 0.0

    start = time.monotonic()
    deadline = start + timeout_s
    matched_line = None
    try:
        while time.monotonic() < deadline and not STOP_REQUESTED:
            line = ser.readline().decode(errors="ignore").strip()
            if not line:
                continue
            print(f"[SERIAL] {line}")
            for pat in patterns:
                if pat.search(line):
                    matched_line = line
                    elapsed = time.monotonic() - start
                    print(f"[BOOT] pattern detected: '{line}' ({elapsed:.2f}s)")
                    return True, matched_line, elapsed
        elapsed = time.monotonic() - start
        print(f"[BOOT] timeout ({elapsed:.2f}s) — no pattern matched")
        return False, None, elapsed
    finally:
        ser.close()

def open_csv_logger(path: Optional[str]):
    if not path:
        return None, None
    p = Path(path)
    new = not p.exists()
    f = p.open("a", newline="", encoding="utf-8")
    w = csv.writer(f)
    if new:
        w.writerow(["time", "cycle", "smartthings", "boot_result", "elapsed_s", "note"])
        f.flush()
    return f, w

def setup_signal_handlers():
    def handler(signum, frame):
        global STOP_REQUESTED
        STOP_REQUESTED = True
        eprint(f"[{now_str()}] received signal {signum}. stopping...")
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)

def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="SmartPlug + Serial Boot Detector (Final)")
    ap.add_argument("--cli", default="smartthings")
    ap.add_argument("--device-id", required=True)
    ap.add_argument("--token", default=os.environ.get("SMARTTHINGS_TOKEN"))
    ap.add_argument("--cycles", type=int, default=1)
    ap.add_argument("--off-hold", type=int, default=10)
    ap.add_argument("--pre-on-min", type=int, default=0)
    ap.add_argument("--pre-on-max", type=int, default=0)
    ap.add_argument("--countdown-step", type=int, default=5)
    ap.add_argument("--serial-port", default="/dev/ttyUSB1")
    ap.add_argument("--baudrate", type=int, default=115200)
    ap.add_argument("--boot-timeout", type=int, default=120)
    ap.add_argument("--boot-pattern", nargs="*", default=[], help="추가 부팅완료 문자열")
    ap.add_argument("--log", default="coldboot_results.csv")
    ap.add_argument("--cmd-max-retries", type=int, default=5)
    ap.add_argument("--cmd-base-sleep", type=float, default=2.0)
    ap.add_argument("--dry-run", action="store_true")
    return ap.parse_args()

def main():
    args = parse_args()
    setup_signal_handlers()

    # 패턴 구성
    patterns = BOOT_DONE_PATTERNS[:]
    for s in args.boot_pattern:
        patterns.append(re.compile(re.escape(s), re.I))

    f, w = open_csv_logger(args.log)

    print(f"[{now_str()}] === SmartPlug Test start ===")
    print(f"device={args.device_id} cycles={args.cycles} serial={args.serial_port}@{args.baudrate}")

    try:
        for c in range(1, args.cycles + 1):
            if STOP_REQUESTED:
                break
            print(f"\n===== CYCLE {c}/{args.cycles} @ {now_str()} =====")

            # OFF
            print("[ACTION] SmartPlug OFF ...", end=" ", flush=True)
            off_ok, off_note = smartthings_command(args.cli, args.device_id, args.token, "off")
            print("OK" if off_ok else f"❌ {off_note}")
            if not off_ok:
                print("[RESULT] ⚠️ SMARTTHINGS API ERROR (OFF)")
                w.writerow([now_str(), c, "API_ERROR", "N/A", 0, "off fail"])
                f.flush()
                continue

            time.sleep(args.off_hold)
            if STOP_REQUESTED: break

            # Pre-on delay
            if args.pre_on_max > 0:
                delay = random.randint(args.pre_on_min, args.pre_on_max)
                print(f"[DELAY] pre-on {delay}s")
                countdown(delay, args.countdown_step)

            # ON
            print("[ACTION] SmartPlug ON ...", end=" ", flush=True)
            on_ok, on_note = smartthings_command(args.cli, args.device_id, args.token, "on")
            print("OK" if on_ok else f"❌ {on_note}")
            if not on_ok:
                print("[RESULT] ⚠️ SMARTTHINGS API ERROR (ON)")
                w.writerow([now_str(), c, "API_ERROR", "N/A", 0, "on fail"])
                f.flush()
                continue

            # 시리얼 감시
            print(f"[{now_str()}] waiting serial log on {args.serial_port} for boot complete ...")
            boot_ok, match_line, boot_time = monitor_serial_for_boot(
                args.serial_port, args.baudrate, args.boot_timeout, patterns
            )

            if boot_ok:
                print(f"[RESULT] ✅ BOOT SUCCESS (SmartThings OK)  [{boot_time:.2f}s]")
                w.writerow([now_str(), c, "OK", "BOOT_OK", f"{boot_time:.2f}", match_line or ""])
            else:
                print(f"[RESULT] ❌ BOOT FAIL (SmartThings OK)  [timeout {boot_time:.2f}s]")
                w.writerow([now_str(), c, "OK", "BOOT_TIMEOUT", f"{boot_time:.2f}", "no pattern"])
            f.flush()

    finally:
        if f:
            f.flush()
            f.close()

    print(f"\n[{now_str()}] === Test End ===")

if __name__ == "__main__":
    main()
