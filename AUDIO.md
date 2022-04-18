# AUDIO interface

## introduction
### Audio Interface
Three types of audio interface are supported; DAI, SPDIF, and CDIF.

| Interface 	| Description                                                                                                                                                                                                                                                   	| Remark                                           	|
|-----------	|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------	|--------------------------------------------------	|
| DAI       	| * I2S, LEft-Justified, and Right-justified waveform format.<br/>   * S16_LE and S24_LE interleaved format.<br/> * Stereo and Multi-Channels<br/> * Master and slave mode<br/> * Sample rates: 8-192 kHz                                                                           	|                                                  	|
| SPDIF     	| Two types of data formats for SPDIF <br/> * PCM data <br/>  * Stereo channel.<br/>   * S16_LE and S24_LE interleaved format.<br/> * compressed audio data(e.g. DTS, Dolby Digital, etc.)<br/>  Note: In case of same Audio Channel, SPDIF Rx Cannot be used with CDIF at the same time. 	| Sample rate list<br/>   * 44.1 kHz<br/> * 48 kHz<br/> * 32 kHz  	|
| CDIF      	| CDIF is available only for slave mode and data reception.<br/>* Data format<br/>   * I2S and Right-justified waveform format.<br/>   * S16_LE interleaved format.<br/> * About clock <br/>  * Bit clock: 32 fs<br/>   * Sample rates: 8-192 kHz                                            	|                                                  	|


### DAI 

 TCC898x는 IIS(Inter-IC Sound)를 준수하는 디지털 오디오 인터페이스를 제공합니다. 
 DAI에는 IIS 인터페이스를 위한 5개의 입력/출력 핀이 있습니다. 
 MCLK, *BCLK*, *LRCK*, *DAI*, *DAO*. 모든 DAI 입/출력 핀은 GPIO 핀으로 multiplexed 됩니다.

 - MCLK : MCLK는 CODEC 시스템 클럭에 사용되는 시스템 클럭 핀입니다. 
 	master 모드에서 MCLK는 DCLK로 알려진 클록 generator에서 생성되거나 
	slave 모드에서 칩 외부에서 공급될 수 있습니다.
	DAI는 128fs, 192fs, 256fs, 288fs, 384fs, 512fs, 768fs 및 1024fs를 시스템 클록으로 처리할 수 있습니다.
	256fs는 시스템 클록이 샘플링 주파수(fs)의 256배를 가짐을 의미합니다.
 - BCLK : BCLK는 IIS 데이터 교환을 위한 serial bit 클록입니다.
	 DAI는 시스템 클록을 나누어 64fs, 48fs 및 32fs를 생성할 수 있습니다.
	 BCLK의 polarity(극성)을 프로그래밍할 수 있습니다.
	   즉, serial bit BCLK의 상승 에지 또는 BCLK의 하강 에지 모두 적용할 수  있습니다.
 - LRCK : LRCK는 스테레오 오디오 채널 왼쪽 및 오른쪽에 대한 frame clock 입니다. 
 	LRCK의 주파수는 fs로 알려져 있습니다. 
	일반적으로 MP3 플레이어, CD 플레이어와 같은 오디오 응용 프로그램의 경우 fs는 8kHz ~ 192kHz로 설정할 수 있습니다.
	오디오 애플리케이션에서 광범위한 샘플링 주파수를 지원하기 위해 DCO 기능은 시스템 클록을 생성하는 데 매우 유용합니다.
	자세한 내용은 SMU&PMU의 PCLKDCOCTRLn 레지스터를 참조하십시오.
> 세 개의 클럭(MCLK, BCLK, LRCK) 모두 master 또는 slave로 선택 가능합니다.
 - DAI and DAO : DAI 및 DAO는 각각 serial data 입력 출력 핀입니다. 
	 DAI에는 내부 입력/출력 버퍼가 있습니다.
	 버퍼의 한 쪽은 데이터를 수신/전송하고 다른 쪽은 읽기/쓰기가 가능한 뱅크 버퍼 구조를 가지고 있습니다.
	   최대 데이터 워드 크기는 24비트입니다.
	     데이터는 32비트의 MSB로 정당화되고 0은 LSB로 채워집니다.

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

