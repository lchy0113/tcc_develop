# MMC

-----

## issue: log debug

```bash
(...)
mmc0: Error -74 starting bkops
(...)
```

 - bkops feature
> bkops : background operations(bkops) feature

 eMMC는 Host에 의해 시작된 normal operations과 별도로 런타임 동안 internal maintenance(관리) 목적에 필요한 다양한 internal background operations을 수행할 수 있습니다. 

 read, write와 같이 time-critical 이 중요한 operations에 time 을 줄이고, idle time 동안 eMMC 제어 전력 소비를 최소화하기 위해, 이 기능은 Host에 device background operations을 지연시키는기능을 제공합니다.


- reference : https://www.jedec.org/sites/default/files/Victor_Tsai.pdf

 - code
 code에서 출력된 로그.
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

   * mmc_start_bkops
  support eMMC card에 대해서 **bkops feature**을 시작하는 함수 입니다. 

   * error code : 
```c
#define	EBADMSG		74	/* Not a data message */
```
