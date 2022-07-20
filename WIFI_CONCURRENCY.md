# Guide for wifi device ap mode operation

- overview 
```bash
+---------------------------------+
|          target device          |
|       wifi concurrency mode     |
|                                 |
|         [iperf server]          |
| (station)          (ap)         |
| wlan0             p2p0          |
| (192.168.0.20)    (172.16.0.1)  |
+-----|------------------|--------+
      |                  |
  +---+-----------+ +----+----------+
  |  router       | | test device   |
  | [iperf client]| | [iperf client]|
  | (192.168.0.1) | | (172.16.0.10) |
  +---------------+ +---------------+
```


- test
```bash
+---------------------------------+                                                                                                                      
|          target device          |                                                                                                                                      
|       wifi concurrency mode     |                                                                                                                               
|                                 |                           
|         [iperf server]          | 
|         network bridge X        |
| (station)          (ap)         |                                                                                                                                   
| wlan0             p2p0          |                                                                                                                                    
| (192.168.0.20)    (172.16.0.1)  |                                                                                                                          
+-----|------------------|--------+                                                                                                                      
      |                  |                                                                                                                                                        
  +---+-----------+ +----+----------+                                                                                                                      
  |  router       | | test device   |                                                                                                                               
  |               | |               |
  |               | | [iperf client]|                                                                                                                             
  | (192.168.0.1) | | (172.16.0.10) |                                                                                                                          
  +---+-----------+ +---------------+ 
      |
+-----|----------+
| test device    |
|                |
| [iperf client] |
| (192.168.0.3)  |
+----------------+
```

## setting configuration
- ip 할당
``` bash
ip link set p2p0 up
ip addr add 172.16.0.1/24 dev p2p0
```

- dnsmasq  
	[dnsmasq.conf](/attachment/dnsmasq.conf)  
	[resolv.conf](/attachment/resolv.conf)  
```bash
dnsmasq -d -C /data/local/tmp/dnsmasq.conf \
			-x /data/local/tmp/dnsmasq.pid \
			-r /data/local/tmp/resolv.conf
```

- hostapd  
	[hostapd.conf](/attachment/hostapd.conf)  
```bash
hostapd -dd /data/local/tmp/hostapd.conf
```

- ip rule
```bash
ip rule add from all lookup main pref 1
```

## note
android routing table issue
> 2개 이상의 네트워크가 동시에 연결되었을때, routing table 발생 이슈에 대해 정리합니다.
ex) p2p0 서버에 강제로 연결해야 하지만, wlan0 인터페이스에 연결되어 서버와 통신이 불가합니다.

```bash
wifidev:/ # ip route
172.16.0.0/24 dev p2p0  proto kernel  scope link  src 172.16.0.1
192.168.0.0/24 dev wlan0  proto kernel  scope link  src 192.168.0.20
wifidev:/ #

wifidev:/ # busybox route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
172.16.0.0      0.0.0.0         255.255.255.0   U     0      0        0 p2p0
192.168.0.0     0.0.0.0         255.255.255.0   U     0      0        0 wlan0
wifidev:/ #

```

ping 어플리케이션을 통해 서버로 전송하지만, 네트워크 인터페이스 옵션을 추가 하지 않는 한 전송 되지 않음. 


### solve

ip route show 명령어는 Android가 많은 별도의 routing table을 유지 관리하기 때문에 일부분만 출력하고 있습니다. 
ip route show table 0 명령은 모든 table의 항목을 출력합니다.

ip rule 시, "main" lookup table은 queried 되지 않았기에, 아래 rule을 추가하여 해결했습니다.
```bash
ip rule add from all lookup main pref 1
```

