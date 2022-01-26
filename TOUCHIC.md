# TOUCHIC
-----

Android driver source code for gt9xx series touch controller.

**Basic Info**

| Supported IC    | GT900 series touch controller |
| --------------- | ----------------------------- |
| I2C address     | 0x5D or 0x14                  |
| Gesture wakeup  | Support                       |
| Stylus          | Support                       |
| Kernel Version  | > 3.10                        |
| Firmware Update | Support                       |

**Simple description of driver files**

`gt9xx.c` (Required): This file contains the most important function such as interrupt handle, touch point report, resume/suspend process and so on.

`gtxx.h` (Required): This file contains the basic structure and macro definition.

`gt9xx_update.c`(Recommended): This file provide firmware update function. If you want support firmware update please compile this file in the driver.

`goodix_tool.c`(Recommended): This file is for debug use. You can add or remove it as you wanted.

`Kconfig`(Required):

`Makefile`(Required):

**Porting step by step**

- copy reference driver folder to $(KER_SRC)/drivers/input/touchscreen/ 

- Modify $(KER_SRC)/drivers/input/touchscreen/Makefile and the following compile command

  ```
  obj-$(CONFIG_TOUCHSCREEN_GT9XX)	+=  gt9xx/
  ```

- Modify $(KER_SRC)/drivers/input/touchscreen/Kconfig and include gt9xx driver kconfig file. 

  ```
  source "drivers/input/touchscreen/gt9xx/Kconfig"
  ```

- Add device tree properties

  You can just copy the following properties into the target device tree with little modify( following dts only contain basic properties for driver to work properly, some extended functionality are removed). Please modify the following properties according you target platform.

  1. I2C address: If the default i2c address (0x5d) conflict with other device you can just change it to 0x14.

  2. reset-gpios: You need assign a reset GPIO for our IC.

  3. irq-gpios: And also an irq GPIO is also needed.

  4. irq-flags: This properties specified the interrupt trigger type. You can set it with the following value

      <1>  rising edge triggered

      <2>  falling edge triggered

  5. touchscreen-max-id: Generally keep the with default value is ok.

  6. touchscreen-size-x: X-axis resolution, need fix according your IC configuration.

  7. touchscreen-size-y: Y-axis resolution, need fix according your IC configuration.

  8. touchscreen-max-w: Generally keep the with default value is ok.

  9. touchscreen-max-p: Generally keep the with default value is ok.

  10. goodix,int-sync: This is property is very for our IC to work properly, please don't modified it. 


```
&i2c2 {
/* gt9xx	*/
	gt9xx@14	{
		compatible = "goodix,gt9xx";
		reg = <0x14>;
		status = "okay";
		pinctrl-names = "default";
		pinctrl-0 = <&tsc_default>;
		
		irq-gpios = <&gpg 18 0>;
		irq-flags = <2>;
		reset-gpios = <&gpg 19 0>;

		touchscreen-max-id = <11>;
		touchscreen-size-x = <1024>;
		touchscreen-size-y = <600>;
		touchscreen-max-w = <1000>;
		touchscreen-max-p = <255>;

		goodix,int-sync = <1>;
		goodix,driver-send-cfg = <0>;
		goodix,swap-x2y = <0>;
		goodix,esd-protect = <1>;
		touchscreen-inverted-x = <0>;
		touchscreen-inverted-y = <0>;
		/*	do not flash configuration values at boot time  */
		goodix,cfg-group2 = [
		46 00 04 58 02 05 3D 00 01 10
		28 08 50 32 03 05 00 00 00 00
		00 00 00 1A 1C 20 14 90 30 AA
		47 49 C1 0E 00 00 01 83 02 11
		00 00 00 00 00 00 00 00 00 00
		00 32 55 94 C5 02 07 00 00 04
		C3 1B 00 A4 21 00 8C 28 00 78
		31 00 69 3B 00 69 00 00 00 00
		F0 50 3A FF FF 27 00 00 00 00
		00 00 00 00 00 00 00 00 00 00
		00 00 00 00 00 00 00 00 00 00
		00 00 00 01 04 05 06 07 08 09
		0C 0D 0E 0F 10 11 14 15 16 17
		18 19 00 00 00 00 00 00 00 00
		00 00 00 02 04 06 07 08 0A 0C
		0D 0E 0F 10 11 12 13 14 19 1B
		1C 1E 1F 20 21 22 23 24 25 26
		27 28 29 2A 00 00 00 00 00 00
		00 00 00 00 0D 01
		];
	};
};

```

