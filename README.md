# ESP8266 Starter

Questo progetto è un punto di partenza per lavorare con l'ESP8266. Include istruzioni per configurare l'ambiente di sviluppo e iniziare a programmare il microcontrollore.

## Introduction

This project serves as a starting point for working with the ESP8266. It includes instructions to set up the development environment and begin programming the microcontroller.

## Prerequisites

Before starting, ensure you have the following:

- A computer with internet access.
- An ESP8266 development board.
- A USB cable compatible with your ESP8266 board.
- Installed Arduino IDE or PlatformIO.
- Basic knowledge of programming and electronics.
- Necessary drivers for your ESP8266 board (e.g., CP2102 or CH340).

## Setting Up Python 3.13.x Locally Using asdf

To set up Python 3.13.x locally using `asdf`, follow these steps:

1. **Install asdf**  
    If you don't already have `asdf` installed, follow the instructions on the [asdf documentation](https://asdf-vm.com/guide/getting-started.html).

2. **Add the Python Plugin**  
    Run the following command to add the Python plugin to `asdf`:
    ```bash
    asdf plugin-add python
    ```

3. **Install Python 3.13.x**  
    Use `asdf` to install the desired version of Python:
    ```bash
    asdf install python 3.13.x
    ```

4. **Set Python 3.13.x as the Local Version**  
    Navigate to your project directory and set Python 3.13.x as the local version:
    ```bash
    cd /path/to/your/project
    asdf local python 3.13.x
    ```

5. **Verify the Installation**  
    Confirm that the correct version of Python is being used:
    ```bash
    python --version
    ```

You are now ready to use Python 3.13.x in your project.

## Flashing the Firmware with esptool

To flash the firmware onto your ESP8266 using `esptool`, follow these steps:

1. **Install esptool**  
    Install `esptool` using `pip`:
    ```bash
    pip install esptool
    ```

2. **Connect Your ESP8266**  
    Connect your ESP8266 board to your computer using a USB cable.

3. **Identify the Serial Port**  
    Find the serial port your ESP8266 is connected to:
    - On Linux/macOS:
      ```bash
      ls /dev/tty.*
      ```
    - On Windows, check the COM port in the Device Manager.

4. **Erase the Flash Memory**  
    Before flashing new firmware, erase the existing flash memory:
    ```bash
    esptool.py --port /dev/ttyUSB0 erase_flash
    ```
    Replace `/dev/ttyUSB0` with the correct serial port for your system.

5. **Flash the Firmware**  
    Flash the firmware onto the ESP8266:
    ```bash
    esptool.py --port /dev/ttyUSB0 write_flash -fm dio 0x00000 firmware.bin
    ```
    Replace `/dev/ttyUSB0` with your serial port and `firmware.bin` with the path to your firmware file.

6. **Verify the Flashing Process**  
    Ensure the flashing process completes successfully. If there are errors, double-check your connections and try again.

Your ESP8266 is now ready with the new firmware.

## MQTT

Send message via mosquitto:
```bash
mosquitto_pub -t "notifications" -m "Hello, NodeMCU", -u "username" -P "password"
```