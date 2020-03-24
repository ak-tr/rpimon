# rpimon - PADD-inspired multi-purpose command line information monitor

Displays information about my RPI4 on a 240x320 Adafruit TFT mini HAT display.

![Image of Display](https://i.imgur.com/XsyPKPx.png)

## Usage

If you would like to run this script on your Pi and your display resolution is larger than 240x320 and your terminal font is set to anything but 6x12 it is highly likely that it will look very buggy.

Before you run this Python script you must install the required libraries:
```
pip3 install requests
pip3 install beautifulsoup4
pip3 install pytemperature
```

Before you run the main script `display.py` , you must run the two scripts in the `data_getters` folder at least once. This is because this is how the main script gets the data for covid stats and network speed. However, if you only run it once, the values shown on the display will only show the data written to the files created by the scripts. If you would like it to constantly update along with the main `display.py` script, I highly recommend setting up a cron schedule to run those scripts like so:
```
*/30 * * * * cd *dir of data_getters* && python3 speedtest.py&
*/6 * * * * cd *dir of data_getters* && python3 covid.py&
```
