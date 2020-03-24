# This script is ran every 30 minutes, the display.py main program
# updates to catch the data produced by this script at 02 and 32 mins
# of each hour through a cron schedule

#!/usr/bin/env python3
import subprocess
import json
from datetime import datetime
import tempfile

temp_dir = tempfile.gettempdir()
file_path = temp_dir + "/speeddata.txt"

def get_network_speed():
    cmd = "speedtest -f json"

    out = subprocess.Popen(cmd,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT,
                           shell=True)

    stdout, stderr = out.communicate()

    out_dec = stdout.decode('utf-8')

    network_stats = json.loads(out_dec)
    bytes2mbits = 0.0000076294

    download = round(int(network_stats['download']['bandwidth'])*bytes2mbits, 1)
    upload = round(int(network_stats['upload']['bandwidth'])*bytes2mbits, 1)
    packetloss = network_stats['packetLoss']
    externalIP = network_stats['interface']['externalIp']
    internalIP = network_stats['interface']['internalIp']
    time_completed = datetime.now().strftime("%d %b, %Y %H:%M:%S")

    network_stats_final = [download, upload, packetloss, externalIP, internalIP, time_completed]

    return network_stats_final

with open(file_path, 'w') as file:
    for el in get_network_speed():
        file.writelines(str(el) + "\n")
