# dependencies
from adafruit_pm25.i2c import PM25_I2C
import asyncio
import adafruit_minimqtt.adafruit_minimqtt as MQTT

import busio
import board
import json
import wifi
import supervisor
import socketpool

MQTT_TOPIC = 'aqi/unset'
MQTT_REPORT_INTERVAL = 5
AQI_READ_INTERVAL = 15

class AppState:
    def __init__(self):
        self.aq_data = {}

async def mqtt_loop(app_state):
    try:
        from secrets import secrets
    except ImportError:
        print("WiFi secrets are kept in secrets.py, please add them there!")
        raise

    try:
        print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])

        # uncomment below if your board doesn't automatically connect
      
        # print("Connecting to %s"%secrets["ssid"])
        # wifi.radio.connect(secrets["ssid"], secrets["password"])
        # print("Connected to %s!"%secrets["ssid"])
        print("My IP address is", wifi.radio.ipv4_address)

        # Create a socket pool
        pool = socketpool.SocketPool(wifi.radio)

        # Set up a MiniMQTT Client
        mqtt_client = MQTT.MQTT(
            broker=secrets["mqtt_broker"],
            port=secrets["mqtt_port"],
            username=secrets["mqtt_username"],
            password=secrets["mqtt_password"],
            socket_pool=pool,
            # ssl_context=ssl.create_default_context(),
        )

        print("Attempting to connect to %s" % mqtt_client.broker)
        mqtt_client.connect()

        while True:
            mqtt_client.ping()
            jsondata = json.dumps(app_state.aq_data)

            mqtt_client.publish(MQTT_TOPIC, jsondata, False, 0)
          
            await asyncio.sleep(MQTT_REPORT_INTERVAL)

    except BaseException as err:
        print(f"mqtt loop err: {err=}, {type(err)=}")
        supervisor.reload()
      
async def sensor_loop(app_state):
    # Create library object, use 'slow' 100KHz frequency!
    i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
    # Connect to a PM2.5 sensor over I2C
    reset_pin = None
    pm25 = PM25_I2C(i2c, reset_pin)
    
    print("Found PM2.5 sensor, beginning main loop...")
    
    while True:
        try:
            aqdata = pm25.read()
    
            data = {
            "standard pm1": aqdata["pm10 standard"],
            "standard pm2.5": aqdata["pm25 standard"],
            "standard pm10": aqdata["pm100 standard"],
            "environmental pm1": aqdata["pm10 env"],
            "environmental pm2.5": aqdata["pm25 env"],
            "environmental pm10": aqdata["pm100 env"],
            "0.3um": aqdata["particles 03um"],
            "0.5um": aqdata["particles 05um"],
            "1.0um": aqdata["particles 10um"],
            "2.5um": aqdata["particles 25um"],
            "5.0um": aqdata["particles 50um"],
            "10.0um": aqdata["particles 100um"]
            }
            app_state.aq_data = data
            jsondata = json.dumps(data)
            print("Data: %s" % jsondata)
    
            await asyncio.sleep(AQI_READ_INTERVAL)
    
    
        except BaseException as err:
            print("Unable to read from sensor, retrying: %s" % err)
            await asyncio.sleep(AQI_READ_INTERVAL)
            continue

async def main():
    app_state = AppState()
    mqtt_task = asyncio.create_task(mqtt_loop(app_state))
    sensor_task = asyncio.create_task(sensor_loop(app_state))
    await asyncio.gather(sensor_task, mqtt_task)
    supervisor.reload()


asyncio.run(main())
