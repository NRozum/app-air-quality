
import tkinter
import tkinter.messagebox
from data_retrieve import DataRetrieve
from database import database
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk)

import numpy as np


def dbClickOnStation(event):
    """
        event that occurs on double click on the station list
    """

    #obtain stationId
    cs = stationslist.curselection() 
    idx = cs[0]
    stationId = idx_map[idx]

    # getMeasurements
    measurementStations = DataRetrieve.DataRetrieve.getMeasurementStations(stationId=stationId)
    if measurementStations:
        db.addMeasurementStations(json=measurementStations)
    else:
        tkinter.messagebox.showwarning("UWAGA","Brak polączenia z API wynik na podstawie danych historycznych")
    measurementStationsDb = db.getMeasurementStations(stationId=stationId)
    ii=0
    measurementStationslist.delete(0,tkinter.END)
    for measurementStation in measurementStationsDb:
        measurementStationslist.insert(ii, measurementStation[2])
        measStationsIdxMap[ii] = measurementStation[0]
        ii+=1

def dbClickOnMeasurementStation(event):
    """
        event that occurs on double click on the list of measurement stations
    """

    #obtain stationId
    xx = measurementStationslist.curselection() 
    idx = xx[0]
    measurementStationId = measStationsIdxMap[idx]

    # getMeasurements
    measurementData = DataRetrieve.DataRetrieve.getMeasurementData(sensorId=measurementStationId)
    if measurementData:
        db.addMeasurementData(json=measurementData, measurementStationId=measurementStationId)
    else:
        tkinter.messagebox.showwarning("UWAGA","Brak polączenia z API wynik na podstawie danych historycznych")
    measurementDataDb = db.getMeasurementData(measurementStationId=measurementStationId, time_h=sliderTime.get())
    yaxisLabel = []
    xdata = []
    ydata = []
    for data in measurementDataDb:
        yaxisLabel = data[0]
        ydata.append(data[1])
        xdata.append(data[2])

    # make plot
    # the figure that will contain the plot 
    plot1.cla()
    if len(ydata) > 0:
        plot1.plot(xdata[::-1],ydata[::-1], marker='o', label=f'Max={np.max(ydata)} Min={np.min(ydata)}, Avg={np.mean(ydata)}')
        plot1.set_xlabel('date')
        plot1.set_ylabel(yaxisLabel)
        plot1.tick_params(axis='x',labelrotation=20)
        plot1.legend(loc='upper center')
        canvas.draw() 
    else:
        tkinter.messagebox.showwarning("UWAGA","Brak danych do wyświetlenia")



db = database.Database("measurements2.db")

stations = DataRetrieve.DataRetrieve.getStationList()
if stations:
    db.addStations(json=stations)
else:
    tkinter.messagebox.showwarning("UWAGA","Brak polączenia z API wynik na podstawie danych historycznych")

m = tkinter.Tk()
fig = Figure(figsize = (7, 7), 
            dpi = 100) 
plot1 = fig.add_subplot(111) 
canvas = FigureCanvasTkAgg(fig, 
                        master = m)
canvas.get_tk_widget().pack(side=tkinter.BOTTOM,expand=True, fill=tkinter.BOTH)   

#create list of stations
w = tkinter.Label(m, text='Wybierz jedną z dostępnych stacji pomiarowych')
w.pack(side=tkinter.TOP, anchor=tkinter.W)
scrollbar = tkinter.Scrollbar(m)
scrollbar.pack(side=tkinter.LEFT, fill=tkinter.Y)
stationslist = tkinter.Listbox(m, yscrollcommand=scrollbar.set)
stationslist.config(width=0)
stations_db = db.getStations()

index=0
idx_map = {}
for station in stations:
    idx_map[index] = station['id']
    stationslist.insert(index, station['stationName'])
    index += 1

stationslist.bind('<Double-1>', dbClickOnStation)  
stationslist.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
scrollbar.config(command=stationslist.yview)

w2 = tkinter.Label(m, text='Wybierz dostępne pomiary')
w2.pack(side=tkinter.TOP,anchor=tkinter.E)

scrollbar2 = tkinter.Scrollbar(m)
scrollbar2.pack(side=tkinter.RIGHT, fill=tkinter.Y)

measStationsIdxMap = {}
measurementStationslist = tkinter.Listbox(m, yscrollcommand=scrollbar2.set, height=10)
measurementStationslist.bind('<Double-1>', dbClickOnMeasurementStation)  
measurementStationslist.pack(side=tkinter.RIGHT, fill=tkinter.BOTH)
scrollbar2.config(command=measurementStationslist.yview)

w3 = tkinter.Label(m, text='Ustaw okno czasowe - ostatnie 0-48 godzin')
w3.pack(side=tkinter.TOP, anchor=tkinter.N)
sliderTime = tkinter.Scale(m, from_=0, to=48, orient=tkinter.HORIZONTAL)
sliderTime.pack()


m.mainloop()