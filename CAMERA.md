# CAMERA

> Telechips 플랫폼의 Camera 모듈에 대해 정리.

---

## HAL 

define


camera_module_t는 아래 경로에 정의되어 있습니다. 
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
