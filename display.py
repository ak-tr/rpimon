import time
from datetime import datetime
import sys
import subprocess
import psutil
import requests
import traceback
import os
import json
import pytemperature
import inspect
import tempfile

t_count = 0
disp_write = [""] * 20
difference = [0] * 4
newstats = [] * 4
usage_smoothing = [0.0] * 5
uptimestr = ""
startwrite = 0
network_speed = []
speed_stats_retrieved = False


def update():
    cpu_stats_get = cpu_stats()
    mem_stats_get = mem_stats()
    disk_stats_get = disk_stats()

    disp_write[2] = "\u001b[36m  /_/--\ |_| \ |_| |_|   \u001b[0m{}".format(current_datetime()[1].rjust(57 - (len("/_/--\ |_| \ |_| |_|   ")) - len(current_datetime()[1])))
    disp_write[5] = "  Upt:   {}".format(get_uptime())
    disp_write[6] = "  CPU:   {}°C              CPU: {} {}%".format(cpu_stats_get[0],
                                                                    progressbar(cpu_stats_get[1], True),
                                                                    cpu_stats_get[1])
    disp_write[7] = "  RAM:   {} {}  DSK: {} {}%".format(
        progressbar(float(mem_stats_get.replace(" ", "").replace("%", "")), True), mem_stats_get,
        progressbar(disk_stats_get, True),
        disk_stats_get)

    if t_count % 1 == 0:
        if ":" in disp_write[19]:
            disp_write[19] = separator("", " ")
        else:
            disp_write[19] = separator(":", " ")


def log_call():
    #send_message(inspect.stack()[1][3])
    pass

def separator(string, sep):
    log_call()
    string = " " + string
    return string.ljust(52, sep)


def get_weather():
    log_call()
    url = "http://api.openweathermap.org/data/2.5/weather?id=3333121&appid=0b8766219f170ee2905ce5b14e3b2e7e"
    response = requests.get(url)

    weather_get = json.loads(response.text)

    weather_type = weather_get['weather'][0]['main']
    temp = str(round(pytemperature.k2c(weather_get['main']['temp']), 1)) + "°C"
    temp_feels_like = str(round(pytemperature.k2c(weather_get['main']['feels_like']), 1)) + "°C"
    cloud_percentage = str(weather_get['clouds']['all']) + "%"
    pressure = str(weather_get['main']['pressure']) + "hPa"
    humidity = str(weather_get['main']['humidity']) + "%"

    weather_stats = [weather_type, temp, temp_feels_like, cloud_percentage, pressure, humidity]

    return weather_stats


def write_weather_stats():
    log_call()
    get_weather_stats = get_weather()
    type_and_temp = str(get_weather_stats[0]) + " / " + get_weather_stats[1]

    disp_write[13] = "  Temp:  {} Feels Like: {}".format(type_and_temp.ljust(19, " "), get_weather_stats[2])
    disp_write[14] = "  Pres:  {} Humidity: {}".format(get_weather_stats[4].ljust(19, " "), get_weather_stats[5])
    disp_write[15] = "  Clds:  {} {}".format(longprogressbar(int(get_weather_stats[3].replace("%", "")), False),
                                             get_weather_stats[3])


def write_error(e):
    with open('errors.txt', 'a') as file:
        file.write("[!] {} {}: {}\n".format(current_datetime()[0], current_datetime()[1], e))


def longprogressbar(percentage, col):
    log_call()
    progressbarstr = "["
    barfill = "■"
    barempty = "·"

    if col == True:
        if percentage >= 50.0:
            progressbarstr = "[\u001b[31m"

    length = round(percentage / (100 / 35))

    i = 0
    while i < length:
        i += 1
        progressbarstr += barfill

    rem_length = 35 - length

    progressbarstr += "\033[0m"

    for x in range(rem_length):
        progressbarstr += barempty

    progressbarstr += "\033[0m]"

    return progressbarstr


def progressbar(percentage, col):
    log_call()
    progressbarstr = "["
    barfill = "■"
    barempty = "·"

    if col == True:
        if percentage >= 50.0:
            progressbarstr = "[\u001b[31m"

    length = round(percentage / 10)

    i = 0
    while i < length:
        i += 1
        progressbarstr += barfill

    rem_length = 10 - length

    progressbarstr += "\033[0m"

    for x in range(rem_length):
        progressbarstr += barempty

    progressbarstr += "\033[0m]"

    return progressbarstr


def get_covid_stats_from_file():
    log_call()
    covid_stats_final = []

    with open(get_file_location("coviddata.txt"), 'r') as file:
        for idx, line in enumerate(file.readlines()):
            if idx <= 5:
                covid_stats_final.append(line.strip())

    return covid_stats_final


