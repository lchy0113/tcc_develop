COMPOSITE (CVBS-OUT) 
=====

> composite (cvbs-out)장치에 대해 정리.



# Device

 - tcc_tve

	 ```dtb
	tcc_tve: tve@12200000 {
		status = "disabled";
		compatible = "telechips,tcc-tve";
		reg = <0x12200000 0x100 0x12200800 0x10>;
		clocks = <&clk_ddi DDIBUS_NTSCPAL &clk_isoip_ddi ISOIP_DDB_VDAC>;
	};
	 ```


 - register 

	 ![](./images/COMPOSITE_01.png)
