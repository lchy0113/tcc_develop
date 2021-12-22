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

* inittab
 하드웨어 인식과 초기화 작업을 마친 커널은 프로세스 id(pid) 1번의 init 을 실행시킨다. 
 시스템의 첫번째 프로세스인 init은 실행하는 모든 프로세스들의 궁금적인 부모 역할을 하는 프로세스다.

 init이 실행될 때는 제일 먼저 /etc 에 있는 inittab 이란 파일을 읽어들인다. 이 파일은 init이 해야 할 모든 일이 적혀 있는 
 주문 양식(order form) 이라 할 수 있다. 
 
 /etc/inittab 파일의 각 항목에는 다음 필드가 있다. 
```
id:rstate :action :process
```

inittab 파일에 대한 필드 설명 


| 필드    	| 설명                                                                                                                     	|
|---------	|--------------------------------------------------------------------------------------------------------------------------	|
| id      	| 항목에 대한 고유 식별자입니다.                                                                                           	|
| rstate  	| 이 항목이 적용되는 실행 레벨을 나열합니다.                                                                               	|
| action  	| process 필드에 지정된 프로세스를 실행할 방법을 식별합니다.  가능한 값은 sysinit, boot, bootwait, wait 및 respawn 입니다. 	|
| process 	| 실행할 명령 또는 스크립트를 정의합니다.                                                                                  	|


## reference
-----
- https://source.android.com/devices/bootloader/images
- https://mediawiki.compulab.com/index.php/Android:_Boot_image
