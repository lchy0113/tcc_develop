from colorama import init, Fore
from datetime import datetime
import serial
import time
import random
import subprocess
import os

log_fail_string = "cx2070x_download_firmware(): download firmware failed, Error"
log_succ_string = "cx2070x_download_firmware(): download firmware successfully"
log_test_string = "TP2860 driver verison 0.10.1 loaded"
log_boot_string = "init: processing action (sys.boot_completed=1) from (/init.rc"

# set serial port 
ser = serial.Serial(port='/dev/ttyUSB1', baudrate=115200, timeout=1, xonxoff=False, rtscts=False, dsrdtr=False)
ser.flushInput()
ser.flushOutput()

count = 0
count_succ = 0
count_fail = 0
filename = "serial_test.log"

# for smartthings
token="61ed264a-248f-4685-86a4-a155d3b469df"
deviceid="a33c21d8-bd0f-4004-8353-14660902510c"

def random_task(delay):
	print(Fore.GREEN + f"random delay task() : {delay}" + Fore.GREEN)

init(autoreset=True) 

print("begin serial interface. if input 'exit' to exit")

while True:
	received_data = ser.readline().decode().strip() #read serial data
	if received_data:
		print(received_data)

	date = datetime.now()
#	if log_test_string in received_data:
#		print(Fore.BLUE + f"[PASS] '{log_test_string}'" + Fore.RESET)
	if log_succ_string in received_data:
		count_succ += 1
		print(Fore.BLUE + f"[PASS] [{date}] '{log_succ_string}'" + Fore.RESET)
		try:
			with open(filename, 'a', encoding='UTF-8') as f:
				f.write(f"[PASS] [{date}] '{log_succ_string}'\n")
		except:
			print("error file open")

	elif log_fail_string in received_data:
		count_fail += 1
		print(Fore.RED + f"[FAIL] [{date}] '{log_fail_string}'" + Fore.RESET)
		try:
			with open(filename, 'a', encoding='UTF-8') as f:
				f.write(f"[FAIL] [{date}] '{log_fail_string}'\n")
		except:
			print("error file open")
		break;

	elif log_boot_string in received_data:
		count += 1
		print(Fore.GREEN + f"[INDEX] : [{date}] TOTAL({count}) [SUCC({count_succ}) / FAIL({count_fail})]" + Fore.RESET)
		#ser.write(b'reboot\r\n')
		command = f"./smartthings devices:commands {deviceid} switch:off --token={token}"
		result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
		print(result.stdout)
		print(Fore.GREEN + f"(power off)" + Fore.RESET)

		random_delay = random.randint(2,10)
		random_task(random_delay)
		time.sleep(random_delay);

		command = f"./smartthings devices:commands {deviceid} switch:on --token={token}"
		result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
		print(result.stdout)
		print(Fore.GREEN + f"(power on)" + Fore.RESET)



#    user_input = input(">> ")  # 사용자 입력 받기
#
#    if user_input.lower() == 'exit':
#        ser.close()
#        break
#    else:
#        # 입력한 문자열을 시리얼 장치로 전송 (CR/LF 추가)
#        ser.write(user_input.encode() + b'\r\n')
#
#        # 장치의 응답을 기다리기 위해 1초 대기
#        time.sleep(1)
#
#        # 시리얼 버퍼에서 데이터 읽기
#		#response = ser.read_all().decode()
#        response = ser.read_until().decode()
#
#        if response:
#            print(f"응답: {response.strip()}")
#