def get_file_location(filename):
    temp_dir = tempfile.gettempdir()
    file_path = temp_dir + "/" + filename

    return file_path


def write_covid_stats():
    log_call()
    stats = get_covid_stats_from_file()
    uk_cases_deaths = str(stats[0]) + "/" + str(stats[1])
    ww_cases_deaths = str(stats[3]) + "/" + str(stats[4])

    disp_write[17] = "  UK C/D: {}UK Recovered: {}".format(uk_cases_deaths.ljust(19, " "), stats[2])
    disp_write[18] = "  WW C/D: {}WW Recovered: {}".format(ww_cases_deaths.ljust(19, " "), stats[5])


def cpu_stats():
    global usage_smoothing
    log_call()
    cmd = "/opt/vc/bin/vcgencmd measure_temp"

    new_usage = 0

    out = subprocess.Popen(cmd,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT,
                           shell=True)

    stdout, stderr = out.communicate()

    current_temp = stdout.decode('utf-8')[5:9]
    current_temp = current_temp.strip()

    current_cpu_usage = psutil.cpu_percent()
    #current_cpu_usage = "{:04.1f}".format(current_cpu_usage)


    if current_cpu_usage > 99:
        current_cpu_usage = int(100)

    usage_smoothing.pop(0)
    usage_smoothing.append(current_cpu_usage)

    new_usage = sum(usage_smoothing)

    new_usage = round(new_usage / len(usage_smoothing), 1)

    cpu_stats = [current_temp, new_usage]

    return cpu_stats


def mem_stats():
    log_call()
    ram_usage = str(psutil.virtual_memory()[2]) + "%"

    return ram_usage.ljust(5, " ")


def get_command_output(cmd):
    out = subprocess.Popen(cmd,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT,
                           shell=True)

    stdout, stderr = out.communicate()

    return stdout.decode('utf-8')


def get_username_hostname():
    cmd = "whoami"
    cmd2 = "hostname"

    username = get_command_output(cmd).replace("\n", "")
    hostname = get_command_output(cmd2).replace("\n", "")

    return username + "@" + hostname


def get_uptime():
    log_call()
    days = 0
    hours = 0
    minutes = 0

    seconds_in_day = 86400
    seconds_in_hour = 3600
    seconds_in_minute = 60

    with open('/proc/uptime', 'r') as f:
        uptime_seconds = round(float(f.readline().split()[0]))

    while uptime_seconds != 0:
        if uptime_seconds >= seconds_in_day:
            days += 1
            uptime_seconds -= seconds_in_day
        elif uptime_seconds >= seconds_in_hour:
            hours += 1
            uptime_seconds -= seconds_in_hour
        elif uptime_seconds >= seconds_in_minute:
            minutes += 1
            uptime_seconds -= seconds_in_minute
        elif uptime_seconds < seconds_in_minute:
            uptime_seconds = 0

    uptime = [days, hours, minutes]

    uptimestr = "{} days, {} hours, {} minutes".format(uptime[0], uptime[1], uptime[2])

    return uptimestr


def get_network_speeds_from_file():
    log_call()
    network_stats_final = []

    with open(get_file_location("speeddata.txt"), 'r') as file:
        for idx, line in enumerate(file.readlines()):
            if idx <= 5:
                network_stats_final.append(line.strip())

    return network_stats_final


def get_network_stats():
    log_call()
    cmd = "iwconfig wlan0"

    out = subprocess.Popen(cmd,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT,
                           shell=True)

    stdout, stderr = out.communicate()

    out_dec = stdout.decode('utf-8')
    out_dec_lines = out_dec.splitlines()

    signal_level = out_dec_lines[5]
    sig_substring = "Signal level="

    signal_level = signal_level.split(sig_substring, 1)[1]
    signal_level = signal_level.replace(" ", "")

    quality_percent = (int(signal_level.replace("dBm", "")) + 110) * 10 / 7

    network_stats = [signal_level, int(quality_percent)]

    return network_stats


def write_network_stats():
    log_call()
    global network_speed
    global speed_stats_retrieved

    mins_now = int(datetime.now().strftime("%M"))

    network_stats = get_network_stats()

    if int(mins_now) == 32 or int(mins_now) == 2 and speed_stats_retrieved == False:
        network_speed = get_network_speeds_from_file()
        speed_stats_retrieved = True

    disp_write[9] = "  Spd:   ↓{}   ↑{}       Pck: {} {}%".format(network_speed[0].ljust(4, " "),
                                                                   network_speed[1].ljust(4, " "),
                                                                   progressbar(int(float(network_speed[2])), False),
                                                                   round(float(network_speed[2]), 2))
    disp_write[10] = "  exIP:  {}Qlt: {} {}%".format(network_speed[3].ljust(20, " "),
                                                     progressbar(network_stats[1], False), network_stats[1])
    disp_write[11] = "  inIP:  {}Signal Level: {}".format(network_speed[4].ljust(20, " "), network_stats[0])


