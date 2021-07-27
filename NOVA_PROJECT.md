# NOVA_PROJECT
Information technology related to the nova project.

- 새 기기 추가
```
tcc8985_nova/device/kdiwin$ find -name vendorsetup.sh
./test/a40i_poc/vendorsetup.sh
./test/a40i_evb/vendorsetup.sh
./test/tcc_nova/vendorsetup.sh
./lobby/nhnlp41/vendorsetup.sh
./lobby/nhnlp51/vendorsetup.sh
./nova/vendorsetup.sh
./nova/a40i/vendorsetup.sh
./wallpad/nhn1051/vendorsetup.sh
./wallpad/nhn1033/vendorsetup.sh
./wallpad/nhn1311/vendorsetup.sh
./wallpad/nhn1041/vendorsetup.sh
```

- Understanding build layers
> Android 빌드 시스템에서는 리소스 오버레이를 사용하여 빌드 시에 제품을 맞춤설정합니다. 리소스 오버레이는 기본값 외에 적용되는 리소스 파일을 지정합니다. 리소스 오버레이를 사용하려면 프로젝트 buildfile을 수정하여 PRODUCT_PACKAGE_OVERLAYS를 최상위 수준 디렉터리에 대한 상대적인 경로로 설정합니다. 이 경로는 빌드 시스템에서 리소스를 검색할 때 현재 루트와 함께 검색되는 섀도 루트가 됩니다.
>
> 가장 일반적인 맞춤설정은 frameworks/base/core/res/res/values/config.xml 파일에 포함됩니다.
>
> 이 파일에 리소스 오버레이를 설정하려면 다음 중 하나를 사용하여 프로젝트 buildfile에 오버레이 디렉터리를 추가합니다.
```
tcc8985_nova/device/kdiwin/wallpad/nhn1041

# Inherit from those products. Most specific first.
$(call inherit-product, device/kdiwin/wallpad/nhn1041/device.mk)
$(call inherit-product, device/kdiwin/wallpad/common/common.mk)							(1)
$(call inherit-product, device/kdiwin/wallpad/common/version.mk)						(2)
$(call inherit-product, device/kdiwin/nova/tcc8985/device.mk)							(3)
$(call inherit-product-if-exists, vendor/kdiwin/prebuilts/apks/prebuilt.mk)				(4)
$(call inherit-product-if-exists, vendor/kdiwin/packages/Wall/product/build/wall.mk)
$(call inherit-product, device/google/atv/products/atv_base.mk)

# Overrides
PRODUCT_NAME := nhn1041
PRODUCT_DEVICE := nhn1041
PRODUCT_MODEL := NHN-1041
PRODUCT_BRAND := Android
PRODUCT_MANUFACTURER := KDNAVIEN
```

(1) : tcc8985_nova/device/kdiwin/wallpad/common/common.mk 
```
DEVICE_PACKAGE_OVERLAYS += \
    device/kdiwin/wallpad/common/overlay

PRODUCT_PACKAGES += \
    peripheral_io.tcc898x

# TODO: Move it to nova/common if the inheritance from <soc>.mk(s) completely removed
# see also device/kdiwin/nova/a40i/device.mk
PRODUCT_COPY_FILES += \
    device/kdiwin/wallpad/common/configs/min_core_hardware.xml:system/etc/permissions/tablet_core_hardware.xml

PRODUCT_COPY_FILES += \
    vendor/kdiwin/lib/libARM_ARCH.so:/system/lib/libARM_ARCH.so \
    vendor/kdiwin/lib/libserial_port.so:/system/lib/libserial_port.so

PRODUCT_PACKAGES += \
    gpio.default    \
    wallpad-keyboard
```


