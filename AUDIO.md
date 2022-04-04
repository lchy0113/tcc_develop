# AUDIO interface

## introduction
### Audio Interface
Three types of audio interface are supported; DAI, SPDIF, and CDIF.

| Interface 	| Description                                                                                                                                                                                                                                                   	| Remark                                           	|
|-----------	|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------	|--------------------------------------------------	|
| DAI       	| * I2S, LEft-Justified, and Right-justified waveform format.<br/>   * S16_LE and S24_LE interleaved format.<br/> * Stereo and Multi-Channels<br/> * Master and slave mode<br/> * Sample rates: 8-192 kHz                                                                           	|                                                  	|
| SPDIF     	| Two types of data formats for SPDIF <br/> * PCM data <br/>  * Stereo channel.<br/>   * S16_LE and S24_LE interleaved format.<br/> * compressed audio data(e.g. DTS, Dolby Digital, etc.)<br/>  Note: In case of same Audio Channel, SPDIF Rx Cannot be used with CDIF at the same time. 	| Sample rate list<br/>   * 44.1 kHz<br/> * 48 kHz<br/> * 32 kHz  	|
| CDIF      	| CDIF is available only for slave mode and data reception.<br/>* Data format<br/>   * I2S and Right-justified waveform format.<br/>   * S16_LE interleaved format.<br/> * About clock <br/>  * Bit clock: 32 fs<br/>   * Sample rates: 8-192 kHz                                            	|                                                  	|


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

### [codec control driver] compatible = "conexant,cx2070xctl"
/drivers/kdiwin/cx2070x/ <br/>
  cx2070x-i2c.h* <br/>
  cx2070x.c* <br/>
  cx2070x.h* <br/>
  cx2070x_fw.h* <br/>
  cxdebug.c* <br/>
  cxdebug.h* <br/>
  cxpump.c* <br/>
  cxpump.h* <br/>
  Makefile* <br/>
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
	|
	+-> static int cx2070x_i2c_probe(struct i2c_client *i2c, const struct i2c_device_id *id)
		/**
		  * cdev, sys class 생성. 
		  * cx2070x 모듈과 i2c 초기화(firmware, register,,)
		  */
```

- log
```
[    3.458922] cx2070x codec driver version: 03,01,10,13
[    3.464082] [CNXT] sDesc = CNXT CHANNEL PATCH  09.00.00, sizeof CHAN_PATH = 19
[    5.459741] cx2070x: firmware download successfully! FW: 5,2,15, FW Patch: 9,0,0 
[    5.467200] cx2070x_download_firmware(): download firmware successfully.
[    5.478203] cx2070x_init(): firmware version 5.2, patch 9.0.0, chip CX20703 (ROM)
[    5.485738] cx2070x_init(): CX2070X patch version 1.1 
[    5.566731] [cx2070x] set register to init_register
[    5.571668] cx2070x: patch firmware successfully.
[    5.576633] cx2070x_init(): codec is ready.                                        
```

### compatible = "conexant,cx2070x"
/sound/soc/codecs/ <br/>
  cx2070x-i2c.c* <br/>
  cx2070x-spi.c* <br/>
  cx2070x-sysfs.c* <br/>
  cx2070x.c* <br/>
  cx2070x.h* <br/>

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

### [codec driver] compatible = "telechips,snd-cx2070x"
/sound/soc/tcc/
  tcc-adma.c
  tcc-dsp-api.c
  tcc-i2s-dsp.c*
  tcc-i2s.c*
  tcc-i2s.h*
  tcc-pcm-dsp.c*
  tcc-pcm-v10.c*
  tcc-pcm-v20.c*
  tcc-pcm.h*
  tcc_board_cx2070x.c

```c
static struct platform_driver cx2070x_driver = {
	.driver = {
		.name = "cx2070x-audio",
		.owner = THIS_MODULE,
		.pm = &snd_soc_pm_ops, /* for suspend */
		.of_match_table = of_match_ptr(tcc_cx2070x_match),
	},
	.probe = tcc_audio_probe,
	.remove = cx2070x_remove,
};
	|
	+-> static int tcc_audio_probe(struct platform_device *pdev)
		/**
		  *  
		  */