def disk_stats():
    log_call()
    return psutil.disk_usage("/").percent


def current_datetime():
    log_call()
    now = datetime.now()
    current_date = now.strftime("%d %b, %Y")
    current_time = now.strftime("%H:%M:%S")

    datetime_val = [current_date, current_time]
    return datetime_val


def send_message(msg):
    os.system("echo " + str(msg) + " > /dev/pts/0")


def write():
    global startwrite

    for idx, el in enumerate(disp_write):
        if startwrite < 20:
            time.sleep(0.075)
            startwrite += 1

        if idx == len(disp_write) - 1:
            sys.stdout.write("\u001b[37m")
            sys.stdout.write("\r" + el)
        elif idx == 0:
            sys.stdout.write("\u001b[37m")
            sys.stdout.write("\033[1m")
            sys.stdout.write("\r" + el + "\n")
        else:
            sys.stdout.write("\u001b[37m")
            sys.stdout.write(el + "\n")


def start():
    global network_speed

    disp_start = [""] * 20

    text = """   ,---.      ,--.-.,-.   .=-.-.   _,---.  
 .--.'  \    /==/- |\  \ /==/_ /.-`.' ,  \ 
 \==\-/\ \   |==|_ `/_ /|==|, |/==/_  _.-' 
 /==/-|_\ |  |==| ,   / |==|  /==/-  '..-. 
 \==\,   - \ |==|-  .|  |==|- |==|_ ,    / 
 /==/ -   ,| |==| _ , \ |==| ,|==|   .--'  
/==/-  /\ - \/==/  '\  ||==|- |==|-  |     
\==\ _.\=\.-'\==\ /\=\.'/==/. /==/   \     
 `--`         `--`      `--`-``--`---'     
"""

    lines_text = text.splitlines()
    len_lines_text = len(lines_text)

    if len_lines_text > 20:
        print("LINE LENGTH TOO LONG EXITING PROG}")
        exit(0)

    start_el = int(20 - (len_lines_text * 1.75))

    for el in lines_text:
        disp_start[start_el] = el.center(53, " ")
        start_el += 1

    os.system("clear")

    for idx, el in enumerate(disp_start):
        time.sleep(0.05)
        if idx == len(disp_write) - 1:
            sys.stdout.write("\u001b[37m")
            sys.stdout.write("\r" + el)
        elif idx == 0:
            sys.stdout.write("\u001b[37m")
            sys.stdout.write("\r" + el + "\n")
        else:
            sys.stdout.write("\u001b[37m")
            sys.stdout.write(el + "\n")

    network_speed = get_network_speeds_from_file()

    if len(network_speed) < 1:
        network_speed = ["0"]*6

    write_weather_stats()
    write_network_stats()
    write_covid_stats()

    os.system("clear")


def main():
    global t_count
    global speed_stats_retrieved

    weather_stats_retrieved = False
    next_reset = "01"

    disp_write[0] = separator("\u001b[36m   __    _     _   ____ \u001b[0m", " ")
    disp_write[1] = "\u001b[36m   / /\  | |_/ | | | |_  \u001b[0m{}".format(get_username_hostname().rjust(26, " "))
    disp_write[4] = separator("RPI4 ", "=")
    disp_write[8] = separator("NETWORK ", "=")
    disp_write[12] = separator("LOCAL WEATHER ", "=")
    disp_write[16] = separator("COVID19 ", "=")

    try:
        while True:
            update()
            time.sleep(0.2)
            t_count += 0.2
            t_count = round(t_count, 1)

            write()

            mins_now = int(datetime.now().strftime("%M"))

            if mins_now % 5 == 0 and weather_stats_retrieved == False:
                next_reset = int(mins_now)+1
                try:
                    write_weather_stats()
                    write_covid_stats()
                    weather_stats_retrieved = True
                except Exception as e:
                    write_error(traceback.format_exc())

            try:
                write_network_stats()
            except Exception as e:
                pass

            if int(mins_now) == 3 or int(mins_now) % 33 == 0:
                speed_stats_retrieved = False

            if mins_now == int(next_reset):
                weather_stats_retrieved = False

    except Exception as error:
        print(traceback.format_exc())

if __name__ == '__main__':
    start()
    main()