Because we use Pinctrl to control irq-gpio state. Please add the following pinctrl state declaration to the target platform device tree. Attention here need fix the irq-gpio number according to the  

```
	tsc_default: tsc_default	{
		telechips,pins = "gpg-18", "gpg-19";
		telechips,pin-function = <0>;
	};
```

-----

# code review
 
```
module_init(gtp_init);
	|
	+-> static int __init gtp_init(void)
		/** 
		 *	add goodix_ts_driver to i2c driver
		 *	I2C 드라이버를 등록하기 위해 "i2c_add_driver()"가 호출되면, I2C 디바이스가 탐색되고 
		 *	드라이버가 탐색중인 디바이스를 지원하는 경우 드라이버의 "probe" 함수가 호출된다.
		 */
			static struct i2c_driver goodix_ts_driver = {
				.probe		= gtp_probe,
				.remove		= gtp_drv_remove,
				.id_table	= gtp_device_id,
				.shutdown	= gtp_shutdown,
				.driver = {
					.name	  = GTP_I2C_NAME,
					.owner	  = THIS_MODULE,
					.of_match_table = gtp_match_table,
					.pm		  = &gtp_pm_ops,
				},
			};
			|
			+-> static int gtp_parse_dt(struct device *dev, struct goodix_ts_platform_data *pdata)
			+-> i2c_set_clientdata(client, ts);
			+-> static int gtp_power_init(struct goodix_ts_data *ts)
			+-> static int gtp_power_on(struct goodix_ts_data *ts)
			+-> static int gtp_pinctrl_init(struct goodix_ts_data *ts)
			+-> static int gtp_request_io_port(struct goodix_ts_data *ts)
			+-> void gtp_reset_guitar(struct i2c_client *client, s32 ms)
			|	/**
			|	  * reset(initialize) chip.
			|	  */
			|	  |
			|	  +-> static int gtp_init_ext_watchdog(struct i2c_client *client)
			|	  	|
			|		+-> /**
			|			  *	initialize external watchdog for esd protect
			|			  * write 0xAA to ESD_Check(0x8041) addr	(return value 1: succed, otherwise: failed)
			|			  */
			+-> s32 gtp_get_fw_info(struct i2c_client *client, struct goodix_fw_info *fw_info)
			+-> static s8 gtp_request_input_dev(struct goodix_ts_data *ts)
			|	/**
			|	  * allocate input device
			|	  */
			+-> static int gtp_request_irq(struct goodix_ts_data *ts)
			|	/**
			|	  * Request interrupt if define irq pin else use delayed workqueue 
			|     * if vailed interrupt gpio pin : 인터럽트 _ gtp_irq_handler
			|	  * else : 폴링(use delayed workqueue) _ gtp_polling_work 
			|	  */
			|		+-> static irqreturn_t gtp_irq_handler(int irq, void *dev_id)
			|		|		+->	static void gtp_work_func(struct goodix_ts_data *ts)
			|		|		|	/** 
			|		|		|	  * goodix touchscreen sensor report function
			|		|		|	  */
			|		|		|		|
			|		|		|		+-> static int gtp_gesture_handler(struct goodix_ts_data *ts)
			|		|		|		|	/**
			|		|		|		|	  * if slide_wakeup enable && DOZE_MODE : check gesture type(ascii character , swipe right, left, down, up, double-tap)
			|		|		|	 	|	  * 	input report key(KEY_POWER) 
			|		|		|	 	|	  */
			|		|		|		+-> static u8 gtp_get_points(struct goodix_ts_data *ts, struct goodix_point_t *points, u8 *key_value)
			|		|		|			/**
			|		|		|			  * return touch state register value 
			|		|		|			  */
			|		|		
			|		+->	static void gtp_polling_work(struct work_struct *work)
			|		|		|	/** Timer interrupt servic routine for polling mode (10ms)
			|		|		+-> static void gtp_work_func(struct goodix_ts_data *ts)
			|
			+-> static int gtp_create_file(struct goodix_ts_data *ts)
			|	/**
			|	  * create proc and sys filesystem 
			|	  */
			+-> static int gtp_esd_init(struct goodix_ts_data *ts)
			|	/**
			|	  * workqueue : static void gtp_esd_check_func(struct work_struct *work)
			|	  * IC와 통신(read ic reg addr 0x8040) 2초 간격 실패 시, Reset IC
			|	  */
			+-> void gtp_esd_on(struct goodix_ts_data *ts)
				/**
				  * delayed work 실행 (timeout = 2*HZ) 
				  * schedule_delayed_work()
				  */

```
