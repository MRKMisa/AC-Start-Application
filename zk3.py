import os

dir_list = os.listdir("CSVs")


telemetry_data = []
with open(f"CSVs/{dir_list[0]}", "r") as f:
    data = f.readlines()

    data.pop(0)

    for line in data:
        data = line.split(";")

        telemetry_data.append({
                            "number":data[0],
                            "time":data[1],
                            "date":data[2],
                            "hour":data[3],
                            "minutes":data[4],
                            "seconds":data[5],
                            "delay":data[6],

                            "speedKmh":data[7],
                            "throttle":data[8],
                            "brake":data[9],
                            "clutch":data[10],
                            "gear":data[11],
                            "FLwheelSlip":data[12],
                            "FRwheelSlip":data[13],
                            "RLwheelSlip":data[14],
                            "RRwheelSlip":data[15]
                            })

print(telemetry_data)