```
/tcc8985_nova/device/kdiwin/wallpad/common/overlay$ tree
.
├── frameworks
│   └── base
│       ├── core
│       │   └── res
│       │       └── res
│       │           ├── values
│       │           │   ├── config.xml
│       │           │   ├── custom.xml
│       │           │   └── dimens.xml
│       │           └── xml
│       │               └── global_keys.xml
│       └── packages
│           └── SettingsProvider
│               └── res
│                   └── values
│                       └── defaults.xml
└── vendor
    └── kdiwin
	        └── packages
	            └── Wall
	                └── service
	                    └── res
	                        └── xml
	                            └── gpio_keys.xml

18 directories, 6 files
```

(2) : tcc8985_nova/device/kdiwin/wallpad/common/version.mk
```
BUILD_VERSION := 0.9.0
BUILD_DATE := $(shell $(DATE) +%y%m%d)

BUILD_NUMBER := $(TARGET_PRODUCT).$(BUILD_VERSION).$(BUILD_DATE)
~
```


(3) : tcc8985_nova/device/kdiwin/nova/tcc8985/device.mk 
```
TARGET_BOARD_SOC := tcc898x
KERNEL_VERSION := v3_18
ARM_VERSION := arm

USB_DEFAULT_HOST := false
USE_MASS_STORAGE := false

ifeq ($(USE_MASS_STORAGE),true)
DEVICE_PACKAGE_OVERLAYS := device/kdiwin/nova/tcc8985/ums/overlay
endif

DEVICE_PACKAGE_OVERLAYS += device/kdiwin/nova/tcc8985/overlay

# Define for Output Mode
PRODUCT_PROPERTY_OVERRIDES += \
        persist.sys.output_mode = 0

# Define for HDMI
# Setting Menu enable
PRODUCT_PROPERTY_OVERRIDES += \
    ro.system.hdmi_active = true

PRODUCT_PROPERTY_OVERRIDES += \
    persist.sys.hdmi_resolution = 125 \
    persist.sys.hdmi_mode = 0 \
    persist.sys.hdmi_resize_up = 0 \
    persist.sys.hdmi_resize_dn = 0 \
    persist.sys.hdmi_resize_lt = 0 \
    persist.sys.hdmi_resize_rt = 0 \
    tcc.hdmi.uisize = 1920x1080

PRODUCT_PROPERTY_OVERRIDES += \
    persist.sys.hdmi_aspect_ratio = 0 \
    persist.sys.hdmi_color_space = 125 \
    persist.sys.hdmi_color_depth = 0


(...)

PRODUCT_COPY_FILES += \
    vendor/kdiwin/lib/libARM_ARCH.so:/system/lib/libARM_ARCH.so \
    vendor/kdiwin/lib/libserial_port.so:/system/lib/libserial_port.so

# nhn1033 Product Package
PRODUCT_PACKAGES += \
    gpio.default    \
    wallpad-keyboard

PRODUCT_CHARACTERISTICS := tv,sdcard
#PRODUCT_CHARACTERISTICS := tablet,sdcard
PRODUCT_AAPT_CONFIG := normal large xlarge xhdpi

# Inherit from parent makefiles. Most specific first.
$(call inherit-product, device/kdiwin/nova/common/device.mk)
```


: tcc8985_nova/device/kdiwin/nova/common/device.mk
```
PRODUCT_COPY_FILES += \
    device/kdiwin/nova/common/init.nova.common.rc:root/init.nova.common.rc

DEVICE_PACKAGE_OVERLAYS += \
    device/kdiwin/nova/common/overlay

ifneq ($(filter userdebug user,$(TARGET_BUILD_VARIANT)),)
# Enable adb authentication
PRODUCT_PROPERTY_OVERRIDES += \
    ro.adb.secure=1
# Copy single adb key allowed for restricted developer(s)
PRODUCT_COPY_FILES += \
   device/kdiwin/nova/common/security/adb_keys:root/adb_keys
# Specify tcp port for adb connection
PRODUCT_PROPERTY_OVERRIDES += \
   persist.adb.tcp.port=5577
endif
```

(4) : 설치할 APK list


- kernel.mk
```
device/kdiwin/nova/common/kernel.mk
```
