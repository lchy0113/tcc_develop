# VIOC 

## Overview
</pr>
VIOC(Video Input/Output Controller)는 시스템 메모리에서 다양한 디스플레이 장치로 이미지 데이터를 보내거나 외부 비디오 입력에서 이미지 데이터를 받아 시스템 메모리에 쓰는 데 사용됩니다.

디스플레이 장치는 TFT-LCD(RGB 인터페이스 유형), NTSC/PAL 인터페이스, HDMI 또는 아날로그 출력과 같은 것이고 비디오 입력은 카메라 또는 TV 입력 등과 같은 것입니다.

VIOC에는 2개의 독립적인 디스플레이 타이밍 컨트롤러와 2개의 독립적인 비디오 입력 컨트롤러가 있습니다.  
 (시간 다중화 모드 사용, VIOC는 2개의 독립적인 비디오 입력 컨트롤러 지원)


다음 그림은 VIOC의 전체 블록 다이어그램을 보여줍니다. VIOC는 component와 interface로 구성됩니다.  
component는 각 하드웨어 블록을 의미하고 interface는 각 하드웨어 블록 사이에서 데이터를 전송하는 채널의 정보입니다.  


VIOC의 각 하드웨어 component는 "SYSTEM TIMER", "GRDMA", "VRDMA", "VWDMA", "DISPLAY", "VIDEO IN", "SCALER", "VIQE(DEINTL_temporal)", "DEINTL_S", " LUT”, “WINMIX_4X2”, “WINMIX_2X2”,”MAP_CONV”, “DEC100” “DTRC”.

각 하드웨어 블록 사이의 화살표는 interface로 정의됩니다.

다음 그림에서 화살표로 연결되지 않은 5개의 component는 각 인터페이스에 삽입되어 있으므로 제대로 작동한다고 가정합니다.
  
- **SYSTEM TIMER**  
  "SYSTEM TIMER"는 streaming control을 위해 PTS(Presentation Time Stamp)에 대한 system time을 만들고 "SYSTEM TIMER"에서는 인터럽트 출력이 가능합니다.  
  "GRDMA" 및 "VRDMA"는 메모리에서 이미지 소스를 읽습니다.  
  "GRDMA"의 경우 1 plane format을 지원됩니다.  
  “VRDMA”의 경우 2 plane foamat과 3 plane format을 지원합니다.  
   마찬가지로 "GWDMA" 및 "VWDMA"는 이미지 데이터를 메모리에 저장하기 위한 블록입니다.  
  "GWDMA"에는 1 plane format이 지원되고 "VWDMA"에는 최대 3 plane format이 지원됩니다. (단, VIOC는 GWDMA를 지원하지 않습니다.)  
  
- **DISPLAY**  
  "DISPLAY"에는 비디오 출력을 위한 타이밍 컨트롤러가 포함되어 있습니다. “VIDEO IN”은 외부로부터 입력으로 영상을 수신할 수 있습니다.  
  
- **SCALER**  
  "SCALER"는 이미지의 size를 변경합니다.  
  "VIQE”는 비디오 화질을 향상시키기 위한 블록으로 메인 영상 채널의 화질을 제어할 수 있습니다.  
  "DEINTL_S”는 단순 디인터레이서를 처리하는 블록으로 서브채널에 사용된다.  
  "FRAME_DELAY"는 특별한 경우에 사용하도록 되어 있으며 추후에 설명하도록 하겠습니다.  
  "LUT"는 룩업 테이블을 기반으로 RGB 색상의 색상 매핑을 변경하며 8bpp 형식의 팔레트로 사용할 수 있습니다.  
  
- **WINMIX_4X2, WINMIX_2X2**  
  "WINMIX_4X2" 및 "WINMIX_2X2"는 overlay mixer에 사용되며 각 입력에 대해 windowing 가능합니다.  
  
  overlay mixer의 출력의 경우 두 개의 인터페이스가 있는 동시 출력이 가능합니다.  
  이들은 다양한 크기의 다중 디스플레이 및 출력에 사용됩니다.  
   (“WINMIX_2X2”의 블록에 하나의 출력이 있는 경우 다른 출력은 사용하지 않습니다.)  

