# DISPLAY 

|     	| bootloader           	| kernel                  	|
|-----	|----------------------	|-------------------------	|
| 10" 	| DISP0: DISP1: lcd    	| DISP0: cvbs DISP1: lcd  	|
| 13" 	| DISP0: hdmi  DISP1:  	| DISP0: cvbs DISP1: hdmi 	|

## bootloader (lk)

```
called from crt0.S	/arch/arm/crt0.S
	|
	+-> void kmain(void)	/kernel/main.c
		|
		+-> static int bootstrap2(void *arg)	/kernel/main.c
			|
			+-> void target_init(void)	/target/tcc898x_stb/init.c
				|
				+-> void display_init(void)	/target/tcc898x_stb/target_display.c
					/*
					 * init display(0; 0x12000000)
					 */
					|
					+-> lcdc_init()	platform/tcc898x/lcdc.c
						|
						+-> lcdc_io_init_hdmi(unsigned char lcdc_num)	/platform/tcc898x/lcdc.c
							/*
							 * 1st(0x12000000) output setting : hdmi
							 */
							|
							+-> hdmi_ddi_config_init(unsigned int display_device)	/dev/hdmi/hdmi_v2_0/hdmi_v2_0.c
								/* 
								 * mapping phy and board api
								 * HDMI init (hdmi core power on, off)
								 * Set clock source for display
								 */
								 |
								 +-> void dwc_hdmi_core_power_on(void)
								 	/*
									 * setting clock,,
									 */
									 |
									 +-> void dwc_hdmi_hw_reset(int reset_on)	/dev/hdmi/hdmi_v2_0/hdmi_v2_0.c
									 /* 
									  * initialize i2c timing
									  * EDID i2c setting
									  */
									  |
									  +-> static void hdmi_prepare_i2c(void)	/dev/hdmi/hdmi_v2_0/hdmi_misc.c
							|
							+-> void VIOC_OUTCFG_SetOutConfig(unsigned nType, unsigned nDisp)	/platform/tcc898x/vioc/vioc_outcfg.c
								/*
								 * set VIOC_OUTCFG(0x12100200) to DISPx
								 */
							|
							+-> void VOIC_DISP_TurnOff(VIOC_DISP *pDISP)	/platform/tcc898x/vioc/vioc_disp.c
								/* 
								 * LCD Controller Stop
								 * set DCTRL(0x12000000)
								 */
							|
							+->	void video_params_reset(videoParams_t *videoParams)	/dev/hdmi/hdmi_v2_0/hdmi_api_lib/src/core/video_params.c
								|
								+-> void hdmi_start(videoParams_t *videoParams)	/dev/hdmi/hdmi_v2_0.c
									|
									+-> void edid_read_cap(void)	/dev/hdmi/hdmi_v2_0/hdmi_edid.c	
					|
					+-> static void lcdc_io_init_composite(unsigned char lcdc_num, unsigned char type)	/platform/tcc898x/lcdc.c
						/*
						 * 2nd(0x12000100) output setting : compsite
						 */
```
## kernel

```
	static __init int hdmi1920x1080_init9void)	/drivers/video/fbdev/tcc-fb/hdmi_1920x1080.c
	static int __init tccfb_init(void)	/driver/video/fbdev/tcc-fb/tcc_vioc_fb.c
	static __init int hdmi1920x1080_init(void)	/drivers/video/fbdev/tcc-fb/hdmi_1920x1080.c
```
