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
  &i2c0 {
    	gt9xx@5d {
          compatible = "goodix,gt9xx";
          reg = <0x5d>; 
          pinctrl-names = "default", "int-output-low","int-output-high", "int-input";
          pinctrl-0 = <&ts_int_default>;
          pinctrl-1 = <&ts_int_output_low>;
          pinctrl-2 = <&ts_int_output_high>;
          pinctrl-3 = <&ts_int_input>;

          reset-gpios = <&msm_gpio 12 0x0>;
          irq-gpios = <&msm_gpio 13 0x2800>;
          irq-flags = <2>;

          touchscreen-max-id = <11>;
          touchscreen-size-x = <1080>;
          touchscreen-size-y = <1920>;
          touchscreen-max-w = <512>;
          touchscreen-max-p = <512>;

          goodix,int-sync = <1>;
      };
  }
  ```

  Because we use Pinctrl to control irq-gpio state. Please add the following pinctrl state declaration to the target platform device tree. Attention here need fix the irq-gpio number according to the  

  ```
  &msmgpio {               
  	/* add pingrp for touchscreen */
  	ts_int_default: ts_int_defalut {
  		mux {
  			pins = "gpio13";
  			function = "gpio";
  		};
  		config {
  			pins = "gpio13";
  			drive-strength = <16>;
  			/*bias-pull-up;*/
  			input-enable;
  			bias-disable;
  		};
  	};

  	ts_int_output_high: ts_int_output_high {
  		mux {
  			pins = "gpio13";
  			function = "gpio";
  		};
  		config {
  			pins = "gpio13";
  			output-high;
  		};
  	};

  	ts_int_output_low: ts_int_output_low {
  		mux {
  			pins = "gpio13";
  			function = "gpio";
  		};
  		config {
  			pins = "gpio65";
  			output-low;
  		};
  	};

  	ts_int_input: ts_int_input {
  		mux {
  			pins = "gpio13";
  			function = "gpio";
  		};
  		config {
  			pins = "gpio13";
  			input-enable;
  			bias-disable;
  		};
  	};
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
			|	  * reset chip.
			|	  */
			|	  |
			|	  +-> static int gtp_init_ext_watchdog(struct i2c_client *client)
			|	  	|
			|		+-> /**
			|			  *	initialize external watchdog for esd protect
			|			  */
			+-> s32 gtp_get_fw_info(struct i2c_client *client, struct goodix_fw_info *fw_info)
			+-> static s8 gtp_request_input_dev(struct goodix_ts_data *ts)
			+-> static int gtp_request_irq(struct goodix_ts_data *ts)
			|	/**
			|	  * Request interrupt if define irq pin else use delayed workqueue 
			|	  * 인터럽트 : gtp_interrupt_work
			|	  * 폴링 : gtp_polling_work 
			|	  */
			+-> static int gtp_create_file(struct goodix_ts_data *ts)
			|	/**
			|	  * create proc and sys filesystem 
			|	  */
			+-> static int gtp_esd_init(struct goodix_ts_data *ts)
			|	/**
			|	  * gtp_esd_check_func workqueue 등록
			|	  * INIT_DELAYED_WORK
			|	  */
			+-> void gtp_esd_on(struct goodix_ts_data *ts)
				/**
				  * delayed work 실행 (timeout = 2*HZ) 
				  * schedule_delayed_work()
				  */



```