- **MAP_CONV**  
  "MAP_CONV"는 HEVC 비디오 디코더(WAVE410, VIDEOBUS 부분 참조)에서 생성된 압축된 비디오 스트림 데이터를 압축 해제합니다.  
  
  "DEC100"은 GC420 2D 비디오 디코더(GC420은 GRAPHIC 부분 참조)에서 생성된 압축 비디오 스트림 데이터를 압축 해제하고, "DTRC"는 VP9 비디오 디코더(VP9는 VIDEOBUS 부분 참조)에서 생성된 압축 비디오 스트림 데이터를 압축 해제합니다.  
  
 ![VIOC Block Diagram](images/vioc_block_diagram.png)


## Component & Interface
</pr>
 VIOC는 몇 가지 구성 요소로 구성됩니다.  사용자는 원하는 구성 요소를 구성할 수 있습니다.



# DDI_CONFIG

## Overview
</pr>
DDI_CONFIG는 LCD port muxing, on-the-fly mode connection, HDMI AES KEY 설정 등과 같은 DDI bus device configurations을 제어합니다.

## DDI_CONFIG Specific Features
</pr>

- Port connection of Scaler, LCDC, and VIQE for on-the-fly-mode
- Control the Connection path of each display devices
 (LCDC, HDMI, TV-Encoder)
- HDMI on-off control
- Set HDMI AESKEY for encryption

## Block Diagram of DDI_CONFIG
</pr>

아래 그림은 DDI_CONFIG 블록의 간단한 블록다이어그램을 설명합니다.  
on-fly mode용 포트 mux는 LCD 컨트롤러와 VIQE/memory to memory scaler0/1 사이에 있어 직접 연결되지 않은 경우 불가피한 중복 메모리 액세스를 제거합니다.  
예를 들어, "VIQE-MSCL-LCDC" 조합은 image enhancement, scaling, external LCD로 출력의 one-stop 처리를 가능하게 하므로 메모리 액세스 시간을 줄일 수 있습니다.  
  
LCD Controller는 HDMI, TV-OUT, LCDC 등 다양한 출력 인터페이스를 지원합니다.  
  
LCDC 인터페이스는 최대 2개의 채널을 제공할 수 있습니다.  
  
 ![Block Diagram of DDI_CONFIG](images/block_diagram_of_DDI_CONFIG.png)


# DISPLAY  DEVELOP

## 13inch display develop

|                | bootloader      | kernel               |
|--------------    |--------------    |----------------    |
| composite()     | DISP1         | DISP1              |
| hdmi()         | DISP0             | DISP0              |

## bootloader (lk)

```c
called from crt0.S    /arch/arm/crt0.S
    |
    +-> void kmain(void)    /kernel/main.c
        |
        +-> static int bootstrap2(void *arg)    /kernel/main.c
            |
            +-> void target_init(void)    /target/tcc898x_stb/init.c
                |
                +-> void display_init(void)    /target/tcc898x_stb/target_display.c
                    /*
                     * init display(0; 0x12000000)
                     */
                    |
                    +-> lcdc_init()    platform/tcc898x/lcdc.c
                    |    |
                    |    +-> lcdc_io_init_hdmi(unsigned char lcdc_num)    /platform/tcc898x/lcdc.c
                    |        /*
                    |         * 1st(0x12000000) output setting : hdmi
                    |         */
                    |        |
                    |        +-> hdmi_ddi_config_init(unsigned int display_device)    /dev/hdmi/hdmi_v2_0/hdmi_v2_0.c
                    |        |    /* 
                    |        |     * mapping phy and board api
                    |        |     * HDMI init (hdmi core power on, off)
                    |        |     * Set clock source for display
                    |        |     */
                    |        |     |
                    |        |     +-> void dwc_hdmi_core_power_on(void)
                    |        |         /*
                    |        |         * setting clock,,
                    |        |         */
                    |        |         |
                    |        |         +-> void dwc_hdmi_hw_reset(int reset_on)    /dev/hdmi/hdmi_v2_0/hdmi_v2_0.c
                    |        |         /* 
                    |        |          * initialize i2c timing
                    |        |          * EDID i2c setting
                    |        |          */
                    |        |          |
                    |        |          +-> static void hdmi_prepare_i2c(void)    /dev/hdmi/hdmi_v2_0/hdmi_misc.c
                    |        |
                    |        +-> void VIOC_OUTCFG_SetOutConfig(unsigned nType, unsigned nDisp)    /platform/tcc898x/vioc/vioc_outcfg.c
                    |        |    /*
                    |        |     * set VIOC_OUTCFG(0x12100200) to DISPx
                    |        |     */
                    |        |
                    |        +-> void VOIC_DISP_TurnOff(VIOC_DISP *pDISP)    /platform/tcc898x/vioc/vioc_disp.c
                    |        |    /* 
                    |        |     * LCD Controller Stop
                    |        |     * set DCTRL(0x12000000)
                    |        |     */
                    |        |
                    |        +->    void video_params_reset(videoParams_t *videoParams)    /dev/hdmi/hdmi_v2_0/hdmi_api_lib/src/core/video_params.c
                    |            |
                    |            +-> void hdmi_start(videoParams_t *videoParams)    /dev/hdmi/hdmi_v2_0.c
                    |                |
                    |                +-> void edid_read_cap(void)    /dev/hdmi/hdmi_v2_0/hdmi_edid.c    
                    |
                    +-> static void lcdc_io_init_composite(unsigned char lcdc_num, unsigned char type)    /platform/tcc898x/lcdc.c
                        /*
                         * 2nd(0x12000100) output setting : compsite
                         */
```

