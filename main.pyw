import time
import configparser
import threading
import csv

from get_shared_mem import get_shared_mem
from datetime import datetime
from show_reaction_time import show_reaction_time
from show_kmph_time import show_kmph_time

info = get_shared_mem()

conf = configparser.ConfigParser()

def load_config():
    conf.read("config.ini")

    # ReactionTimeGraphic
    ShowReactionTimeGraphic = conf["ReactionTimeGraphic"]["ShowReactionTimeGraphic"]

    ReactionTimeGraphicScale = conf["ReactionTimeGraphic"]["ReactionTimeGraphicScale"]

    ReactionTimeGraphicX = conf["ReactionTimeGraphic"]["ReactionTimeGraphicX"]

    ReactionTimeGraphicY = conf["ReactionTimeGraphic"]["ReactionTimeGraphicY"]

    #0-100kmphTimeGraphic
    ShowkmphTimeGraphic = conf["0-100kmphTimeGraphic"]["Show0-100kmphTimeGraphic"]

    kmphTimeGraphicScale = conf["0-100kmphTimeGraphic"]["0-100kmphTimeGraphicScale"]

    kmphTimeGraphicX = conf["0-100kmphTimeGraphic"]["0-100kmphTimeGraphicX"]

    kmphTimeGraphicY = conf["0-100kmphTimeGraphic"]["0-100kmphTimeGraphicY"]

    #Misc
    driverName = conf["Misc"]["driverName"]

    recordCsv = conf["Misc"]["recordCsv"]

    csvDataFrequency = conf["Misc"]["csvDataFrequency"]


    configSettings = {"ShowReactionTimeGraphic":ShowReactionTimeGraphic,
                      "ReactionTimeGraphicScale":ReactionTimeGraphicScale,
                      "ReactionTimeGraphicX":ReactionTimeGraphicX,
                      "ReactionTimeGraphicY":ReactionTimeGraphicY,

                      "ShowkmphTimeGraphic":ShowkmphTimeGraphic,
                      "kmphTimeGraphicScale":kmphTimeGraphicScale,
                      "kmphTimeGraphicX":kmphTimeGraphicX,
                      "kmphTimeGraphicY":kmphTimeGraphicY,

                      "driverName":driverName,
                      "recordCsv":recordCsv,
                      "csvDataFrequency":csvDataFrequency
                        }
    
    return configSettings

change = False
reset = False

telemetry_data = []
run = True

def recording_telemetry_data():
    global telemetry_data
    telemetry_data = []

    global run
    while run:
        speedKmh, throttle, brake, clutch, gear, wheelSlip = info.physics.speedKmh, info.physics.gas, info.physics.brake, info.physics.clutch, info.physics.gear, info.physics.wheelSlip
        currentTime = info.graphics.currentTime


        now = datetime.now()
        date = now.date()
        if int(now.minute) < 10:
            minute = "0"+str(now.minute)
        else:
            minute = now.minute
        if int(now.second) < 10:
            second = "0"+str(now.second)
        else:
            second = now.second

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

                          "currentTime":currentTime,

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
        
        time.sleep(int(1000/int(load_config()["csvDataFrequency"]))/1000)

def start_recording_telemery_data():
    t1 = threading.Thread(target=recording_telemetry_data)

    t1.start()

    return t1    

def end_recording_telemetry_data():
    global run
    run = False

