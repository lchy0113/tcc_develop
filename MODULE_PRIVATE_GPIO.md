# MODULE PRIVATE_GPIO 
> A module that passes the GPIO interface to the Android framework.

```
module_platform_driver(kdiwin_gpio_driver); 
/* platform driver 용 진입부 */
|
+->	static struct platform_driver kdiwin_gpio_driver = {
    .probe = kdiwin_gpio_probe,
    .remove = kdiwin_gpio_remove,
	.driver = {
		.name = KDIWIN_GPIO_NAME, 
		.owner = THIS_MODULE,
		.of_match_table = kdiwin_gpio_of_match,
	},
};
	|
	+-> static int kdiwin_gpio_probe(struct platform_device *pdev)
		|
		+-> static int kdiwin_gpio_parse_dt(strcut device *dev, struct kdiwin_gpio_data *kdiwin_gpio) 
			/* Enter the GPIO Number and Config in the GPIO array. */
		+-> /* initialize workqueue and register handler */
		+-> static int kdiwin_gpio_request_io_port(struct kdiwin_gpio_data *kdiwin_gpio)
			/* initialize gpio */
			|
			+-> static int kdiwin_gpio_request_irq(struct kdiwin_gpio_data *kdiwin_gpio, int gpio)
				

	
```
