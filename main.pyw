import time
from datetime import datetime
import configparser
import threading
import csv
import sys
import os

from Utils.get_shared_mem import get_shared_mem
from Utils.show_reaction_time import show_reaction_time
from Utils.show_kmph_time import show_kmph_time

from Utils.log import *

write_script_start()

info = get_shared_mem()

conf = configparser.ConfigParser()

sys.excepthook = log_errors

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

    csvAutoDelete = conf["Misc"]["csvAutoDelete"]

    csvMaxFiles = conf["Misc"]["csvMaxFiles"]


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
                      "csvDataFrequency":csvDataFrequency,
                      "csvAutoDelete":csvAutoDelete,
                      "csvMaxFiles":csvMaxFiles
                        }
    
    return configSettings

change = False
reset = False

def recording_telemetry_data():
    global telemetry_data
    telemetry_data = []

    global run
    run = True
    while run:
        speedKmh, throttle, brake, clutch, gear, wheelSlip = info.physics.speedKmh, info.physics.gas, info.physics.brake, info.physics.clutch, info.physics.gear, info.physics.wheelSlip
        currentTime = info.graphics.currentTime


        now = datetime.now()

        if len(telemetry_data) != 0:
            delay = time.time()-float(telemetry_data[len(telemetry_data)-1]["time"])
        else:
            delay = "None"
        
        telemetry_data.append({
                          "number":len(telemetry_data),
                          "time":time.time(),
                          "date":now.date(),
                          "hour":now.hour,
                          "minutes":now.minute,
                          "seconds":now.second,
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
            
            write_script_output("Race start registed")

            if load_config()["recordCsv"].lower() == "true" or load_config()["recordCsv"].lower() == "1":
                t1 = start_recording_telemery_data()
                write_script_output("Starting recording telemetry")
            race_start_time = time.time()

            clutch = info.physics.clutch
            while clutch == 0.0:
                clutch = info.physics.clutch

            reaction_time = time.time()-race_start_time
            write_script_output(f"Reaction registed: {reaction_time}")

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

            write_script_output(f"100km/h registed: {kmph_delay}")

            if load_config()["recordCsv"].lower() == "true" or load_config()["recordCsv"].lower() == "1":
                for i, thread in enumerate(threading.enumerate()):
                    write_script_output(f"Thread{i}, Name: {thread.name}, Daemon: {thread.daemon}, Alive: {thread.is_alive()}")
                time.sleep(int(1000/int(load_config()["csvDataFrequency"]))/1000)
                end_recording_telemetry_data()
                t1.join()
                write_script_output("Recording telemetry ended")
                for i, thread in enumerate(threading.enumerate()):
                    write_script_output(f"Thread{i}, Name: {thread.name}, Daemon: {thread.daemon}, Alive: {thread.is_alive()}")

            now = datetime.now()
            timestamp = now.strftime("%Y-%m-%d | %H:%M:%S")

            with open("output.txt", "a") as f:
                f.write(f"{time.time()} | {timestamp} | {info.static.track} | {info.static.carModel} | {round(reaction_time, 3)} | {kmph_delay} \n")
                write_script_output("Output writed")

            configSettings = load_config()

            if configSettings["ShowReactionTimeGraphic"].lower() == "true" or load_config()["ShowReactionTimeGraphic"].lower() == "1":
                show_reaction_time(configSettings["ReactionTimeGraphicX"], configSettings["ReactionTimeGraphicY"], configSettings["ReactionTimeGraphicScale"], configSettings["driverName"], reaction_time)
            
            if configSettings["ShowkmphTimeGraphic"].lower() == "true" or load_config()["ShowkmphTimeGraphic"].lower() == "1":
                show_kmph_time(configSettings["kmphTimeGraphicX"], configSettings["kmphTimeGraphicY"], configSettings["kmphTimeGraphicScale"], configSettings["driverName"], kmph_delay)

            now = datetime.now()
            timestamp = now.strftime("%Y-%m-%d %H-%M-%S")
            if load_config()["recordCsv"].lower() == "true"or load_config()["recordCsv"].lower() == "1":
                file_name = f"{timestamp}  {info.static.track}  {info.static.carModel}  {round(reaction_time, 3)}  {kmph_delay}.csv"

                with open(f"CSVs/{file_name}", "w", newline="") as csvfile:

                    if load_config()["csvAutoDelete"].lower() == "true" or load_config()["csvAutoDelete"].lower() == "1":
                        write_script_output("Auto cleaning is turn on")
                        dir_list = os.listdir("CSVs")

                        rev_dir_list = dir_list

                        rev_dir_list.reverse()

                        for i, file in enumerate(rev_dir_list):
                            if i > int(load_config()["csvMaxFiles"])-1:
                                os.remove(f"CSVs/{file}")
                                write_script_output(f"Remove: {file}")

                    if len(telemetry_data) == 0:
                        write_script_output(f"Telemetry data is empty, waiting for thread end")
                        for t in range(20):
                            if len(telemetry_data) != 0:
                                break
                            time.sleep(0.2)
                    
                    if len(telemetry_data) == 0:
                        write_script_output(f"WARNING!!! Telemetry data can not be recorded")
                    else:
                        fieldnames = telemetry_data[0].keys()

                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")

                        writer.writeheader()
                        writer.writerows(telemetry_data)

                        write_script_output("Csv saved")

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
            
            write_script_output("Race start registed")

            if load_config()["recordCsv"].lower() == "true" or load_config()["recordCsv"].lower() == "1":
                t1 = start_recording_telemery_data()
                write_script_output("Starting recording telemetry")
            race_start_time = time.time()

            gear = info.physics.gear
            while gear == 1:
                gear = info.physics.gear

            reaction_time = time.time()-race_start_time
            write_script_output(f"Reaction registed: {reaction_time}")

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

            if kmph_delay != "None" and kmph_delay != "Braked":
                kmph_delay = time.time()-race_start_time

            write_script_output(f"100km/h registed: {kmph_delay}")

            if load_config()["recordCsv"].lower() == "true" or load_config()["recordCsv"].lower() == "1":
                for i, thread in enumerate(threading.enumerate()):
                    write_script_output(f"Thread{i}, Name: {thread.name}, Daemon: {thread.daemon}, Alive: {thread.is_alive()}")
                time.sleep(int(1000/int(load_config()["csvDataFrequency"]))/1000)
                end_recording_telemetry_data()
                t1.join()
                write_script_output("Recording telemetry ended")
                for i, thread in enumerate(threading.enumerate()):
                    write_script_output(f"Thread{i}, Name: {thread.name}, Daemon: {thread.daemon}, Alive: {thread.is_alive()}")
                

            now = datetime.now()
            timestamp = now.strftime("%Y-%m-%d | %H:%M:%S")

            with open("output.txt", "a") as f:
                f.write(f"{time.time()} | {timestamp} | {info.static.track} | {info.static.carModel} | {round(reaction_time, 3)} | {kmph_delay} \n")
                write_script_output("Output writed")
            
            configSettings = load_config()

            if configSettings["ShowReactionTimeGraphic"].lower() == "true" or load_config()["ShowReactionTimeGraphic"].lower() == "1":
                show_reaction_time(configSettings["ReactionTimeGraphicX"], configSettings["ReactionTimeGraphicY"], configSettings["ReactionTimeGraphicScale"], configSettings["driverName"], reaction_time)
            
            if configSettings["ShowkmphTimeGraphic"].lower() == "true" or load_config()["ShowkmphTimeGraphic"].lower() == "1":
                show_kmph_time(configSettings["kmphTimeGraphicX"], configSettings["kmphTimeGraphicY"], configSettings["kmphTimeGraphicScale"], configSettings["driverName"], kmph_delay)

            now = datetime.now()
            timestamp = now.strftime("%Y-%m-%d %H-%M-%S")
            if load_config()["recordCsv"].lower() == "true" or load_config()["recordCsv"].lower() == "1":
                file_name = f"{timestamp}  {info.static.track}  {info.static.carModel}  {round(reaction_time, 3)}  {kmph_delay}.csv"

                with open(f"CSVs/{file_name}", "w", newline="") as csvfile:

                    if load_config()["csvAutoDelete"].lower() == "true" or load_config()["csvAutoDelete"].lower() == "1":
                        write_script_output("Auto cleaning is turn on")
                        dir_list = os.listdir("CSVs")

                        rev_dir_list = dir_list

                        rev_dir_list.reverse()

                        for i, file in enumerate(rev_dir_list):
                            if i > int(load_config()["csvMaxFiles"])-1:
                                os.remove(f"CSVs/{file}")
                                write_script_output(f"Remove: {file}")

                    if len(telemetry_data) == 0:
                        write_script_output(f"Telemetry data is empty, waiting for thread end")
                        for t in range(20):
                            if len(telemetry_data) != 0:
                                break
                            time.sleep(0.2)
                    
                    if len(telemetry_data) == 0:
                        write_script_output(f"WARNING!!! Telemetry data can not be recorded")
                    else:
                        fieldnames = telemetry_data[0].keys()

                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")

                        writer.writeheader()
                        writer.writerows(telemetry_data)

                        write_script_output("Csv saved")

            continue
    else:
        time.sleep(2)
