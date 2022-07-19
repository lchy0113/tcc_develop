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
