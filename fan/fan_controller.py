from xml.etree.ElementTree import PI
import RPi.GPIO as GPIO
import time
import json
import os
import logging
import datetime


def create_log(is_debug: bool = False) -> logging.Logger:
    # set log level
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    if is_debug:
        logger.setLevel(logging.DEBUG)
    # create directory 'log' if not exists
    os.makedirs('log', exist_ok=True)
    # set save log path
    handler_log_path = logging.FileHandler(datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S.log"))
    logger.addHandler(handler_log_path)
    # set log format
    handler_log_format = logging.Formatter(fmt="%(asctime)s %(levelname)s %(filename)s %(funcName)s  %(lineno)s : %(message)s")
    logger.addHandler(handler_log_format)
    return logger


class PWM:
    def __init__(self, interval: int, pin: int, logger: logging.Logger) -> None:
        try:
            self.interval = interval
            self.pin = pin
            self.logger = logger
            # set gpio
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin, GPIO.OUT)
            # for debugging
            self.logger.debug(f'Interval is {self.interval} & PIN is GPIO{self.pin}.')
            self.logger.debug(f'Successfully created Instance "PWM".')
        except Exception as e:
            self.logger.error(e)

    def measure_temperature(self):
        # for debugging
        self.logger.debug('Measureing temperature...')
        # measure temperature
        with open('/sys/class/thermal/thermal_zone0/temp', 'r')as f:
            _temperature = f.read()
        self.temperature = int(_temperature) / 1000
        # for debugging
        self.logger.debug(f'Successfully measured temperature. Temperature was {self.temperature}C.')

    def run(self, fan) -> None:
        # for debugging
        self.logger.debug('Changing fan power...')
        # change fun power
        fan_power = 20 + 4 * (self.temperature - 50)
        if self.temperature < 50:
            fan_power = 0
        if self.temperature > 70:
            fan_power = 100
        fan.ChangeDutyCycle(fan_power)
        # for debugging
        self.logger.debug(f'Successfully changed fan power to {fan_power}.')

    def loop(self):
        try:
            # measure temperature
            self.measure_temperature()
            fan = GPIO.PWM(self.pin, 50)
            fan.start(20)
            self.logger.debug('Successfully started PWM.')
            while True:
                self.run(fan)
                time.sleep(self.interval)
        except Exception as e:
            self.logger.error(e)
        finally:
            # stop & clean-up
            fan.stop()
            GPIO.cleanup()


if __name__ == '__main__':
    # load settings
    _settings = open('settings.json', 'r')
    settings = json.load(_settings)
    INTERVAL = settings['interval']
    PIN = settings['pin']
    IS_DEBUG = settings['is_debug']

    # set log
    logger = create_log(IS_DEBUG)
    logger.debug('Successfully created log.')

    # init
    pwm = PWM(INTERVAL, PIN, logger)