```

#### data structure
```c
static struct snd_soc_dai_link cx2070x_dai_link = {
	.name = "ASOC-CX2070X",
	.stream_name = "CX2070X_DP1",
//	.cpu_dai_name = str_dai_name,
	.codec_dai_name = "cx2070x-dp1",
	.ops = &cx2070x_ops,
//	.symmetric_rates = 1,
	.init = cx2070x_dai_init,
	.dai_fmt = (SND_SOC_DAIFMT_I2S | SND_SOC_DAIFMT_NB_NF | SND_SOC_DAIFMT_CBS_CFS),
	// master mode : SND_SOC_DAIFMT_CBS_CFS
	// slave mode : SND_SOC_DAIFMT_CBM_CFM
};

static struct snd_soc_card cx2070x_card = {
	.name = "TCC Audio", /* proc/asound/cards */
	.long_name = "Telechips Board",
//	.name = "I2S-CX2070X", /* proc/asound/cards */
	.owner = THIS_MODULE,
	.dai_link = &cx2070x_dai_link,
	.num_links = 1,
	.suspend_pre = &cx2070x_suspend_pre,
	.resume_pre = &cx2070x_resume_pre,
	.resume_post = &cx2070x_resume_post,
	.dapm_widgets = cx2070x_dapm_widgets,
	.num_dapm_widgets = ARRAY_SIZE(cx2070x_dapm_widgets),
#if 0
	.dapm_routes = cx2070x_audio_map,
	.num_dapm_routes = ARRAY_SIZE(cx2070x_audio_map),
#endif
	.dapm_routes = audio_map,
	.num_dapm_routes = ARRAY_SIZE(audio_map),
};

```

- log
```
    [    5.603512] tcc_audio_probe TCC Audio Card 
	[    5.607941] cx2070x 6-0014: cx2070x_codec_probe() 
	[    5.613848] cx2070x 6-0014: ASoC: no source widget found for LHPOUT 
	[    5.620187] cx2070x 6-0014: ASoC: Failed to add route LHPOUT -> direct -> Headset Jack 
	[    5.628233] cx2070x 6-0014: ASoC: no source widget found for LHPOUT
	[    5.634562] cx2070x 6-0014: ASoC: Failed to add route LHPOUT -> direct -> Headphone Jack 
	[    5.642781] cx2070x 6-0014: ASoC: no source widget found for RHPOUT 
	[    5.649174] cx2070x 6-0014: ASoC: Failed to add route RHPOUT -> direct -> Headphone Jack 
	[    5.657334] cx2070x 6-0014: ASoC: no source widget found for ROUT
	[    5.663547] cx2070x 6-0014: ASoC: Failed to add route ROUT -> direct -> Ext Spk  
	[    5.670984] cx2070x 6-0014: ASoC: no source widget found for LOUT  
	[    5.677147] cx2070x 6-0014: ASoC: Failed to add route LOUT -> direct -> Ext Spk   
	[    5.685186] cx2070x-audio sound: cx2070x-dp1 <-> 16201000.i2s mapping ok   
	[    5.691964] cx2070x-audio sound: ASoC: no source widget found for HPOUTR   
	[    5.698797] cx2070x-audio sound: ASoC: Failed to add route HPOUTR -> direct -> Headphone Jack 
	[    5.707449] cx2070x-audio sound: ASoC: no source widget found for HPOUTL 
	[    5.714212] cx2070x-audio sound: ASoC: Failed to add route HPOUTL -> direct -> Headphone Jack
	[    5.722870] cx2070x-audio sound: ASoC: no source widget found for ROP   
	[    5.729439] cx2070x-audio sound: ASoC: Failed to add route ROP -> direct -> Int Spk
	[    5.737166] cx2070x-audio sound: ASoC: no source widget found for RON      
	[    5.743728] cx2070x-audio sound: ASoC: Failed to add route RON -> direct -> Int Spk
	[    5.751514] cx2070x-audio sound: ASoC: no source widget found for LOP
	[    5.758023] cx2070x-audio sound: ASoC: Failed to add route LOP -> direct -> Int Spk
	[    5.765800] cx2070x-audio sound: ASoC: no source widget found for LON
	[    5.772308] cx2070x-audio sound: ASoC: Failed to add route LON -> direct -> Int Spk        
```