## kernel

### display

```c
    arch_initcall(vioc_viqe_init)    drivers/video/fbdev/tcc-fb/vioc/vioc_viqe.c
    |
    +->    vioc_viqe:vioc_viqe@1200d000 {...} arch/arm/boot/dts/tcc/tcc898x.dtsi    
    +-> get memory viqe0(0x1200 d000) viqe1(0x1201 0000)

    arch_initall(vioc_mc_init)    drivers/video/fbdev/tcc-fb/vioc/vioc_mc.c
    |
    +-> vioc_mc@12009000 {...}    arch/arm/boot/dts/tcc/tcc898x.dtsi 

    arch_initcall(vioc_dtrc_init)    drivers/video/fbdev/tcc-fb/vioc/vioc_dtrc.c    
    |
    +-> vioc_dtrc@12002600 {...}    arch/arm/boot/dts/tcc/tcc898x.dtsi

    arch_initcall(vioc_config_init)    drivers/video/fbdev/tcc-fb/vioc/vioc_config.c
    |
    +-> vioc_config:vioc_config@1200a000 {...} arch/arm/boot/dts/tcc/tcc898x.dtsi
    +-> void vioc_dma_path_init(void)    drivers/video/fbdev/tcc-fb/vioc/vioc_config.c    /* init rdma path */

    arch_initcall(vioc_disp_init)    drivers/video/fbdev/tcc-fb/vioc/vioc_disp.c
    |
    +-> vioc_disp:vioc_disp@12000000 {...} arch/arm/boot/dts/tcc/tcc898x.dtsi

    arch_initcall(vioc_outputconfig_init)    drivers/video/fbdev/tcc-fb/vioc/vioc_config.c
    |
    +-> clear VIN_DEMUX register       
    +-> set viocOutputConfig register

    module_init(tccxxx_overlay_init)    driver/video/fbdev/tcc-fb/tcc_overlay.c
    |
    +-> tcc_overlay_drv {...} arch/arm/boot/dts/tcc/tcc898x.dtsi
    +-> static int tcc_overlay_probe(struct platform_device *pdev)
        |
        +-> struct overlay_drv_type *overlay_drv : set framebuffer 
        +-> misc_register(overlay_drv->misc) // create misc device
        +-> set rdmas, wmix 

    module_init(tcc_vsync_init)    driver/video/fbdev/tcc-fb/tcc_vsync.c
    |
    +-> tcc_vsync_dev {...} arch/arm/boot/dts/tcc/tcc8985-soc-module-hdmi-p01.dtsi
    +-> static int tcc_vsync_probe(struct platform_device *pdev) 
    
    static int __init tccfb_init(void)    drivers/video/fbdev/tcc-fb/tcc_vioc_fb.c
    |
    +-> fbdisplay: fbdisplay@12000000 {...}    arch/arm/boot/dts/tcc/tcc898x.dtsi    
    +-> static int tccfb_probe(struct platform_device *pdev)
```

### hdmi

