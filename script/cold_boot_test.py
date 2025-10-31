#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SmartThings + 시리얼 부팅 감지 + 누적 통계 출력

예시:
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
    import serial  # pip install pyserial
except ImportError:
    print("pyserial이 필요합니다. 설치: pip install pyserial", file=sys.stderr)
    sys.exit(1)

STOP_REQUESTED = False

OK_STRINGS = ("Command executed successfully", "request completed")
PAT_TOO_MANY = re.compile(r"Too\s*Many\s*Requests", re.I)
PAT_429 = re.compile(r"\b429\b")
PAT_401 = re.compile(r"\b401\b|Authorization Required|Unauthorized|invalid token", re.I)
PAT_404 = re.compile(r"\b404\b|Not Found", re.I)
PAT_OFFLINE = re.compile(r"Device\s*is\s*offline|DeviceOffline", re.I)

BOOT_DONE_PATTERNS = [
    re.compile(r"Boot animation end", re.I),
    re.compile(r"HDMI Init", re.I),
    re.compile(r"boot completed", re.I),
]

# ---------- UTILS ----------

def now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def eprint(msg: str) -> None:
    sys.stderr.write(msg + "\n")
    sys.stderr.flush()

def run_cmd(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def is_rate_limited(out: str) -> bool:
    return bool(PAT_TOO_MANY.search(out) or PAT_429.search(out))

def classify_api_error(out: str) -> str:
    """문자열로 SmartThings API 오류 유형 반환"""
    if PAT_401.search(out):
        return "AUTH_401"
    if PAT_404.search(out):
        return "NOT_FOUND_404"
    if PAT_OFFLINE.search(out):
        return "DEVICE_OFFLINE_409"
    if is_rate_limited(out):
        return "RATE_LIMIT_429"
    return "OTHER"

# ---------- SMARTTHINGS ----------

def smartthings_command(
    cli: str,
    dev: str,
    token: Optional[str],
    action: str,
    max_retries: int = 5,
    base_sleep: float = 2.0
) -> Tuple[bool, str]:
    """SmartThings on/off 명령 수행 및 결과 반환"""
    attempt = 0
    while True:
        if STOP_REQUESTED:
            return False, "Interrupted"
        base = [cli, "devices:commands", dev, f"switch:{action}"]
        if token:
            base += ["--token", token]
        cp = run_cmd(base)
        out = (cp.stdout or "") + (cp.stderr or "")
        ok = (cp.returncode == 0) and any(s in out for s in OK_STRINGS)
        if ok:
            return True, "OK"

        err_type = classify_api_error(out)
        if attempt < max_retries and err_type == "RATE_LIMIT_429":
            sleep_s = base_sleep * (2 ** attempt)
            eprint(f"[{now_str()}] 429 Too Many Requests → retry in {sleep_s:.1f}s ...")
            time.sleep(sleep_s)
            attempt += 1
            continue

        if err_type == "AUTH_401":
            return False, "AUTH_401 (토큰 무효/미전달)"
        if err_type == "NOT_FOUND_404":
            return False, "NOT_FOUND_404 (DEVICE_ID 확인 필요)"
        if err_type == "DEVICE_OFFLINE_409":
            return False, "DEVICE_OFFLINE_409 (스마트플러그 오프라인)"

        err = out.strip().splitlines()[-1] if out.strip() else "unknown error"
        return False, err

def smartthings_healthcheck(
    cli: str,
    token: Optional[str],
    device_id: str,
    timeout_s: float = 10.0
) -> Tuple[bool, str]:
    """
    실행 전 사전점검:
      1) 토큰 유효성 (locations)
      2) 디바이스 접근성 (devices:status <DEVICE_ID>)
    """
    if not token:
        return False, "토큰이 비어있음(SMARTTHINGS_TOKEN 미설정)."

    # 1) 토큰 체크
    cp1 = run_cmd([cli, "locations", "--token", token])
    out1 = (cp1.stdout or "") + (cp1.stderr or "")
    if cp1.returncode != 0:
        t = classify_api_error(out1)
        if t == "AUTH_401":
            return False, "토큰 무효(401). 새 토큰 발급 필요."
        if t == "RATE_LIMIT_429":
            return False, "Rate Limit(429). 잠시 후 재시도."
        return False, f"토큰 확인 실패: {out1.strip().splitlines()[-1] if out1.strip() else 'unknown'}"

    # 2) 디바이스 상태 접근 체크
    cp2 = run_cmd([cli, "devices:status", device_id, "--token", token])
    out2 = (cp2.stdout or "") + (cp2.stderr or "")
    if cp2.returncode != 0:
        t = classify_api_error(out2)
        if t == "NOT_FOUND_404":
            return False, "DEVICE_ID가 잘못되었거나 접근 권한 없음(404)."
        if t == "AUTH_401":
            return False, "토큰 무효(401)."
        if t == "DEVICE_OFFLINE_409":
            # 오프라인이어도 테스트는 진행 가능할 수 있으니 '주의'로 통과
            return True, "디바이스가 오프라인(409). 전원/네트워크 확인 권장."
        return False, f"디바이스 상태 확인 실패: {out2.strip().splitlines()[-1] if out2.strip() else 'unknown'}"

    return True, "OK"

# ---------- SERIAL ----------

def monitor_serial_for_boot(
    port: str, baud: int, timeout_s: int, patterns
) -> Tuple[bool, Optional[str], float]:
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

# ---------- LOG ----------

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

# ---------- SIGNAL ----------

def setup_signal_handlers():
    def handler(signum, frame):
        global STOP_REQUESTED
        STOP_REQUESTED = True
        eprint(f"[{now_str()}] received signal {signum}. stopping...")
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)

