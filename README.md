# CircuitPython PMS5003 to MQTT

This is a simple example that lets you collect data from a PMS5003 air particulate sensor and report it to MQTT.

## Instructions

Ensure you have the dependencies in `/lib`, and add a `secrets.py` with the appropriate values.

Change reporting interval as required. PMSA003i laser has a rated lifespan of 3 years.

## Dependencies

* adafruit_pm25
* adafruit_minimqtt
* asyncio

## Tested on

* Adafruit ESP32-C3
* Adafruit Funhouse

## Bill of Materials

* Adafruit ESP32 C3: https://www.adafruit.com/product/5405
* PMSA003i Particulate Sensor: https://www.adafruit.com/product/4632
* 50mm Stemma QT cable: https://www.adafruit.com/product/4399
* USB-C cable and power source
* 3D printed enclosure: https://cad.onshape.com/documents/631774ba247648000195a443/w/5c284afbea7b5b0b521a5afd/e/f65699d12f76ab22b3026994?renderMode=0&uiState=640414876457f41eb16caf33

## Disclaimer

You use this at your own risk. Do not expect any support from me unless I know you!

## License

MIT
