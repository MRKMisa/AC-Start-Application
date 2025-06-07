from tkinter import *
from tkinter import messagebox
import os
import math

from plotly.subplots import make_subplots
import plotly.graph_objs as go
import plotly.io as pio

dir_list = os.listdir("CSVs")

def open_graphs():
    width=2
    size=6

    if len(lb.curselection()) > 4:
        print(f"ERROR - Cant choose more than 4 files: {lb.curselection()}")
        messagebox.showerror("Error", f"Can not choose more than 4 files!!")
        return
    
    rows, cols = int(math.ceil(len(lb.curselection())/2)), 1 if len(lb.curselection())==1 else 2
    print(f"Make rows: {rows}, cols: {cols}")

    fig = make_subplots(rows=int(math.ceil(len(lb.curselection())/2)), cols=1 if len(lb.curselection())==1 else 2, subplot_titles=[dir_list[i] for i in lb.curselection()])
    
    for i, n in enumerate(lb.curselection()):
        file = dir_list[n]
        print(file)

        telemetry_data = []
        with open(f"CSVs/{file}", "r") as f:
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

        x = []
        throttle = []
        speed = []
        clutch = []
        wheel_slip = []


        times = []
        currentTimes = []
        dates = []
        delays = []
        for row in telemetry_data:
            x.append(row["number"])
            throttle.append(round(float(row["throttle"]), 2)*100)
            speed.append(round(float(row["speedKmh"]), 2))
            clutch.append(round(float(row["clutch"]), 2)*100)
            wheel_slip.append(round((float(row["RLwheelSlip"])+float(row["RRwheelSlip"]))/2, 2)*10)

            times.append(row["time"])

            currentTimes.append(row["currentTime"])

            dates.append(f"{row['date']} {row['hour']}:{row['minutes']}:{row['seconds']}")

            delays.append(row["delay"])   
        
        trace1 = go.Scatter(
            x=x,
            y=throttle,

            mode='lines+markers+text',
            name=f"Throttle",
            line=dict(color="green", width=width),
            marker=dict(size=size, color='green'),

            hovertemplate='<br>Number: %{x}<br>currentTime: %{customdata[0]}<br>realTime: %{customdata[1]}<br>Time: %{customdata[2]}<br>Delay: %{customdata[3]}<br><br>Throttle: %{y}',
            customdata=[[currentTimes[i], dates[i], times[i], delays[i]] for i in range(len(x))]
            
        )

        trace2 = go.Scatter(
            x=x,
            y=speed,
            mode='lines+markers+text',
            name="Speed",
            line=dict(color="purple", width=width),
            marker=dict(size=size, color='purple'),
            hovertemplate='<br>Number: %{x}<br>currentTime: %{customdata[0]}<br>realTime: %{customdata[1]}<br>Time: %{customdata[2]}<br>Delay: %{customdata[3]}<br><br>Speed: %{y}',
            customdata=[[currentTimes[i], dates[i], times[i], delays[i]] for i in range(len(x))]
            
        )

        trace3 = go.Scatter(
            x=x,
            y=clutch,
            mode='lines+markers+text',
            name="Clutch",
            line=dict(color="blue", width=width),
            marker=dict(size=size, color='blue'),
            hovertemplate='<br>Number: %{x}<br>currentTime: %{customdata[0]}<br>realTime: %{customdata[1]}<br>Time: %{customdata[2]}<br>Delay: %{customdata[3]}<br><br>Clutch: %{y}',
            customdata=[[currentTimes[i], dates[i], times[i], delays[i]] for i in range(len(x))]
            
        )

        trace4 = go.Scatter(
            x=x,
            y=wheel_slip,
            mode='lines+markers+text',
            name="Rear wheels slip",
            line=dict(color="yellow", width=width),
            marker=dict(size=size, color='yellow'),
            hovertemplate='<br>Number: %{x}<br>currentTime: %{customdata[0]}<br>realTime: %{customdata[1]}<br>Time: %{customdata[2]}<br>Delay: %{customdata[3]}<br><br>Rear wheels slip: %{y}',
            customdata=[[currentTimes[i], dates[i], times[i], delays[i]] for i in range(len(x))]
            
        )

        row, col = math.ceil((i+1)/2), (i%cols)+1
        print(row, col, i)

        fig.add_trace(trace1, row=row, col=col)
        fig.add_trace(trace2, row=row, col=col)
        fig.add_trace(trace3, row=row, col=col)
        fig.add_trace(trace4, row=row, col=col)

        for annotation in fig['layout']['annotations']:
            annotation['font'] = dict(size=7)

        updates = {
            "title":"AC Start telemetry"
        }
        if i == 0:
            updates[f"xaxis_title"] = "Number of record"
            updates[f"yaxis_title"] = "Value"
        else:
            updates[f"xaxis{i+1}_title"] = "Number of record"
            updates[f"yaxis{i+1}_title"] = "Value"

        fig.update_layout(**updates)
    
    pio.show(fig)

root = Tk()
root.title("csv reader")
root.geometry("750x400")

l = Label(root, text="Choose csv:")
l.pack()

lb = Listbox(root, width=50, selectmode="extended")

for file in dir_list:
    lb.insert("end", file)

lb.pack()

b = Button(root, text="Open graph", width=25, command=open_graphs)
b.pack()

root.mainloop()