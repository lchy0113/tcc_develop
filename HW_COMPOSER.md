HW COMPOSER 
=====

- atrace : 
```bash
$ atrace --list_categories
         gfx - Graphics
       input - Input
        view - View System
     webview - WebView
          wm - Window Manager
          am - Activity Manager
          sm - Sync Manager
       audio - Audio
       video - Video
      camera - Camera
         hal - Hardware Modules
         app - Application
         res - Resource Loading
      dalvik - Dalvik VM
          rs - RenderScript
      bionic - Bionic C Library
       power - Power Management
          pm - Package Manager
          ss - System Server
    database - Database
     network - Network
         adb - ADB
         pdx - PDX services
       sched - CPU Scheduling
         irq - IRQ Events
        freq - CPU Frequency
        idle - CPU Idle
        disk - Disk I/O
        load - CPU Load
        sync - Synchronization
       workq - Kernel Workqueues
  memreclaim - Kernel Memory Reclaim
  regulators - Voltage and Current Regulators
  binder_driver - Binder Kernel driver
  binder_lock - Binder global lock trace

```

	:  Load and prepare the hardware composer module.  Sets mHwc

```cpp
// frameworks/native/services/surfaceflinger/DisplayHardware/HWComposer_hwc1.cpp	
	HWComposer::HWComposer 
		|
		+->	void HWComposer::loadHwcModule()
			|
			+->	hw_get_module(HWC_HARDWARE_MODULE_ID, ...);


```


- grallocd
	: Android HwRenderer를 호출하는 upper layer는 gallocd.    
	: gallocd는 그래픽 하드웨어에 대한 access를 제공하는 서비스.
	: HwRenderer는 그래픽 하드웨어를 사용하여 rendering하는데 사용하는 라이브러리. 
	: gallocd는 HwRenderer가 그래픽 하드웨어에 액세스 할 수 있도록 하여 HwRenderer가 화면에 rendering 할수 있도록 한다.


- tc_hwc : Telechips Hardware Composer HAL.
```cpp
// hardware/telechips/common/hwcomposer/tc_hwc.cpp
	tc_hwc_device_open(..)
	|
	+->	tc_cfg_open(...)
		|
		+->	int tc_cfg_open(TccHwcCfg *TccCfg)
			// hardware/telechips/common/hwcomposer/tc_hwc_dedicated.cpp
			/**
			  * malloc render memory 
			  */

```



- HwRenderer
```cpp
// hardware/telechips/common/hwcomposer/tc_hwc_overlay.cpp
// hardware/telechips/common/hwcomposer/tc_hwc_overlay.h
	|
	+-> class HwRenderer
		(...)
		int initDevice(int inWIdth, int inHeight, int overlay_ch, unsigned int fd_0, char* handle)
		(...)


```