```c
static __init int hdmi1920x1080_init(void)    /drivers/video/fbdev/tcc-fb/hdmi_1920x1080.c
    |
    +->    static struct platform_driver hdmi1920x1080_driver = {
            .probe  = hdmi1920x1080_probe,
            .remove = hdmi1920x1080_remove,
            .driver = {
                .name   = "hdmi1920x1080_lcd",
                .owner  = THIS_MODULE,
                .of_match_table = of_match_ptr(hdmi1920x1080_of_match),
            },
        };
            |
            +-> tatic int hdmi1920x1080_probe(struct platform_device *pdev)
                |
                +-> tccfb_register_panel(&hdmi1920x1080_panel); 
(...)
static int __init tccfb_init(void)    /driver/video/fbdev/tcc-fb/tcc_vioc_fb.c
    |
    +-> static struct platform_driver tccfb_driver = {
            .probe      = tccfb_probe,
            .remove     = tccfb_remove,
            .driver     = {
                .name   = "tccfb",
                .owner  = THIS_MODULE,
        #ifdef CONFIG_PM_RUNTIME
                .pm        = &tccfb_pm_ops,
        #endif
                .of_match_table = of_match_ptr(tccfb_of_match),
            },
        };
            |
            +-> static int tccfb_probe(struct platform_device *pdev)
                |
                +->    static int tcc_dp_dt_parse_data(struct tccfb_info *info)
                |    |    /**
                |    |      * Parsing data from dt
                |    |      * main_np = fb_displayX
                |    |      * extend_np = fb_displayX
                |    |      */
                |    |
                |    +-> unsgiend int tcc_vioc_display_dt_parse(struct device_node *np, struct tcc_dp_device *dp_data)
                |            /**
                |              * Parsing the default display block and sub display block properties from dt.
                |              * ddc, wmixer , rdma, wdma
                |              */
                |
                +-> /** Setting fb_info structure properties and framebuffer operation function */
                +-> /** initialize video memory */
                +-> /** register framebuffer  */ 
                +-> /** start display and show logo on boot */
                +-> /**
                      * Initialize workqueue sending vsync uevents from kernel to userspace.
                      * send_vsync_event(kernelspace) -> tc_hwc_vsync_thread (userspace)
                      */
                +-> /** call init() from lcd_panel module */
                |    |
                |    +-> static __init int hdmi1920x1080_init(void)    /drivers/video/fbdev/tcc-fb/hdmi_1920x1080.c
                +-> int tca_fb_init(struct tccfb_info *fbi)    /drivers/video/fbdev/tcc-fb/tcc_vioc_interface.c
                        |
                        +-> /** get telechips,scaler node from dt
                                get telechips,vioc_config node from dt */
                            /** prepare vioc, ddc clock */
``` 

### composite

```c
int __init tcc_composite_init(void)    drivers/video/fbdev/tcc-fb/vioc/tcc_composite.c
    |
    +->    static struct platform_driver tcc_compostite = {
            .probe = composite_probe,
            .remove = composite_remove,
            .driver = {
                .name = "tcc_composite",
                .owner = THIS_MODULE,
                .pm = &composite_pm_ops,
                .of_match_table = of_match_ptr(composite_of_match),
            },
        };
            |
            +->     static int composite_probe(struct platform_device *pdev)    
                    |
                    +->    static int composite_parse_dt(struct device_node *np)
                    |    /** get composite_lcdc0_clk, composite_lcdc1_clk value */
                    |    /** get scaler, config, ddicfg value from dt */
                    |    /** get the information of vioc-fbfb device node */
                    |
                    +-> misc_register(&tcc_composite_misc_device)
                    |    /** register composite misc driver(file_operations) */
                    +-> void internal_tve_init(void)    drivers/video/fbdev/tcc-fb/vioc/tcc_composite_internal.c


void tcc_composite_attach(char lcdc_num, char mode, char starter_flag)
    |    /** 
    |      * lcdc_num     : 
    |      * mode         : 
    |      * start_flag    : reset privious display path
    |      */
	+->    void tcc_composite_clock_onoff(char OnOff)
	|
	|
    +->    void tcc_composite_start(TCC_COMPOSITE_TYPE mode)
    |       +-> int tcc_composite_connect_lcdc(int lcdc_num, int enable)
    |       |   /**
    |       |     * set SDVESEL field of MISC Register(0x1210020C; SDVENC (NTSC/PAL) Output Select) to Display Device 0 Component. 
    |       |     * enable NTSC/PAL DDI bus.
    |       |     */
    |       +->    void tcc_composite_set_lcd2tv(COMPOSITE_MODE_TYPE type)
    |                /**
    |                  * composite device 의 mode에 맞는 timing 및 control 세팅. 
    |                  * tcc_composite의 fb 초기화.
    |                  * vioc display block 초기화.
    |                  * composite device 초기화.
    |                  */
    +->    void tca_fb_attach_start(struct tccfb_info *info)
               /**
                 * disp1 -> disp0 간 data attach을 위한 메모리 초기화.
                 */
```


