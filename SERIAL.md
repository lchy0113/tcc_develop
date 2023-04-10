SERIAL
=====

# tty driver framework analysis

![](./images/SERIAL_01.png)

전체 uart 프레임워크의 일반적인 모습은 위의 그림과 같이 대략 4개의 계층으로 나눌 수 있습니다.  
 첫 번째 계층은 하드웨어와 직접 접촉하는 직렬 포트 드라이버 계층입니다.구조체를 채워야 합니다.  
 uart_ops 구조, 그 다음은 tty core 상위 계층은 line discipline,   
 상위 계층은 userspace 와 직접 연결 각각 Ops 구조를 가지며 userspcae은 등록된 캐릭터 디바이스 노드를 통해 접근 이런 식으로 위의 그림과 같이 4개의 ops 구조, layer by layer jump가 포함됩니다.  
 그중에서 드라이버를 추가하려고 할 때 수행해야 할 주요 작업은 기본 드라이버이고 커널의 다른 세 계층은 구현되었습니다.  
 다음으로 계층 구조를 분석하고 분석해 보겠습니다.   
 amba_pl011 드라이버를 예로 들어 보겠습니다.


# develop 

- 지원하는 RS485 인터페이스
  * DF_DP(RF도어폰_통신)
	+ GPIO_C23	- RF_DP_TXD
    + GPIO_C24	- RF_DP_RXD
	+ GPIO_C27	- RF_DP_TX_EN

  * SUB_통신(도어락 연동모듈 포함)
    + GPIO_F22	- SUB_TXD
	+ GPIO_F23	- SUB_RXD
	+ GPIO_G05	- SUB_TX_EN
  


# datasheet

- Chapter 16 UART SUB SYSTEM
 
  * register : 0x1660_0000

# patch

```
CONFIG_SERIAL_AMBA_PL011_SOFT_RS485 // config define

static void pl011_rs485_start_rts_delay() // add function

```
