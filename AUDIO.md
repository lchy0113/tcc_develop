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

	/*	inter-ic sound, or integrated interchip sound */
	i2s@16101000 {
        pinctrl-names = "default";
        pinctrl-0 = <&m0dai1_clks &m0dai1_d0>; 
		port-mux = <1>;
        status = "disable";
	};

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

```dts

/*****************************************************
* Audio PinCtrl Start
******************************************************/
/*****************************************************
* Audio0 DAI Port_0 m:multi, m0:Audio0, dai0:port0 
******************************************************/

    m0dai0_clks: m0dai0_clks{
        telechips,pins = "gpf-0", "gpf-1", "gpf-2";
        telechips,pin-function = <2>;
    };

    m0dai0_d0: m0dai0_d0{
        telechips,pins = "gpf-3", "gpf-4";
        telechips,pin-function = <2>;
    };

    m0dai0_d1: m0dai0_d1{
        telechips,pins = "gpf-5", "gpf-6";
        telechips,pin-function = <2>;
    };

    m0dai0_d2: m0dai0_d2{
        telechips,pins = "gpf-7", "gpf-8";
        telechips,pin-function = <2>;
    };

    m0dai0_d3: m0dai0_d3{
        telechips,pins = "gpf-9", "gpf-10";
        telechips,pin-function = <2>;
    };

    m0dai0_spdif_rx: m0dai0_spdif_rx{
        telechips,pins = "gpf-13";
        telechips,pin-function = <2>;
    };

    m0dai0_spdif_tx: m0dai0_spdif_tx{
        telechips,pins = "gpf-14";
        telechips,pin-function = <2>;
    };

/*****************************************************
* Audio0 DAI Port_1 m:multi, m0:Audio0, dai1:port1
******************************************************/
    m0dai1_clks: m0dai1_clks{
        telechips,pins = "gpg-0", "gpg-1", "gpg-2";
        telechips,pin-function = <1>;
    };

    m0dai1_d0: m0dai1_d0{
        telechips,pins = "gpg-3", "gpg-4";
        telechips,pin-function = <1>;
    };

    m0dai1_spdif_rx: m0dai1_spdif_rx{
        telechips,pins = "gpg-5";
        telechips,pin-function = <2>;
    };

    m0dai1_spdif_tx: m0dai1_spdif_tx{
        telechips,pins = "gpg-5";
        telechips,pin-function = <1>;
    };

/*****************************************************
* Audio0 DAI Port_2 m:multi, m0:Audio0, dai2:port2
******************************************************/

    m0dai2_clks: m0dai2_clks{
        telechips,pins = "gpg-6", "gpg-7", "gpg-8";
        telechips,pin-function = <1>;
    };

    m0dai2_d0: m0dai2_d0{
        telechips,pins = "gpg-9", "gpg-10";
        telechips,pin-function = <1>;
    };

    m0dai2_d1: m0dai2_d1{
        telechips,pins = "gpg-11", "gpg-12";
        telechips,pin-function = <1>;
    };

    m0dai2_d2: m0dai2_d2{
        telechips,pins = "gpg-13", "gpg-14";
        telechips,pin-function = <1>;
    };

    m0dai2_d3: m0dai2_d3{
        telechips,pins = "gpg-15", "gpg-16";
        telechips,pin-function = <1>;
    };

    m0dai2_spdif_rx: m0dai2_spdif_rx{
        telechips,pins = "gpg-17";
        telechips,pin-function = <2>;
    };

    m0dai2_spdif_tx: m0dai2_spdif_tx{
        telechips,pins = "gpg-18";
        telechips,pin-function = <2>;
    };

/*****************************************************
* Audio1 DAI Port_0 m:multi, m1:Audio1, dai0:port0 
******************************************************/

    m1dai0_clks: m1dai0_clks{
        telechips,pins = "gpf-0", "gpf-1", "gpf-2";
        telechips,pin-function = <8>;
    };

    m1dai0_d0: m1dai0_d0{
        telechips,pins = "gpf-3", "gpf-4";
        telechips,pin-function = <8>;
    };

    m1dai0_d1: m1dai0_d1{
        telechips,pins = "gpf-5", "gpf-6";
        telechips,pin-function = <8>;
    };

    m1dai0_d2: m1dai0_d2{
        telechips,pins = "gpf-7", "gpf-8";
        telechips,pin-function = <8>;
    };

    m1dai0_d3: m1dai0_d3{
        telechips,pins = "gpf-9", "gpf-10";
        telechips,pin-function = <8>;
    };

    m1dai0_d4: m1dai0_d4{
        telechips,pins = "gpf-11", "gpf-12";
        telechips,pin-function = <8>;
    };

    m1dai0_spdif_rx: m1dai0_spdif_rx{
        telechips,pins = "gpf-13";
        telechips,pin-function = <8>;
    };

    m1dai0_spdif_tx: m1dai0_spdif_tx{
        telechips,pins = "gpf-14";
        telechips,pin-function = <8>;
    };

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

/*****************************************************
* Audio1 DAI Port_0 m:multi, m1:Audio1, dai2:port2 
******************************************************/

    m1dai2_clks: m1dai2_clks{
        telechips,pins = "gpg-6", "gpg-7", "gpg-8";
        telechips,pin-function = <3>;
    };

    m1dai2_d0: m1dai2_d0{
        telechips,pins = "gpg-9", "gpg-10";
        telechips,pin-function = <3>;
    };

    m1dai2_d1: m1dai2_d1{
        telechips,pins = "gpg-11", "gpg-12";
        telechips,pin-function = <3>;
    };

    m1dai2_d2: m1dai2_d2{
        telechips,pins = "gpg-13", "gpg-14";
        telechips,pin-function = <3>;
    };

    m1dai2_d3: m1dai2_d3{
        telechips,pins = "gpg-15", "gpg-16";
        telechips,pin-function = <3>;
    };

    m1dai2_d4: m1dai2_d4{
        telechips,pins = "gpg-17", "gpg-18";
        telechips,pin-function = <3>;
    };

    m1dai2_spdif_rx: m1dai2_spdif_rx{
        telechips,pins = "gpg-17";
        telechips,pin-function = <4>;
    };

    m1dai2_spdif_tx: m1dai2_spdif_tx{
        telechips,pins = "gpg-18";
        telechips,pin-function = <4>;
    };

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
