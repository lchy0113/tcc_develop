# DISPLAY 

## bootloader (lk)

```
called from crt0.S	/arch/arm/crt.S
	|
	+->	void kmain(void)	/kernel/main.c
		|
		+->	static int bootstrap2(void *arg)	/kernel/main.c
			|
			+->	void target_init(void)	/target/tcc898x_stb/init.c
				|
				+->	void display_init(void)	/target/tcc898x_stb/target_display.c
					|
					+->	lcdc_init()	platform/tcc898x/lcdc.c
						|
						+->	lcdc_io_init_hdmi(unsigned char lcdc_num)	/platform/tcc898x/lcdc.c
							|
							+->	hdmi_ddi_config_init(unsigned int display_device)	/dev/hdmi/hdmi_v2_0/hdmi_v2_0.c
								/* 
								 * mapping phy and board api
								 * HDMI init (hdmi core power on, off)
								 */
```
