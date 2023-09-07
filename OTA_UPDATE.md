OTA_UPDATE
====

> android ota update 방법에 대해 정리.


# releaseKeys

```
function build_releasekeys()
{
    echo "----------------"
    echo "| release keys |"
    echo "----------------"
    cd ${ANDROID_BUILD_TOP}
    subject='/C=US/ST=California/L=Mountain View/O=Android/OU=Android/CN=Android/emailAddress='${BUILD_ACCOUNT}
    if [ ! -d ${RELEASEKEY_DIR} ];  then
        mkdir ${RELEASEKEY_DIR}
    fi
    for x in releasekey platform shared media; do \
        ${ANDROID_BUILD_TOP}/development/tools/make_key ${RELEASEKEY_DIR}/$x "$subject"; \
    done
}
```

# releaseImage

```
function build_releaseimage()
{
    echo "-----------------------"
    echo "| build release image |"
    echo "-----------------------"
    cd ${ANDROID_BUILD_TOP}
    build_dist
    if [ ! -d ${RELEASEKEY_DIR} ]; then
        build_releasekeys
    fi
    ################################################################################
    # Signing release image.                                                       #
    # To generate a release image                                                  #
    # The newly signed images can be found under IMAGE/ in signed-target_files.zip #
    ################################################################################
    ./build/tools/releasetools/sign_target_files_apks -o --default_key_mappings  ${RELEASEKEY_DIR} ${DEV_DIST_DIR}/*-target_files-*.zip signed-target_files.zip
    echo "output : signed-target_files.zip"
}
```

# otaImage

```
function build_otaimage()
{
    echo "-------------------"
    echo "| build ota image |"
    echo "-------------------"
    cd ${ANDROID_BUILD_TOP}
    build_releaseimage
    ########################
    # Signing OTA packages #
    ########################
    ./build/tools/releasetools/ota_from_target_files    \
        -k ${RELEASEKEY_DIR}/releasekey \
        signed-target_files.zip \
        signed-ota_update.zip
    echo "output : signed-ota_update.zip"
    ###################################################################################################
    # $> adb push signed-ota_update.zip /data/
    # $> adb shell "echo "--update_package=/data/signed-ota_update.zip" > /cache/recovery/command"
    # $> adb reboot recovery
    ###################################################################################################
     
    ##############################################
    # Test: Create An incremental update package #
    ##############################################
    #./build/tools/releasetools/ota_from_target_files   \
    #   -k ${RELEASEKEY_DIR}/releasekey \
    #   -i ./old-signed-target_files.zip ./new-signed-target_files.zip  \
    #   ./old_to_new-incremental-ota-update.zip
     
    #################################################
    # Test: everything is signed with the test key. #
    #################################################
    #   ./build/tools/releasetools/ota_from_target_files    \
    #       ${DEV_DIST_DIR}/full_tcc898x-target_files-eng.lchy0113.zip  \
    #       full_ota_update_${DATE}.zip
}
```