- composite out clock enable disable
>  VENCON register 를 사용하여 확인 가능.
```bash
# mem r 0x12200800 w 0x4
12200800 memory mapped at address 0xb6aff000.
0x12200800: 0x00000000
```

### tcc_overlay

```c
static int __init tccxxx_overlay_init(void)    drivers/video/fbdev/tcc-fb/tcc_overlay.c
    |
    +-> platform_driver_register(&tcc_overlay_driver)
        /** Register tcc_overlay_driver to platform driver */
        static struct platform_driver tcc_overlay_driver = {
            .probe          = tcc_overlay_probe,
            .remove         = tcc_overlay_remove,
            .suspend        = tcc_overlay_suspend,
            .resume         = tcc_overlay_resume,
            .driver         = { 
                .name   = "tcc_overlay",
                .owner  = THIS_MODULE,
                .of_match_table = of_match_ptr(tcc_overlay_of_match),
            },
        };
            |
            +-> /** register tcc_overlay misc device */
            |    static const struct file_operations tcc_overlay_fops =
            |    {
            |        .owner          = THIS_MODULE,
            |        .poll           = tccxxx_overlay_poll,
            |        .unlocked_ioctl = tccxxx_overlay_ioctl,
            |        .mmap           = tccxxx_overlay_mmap,
            |        .open           = tccxxx_overlay_open,
            |        .release        = tccxxx_overlay_release,
            |    }
            +-> /** Get rdma information. 
                    If fbdisplay_num is 0, rdma0,1,2,3
                    If fbdisplay_num is 1, rdma4,5,6,7
                */
                /** Set default overlay */
                /** get wmix information. */
                /** Set this driver data in platform device structure */
```

### tcc_vioc_interface

```

```

### tcc_vioc_fb

```

```

### tcc_vsync

```c
static int __init tcc_vsync_init(void)    drivers/video/fbdev/tcc-fb/tcc_vsync.c
    |
    +->    /** Allocate and initialize buffer for hdmi display lastframe. */
        /** register tcc_vsync_driver to platform_driver */
            static struct platform_driver tcc_vsync_driver = {
                .probe      = tcc_vsync_probe,
                .remove     = tcc_vsync_remove,
                .driver     = {
                    .name   = "tcc_vsync",
                    .owner  = THIS_MODULE,
                    .pm     = &tcc_vsync_pm_ops,
                    .of_match_table = of_match_ptr(vsync_of_match),
                },
            };
                |
                +-> static int tcc_vsync_probe(struct platform_device *pdev)
                    /**
                      * LCD_LCDC_NUM(1) EX_OUT_LCDC(0)
                      * create tcc_vsync0, tcc_vsync1 misc driver 
                      */

```

#### tcc_vsync : end video output

```c
static void tcc_vsync_end(tcc_video_disp *p, VSYNC_CH_TYPE type)    drivers/video/fbdev/tcc-fb/tcc_vsync.c
    |
    +->    void tca_vsync_video_display_disable(void)    drivers/video/fbdev/tcc-fb/tcc_vsync.c

```


```c
void tccfb_extoutput_activate(int stage)    drivers/video/fbdev/tcc-fb/tcc_vioc_fb.c
    |
    +->    void tcc_vsync_hdmi_start(struct tcc_dp_device *pdp_data,int* lcd_video_started)    drivers/video/fbdev/tcc-fb/tcc_vsync.c
```