while True:
    currentTime = info.graphics.currentTime

    if currentTime == "-:--:---":
        gear, clutch = info.physics.gear, info.physics.clutch


        if gear != 1 and clutch == 0.0:
            while currentTime == "-:--:---":
                gear, clutch, currentTime = info.physics.gear, info.physics.clutch, info.graphics.currentTime
                if gear == 1 and clutch != 0.0:
                    change = True
                    break

                if gear != 1 and clutch != 0.0:
                    reset = True
                    break
                
            if change:
                change = False
                continue
            if reset:
                reset = False
                continue
            
            if load_config()["recordCsv"].lower() == "true":
                t1 = start_recording_telemery_data()
            race_start_time = time.time()

            clutch = info.physics.clutch
            while clutch == 0.0:
                clutch = info.physics.clutch

            reaction_time = time.time()-race_start_time

            speedKmh = info.physics.speedKmh

            kmph_delay = 0
            speedMax = 0
            while speedKmh < 100:
                speedKmh = info.physics.speedKmh
                brake = info.physics.brake

                if brake:
                    kmph_delay = "Braked"
                    break
                
                if speedKmh > speedMax:
                    speedMax = speedKmh
                
                if speedKmh+1 < speedMax:
                    kmph_delay = "None"
                    break

            if kmph_delay != "None" and kmph_delay != "Braked":
                kmph_delay = time.time()-race_start_time

            if load_config()["recordCsv"].lower() == "true":
                time.sleep(int(1000/int(load_config()["csvDataFrequency"]))/1000)
                end_recording_telemetry_data()
                t1.join()

            now = datetime.now()

            if int(now.minute) < 10:
                minute = "0"+str(now.minute)
            else:
                minute = now.minute
            if int(now.second) < 10:
                second = "0"+str(now.second)
            else:
                second = now.second

            with open("output.txt", "a") as f:
                f.write(f"{now.date()} | {now.hour}:{minute}:{second} | {info.static.track} | {info.static.carModel} | {round(reaction_time, 3)} | {kmph_delay} \n")

            configSettings = load_config()

            if configSettings["ShowReactionTimeGraphic"].lower() == "true":
                show_reaction_time(configSettings["ReactionTimeGraphicX"], configSettings["ReactionTimeGraphicY"], configSettings["ReactionTimeGraphicScale"], configSettings["driverName"], reaction_time)
            
            if configSettings["ShowkmphTimeGraphic"].lower() == "true":
                show_kmph_time(configSettings["kmphTimeGraphicX"], configSettings["kmphTimeGraphicY"], configSettings["kmphTimeGraphicScale"], configSettings["driverName"], kmph_delay)

            if load_config()["recordCsv"].lower() == "true":
                file_name = f"{now.date()}  {now.hour}-{minute}-{second}  {info.static.track}  {info.static.carModel}  {round(reaction_time, 3)}  {kmph_delay}.csv"

                with open(f"CSVs/{file_name}", "w", newline="") as csvfile:

                    if len(telemetry_data) == 0:
                        for t in range(20):
                            if len(telemetry_data) != 0:
                                break
                            time.sleep(0.2)
                    
                    if len(telemetry_data) == 0:
                        print(f"WARNING!!! Telemetry data can not be recorded")
                    else:
                        fieldnames = telemetry_data[0].keys()

                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")

                        writer.writeheader()
                        writer.writerows(telemetry_data)

            continue

        elif gear == 1 and clutch == 1.0:
            currentTime = info.graphics.currentTime
            while currentTime == "-:--:---":
                gear, clutch, currentTime = info.physics.gear, info.physics.clutch, info.graphics.currentTime
                if clutch != 1.0:
                    change = True
                    break
                
                if gear != 1:  
                    reset = True
                    break

            if change:
                change = False
                continue
            if reset:
                reset = False
                continue
            
            if load_config()["recordCsv"].lower() == "true":
                start_recording_telemery_data()
            race_start_time = time.time()

            gear = info.physics.gear
            while gear == 1:
                gear = info.physics.gear

            reaction_time = time.time()-race_start_time

            speedKmh = info.physics.speedKmh

            speedMax = 0
            while speedKmh < 100:
                speedKmh = info.physics.speedKmh
                brake = info.physics.brake

                if brake:
                    kmph_delay = "Braked"
                    break

                if speedKmh >= speedMax:
                    speedMax = speedKmh

                if speedKmh+1 < speedMax:
                    kmph_delay = "None"
                    break
            if load_config()["recordCsv"].lower() == "true":
                end_recording_telemetry_data()

            if kmph_delay != "None" and kmph_delay != "Braked":
                kmph_delay = time.time()-race_start_time

            now = datetime.now()

            if int(now.minute) < 10:
                minute = "0"+str(now.minute)
            else:
                minute = now.minute
            if int(now.second) < 10:
                second = "0"+str(now.second)
            else:
                second = now.second

            with open("output.txt", "a") as f:
                f.write(f"{now.date()} | {now.hour}:{minute}:{second} | {info.static.track} | {info.static.carModel} | {round(reaction_time, 3)} | {kmph_delay} \n")

            if configSettings["ShowReactionTimeGraphic"].lower() == "true":
                show_reaction_time(configSettings["ReactionTimeGraphicX"], configSettings["ReactionTimeGraphicY"], configSettings["ReactionTimeGraphicScale"], configSettings["driverName"], reaction_time)
            
            if configSettings["ShowkmphTimeGraphic"].lower() == "true":
                show_kmph_time(configSettings["kmphTimeGraphicX"], configSettings["kmphTimeGraphicY"], configSettings["kmphTimeGraphicScale"], configSettings["driverName"], kmph_delay)

            if load_config()["recordCsv"].lower() == "true":
                file_name = f"{now.date()}  {now.hour}-{minute}-{second}  {info.static.track}  {info.static.carModel}  {round(reaction_time, 3)}  {kmph_delay}.csv"

                with open(f"CSVs/{file_name}", "w", newline="") as csvfile:
                    fieldnames = telemetry_data[0].keys()

                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")

                    writer.writeheader()
                    writer.writerows(telemetry_data)

            continue
    else:
        time.sleep(2)
