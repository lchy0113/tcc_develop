# DISPLAY 

## bootloader (lk)

```
called from crt0.S	/arch/arm/crt.S
	|
	+-> void kmain(void)	/kernel/main.c
		|
		+-> static int bootstrap2(void *arg)	/kernel/main.c
			|
			+-> void target_init(void)	/target/tcc898x_stb/init.c
				|
				+-> void display_init(void)	/target/tcc898x_stb/target_display.c
					|
					+-> lcdc_init()	platform/tcc898x/lcdc.c
						|
						+-> lcdc_io_init_hdmi(unsigned char lcdc_num)	/platform/tcc898x/lcdc.c
							/*
							 * 1st output setting : hdmi
							 */
							|
							+-> hdmi_ddi_config_init(unsigned int display_device)	/dev/hdmi/hdmi_v2_0/hdmi_v2_0.c
								/* 
								 * mapping phy and board api
								 * HDMI init (hdmi core power on, off)
								 */
								 |
								 +-> void dwc_hdmi_core_power_on(void)
								 	/*
									 * setting clock, i2c,,
									 */
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
						 * 2nd output setting : compsite
						 */
```