### [develop] : decoder data composite output
- ImageInfo 의 enable 필드를 참고하여 tcc_sub_display_ctl() 를 호출한다.
- sub display(cvbs)에 디코더 데이터를 출력 시킬 경우, ImageInfo 의 data addr을 cvbs rdma addr 에 세팅한다. 
- sub display(cvbs)에 디코더 데이터를 출력 시키지 않을 경우, sub display(cvbs) 의 rdma를 비활성화 세팅한다.
```c
void tca_scale_display_update(struct tcc_dp_device *pdp_data, struct tcc_lcdc_image_update *ImageInfo)	drivers/video/fbdev/tcc-fb/tcc_vioc_interface.c
	|	/**
	|	  * 비디오 재생(decoder 데이터 출력) sequence에서 호출되는 함수.
	|	  * pdp_data : display device info
	|	  * ImageInfo : display data 
	|	  */
	+-> void tcc_sub_display_ctl(SUB_DISPLAY_MODE mode, struct tcc_lcdc_image_update *ImageInfo)	
		/**
		  * sub display(cvbs)의 데이터 출력을 제어하는 함수.
		  * mode : sub display(cvbs) 출력 제어 모드.
		  * ImageInfo : display data
		  */

```

## HAL 

### tc_hwc

```cpp
/*****************************************************************************/
static struct hw_module_methods_t hwc_module_methods = {
    open: tc_hwc_device_open
};

hwc_module_t HAL_MODULE_INFO_SYM = {
    common: {
        tag: HARDWARE_MODULE_TAG,
        module_api_version: HWC_MODULE_API_VERSION_0_1,
        hal_api_version: HARDWARE_HAL_API_VERSION,
        id: HWC_HARDWARE_MODULE_ID,
        name: "Telechips Hardware Composer HAL",
        author: "Telechips, Inc.",
        methods: &hwc_module_methods,
    }
};
/*****************************************************************************/

static int tc_hwc_device_open(const struct hw_module_t* module, const char* name, struct hw_device_t** device)    hardware/telechips/common/hwcomposer/tc_hwc.cpp
    |
    +-> int tc_cfg_open(TccHwcCfg *TccCfg)    hardware/telechips/commmon/hwcomposer/tc_hwc_dedicated.cpp 
    |    /**
    |      * open /dev/graphics/fb0
    |      * get framebuffer info from fbmem kernel module
    |      */
    |
    +->    /**
    |      * initialize the procs 
    |      */
    |        dev->device.common.tag          = HARDWARE_DEVICE_TAG;
    |        dev->device.common.version      = TCC_HWC_VERSION;
    |        dev->device.common.module       = const_cast<hw_module_t*>(module);
    |        dev->device.common.close        = tc_hwc_device_close;
    |
    |        dev->device.prepare             = tc_hwc_prepare;
    |        dev->device.set                 = tc_hwc_set;
    |    //    dev->device.fbTargetUpdate      = tc_hwc_update_fbTarget_async;
    |        dev->device.eventControl        = tc_hwc_eventControl;
    |        dev->device.registerProcs       = tc_hwc_registerProcs;
    |        dev->device.query               = tc_hwc_query;
    |        dev->device.blank               = tc_hwc_blank;
    |        dev->device.dump                = NULL;
    |        dev->device.getDisplayConfigs   = tc_hwc_getDisplayConfigs;
    |        dev->device.getDisplayAttributes = tc_hwc_getDisplayAttributes;
    |
    |    #if (TCC_HWC_VERSION >= HWC_DEVICE_API_VERSION_1_4)
    |        dev->device.setPowerMode            = tc_hwc_setPowerMode;
    |        dev->device.getActiveConfig         = tc_hwc_getActiveConfig;
    |        dev->device.setActiveConfig         = tc_hwc_setActiveConfig;
    |        dev->device.setCursorPositionAsync  = tc_hwc_setCursorPositionAsync;
    |    #endif
    |
    +-> static void *tc_hwc_vsync_thread(void *data)
    |    /** 
    |      * create tc_hwe_vsync_thread 
    |      * received uevent data from kernel
    |      */
    +->    ExtendDisplayClient->init()
    |    /** 
    |      * init ExtendDisplayClient 
    |      */
    +-> /** return 0 */


    dev->device.prepare
        |
        +->    static int tc_hwc_prepare(hwc_composer_device_1_t *dev, size_t numDisplays, hwc_display_contents_1_t** displays)     hardware/telechips/common/hwcomposer/tc_hwc.cpp
            |
            +-> int tc_create_renderer(TccHwcCfg *TccCfg, hwc_display_contents_1_t *primary_contents, hwc_display_contents_1_t *external_contents, int overlay_primary_idx, int overlay_external_idx) hardware/telechips/common/hwcomposer/tc_hwc_dedicated.cpp
                |
                +-> int __tc_try_render_creation(TccHwcCfg *TccCfg, hwc_display_contents_1_t *contents, int overlay_idx, int disp)    hardware/telechips/common/hwcomposer/tc_hwc_dedicated.cpp
                    |
                    +-> static int __tc_create_renderer(TccHwcCfg *TccCfg, hwc_display_contents_1_t *contents, int disp)     hardware/telechips/common/hwcomposer/tc_hwc_dedicated.cpp
                        |
                        +-> static void __tc_refresh_renderer(TccHwcCfg *TccCfg,hwc_display_contents_1_t *contents)    hardwrae/telechips/common/hwcomposer/tc_hwc_dedicated.cpp
                            |
                            +>    int HwRenderer::render(unsigned int fd_0, int inWidth, int inHeight, int outLeft, int outTop, int outRight, int outBottom, unsigned int transform) hardware/telechips/common/hwcomposer/tc_hwc_overlay.cpp
                                |
                                +-> bool HwRenderer::output_Overlay(output_overlay_param_t * pOverlayInfo, bool *overlayCheckRet)    hardware/telechips/common/hwcomposer/tc_hwc_overlay.cpp 
            
```

