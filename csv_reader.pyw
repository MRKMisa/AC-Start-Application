from tkinter import *
import os

import plotly.graph_objs as go
import plotly.io as pio

dir_list = os.listdir("CSVs")

def open_throttle_graph():
    print(dir_list[lb.curselection()[0]])

    telemetry_data = []
    with open(f"CSVs/{dir_list[lb.curselection()[0]]}", "r") as f:
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

                                "currentTime":data[7],

                                "speedKmh":data[8],
                                "throttle":data[9],
                                "brake":data[10],
                                "clutch":data[11],
                                "gear":data[12],
                                "FLwheelSlip":data[13],
                                "FRwheelSlip":data[14],
                                "RLwheelSlip":data[15],
                                "RRwheelSlip":data[16]
                                })

    x, y = [], []
    times = []
    currentTimes = []
    dates = []
    delays = []
    for row in telemetry_data:
        x.append(row["number"])
        y.append(round(float(row["throttle"]), 2))

        times.append(row["time"])

        currentTimes.append(row["currentTime"])

        dates.append(f"{row['date']} {row['hour']}:{row['minutes']}:{row['seconds']}")

        delays.append(row["delay"])
    
    trace = go.Scatter(
        x=x,
        y=y,
        mode='lines+markers+text',
        line=dict(color='#a074c4', width=2),
        marker=dict(size=8, color='#a074c4'),
        hovertemplate='<br>Number: %{x}<br>currentTime: %{customdata[0]}<br>realTime: %{customdata[1]}<br>Time: %{customdata[2]}<br>Delay: %{customdata[3]}<br><br>Throttle: %{y}',
        customdata=[[currentTimes[i], dates[i], times[i], delays[i]] for i in range(len(x))]
        
    )

    fig = go.Figure(data=[trace])
    pio.show(fig)

def open_speed_graph():
    print(dir_list[lb.curselection()[0]])

    telemetry_data = []
    with open(f"CSVs/{dir_list[lb.curselection()[0]]}", "r") as f:
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

                                "currentTime":data[7],

                                "speedKmh":data[8],
                                "throttle":data[9],
                                "brake":data[10],
                                "clutch":data[11],
                                "gear":data[12],
                                "FLwheelSlip":data[13],
                                "FRwheelSlip":data[14],
                                "RLwheelSlip":data[15],
                                "RRwheelSlip":data[16]
                                })

    x, y = [], []
    times = []
    currentTimes = []
    dates = []
    delays = []
    for row in telemetry_data:
        x.append(row["number"])
        y.append(round(float(row["speedKmh"]), 2))

        times.append(row["time"])

        currentTimes.append(row["currentTime"])

        dates.append(f"{row['date']} {row['hour']}:{row['minutes']}:{row['seconds']}")

        delays.append(row["delay"])
    
    trace = go.Scatter(
        x=x,
        y=y,
        mode='lines+markers+text',
        line=dict(color='#a074c4', width=2),
        marker=dict(size=8, color='#a074c4'),
        hovertemplate='<br>Number: %{x}<br>currentTime: %{customdata[0]}<br>realTime: %{customdata[1]}<br>Time: %{customdata[2]}<br>Delay: %{customdata[3]}<br><br>Speed: %{y}',
        customdata=[[currentTimes[i], dates[i], times[i], delays[i]] for i in range(len(x))]
        
    )

    fig = go.Figure(data=[trace])
    pio.show(fig)

def open_clutch_graph():
    print(dir_list[lb.curselection()[0]])

    telemetry_data = []
    with open(f"CSVs/{dir_list[lb.curselection()[0]]}", "r") as f:
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

                                "currentTime":data[7],

                                "speedKmh":data[8],
                                "throttle":data[9],
                                "brake":data[10],
                                "clutch":data[11],
                                "gear":data[12],
                                "FLwheelSlip":data[13],
                                "FRwheelSlip":data[14],
                                "RLwheelSlip":data[15],
                                "RRwheelSlip":data[16]
                                })

    x, y = [], []
    times = []
    currentTimes = []
    dates = []
    delays = []
    for row in telemetry_data:
        x.append(row["number"])
        y.append(round(float(row["clutch"]), 2))

        times.append(row["time"])

        currentTimes.append(row["currentTime"])

        dates.append(f"{row['date']} {row['hour']}:{row['minutes']}:{row['seconds']}")

        delays.append(row["delay"])
    
    trace = go.Scatter(
        x=x,
        y=y,
        mode='lines+markers+text',
        line=dict(color='#a074c4', width=2),
        marker=dict(size=8, color='#a074c4'),
        hovertemplate='<br>Number: %{x}<br>currentTime: %{customdata[0]}<br>realTime: %{customdata[1]}<br>Time: %{customdata[2]}<br>Delay: %{customdata[3]}<br><br>Clutch: %{y}',
        customdata=[[currentTimes[i], dates[i], times[i], delays[i]] for i in range(len(x))]
        
    )

    fig = go.Figure(data=[trace])
    pio.show(fig)

def open_wheel_slip_graph():
    print(dir_list[lb.curselection()[0]])

    telemetry_data = []
    with open(f"CSVs/{dir_list[lb.curselection()[0]]}", "r") as f:
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

                                "currentTime":data[7],

                                "speedKmh":data[8],
                                "throttle":data[9],
                                "brake":data[10],
                                "clutch":data[11],
                                "gear":data[12],
                                "FLwheelSlip":data[13],
                                "FRwheelSlip":data[14],
                                "RLwheelSlip":data[15],
                                "RRwheelSlip":data[16]
                                })

    x, y = [], []
    times = []
    currentTimes = []
    dates = []
    delays = []
    for row in telemetry_data:
        x.append(row["number"])
        y.append(round((float(row["RLwheelSlip"])+float(row["RRwheelSlip"]))/2, 2))

        times.append(row["time"])

        currentTimes.append(row["currentTime"])

        dates.append(f"{row['date']} {row['hour']}:{row['minutes']}:{row['seconds']}")

        delays.append(row["delay"])
    
    trace = go.Scatter(
        x=x,
        y=y,
        mode='lines+markers+text',
        line=dict(color='#a074c4', width=2),
        marker=dict(size=8, color='#a074c4'),
        hovertemplate='<br>Number: %{x}<br>currentTime: %{customdata[0]}<br>realTime: %{customdata[1]}<br>Time: %{customdata[2]}<br>Delay: %{customdata[3]}<br><br>Rear wheels slip: %{y}',
        customdata=[[currentTimes[i], dates[i], times[i], delays[i]] for i in range(len(x))]
        
    )

    fig = go.Figure(data=[trace])
    pio.show(fig)


root = Tk()
root.title("csv reader")
root.geometry("750x400")

l = Label(root, text="Choose csv:")
l.pack()

lb = Listbox(root, width=50)

for file in dir_list:
    lb.insert("end", file)

lb.pack()

b1 = Button(root, text="Open throttle graph", width=25, command=open_throttle_graph)
b1.pack()

b2 = Button(root, text="Open speed graph", width=25, command=open_speed_graph)
b2.pack()


b3 = Button(root, text="Open clutch graph", width=25, command=open_clutch_graph)
b3.pack()

b4 = Button(root, text="Open wheels slip graph", width=25, command=open_wheel_slip_graph)
b4.pack()

root.mainloop()