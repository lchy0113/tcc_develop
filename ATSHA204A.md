# ATSHA204A
> ATSHA204A Microchip CryptoAuthentication

- Device 구성
ATSHA204A 장치에는 아래 메모리 블록으로 구성되어 있습니다.
  * EEPROM
  * SRAM

	  + EEPROM 구성
	  664 Bytes 크기이며 아래 zone으로 분리되어 있습니다.
		ATSHA204A Zones
		|           **Zone**          	|                                                                                                                                                                                           **Description**                                                                                                                                                                                          	|                                  **Nomenclature**                                  	|
		|:---------------------------:	|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:	|:----------------------------------------------------------------------------------:	|
		| Data                        	| 일반적으로 key, calibration data, model number 또는 other information를 저장하는 데 사용할 수 있는 32bytes(256bit)의 general purpose read only 또는 read/write 메모리 슬롯 16개로 분할된 512바이트(4.0kb) 영역 ATSHA204A 장치가 부착된 항목과 관련됩니다.  각 데이터 슬롯의 액세스 정책은 해당 구성 값에 프로그래밍된 값에 의해 결정됩니다.  그러나 정책은 LockValue 바이트만 설정해야 적용됩니다. 	| Slot<YY> = The entire contents stored in Slot YY of the Data zone.                 	|
		| Configuration               	| serial number 및 other ID information를 포함하는 88bytes(704bit) EEPROM의 영역은 데이터 메모리의 각 슬롯에 대한 권한 정보에 액세스합니다.  구성 영역에 프로그래밍된 값은 각 데이터 슬롯이 응답하는 방식에 대한 액세스 정책을 결정합니다.  구성 영역은 잠길 때까지 수정할 수 있습니다(LockConfig가 !=0x55로 설정됨).  액세스 정책을 활성화하려면 LockValue 바이트를 설정해야 합니다. (위 섹션 참조) 	| SN<A:b> = A range of bytes within a field of the Configuration zone.               	|
		| One Time Programmable (OTP) 	| 64bytes(512bit)의 OTP 비트 영역입니다.  OTPzone을 잠그기 전에 표준 쓰기 명령을 사용하여 비트를 자유롭게 쓸 수 있습니다.  OTP 영역은 읽기 전용 데이터 또는 단방향 퓨즈 유형 소비 로깅 정보를 저장하는 데 사용할 수 있습니다.                                                                                                                                                                        	| OTP<bb> = A byte within the OTP zone, while OTP<aa:bb> indicates a range of bytes. 	|
<br />

## driver code


