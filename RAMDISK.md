# boot.img 
-----

boot.img or recovery.img = kernel(zImage) + ramdisk 

## boot.img 생성방법
-----

- boot.img : from comdline (for offsets and sized, refer to system/core/mkbootimg/bootimg.h)
	> boot.img is a composite image which includes the kernel zImage, ramdisk, and boot parameters.

example)
```
mkbootimg --kernel zImage --ramdisk ramdisk.img --base 0x80000000 --cmdline "console=ttyO2,115200n8 mem=456M@0x80000000 mem=512M@0xA0000000 init=/init vram=10M omapfb.vram=0:4M androidboot.console=ttyO2" --board omap4 -o boot.img.new
[출처] 안드로이드용 boot.img system.img ramdisk.img userdata.img 만들기, 만든후 unpack방법|작성자 s3c24xx

mkbootimg --kernel zImage --ramdisk ramdisk.img.gz -o --boot.img

```

 * tcc8985 AOSP boot image version : Legacy boot image header, version 0
	 

### develop
-----

```
$ /bin/bash -c "out/host/linux-x86/bin/mkbootimg  --kernel out/target/product/nhn1033/kernel --ramdisk out/target/product/nhn1033/ramdisk.img --base 0x20000000 --cmdline \"androidboot.selinux=permissive buildvariant=userdebug\" --os_version 8.1.0 --os_patch_level 2018-04-05  --output out/target/product/nhn1033/boot.img"
```

## boot.img 분석
-----

```
$ abootimg -x boot.img
writing boot image config in bootimg.cfg
extracting kernel in zImage
extracting ramdisk in initrd.img

```

## system.img 생성방법
-----

example
```
system.img 만들기.
make_ext4fs -s -l 268435456 -a system system.img ./system
-l : ext4 파티션 사이즈.
-a : 안드로이드 마운트 지점.
system.img : 생성될 파일이름.
./system : 패키징할 디렉토리.
[출처] 안드로이드용 boot.img system.img ramdisk.img userdata.img 만들기, 만든후 unpack방법|작성자 s3c24xx
```

## RAMDISK
-----

initramfs_data.cpio.gz 
```
$ gzip -d initramfs_data.cpio.gz
```

## init
-----

- init - 커널 실행순서
 /init 이 실행되기 전까지 커널은 일반커널의 동작과 전혀 차이가 없다. 
 커널 내 몇가지 option이 안드로이드용으로 추가된것은 있지만 흐름은 같다.

 bootloader 실행 -> 커널 loading >  커널 실행 까지 같음.

 커널 실행 후 최초 프로세스인 /init 이 실행될때 안드로이드는 안드로이드 용 init을 실행한다.
 일반적인 리눅스라면 /etc/inittab 을 참조하고, /etc/init.d/rcS를 실행한다.
 (안드로이드는 init.rc 를 수행한다.)
 참조 코드 : system/core/init.c

- linux와 android 비교
|          	| linux         	| android                                           	|
|----------	|---------------	|---------------------------------------------------	|
| init     	| /sbin/init    	| /init                                             	|
| 설정     	| /etc/inittab  	| /init.rc                                          	|
| 암호     	| /etc/password 	| 없음 (사용자가 한명이므로 별도 관리하지 않음)     	|
| 접근권한 	| /etc/group    	| 없음 (대신 별도의 헤더 파일에 하드 코딩되어 있음) 	|


## reference
-----
- https://source.android.com/devices/bootloader/images
- https://mediawiki.compulab.com/index.php/Android:_Boot_image