안드로이드는 번호로 찾노할 수 있는 routing tables을 유지 관리 합니다.  
"local"과 "main"이라는 특별한 것이 있습니다. 
ip route show 명령어는 "main" table의 정보만 출력하고 있습니다.  
ip route show table 0 명령어는 모든 정보를 출력합니다.
```bash
wifidev:/ # ip route show
172.16.0.0/24 dev p2p0  proto kernel  scope link  src 172.16.0.1
192.168.0.0/24 dev wlan0  proto kernel  scope link  src 192.168.0.20


wifidev:/ # ip route show table local
broadcast 127.0.0.0 dev lo  proto kernel  scope link  src 127.0.0.1
local 127.0.0.0/8 dev lo  proto kernel  scope host  src 127.0.0.1
local 127.0.0.1 dev lo  proto kernel  scope host  src 127.0.0.1
broadcast 127.255.255.255 dev lo  proto kernel  scope link  src 127.0.0.1
broadcast 172.16.0.0 dev p2p0  proto kernel  scope link  src 172.16.0.1
local 172.16.0.1 dev p2p0  proto kernel  scope host  src 172.16.0.1
broadcast 172.16.0.255 dev p2p0  proto kernel  scope link  src 172.16.0.1
broadcast 192.168.0.0 dev wlan0  proto kernel  scope link  src 192.168.0.20
local 192.168.0.20 dev wlan0  proto kernel  scope host  src 192.168.0.20
broadcast 192.168.0.255 dev wlan0  proto kernel  scope link  src 192.168.0.20


wifidev:/ # ip route show table main
172.16.0.0/24 dev p2p0  proto kernel  scope link  src 172.16.0.1
192.168.0.0/24 dev wlan0  proto kernel  scope link  src 192.168.0.20


wifidev:/ # ip route show table 0
default dev dummy0  table dummy0  proto static  scope link
default via 192.168.0.1 dev wlan0  table wlan0  proto static
192.168.0.0/24 dev wlan0  table wlan0  proto static  scope link
172.16.0.0/24 dev p2p0  proto kernel  scope link  src 172.16.0.1
192.168.0.0/24 dev wlan0  proto kernel  scope link  src 192.168.0.20
broadcast 127.0.0.0 dev lo  table local  proto kernel  scope link  src 127.0.0.1
local 127.0.0.0/8 dev lo  table local  proto kernel  scope host  src 127.0.0.1
local 127.0.0.1 dev lo  table local  proto kernel  scope host  src 127.0.0.1
broadcast 127.255.255.255 dev lo  table local  proto kernel  scope link  src 127.0.0.1
broadcast 172.16.0.0 dev p2p0  table local  proto kernel  scope link  src 172.16.0.1
local 172.16.0.1 dev p2p0  table local  proto kernel  scope host  src 172.16.0.1
broadcast 172.16.0.255 dev p2p0  table local  proto kernel  scope link  src 172.16.0.1
broadcast 192.168.0.0 dev wlan0  table local  proto kernel  scope link  src 192.168.0.20
local 192.168.0.20 dev wlan0  table local  proto kernel  scope host  src 192.168.0.20
broadcast 192.168.0.255 dev wlan0  table local  proto kernel  scope link  src 192.168.0.20
unreachable default dev lo  proto kernel  metric 4294967295  error -101
unreachable default dev lo  proto kernel  metric 4294967295  error -101
unreachable default dev lo  proto kernel  metric 4294967295  error -101
fe80::/64 dev dummy0  table dummy0  proto kernel  metric 256
default dev dummy0  table dummy0  proto static  metric 1024
unreachable default dev lo  proto kernel  metric 4294967295  error -101
fe80::/64 dev wlan0  table wlan0  proto kernel  metric 256
fe80::/64 dev wlan0  table wlan0  proto static  metric 1024
unreachable default dev lo  proto kernel  metric 4294967295  error -101
fe80::/64 dev p2p0  table 1006  proto kernel  metric 256
unreachable default dev lo  proto kernel  metric 4294967295  error -101
unreachable default dev lo  proto kernel  metric 4294967295  error -101
local ::1 dev lo  table local  proto none  metric 0
local fe80::432:f4ff:fe06:bd94 dev lo  table local  proto none  metric 0
local fe80::632:f4ff:fe06:bd94 dev lo  table local  proto none  metric 0
local fe80::c87d:f7ff:feff:ef5b dev lo  table local  proto none  metric 0
ff00::/8 dev dummy0  table local  metric 256
ff00::/8 dev wlan0  table local  metric 256
ff00::/8 dev p2p0  table local  metric 256
unreachable default dev lo  proto kernel  metric 4294967295  error -101
```


kernel은 ip rule에 명시된 테이블을 사용하고 있습니다.
```bash
wifidev:/ # ip rule
0:      from all lookup local
1:      from all lookup main
10000:  from all fwmark 0xc0000/0xd0000 lookup legacy_system
10500:  from all oif dummy0 lookup dummy0
10500:  from all oif wlan0 lookup wlan0
13000:  from all fwmark 0x10063/0x1ffff lookup local_network
13000:  from all fwmark 0x10064/0x1ffff lookup wlan0
14000:  from all oif dummy0 lookup dummy0
14000:  from all oif wlan0 lookup wlan0
15000:  from all fwmark 0x0/0x10000 lookup legacy_system
16000:  from all fwmark 0x0/0x10000 lookup legacy_network
17000:  from all fwmark 0x0/0x10000 lookup local_network
19000:  from all fwmark 0x64/0x1ffff lookup wlan0
22000:  from all fwmark 0x0/0xffff lookup wlan0
23000:  from all fwmark 0x0/0xffff lookup main
32000:  from all unreachable
wifidev:/ #

```

"main" routing table 에 원하는 항목이 있었지만 rule에서 참조되지 않았습니다.
그래서 아래 rule을 추가했습니다.
```bash
wifidev:/ # ip rule add from all lookup main pref 1
```

그리고 추가된 리스트를 아래와 같이 확인 했습니다.
```bash
wifidev:/ # ip rule
0:      from all lookup local
1:      from all lookup main
10000:  from all fwmark 0xc0000/0xd0000 lookup legacy_system
10500:  from all oif dummy0 lookup dummy0
10500:  from all oif wlan0 lookup wlan0
13000:  from all fwmark 0x10063/0x1ffff lookup local_network
13000:  from all fwmark 0x10064/0x1ffff lookup wlan0
14000:  from all oif dummy0 lookup dummy0
14000:  from all oif wlan0 lookup wlan0
15000:  from all fwmark 0x0/0x10000 lookup legacy_system
16000:  from all fwmark 0x0/0x10000 lookup legacy_network
17000:  from all fwmark 0x0/0x10000 lookup local_network
19000:  from all fwmark 0x64/0x1ffff lookup wlan0
22000:  from all fwmark 0x0/0xffff lookup wlan0
23000:  from all fwmark 0x0/0xffff lookup main
32000:  from all unreachable
```
