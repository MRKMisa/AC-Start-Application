import csv, time
from datetime import datetime

telemetry_data = []

for i in range(2):
    speedKmh = 56
    throttle = 48
    brake = 1
    clutch = 0.2
    gear = 2
    wheelSlip = [10, 25, 30, 25]

    now = datetime.now()

    if int(now.minute) < 10:
        minute = "0"+str(now.minute)
    else:
        minute = now.minute
    if int(now.second) < 10:
        second = "0"+str(now.second)
    else:
        second = now.second

    date = now.date()

    if len(telemetry_data) != 0:
        delay = time.time()-float(telemetry_data[len(telemetry_data)-1]["time"])
    else:
        delay = "None"

    telemetry_data.append({
                            "number":len(telemetry_data),
                            "time":time.time(),
                            "date":date,
                            "hour":now.hour,
                            "minutes":minute,
                            "seconds":second,
                            "delay":delay,
                            "speedKmh":speedKmh,
                            "throttle":throttle,
                            "brake":brake,
                            "clutch":clutch,
                            "gear":gear,

                            "FLwheelSlip":wheelSlip[0],
                            "FRwheelSlip":wheelSlip[1],
                            "RLwheelSlip":wheelSlip[2],
                            "RRwheelSlip":wheelSlip[3]
                            })
    time.sleep(0.2)

with open("data.csv", "w", newline="") as csvfile:
    fieldnames = telemetry_data[0].keys()

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")

    writer.writeheader()
    writer.writerows(telemetry_data)