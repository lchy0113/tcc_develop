# Device tree for tcc8985 SoC in Kdiwin 

```
tcc898x.dtsi 
	|	define SECURE_MEM_BASE, SECURE_MEM_SIZE
	|	define RESERVED_MEM_BASE, RESERVED_MEM_SIZE 
	|	set bootargs 
	|	set aliases
	|	set reserved-memory
tcc8985-pinctrl.dtsi
	|	define pinctrl
	|
	tcc8985.dtsi
		|	(empty)
		|
	tcc898x-android.dtsi
		|	VBOOT 1.0 DT fstab : Mounts partitions specified by fstab in device tree.
		|
		tcc8985-android-$(TARGET_PRODUCT).dts
	

```

</pr>

* 디바이스 트리 오버레이 노트
> 이 문서는 drivers/of/overlay.c 에 구현된 커널 디바이스 트리 오버레이 기능의 구현에 대해 설명합니다. 이 문서는 Documentation/devicetree/dt-object-internal.txt & Documentation/devicetree/dynamic-resolution-notes.txt 와 같이 보면 좋습니다.
* 오버리에는 어떻게 동작하는가?
> 디바이스 트리 오버레이의 목적은 커널의 라이브 트리를 수정하기 위함입니다. 또한 커널 상태에 영향을 주는 수정을 반영하고 있습니다. 커널은 주로 장치를 다루기 때문에, 활성화된 장치는 새로운 디바이스 노드를 생성해야 합니다. 비활성화 되었거나 제거된 장치는 등록이 취소되어야 합니다.

아래 예제는 베이스 트리에 있는 foo board 입니다.
```
---- foo.dts ----------------------
    /* FOO platform */
    / {
        compatible = "corp,foo";

        /* shared resources */
        res: res {
        };

        /* On chip peripherals */
        ocp: ocp {
            /* peripherals that are always instantiated */
            peripheral1 { ... };
        }
    };
---- foo.dts ------------------------
```

bat.dts 오버레이가 아래와 같이 로딩되었습니다.
```
---- bar.dts -------------------------
/plugin/;   /* allow undefined label references and record them */
/ {
    ....    /* various properties for loader use; i.e. part id etc. */
    fragment@0 {
        target = ;
        __overlay__ {
            /* bar peripheral */
            bar {
                compatible = "corp,bar";
                ... /* various properties and child nodes */
            }
        };
    };
};
---- bar.dts ---------------------------
```

결과적으로 foo + bar.dts는 아래와 같습니다.
```
---- foo+bar.dts ----------------------
    /* FOO platform + bar peripheral */
    / {
        compatible = "corp,foo";

        /* shared resources */
        res: res {
        };

        /* On chip peripherals */
        ocp: ocp {
            /* peripherals that are always instantiated */
            peripheral1 { ... };

            /* bar peripheral */
            bar {
                compatible = "corp,bar";
                ... /* various properties and child nodes */
            }
        }
    };
---- foo+bar.dts -------------------------
```
오버레이의 결과로, 새로운 장치 노드(bar)가 생성되었습니다. 따라서 bar 플랫폼 장치가 등록되고, 일치하는 디바이스 드라이버가 로드되면 예상되로 생성됩니다.

*오버레이 Kernel API
API는 사용하기 매우 쉽습니다.

1. of_overlay_create ()를 호출하여 오버레이를 만들고 적용합니다. 반환 값 이 오버레이를 식별하는 쿠키입니다.
2. 이전에 오버레이를 제거하고 정리하는 of_overlay_destroy ()를 호출합니다. of_overlay_create ()에 대한 호출을 통해 생성됩니다. 다른것에 의해 겹쳐진 오버레이를 제거하는 것은 허용되지 않습니다.

마지막으로 한 번에 모든 오버레이를 제거해야하는 경우 of_overlay_destroy_all () : 올바른 순서로 모든 단일 항목을 제거합니다.

* 오버레이 DTS 포맷
> DTS 오버레이는 아래와 같은 형식을 가져야 합니다. 
```
{
    /* ignored properties by the overlay */

    fragment@0 {    /* first child node */

        target=;    /* phandle target of the overlay */
    or
        target-path="/path";    /* target path of the overlay */

        __overlay__ {
            property-a; /* add property-a to the target */
            node-a {/* add to an existing, or create a node-a */
                ...
            };
        };
    }
    fragment@1 {    /* second child node */
        ...
    };
    /* more fragments follow */
}
```
