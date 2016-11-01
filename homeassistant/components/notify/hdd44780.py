"""
Support for the HDD44780 LCD display.

Configuration:

notify:
  platform: hdd44780
  pin_rs: 16
  pin_en: 20
  pin_d4: 5
  pin_d5: 6
  pin_d6: 13
  pin_d7: 19
  pin_bl: 21
  rows: 4
  cols: 20

GPIO pin numbers for the different functions of the display.
"""
import logging

import voluptuous as vol

from homeassistant.components.notify import (
    ATTR_TITLE, PLATFORM_SCHEMA, BaseNotificationService)
import homeassistant.helpers.config_validation as cv

REQUIREMENTS = ['Adafruit-CharLCD==1.1.0']

CONF_RS = 'pin_rs'
CONF_EN = 'pin_en'
CONF_D4 = 'pin_d4'
CONF_D5 = 'pin_d5'
CONF_D6 = 'pin_d6'
CONF_D7 = 'pin_d7'
CONF_BL = 'pin_bl'
CONF_COLS = 'cols'
CONF_ROWS = 'rows'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_RS): cv.positive_int,
    vol.Required(CONF_EN): cv.positive_int,
    vol.Required(CONF_D4): cv.positive_int,
    vol.Required(CONF_D5): cv.positive_int,
    vol.Required(CONF_D6): cv.positive_int,
    vol.Required(CONF_D7): cv.positive_int,
    vol.Optional(CONF_COLS, default=16): cv.positive_int,
    vol.Optional(CONF_ROWS, default=2): cv.positive_int,
    vol.Optional(CONF_BL, default=0): cv.positive_int,
})

_LOGGER = logging.getLogger(__name__)


def get_service(hass, config):
    """Get the hdd44780 notification service."""
    pin_rs = config[CONF_RS]
    pin_en = config[CONF_EN]
    pin_d4 = config[CONF_D4]
    pin_d5 = config[CONF_D5]
    pin_d6 = config[CONF_D6]
    pin_d7 = config[CONF_D7]
    pin_bl = config[CONF_BL]
    cols = config[CONF_COLS]
    rows = config[CONF_ROWS]

    return Hdd44780NotificationService(hass, pin_rs, pin_en,
                                       pin_d4, pin_d5, pin_d6,
                                       pin_d7, pin_bl,
                                       cols, rows)


# pylint: disable=too-few-public-methods
class Hdd44780NotificationService(BaseNotificationService):
    """Implement the notification service for the hdd44780 lcd."""

    # pylint: disable=too-many-arguments
    def __init__(self, hass, rs, en, d4, d5, d6, d7, bl, cols, rows):
        """Initialize the service."""
        import Adafruit_CharLCD as LCD

        self.lcd = LCD.Adafruit_CharLCD(rs, en, d4, d5, d6,
                                        d7, cols, rows, bl,
                                        invert_polarity=False)
        self.lcd.clear()

    def send_message(self, message="", **kwargs):
        """Send a message to a display."""
        self.lcd.clear()

        title = kwargs.get(ATTR_TITLE)
        out = title + "\n" + message if title else message
        self.lcd.message(out)
