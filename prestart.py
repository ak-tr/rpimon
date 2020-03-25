import tempfile
import os

temp_dir = tempfile.gettempdir()

print("[*] Running covid.py to generate file coviddata.txt at " + str(temp_dir))
if os.path.isfile(temp_dir + "/coviddata.txt"):
    print(" [*] File already exists")
else:
    os.system("python3 data_getters/covid.py")

    if os.path.isfile(temp_dir + "/coviddata.txt"):
        print(" [*] File successfully created")
    else:
        print(" [*] File cannot be found in temp directory, main script may not run as expected")

print("\n[*] Running speedtest.py to generate file speeddata.txt at " + str(temp_dir))
if os.path.isfile(temp_dir + "/speeddata.txt"):
    print(" [*] File already exists")
else:
    os.system("python3 data_getters/speedtest.py")

    if os.path.isfile(temp_dir + "/speeddata.txt"):
        print(" [*] File successfully created")
    else:
        print(" [*] File cannot be found in temp directory, main script may not run as expected")

print("\n[*] Configuring OpenWeatherMap API")
apikey = input(str(" [*] Enter your api-key: "))
cityid = input(str(" [*] Enter your city-id: "))

oldfile = []

with open('display.py', 'r') as file:
    for line in file.readlines():
        if 'url = "http://api.openweathermap.org/data/2.5/weather?id={city-id}&appid={api-key}"' in line:
            line = line.replace("{city-id}", cityid)
            line = line.replace("{api-key}", apikey)
        oldfile.append(line)

with open('displaynew.py', 'w') as file:
    for el in oldfile:
        file.write(el)

print("/n[*] Removing old file display.py")
os.remove("display.py")
print("[*] Renaming new file displaynew.py -> display.py")
os.rename("displaynew.py", "display.py")