### extenddisplay_v02

```cpp
class ExtendDisplayClient : public tcc::BnTClient    hardware/telechips/common/extenddisplay_v2/extenddisplay.h
    |
    +->    int ExtendDisplayClient::init()    hardware/telechips/common/extenddisplay_v2/extenddsiaplay.cpp
        |
        +->    /** run extenddisplay thread */


```

## lcd display(nhn1033)

* 하드웨어 디코더 동작
```



```

## hdmi display(nhn1311)

* 하드웨어 디코더 동작
```cpp
static struct hw_module_methods_t hwc_module_methods
    hardware/telechps/common/hwcomposer/tc_hwc.cpp
int tc_cfg_open(TccHwcCfg *tccCfg)
    hareware/telechips/hwcomposer/tc_hwc.cpp
    +-> TccCfg->render 
int HwRenderer::initDevice(int inWidth, int inHeight, int overlay_ch, unsigned int fd_0, char* handle)
    hardware/telechips/common/hwcomposer/tc_hwc_overlay.cpp 

```

</pr>
  
# analyse : tcc8985 evboard  
=====

```bash

tcc898x:/ # mem r 0x12000000 w 0x4 ; mem r 0x12000100 w 0x4
0x12000000 memory mapped at address 0xafd31000.
12000000: 1106be61                            : a...
0x12000100 memory mapped at address 0xb6873000.
12000100: 140c82a1                            : ....
tcc898x:/ #
```

```markdown
(composite)
 persist.sys.output_mode 2
fbdisplay0
    |
    +-> vioc_display0 
    +-> vioc_wmixer 0
    +-> vioc_rdma 0 1 2 3 
    +-> vioc_wdma 0

(hdmi & lcd)
 persist.sys.output_mode 1 
fbdisplay1
    |
    +-> vioc_display1
    +-> vioc_wmixer 1
    +-> vioc_rdma 4 5 6 7
    +-> vio_wdma 1

tcc_video_viqe_external
    |
    +-> vioc_wmixer 0
    +-> vioc_rdma 3
    +-> vioc_display0
    +-> vioc_scaler 1
    

tcc_video_viqe_lcd
    |
    +-> vioc_wmixer 1
    +-> vioc_rdma 7
    +-> vioc_display1
    +-> vioc_scaler 1
    
```


 persist.sys.output_mode 1 


# analyse : extenddisplay_v02 hal
=====

```cpp
class ExtendDisplayClient
```

```cpp
int ExtendDisplayClient::init()
    |
    +-> pthread_create(&client_thread-id, NULL, &static_client_thread, this)
```
