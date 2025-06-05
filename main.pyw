import time
from get_shared_mem import get_shared_mem
from datetime import datetime
from show_reaction_time import show_reaction_time

info = get_shared_mem()

def load_config():
    with open("config.ini", "r") as f:
        configs = f.readlines()

    for line in configs:
        line = line.strip()

        if "x=" in line:
            if line.replace("x=", "") == "auto":
                x = "auto"
                continue
            else:
                if line.replace("x=", "").isdigit():
                    x = int(line.replace("x=", ""))
                else:
                    x = "auto"

        elif "y=" in line:
            if line.replace("y=", "") == "auto":
                y = "auto"
                continue
            else:
                if line.replace("y=", "").isdigit():
                    y = int(line.replace("y=", ""))
                else:
                    y = "auto"

        elif "scale=" in line:
            if line.replace("scale=", "").isdigit():
                scale = int(line.replace("scale=", ""))
            else:
                scale = 1

        elif "driverName=" in line:
            if line.replace("driverName=", "") == "auto":
                driverName = info.static.playerName
                continue
            else:
                driverName = line.replace("driverName=", "")
                continue  
    
    return x, y, scale, driverName

change = False
reset = False

while True:
    gear, clutch, currentTime = info.physics.gear, info.physics.clutch, info.graphics.currentTime

    if currentTime == "-:--:---":
        gear, clutch, currentTime = info.physics.gear, info.physics.clutch, info.graphics.currentTime


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

            start_time = time.time()

            clutch = info.physics.clutch
            while clutch == 0.0:
                clutch = info.physics.clutch

            end = time.time()

            reaction_time = end-start_time

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
                f.write(f"{now.date()} | {now.hour}:{minute}:{second} | Reaction time: {round(reaction_time, 3)} s\n")

            x, y, scale, driverName = load_config()

            show_reaction_time(x, y, scale, driverName, reaction_time)

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

            start_time = time.time()
            while gear == 1:
                gear = info.physics.gear


            end = time.time()

            reaction_time = end-start_time

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
                f.write(f"{now.date()} | {now.hour}:{minute}:{second} | Reaction time: {round(reaction_time, 3)} s\n")

            x, y, scale, driverName = load_config()

            show_reaction_time(x, y, scale, driverName, reaction_time)

            continue
    else:
        time.sleep(2)
