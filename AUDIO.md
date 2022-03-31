# AUDIO interface

## introduction
### Audio Interface
Three types of audio interface are supported; DAI, SPDIF, and CDIF.

| Interface 	| Description                                                                                                                                                                                                                                                   	| Remark                                           	|
|-----------	|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------	|--------------------------------------------------	|
| DAI       	| * I2S, LEft-Justified, and Right-justified waveform format.   * S16_LE and S24_LE interleaved format. * Stereo and Multi-Channels * Master and slave mode * Sample rates: 8-192 kHz                                                                           	|                                                  	|
| SPDIF     	| Two types of data formats for SPDIF * PCM data   * Stereo channel.   * S16_LE and S24_LE interleaved format. * compressed audio data(e.g. DTS, Dolby Digital, etc.)  Note: In case of same Audio Channel, SPDIF Rx Cannot be used with CDIF at the same time. 	| Sample rate list   * 44.1 kHz * 48 kHz * 32 kHz  	|
| CDIF      	| CDIF is available only for slave mode and data reception. * Data format   * I2S and Right-justified waveform format.   * S16_LE interleaved format. * About clock   * Bit clock: 32 fs   * Sample rates: 8-192 kHz                                            	|                                                  	|


## kernel device tree
- Define DAI device with GPIO Port Information
  * To add audio device, redefine and enable DAI device in device tree for target board. 
```dts
// tcc8985-soc-module-p04.dtsi
	/*
	 * dummy i2c (used sound codec)
	 */
	i2c_gpio6:i2c@6 {
		compatible = "i2c-gpio";
		status = "okay";
		/* remap to dummy gpios */
		gpios = <&gpd 13 0
			&gpd 14 0
			>;
		i2c-gpio,delay-us = <10>; 
		#address-cells = <1>;
		#size-cells = <0>;

		cx2070x: cx2070x@14 {
			#sound-dai-cells = <0>;
			compatible = "conexant,cx2070x";
			reg = <0x14>;
			reset-gpio = <&gpg 0 0>;
		};
	};


	/* sound */
	sound {
		compatible = "telechips,snd-cx2070x";
		telechips,model = "TCC Audio Card";

		telechips,audio-routing = 
			"Headphone Jack", "HPOUTR",
            "Headphone Jack", "HPOUTL",
            "Int Spk", "ROP",
            "Int Spk", "RON",
            "Int Spk", "LOP",
            "Int Spk", "LON";
		telechips,dai-controller = <&i2s1>;
		telechips,audio-codec = <&cx2070x>;

		status="okay";
	};


	(...)

	/**
      * pinctrl-names : The name of pinctrl for DAI.
	  * pinctrl-0, pinctrl-1 : The group of GPIO port in each case of pinctrl-names.
	  * port-mux : 
	  */
	i2s@16201000 {
        pinctrl-names = "default";
        pinctrl-0 = <&m1dai1_clks &m1dai1_d0>;
		port-mux = <1>;
        status = "okay";
	};

	/* i2c1 devices	*/
	i2c@16310000 {
		status = "okay";
		port-mux = <7>;
		pinctrl-names = "default";
		pinctrl-0 = <&i2c7_bus>;

		/* cx2070xctrl	*/
		cx2070xctl: cx2070xctl@14 {
			compatible = "conexant,cx2070xctl";
			reg = <0x14>;
			reset-gpio = <&gpg 0 0>;
		};
	};

```

- This is a part of GPIO port group for audio interfaces.
```dts

/*****************************************************
* Audio PinCtrl Start
******************************************************/

	(...)

/*****************************************************
* Audio1 DAI Port_0 m:multi, m1:Audio1, dai1:port1 
******************************************************/

	x_nrset_cx: x_nrset_cx	{
		telechips,pins = "gpg-0";
		telechips,pin-function = <0>;
	};

    m1dai1_clks: m1dai1_clks{
        telechips,pins = "gpg-1", "gpg-2";
        telechips,pin-function = <3>;
    };

    m1dai1_d0: m1dai1_d0{
        telechips,pins = "gpg-3", "gpg-4";
        telechips,pin-function = <3>;
    };


    m1dai1_spdif_rx: m1dai1_spdif_rx{
        telechips,pins = "gpg-5";
        telechips,pin-function = <4>;
    };

    m1dai1_spdif_tx: m1dai1_spdif_tx{
        telechips,pins = "gpg-5";
        telechips,pin-function = <3>;
    };

	(...)

/*****************************************************
* Audio PinCtrl END
******************************************************/
```

```dts

// tcc898x.dtsi

/ {
	compatible = "telechips,tcc898x";
	interrupt-parent = <&gic>;
	#address-cells = <1>;
	#size-cells = <1>;

	chosen {
		bootargs = "vmalloc=480M";
	};

	aliases {
		i2c0 = &i2c0;
		i2c1 = &i2c1;
		i2c2 = &i2c2;
		i2c3 = &i2c3;
		pcm0 = &pcm0;
		pcm1 = &pcm1;
		adma0 = &adma0;
		adma1 = &adma1;
		i2s0 = &i2s0;
		i2s1 = &i2s1;
(...)

	adma0: adma@16100000 {
		compatible = "telechips,adma";
		reg = <0x16100000 0x200>;
		interrupts = <GIC_SPI 54 IRQ_TYPE_LEVEL_HIGH>;
	};

	adma1: adma@16200000 {
		compatible = "telechips,adma";
		reg = <0x16200000 0x200>;
		interrupts = <GIC_SPI 56 IRQ_TYPE_LEVEL_HIGH>;
	};

    i2s0: i2s@16101000 {
        compatible = "telechips,i2s";
        reg = <0x16101000 0x50>;
        clocks = <&clk_peri PERI_MDAI0 &clk_io IOBUS_DAI0>;
        clock-frequency = <32000>;   // For HDMI Audio first Setting
		adma = <&adma0>;
        status = "disabled";
    };

    i2s1: i2s@16201000 {
        compatible = "telechips,i2s";
        reg = <0x16201000 0x50>;
        clocks = <&clk_peri PERI_MDAI1 &clk_io IOBUS_DAI1>;
        clock-frequency = <32000>;   // For HDMI Audio first Setting
		adma = <&adma1>;
        status = "disabled";
    };

(...)

```

## analysis cx2070x

### compatible = "conexant,cx2070xctl"
- drivers/kdiwin/cx2070x/cx2070x.c 

```c
static struct i2c_driver cx2070x_i2c_driver = {
  .driver = {
    	.name = "cx2070xctl",
    	.owner = THIS_MODULE,
		.of_match_table = cx2070x_of_match,
   },
  .probe=cx2070x_i2c_probe,
  .remove=cx2070x_i2c_remove,
  .id_table=cx2070x_i2c_id,
};

struct cx2070x_priv
{
  //enum snd_soc_control_type control_type;	// KJW
  void *control_data;	/* i2c */
  unsigned int sysclk;
  int	       master;
  enum Cx_INPUT_SEL input_sel;
  enum Cx_OUTPUT_SEL output_sel;
  unsigned int mute;
  struct gpio_desc *reset_gpio;
};


```

### compatible = "conexant,cx2070x"
- sound/soc/codecs/cx2070x-i2c.c
- sound/soc/codecs/cx2070x.c

```c
static struct i2c_driver cx2070x_i2c_driver = {
	.driver = {
		.name = "cx2070x",
		.of_match_table = cx2070x_of_match,
	},
	.probe = cx2070x_i2c_probe,
	.remove = cx2070x_i2c_remove,
	.id_table = cx2070x_i2c_id,
};

```
- sound/soc/tcc/tcc_board_cx2070x.c