# ---------- ARG ----------

def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="SmartPlug + Serial Boot Detector (with Stats)")
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
    ap.add_argument("--no-preflight", action="store_true",
                    help="시작 전에 SmartThings 토큰/디바이스 사전점검을 생략")
    return ap.parse_args()

# ---------- MAIN ----------

def countdown(total: int, step: int, label="pre-on"):
    remain = total
    while remain > 0 and not STOP_REQUESTED:
        tick = min(step, remain)
        time.sleep(tick)
        remain -= tick
        print(f"[{now_str()}] {label} countdown: {remain}s remaining")

def main():
    args = parse_args()
    setup_signal_handlers()

    # 부팅 패턴 구성
    patterns = BOOT_DONE_PATTERNS[:]
    for s in args.boot_pattern:
        patterns.append(re.compile(re.escape(s), re.I))

    f, w = open_csv_logger(args.log)

    # 사전 점검
    if not args.no_preflight:
        ok, note = smartthings_healthcheck(args.cli, args.token, args.device_id)
        if not ok:
            eprint(f"[{now_str()}] ❌ Preflight 실패: {note}")
            sys.exit(2)
        else:
            print(f"[{now_str()}] ✅ Preflight 통과: {note}")

    print(f"[{now_str()}] === SmartPlug Test start ===")
    print(f"device={args.device_id} cycles={args.cycles} serial={args.serial_port}@{args.baudrate}")

    stats = {"total": 0, "success": 0, "fail": 0, "api_error": 0}

    try:
        for c in range(1, args.cycles + 1):
            if STOP_REQUESTED:
                break
            print(f"\n===== CYCLE {c}/{args.cycles} @ {now_str()} =====")
            stats["total"] += 1

            # Prep-off delay
            print(f"[DELAY] pre-off 5s")
            time.sleep(5)

            # OFF
            print("[ACTION] SmartPlug OFF ...", end=" ", flush=True)
            off_ok, off_note = smartthings_command(
                args.cli, args.device_id, args.token, "off",
                max_retries=args.cmd_max_retries, base_sleep=args.cmd_base_sleep
            )
            print("OK" if off_ok else f"❌ {off_note}")
            if not off_ok:
                stats["api_error"] += 1
                print(f"[RESULT] ⚠️ SMARTTHINGS API ERROR (OFF) -> {off_note}")
                print(f"          → [STATS] total={stats['total']} | success={stats['success']} | fail={stats['fail']} | api_error={stats['api_error']}")
                if w:
                    w.writerow([now_str(), c, "API_ERROR", "N/A", 0, f"off fail: {off_note}"])
                    f.flush()
                continue

            time.sleep(args.off_hold)

            # Pre-on delay
            if args.pre_on_max > 0:
                delay = random.randint(args.pre_on_min, args.pre_on_max)
                print(f"[DELAY] pre-on {delay}s")
                countdown(delay, args.countdown_step)

            # ON
            print("[ACTION] SmartPlug ON ...", end=" ", flush=True)
            on_ok, on_note = smartthings_command(
                args.cli, args.device_id, args.token, "on",
                max_retries=args.cmd_max_retries, base_sleep=args.cmd_base_sleep
            )
            print("OK" if on_ok else f"❌ {on_note}")
            if not on_ok:
                stats["api_error"] += 1
                print(f"[RESULT] ⚠️ SMARTTHINGS API ERROR (ON) -> {on_note}")
                print(f"          → [STATS] total={stats['total']} | success={stats['success']} | fail={stats['fail']} | api_error={stats['api_error']}")
                if w:
                    w.writerow([now_str(), c, "API_ERROR", "N/A", 0, f"on fail: {on_note}"])
                    f.flush()
                continue

            # Serial detect
            print(f"[{now_str()}] waiting serial log on {args.serial_port} for boot complete ...")
            boot_ok, match_line, boot_time = monitor_serial_for_boot(
                args.serial_port, args.baudrate, args.boot_timeout, patterns
            )

            if boot_ok:
                stats["success"] += 1
                print(f"[RESULT] ✅ BOOT SUCCESS (SmartThings OK) [elapsed {boot_time:.2f}s]")
            else:
                stats["fail"] += 1
                print(f"[RESULT] ❌ BOOT FAIL (SmartThings OK) [timeout {boot_time:.2f}s]")

            # 누적 통계 출력
            print(f"          → [STATS] total={stats['total']} | success={stats['success']} | fail={stats['fail']} | api_error={stats['api_error']}")

            # CSV 기록
            if w:
                w.writerow([
                    now_str(),
                    c,
                    "OK",
                    "BOOT_OK" if boot_ok else "BOOT_FAIL",
                    f"{boot_time:.2f}",
                    match_line or "no pattern",
                ])
                f.flush()

    finally:
        if f:
            f.flush()
            f.close()

    print(f"\n[{now_str()}] === Test End ===")
    print(f"[SUMMARY] total={stats['total']} | success={stats['success']} | fail={stats['fail']} | api_error={stats['api_error']}")
    rate = (stats["success"] / stats["total"] * 100) if stats["total"] else 0
    print(f"[SUMMARY] success rate = {rate:.1f}%")

if __name__ == "__main__":
    main()
