# MMC

-----

## issue: log debug

```bash
(...)
mmc0: Error -74 starting bkops
(...)
```

 - error number
```c
#define	EBADMSG		74	/* Not a data message */
```

### bkops feature
> bkops : background operations(bkops) feature

 eMMC는 Host에 의해 시작된 normal operations과 별도로 런타임 동안 internal maintenance(관리) 목적에 필요한 다양한 internal background operations을 수행할 수 있습니다. 

 read, write와 같이 time-critical 이 중요한 operations에 time 을 줄이고, idle time 동안 eMMC 제어 전력 소비를 최소화하기 위해, 이 기능은 Host에 device background operations을 지연시키는기능을 제공합니다.


 - reference : https://www.jedec.org/sites/default/files/Victor_Tsai.pdf

 - *code*

 > 로그가 출력된 code
 > support eMMC card에 대해서 **bkops feature**을 시작하는 함수 입니다. 
```c
/**
 *	mmc_start_bkops - start BKOPS for supported cards
 *	@card: MMC card to start BKOPS
 *	@form_exception: A flag to indicate if this function was
 *			 called due to an exception raised by the card
 *
 *	Start background operations whenever requested.
 *	When the urgent BKOPS bit is set in a R1 command response
 *	then background operations should be started immediately.
*/
void mmc_start_bkops(struct mmc_card *card, bool from_exception)
{
	int err;
	int timeout;
	bool use_busy_signal;

	BUG_ON(!card);

	if (!card->ext_csd.bkops_en || mmc_card_doing_bkops(card))
		return;

	err = mmc_read_bkops_status(card);
	if (err) {
		pr_err("%s: Failed to read bkops status: %d\n",
		       mmc_hostname(card->host), err);
		return;
	}

	if (!card->ext_csd.raw_bkops_status)
		return;

	if (card->ext_csd.raw_bkops_status < EXT_CSD_BKOPS_LEVEL_2 &&
	    from_exception)
		return;

	mmc_claim_host(card->host);
	if (card->ext_csd.raw_bkops_status >= EXT_CSD_BKOPS_LEVEL_2) {
		timeout = MMC_BKOPS_MAX_TIMEOUT;
		use_busy_signal = true;
	} else {
		timeout = 0;
		use_busy_signal = false;
	}

	err = __mmc_switch(card, EXT_CSD_CMD_SET_NORMAL,
			EXT_CSD_BKOPS_START, 1, timeout,
			use_busy_signal, true, false);
	if (err) {
		pr_warn("%s: Error %d starting bkops\n",
			mmc_hostname(card->host), err);
		goto out;
	}

	/*
	 * For urgent bkops status (LEVEL_2 and more)
	 * bkops executed synchronously, otherwise
	 * the operation is in progress
	 */
	if (!use_busy_signal)
		mmc_card_set_doing_bkops(card);
out:
	mmc_release_host(card->host);
}
EXPORT_SYMBOL(mmc_start_bkops);
```






-----

eMMC 

=====

> eMMC 장치가 제대로 동작되는지 확인 하는 방법.

-----

아래 방법으로 eMMC가 제대로 동작되는지 확인 할 수 있습니다.

1. eMMC의 전원을 켜고, eMMC가 장착된 장치를 부팅합니다.
2. 부팅이 완료되면, eMMC 의 용량을 확인합니다.

```bash
// getting eMMC info
[2023-04-03 09:58:37] [    3.512325] mmc0: BKOPS_EN bit is not set
[2023-04-03 09:58:37] [    3.514628] mmc0: switch to bus width 8
[2023-04-03 09:58:37] [    3.522942] usb usb1: New USB device found, idVendor=1d6b, idProduct=0002
[2023-04-03 09:58:37] [    3.529795] usb usb1: New USB device strings: Mfr=3, Product=2, SerialNumber=1
[2023-04-03 09:58:37] [    3.530806] mmc0: new DDR MMC card at address 0001
[2023-04-03 09:58:37] [    3.531061] mmcblk0: mmc0:0001 H8G4a2 7.28 GiB
[2023-04-03 09:58:37] [    3.531138] mmcblk0boot0: mmc0:0001 H8G4a2 partition 1 4.00 MiB
[2023-04-03 09:58:37] [    3.531203] mmcblk0boot1: mmc0:0001 H8G4a2 partition 2 4.00 MiB
[2023-04-03 09:58:37] [    3.534351]  mmcblk0: p1 p2 p3 p4 p5 p6 p7 p8 p9 p10 p11
[
```

3. sysfs의 device 정보를 확인합니다.

```bash
target_dev:/sys/class/mmc_host/mmc0/mmc0:0001 $ cat cid
90014a483847346132a4001203b95800
target_dev:/sys/class/mmc_host/mmc0/mmc0:0001 $ cat manfid
0x000090
target_dev:/sys/class/mmc_host/mmc0/mmc0:0001 $ cat oemid
0x014a
target_dev:/sys/class/mmc_host/mmc0/mmc0:0001 $ cat name
H8G4a2
target_dev:/sys/class/mmc_host/mmc0/mmc0:0001 $ cat serial
0x001203b9
target_dev:/sys/class/mmc_host/mmc0/mmc0:0001 $ cat date
05/2021
target_dev:/sys/class/mmc_host/mmc0/mmc0:0001 $
```

```bash
target_dev:/sys/class/mmc_host/mmc0/mmc0:0001/block/mmcblk0 $ cat size
15269888
```
 - 15269888 는 sector size입니다. 
 - 15269888 * 512 = 7818182656 / 1024 / 1024 / 1024 = 7.28 GiB

4. eMMC 장치에 파일을 저장하고, 저장된 파일을 읽어 봅니다.

 - sample (./attachment/SD_Card_test.2.0.apk)

  ![](./images/MMC_01.png)
  ![](./images/MMC_02.png)
	 
5. eMMC의 속도를 측정합니다.

  ![](./images/MMC_03.png)