## 📌 analysis cx2070x

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
	|
	+-> static int cx2070x_i2c_probe(struct i2c_client *i2c, const struct i2c_device_id *id)
		/**
		  * regmap 초기화
		  */
		|
		+-> int cx2070x_probe(struct device *dev, struct regmap *regmap)
			/* codec private data 초기화 */
			struct cx2070x_priv {
				struct regmap *regmap;
				unsigned int sysclk;
				int is_clk_gated[NUM_OF_DAI];
				int master[NUM_OF_DAI];
				struct device *dev;
				const struct snd_soc_codec_driver *codec_drv;	/* codec driver(ops) */
				struct snd_soc_dai_driver *dai_drv;	/* dai driver */
				int num_dai;
				struct mutex update_lock;
				struct snd_soc_codec *codec;
				struct i2c_client *cx_i2c;
				struct gpio_desc *reset_gpio;
			| 
			+-> static int cx2070x_register_codec_driver(struct cx2070x_priv *cx2070x)
				/* snd_soc_dai_ops 초기화, codec driver 초기화. */
				/* Register a codec with the ASoC core : snd_soc_register_codec() */
```

### [codec driver] compatible = "telechips,snd-cx2070x"
/sound/soc/tcc/ <br/>
  tcc-adma.c <br/>
  tcc-dsp-api.c <br/>
  tcc-i2s-dsp.c* <br/>
  tcc-i2s.c* <br/>
  tcc-i2s.h* <br/>
  tcc-pcm-dsp.c* <br/>
  tcc-pcm-v10.c* <br/>
  tcc-pcm-v20.c* <br/>
  tcc-pcm.h* <br/>
  tcc_board_cx2070x.c <br/>

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
		  * codec driver
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

----- 

## 📌 analysis ak7755

### [snd_codec_driver]  ak7755
/sound/soc/codecs/ <br/>
  ak7755.c	<br/>
  ak7755_dsp_code.h	<br/>
  ak7755_dsp_code2.h <br/>
  ak7755.h <br/>

```dts
	ak7755: ak7755@18	{
		compatible = "akm.ak7755";
		reg = <0x18>;
		ak7755,pdn-gpio = <&gpg 0 0>;
	};
```

```c
static int ak7755_i2c_probe(struct i2c_client *i2c, const struct i2c_device_id *id)
	|	/**
	|	* ret = snd_soc_register_codec(&i2c->dev, 
	|	* 	&soc_codec_dev_ak7755, &ak7755_dai[0], ARRAY_SIZE(ak7755_dai));
	|	*/
	+-> struct snd_soc_codec_driver soc_codec_dev_ak7755 = {  // '15/10/23
	|		.probe = ak7755_probe,
	|		.remove = ak7755_remove,
	|		.suspend =	ak7755_suspend,
	|		.resume =	ak7755_resume,
	|	
	|	
	|		.idle_bias_off = true,
	|		.set_bias_level = ak7755_set_bias_level,
	|	
	|	#ifdef AK7755_DEBUG	//16/05/20
	|		.read = ak7755_reg_read,  // '16/02/22
	|		.write = ak7755_reg_write,
	|	#endif
	|		.controls = ak7755_snd_controls,
	|		.num_controls = ARRAY_SIZE(ak7755_snd_controls),
	|		.dapm_widgets = ak7755_dapm_widgets,
	|		.num_dapm_widgets = ARRAY_SIZE(ak7755_dapm_widgets),
	|		.dapm_routes = ak7755_intercon,
	|		.num_dapm_routes = ARRAY_SIZE(ak7755_intercon),
	|	}	
	|
	+-> static struct snd_soc_dai_ops ak7755_dai_ops = { 
			.hw_params	= ak7755_hw_params,
			.set_sysclk	= ak7755_set_dai_sysclk,
			.set_fmt	= ak7755_set_dai_fmt,
			.trigger = ak7755_trigger,
			.digital_mute = ak7755_set_dai_mute,
		};
		
		struct snd_soc_dai_driver ak7755_dai[] = {   
			{										 
				.name = "ak7755-AIF1",
				.playback = {
				       .stream_name = "Playback",
				       .channels_min = 1,
				       .channels_max = 2,
				       .rates = AK7755_RATES,
				       .formats = AK7755_FORMATS,
				},
				.capture = {
				       .stream_name = "Capture",
				       .channels_min = 1,
				       .channels_max = 4,
				       .rates = AK7755_RATES,
				       .formats = AK7755_FORMATS,
				},
				.ops = &ak7755_dai_ops,
			},										 
		};


static int ak7755_probe(struct snd_soc_codec *codec)
	| // parse devicetree
	+-> static int ak7755_init_reg(struct snd_soc_codec *codec)
		/**
		  * read device id
		  * initialize parameters
		  * initialize registers
		  */
		  	|
			+-> int snd_soc_update_bits(struct snd_soc_codec *codec, unsigned int reg, 
						unsigned int mask, unsigne dint value)
				/*
				 * update codec register bits
				 * : write new register value
				 */

	
```

- codec initialize
  *  read regs dump 
```c
static void read_regs_dump_ak7755(struct snd_soc_codec *codec)
	|
	+-> unsigned int ak7755_reg_read(struct snd_soc_codec *codec, unsigned int reg)
		/**
		  * return read data 
		  */
```
  * write regs init ak7755 
```c
static void write_regs_init_ak7755(struct snd_soc_codec *codec)
	|
	+-> static int ak7755_reg_write(struct snd_soc_codec *codec, unsigned int reg, unsigned int value)
		/**
		  * tx[0] = reg address
		  * tx[1] = reg value
		  * i2c_master_send i2c transmit 함수를 통해 전송
		  */
		  

```

### [snd_soc_card]  ak7755
/sound/soc/tcc/ <br/>
  tcc_board_ak7755.c <br/>

```dts
	/* sound */
	sound {
		compatible = "telechips,snd-ak7755";
		telechips,model = "TCC Audio Card";

		telechips,audio-routing = 
			"Headphone Jack", "HPOUTR",
            "Headphone Jack", "HPOUTL",
            "Int Spk", "ROP",
            "Int Spk", "RON",
            "Int Spk", "LOP",
            "Int Spk", "LON";
		telechips,dai-controller = <&i2s1>;
		telechips,audio-codec = <&ak7755>;
		status="okay";
	};

```


### [Functions] 

1. Mixer Control
ALSA의 mixer control 은 아래 기능을 제어 할 수 있다.
(1) Volume control and Function control
(2) Path control and Switch
(3) DSP control

1-1. Volume control and Function control
1-2. Path control and Switch
1-3. DSP control
(1) DSP PRAM Download
 "DSP Firmware PARM"의 mixer control는 PRAM data 를 AK7755의 PRAM에 write 한다. 
 "basic"은 ak7755_dsp_code.h의 ak7755_pram_basic[]을 PRAM에 write한다.
 "data*"는 ak7755_pram_data*.bin을 PRAM에 write한다. 
 ak7755_pram_dtaa*는 '/system/vendor/firmware/'경로에 위치해야 한다.
 [Format of ak7755_pram_xxxx.bin]
 PRAM Write Command 0xB8 (1byte)
 PRAM Write Address (2byte)
 PRAM CODEC

(2) DSP CRAM Download
 "DSP Firmware CRAM"의 mixer control는 AK7755의 CRAM에 CRAM data를 write 한다.
 "basic"은 ak7755_dsp_codec.h의 ak7755_cram_basic[]을 CRAM에 write 한다.
 "data*"는 ak7755_cram_data*.bin을 write한다. ak7755_cram_data*.bin은 '/system/vendor/firmware/'에 위치해야 한다.
 [Format of ak7755_cram_xxxx.bin]
 CRAM Write Command 0xB4 (1byte)
 CRAM Write Address (2byte)
 CRAM CODEC

(3) DSP OFREG Download
 "DSP Firmware OFREG"의 mixer control는 OFREG data를 AK7755의 OFREG에 write 한다.
 "basic"은 ak7755_dsp_code.h의 ak7755_pram_basic[]을 OFREG에 write 한다.
 "data*"는 ak7755_ofreg_data*.bin 을 OFREG에 write 한다. ak7755_ofreg_dtata*.bin 은 '/system/vendor/firmware'에 위치해야 한다.
 [Format of ak7755_ofreg_xxxx.bin]
 OFREG Write Command 0xB2 (1byte)
 OFREG Write Address (2byte)
 OFREG CODEC


#### Reference 
- PRAM : Program RAM
- CRAM : Coefficient RAM
- OFREG : Offset REG
- ACCRAM : Accelerator Coefficient RAM
