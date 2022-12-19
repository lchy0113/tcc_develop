# CAMERA

> Telechips 플랫폼의 Camera 모듈에 대해 정리.

---

## The Camera Provider of the Android Camera principle starts

1. Camera provider process 소개.

```bash
nhn1033:/ # ps -e  | grep camrea
1|nhn1033:/ # ps -e  | grep camera
cameraserver  1775     1   42092   6608 binder_thread_read b52de2f8 S android.hardware.camera.provider@2.4-service
cameraserver  1812     1   47524  12956 binder_thread_read b31d62f8 S cameraserver
nhn1033:/ #
```

 pid 1775은 camera provider프로세스로서 cameraserver보다 일찍 실행. 
 디바이스에서 실행되는 android.hardware.cameraprovider@2.4-service process는 camera 작동을 지원하는 중요한 프로세스.
 
 ![Camera 구조](images/CAMERA_01.png)

 위의 그림에서 camera architecture는 camera provider process의 위치를 보여준다. 
 HAL layer는 camera provider process에서 실행된다.

2. android.hardware.camera.provider@2.4-service 프로세스.

소스코드 위치 : hardware/interfaces/camera/provider/
 ![](images/CAMERA_02.png)

 hardware/interfaces/camera/provider/2.4/default/ 경로에 android.hardware.camera.provider@2.4-service.rc파일이 존재한다. 
 Android 초기화는 이러한 rc파일을 실행하는 것이다. 
 실행 코드를 살펴보자.

```bash
service camera-provider-2-4 /vendor/bin/hw/android.hardware.camera.provider@2.4-service
    class hal
	user cameraserver
	group audio camera input drmrpc
	ioprio rt 4
	writepid /dev/cpuset/foreground/tasks
```

 첫번째 줄에서 /vendor/bin/hw/android.hardware.camera.provider@2.4-service 프로세스가 시작되었음을 알 수 있다. 

 ![](images/CAMERA_03.png)

 - camera provider start process. 
 
 ![](images/CAMERA_04.png)

 - service.cpp : hardware/interfaces/camera/provider/2.4/default/service.cpp
 - CameraProvider : hardware/interfacs/camera/provider/2.4/default/CameraProvider.cpp
 - hardware.c : hardware/libhardware/hardware.c
 - CameraModule : hardware/interfaces/camera/common/1.0/default/CameraModule.cpp
 - tcamera : hardware/telechips/camera/libcamera_v2/common/TCamera_common.cpp




-----

## CAMERA HAL 

 - hardware/telechips/camera 

 - camera_module_t는 아래 경로에 정의되어 있습니다. 
```c
// hardware/libhardware/include/hardware/camera_common.h

typedef struct camera_module {
    hw_module_t common;
    int (*get_number_of_cameras)(void);
    int (*get_camera_info)(int camera_id, struct camera_info *info);
    int (*set_callbacks)(const camera_module_callbacks_t *callbacks);
    void (*get_vendor_tag_ops)(vendor_tag_ops_t* ops);
    int (*open_legacy)(const struct hw_module_t* module, const char* id,
            uint32_t halVersion, struct hw_device_t** device);
    int (*set_torch_mode)(const char* camera_id, bool enabled);
    int (*init)();
    void* reserved[5];
} camera_module_t;

// hardware/telechips/camera/libcamera_v2/tcamera.cpp

#include "TCamera_Common.h"

static struct hw_module_methods_t tcamera_module_methods = {
    .open = tcamera::TCameraCommon::camera_device_open
};

camera_module_t HAL_MODULE_INFO_SYM = {
    .common = {
        .tag                    = HARDWARE_MODULE_TAG,
        .module_api_version     = CAMERA_MODULE_API_VERSION_1_0,
        .hal_api_version        = HARDWARE_HAL_API_VERSION,
        .id                     = CAMERA_HARDWARE_MODULE_ID,
        .name                   = "Telechips Camera HAL Module",
        .author                 = "Telechips, Inc.",
        .methods                = &tcamera_module_methods,
        .dso                    = NULL,
        .reserved               = { 0 },
    },
    .get_number_of_cameras      = tcamera::TCameraCommon::get_number_of_cameras,
    .get_camera_info            = tcamera::TCameraCommon::get_camera_info,
    .set_callbacks              = NULL,
    .get_vendor_tag_ops         = NULL,
    .reserved                   = { 0 },
}
```

- camera preview call flow

```c
camera_device_ops_t TAvnModule::m_CameraOps = {
    .set_preview_window =        TAvnModule::set_preview_window,
    .set_callbacks =             TAvnModule::set_CallBacks,
    .enable_msg_type =           TAvnModule::enable_msg_type,
    .disable_msg_type =          TAvnModule::disable_msg_type,
    .msg_type_enabled =          TAvnModule::msg_type_enabled,

    .start_preview =             TAvnModule::start_preview,
    .stop_preview =              TAvnModule::stop_preview,
    .preview_enabled =           TAvnModule::preview_enabled,
    .store_meta_data_in_buffers= TAvnModule::store_meta_data_in_buffers,

    .start_recording =           TAvnModule::start_recording,
    .stop_recording =            TAvnModule::stop_recording,
    .recording_enabled =         TAvnModule::recording_enabled,
    .release_recording_frame =   TAvnModule::release_recording_frame,

    .auto_focus =                TAvnModule::auto_focus,
    .cancel_auto_focus =         TAvnModule::cancel_auto_focus,

    .take_picture =              TAvnModule::take_picture,
    .cancel_picture =            TAvnModule::cancel_picture,

    .set_parameters =            TAvnModule::set_parameters,
    .get_parameters =            TAvnModule::get_parameters,
    .put_parameters =            TAvnModule::put_parameters,
    .send_command =              TAvnModule::send_command,

    .release =                   TAvnModule::release,
    .dump =                      TAvnModule::dump,
};

int32_t TAvnModule::start_preview(struct camera_device *device)
	// start preview
	|
	+-> int32_t TAvnHardwareInterface::startPreview(void)
		// start preview processing
```

note : https://cleanli.github.io/cleanhome/posts/2017-08-12/Android_x86_Camera_HAL.html

---

## KERNEL
