# duino_vscode_settings

Creates a vscode settings file with all of the compiler defines and include paths in it.

This program works by taking the command uses to invoke the compiler (with all of the -D, -I etc
options) and it parses the options and generates a VSCode settings file (more precisely,
a c_cpp_properties.json file).

duino_vscode_settings also supports storing multiple configurations, so you can have a configuation
for running the host compiler (say to run a C++ test suite), and have a configuration for
each type of Arduino Board that you use.

duino_vscode_settings will tries to merge any existing options so as not to overwrite
customizations.

## Typical Usage

```bash
make-vscode-settings ./.vscode/c_cpp_properties.json -- g++ -DFOO -IsomePath -IotherPath
```
will generate a c_cpp_properties.json which looks something like this:
```json
{
    "configurations": [
        {
            "cStandard": "gnu11",
            "compilerPath": "g++",
            "cppStandard": "g++17",
            "defines": [
                "FOO"
            ],
            "includePath": [
                "somePath",
                "otherPath"
            ],
            "intelliSenseMode": "gcc-arm",
            "mergeConfigurations": true,
            "name": "Arduino"
        }
    ]
}
```

Using a NeoPixelExample compiled for a WaveShare RP2040 Zero, I would normally compile this using
something like:
```bash
arduino-cli compile --fqbn rp2040:rp2040:waveshare_rp2040_zero
```
If you pass in the `--verbose` then arduino-cli will print out the compiler invocations. If you
grab the one for the .ino file then I use that.

```bash
arduino-cli compile --verbose --fqbn rp2040:rp2040:waveshare_rp2040_zero 2>/dev/null | grep g++ | grep .ino.cpp | grep -v -- -lc | tail -1
```
This will produce this output:
```bash
/home/dhylands/.arduino15/packages/rp2040/tools/pqt-gcc/2.3.0-dfd82b2/bin/arm-none-eabi-g++ \
    -I /tmp/arduino/sketches/7F7CB296241CD53CB3A2A1C9D0C29E09/core -c -Werror=return-type \
    -Wno-psabi -DUSBD_PID=0x0003 -DUSBD_VID=0x2e8a -DUSBD_MAX_POWER_MA=500 \
    -DUSB_MANUFACTURER="Waveshare" -DUSB_PRODUCT="RP2040 Zero" -DLWIP_IPV6=0 -DLWIP_IPV4=1 \
    -DLWIP_IGMP=1 -DLWIP_CHECKSUM_CTRL_PER_NETIF=1 -DARDUINO_VARIANT="waveshare_rp2040_zero" \
    -DPICO_FLASH_SIZE_BYTES=2097152 \
    @/home/dhylands/.arduino15/packages/rp2040/hardware/rp2040/4.0.3/lib/rp2040/platform_def.txt \
    -march=armv6-m -mcpu=cortex-m0plus -mthumb -ffunction-sections -fdata-sections -fno-exceptions \
    -iprefix/home/dhylands/.arduino15/packages/rp2040/hardware/rp2040/4.0.3/ \
    @/home/dhylands/.arduino15/packages/rp2040/hardware/rp2040/4.0.3/lib/rp2040/platform_inc.txt \
    @/home/dhylands/.arduino15/packages/rp2040/hardware/rp2040/4.0.3/lib/core_inc.txt \
    -I/home/dhylands/.arduino15/packages/rp2040/hardware/rp2040/4.0.3/include -fno-rtti \
    -std=gnu++17 -g -pipe -w -x c++ -E -CC -DF_CPU=133000000L -DARDUINO=10607 \
    -DARDUINO_WAVESHARE_RP2040_ZERO -DBOARD_NAME="WAVESHARE_RP2040_ZERO" -DARDUINO_ARCH_RP2040 \
    -Os -DWIFICC=CYW43_COUNTRY_WORLDWIDE \
    -I/home/dhylands/.arduino15/packages/rp2040/hardware/rp2040/4.0.3/cores/rp2040 \
    -I/home/dhylands/.arduino15/packages/rp2040/hardware/rp2040/4.0.3/variants/waveshare_rp2040_zero \
    /tmp/arduino/sketches/7F7CB296241CD53CB3A2A1C9D0C29E09/sketch/NeoPixelExample.ino.cpp -o /dev/null
```
If you assigned the above to a variable called `COMPILER_CMD` then I would run make-vscode-settings
like this:
```bash
COMPILER_CMD=$(arduino-cli compile --verbose --fqbn rp2040:rp2040:waveshare_rp2040_zero 2>/dev/null | grep g++ | grep .ino.cpp | grep -v -- -lc | tail -1)
make-vscode-settings -c Arduino-zero ./.vscode/c_cpp_properties.json -- ${COMPILER_CMD}
```
and that would generate `./.vscode/c_cpp_properties.json` with contents something like this:
```json
{
    "configurations": [
        {
            "cStandard": "gnu11",
            "compilerPath": "/home/dhylands/.arduino15/packages/rp2040/tools/pqt-gcc/2.3.0-dfd82b2/bin/arm-none-eabi-g++",
            "cppStandard": "gnu++17",
            "defines": [
                "ARDUINO=10607",
                "ARDUINO_ARCH_RP2040",
                "ARDUINO_VARIANT=\"waveshare_rp2040_zero\"",
                "ARDUINO_WAVESHARE_RP2040_ZERO",
                "ARM_MATH_CM0_FAMILY",
                "ARM_MATH_CM0_PLUS",
                "BOARD_NAME=\"WAVESHARE_RP2040_ZERO\"",
                "CFG_TUSB_MCU=OPT_MCU_RP2040",
                "CYW43_LWIP=1",
                "F_CPU=133000000L",
                "LWIP_CHECKSUM_CTRL_PER_NETIF=1",
                "LWIP_IGMP=1",
                "LWIP_IPV4=1",
                "LWIP_IPV6=0",
                "PICO_CYW43_ARCH_THREADSAFE_BACKGROUND=1",
                "PICO_FLASH_SIZE_BYTES=2097152",
                "PICO_RP2040=1",
                "TARGET_RP2040",
                "USBD_MAX_POWER_MA=500",
                "USBD_PID=0x0003",
                "USBD_VID=0x2e8a",
                "USB_MANUFACTURER=\"Waveshare\"",
                "USB_PRODUCT=\"RP2040",
                "WIFICC=CYW43_COUNTRY_WORLDWIDE"
            ],
            "includePath": [
                "/tmp/arduino/sketches/7F7CB296241CD53CB3A2A1C9D0C29E09/core",
                "/home/dhylands/.arduino15/packages/rp2040/hardware/rp2040/4.0.3/include",
                "/home/dhylands/.arduino15/packages/rp2040/hardware/rp2040/4.0.3/cores/rp2040",
                "/home/dhylands/.arduino15/packages/rp2040/hardware/rp2040/4.0.3/variants/waveshare_rp2040_zero"
            ],
            "intelliSenseMode": "gcc-arm",
            "mergeConfigurations": true,
            "name": "Arduino-zero"
        }
    ]
}
```
 I typically make a seperate VSCode workspace for each Arduino project, and when I open the
 workspace and then select `Arduino-zero` in the bottom right corner. All of the red-squiggles
 should be gone, and you can Control-Click on a symbol and it takes you to the place where
 it's defined.
