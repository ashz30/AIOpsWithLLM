from _pydatetime import datetime

import win32evtlog
import psutil, os, cpuinfo

#mneed to run as admin /access rights for event log

def getEventLogsAndMetrics():
    hand = win32evtlog.OpenEventLog("BPIN038", "Blue Prism")
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ
    total = win32evtlog.GetNumberOfEventLogRecords(hand)
    event_no = 1
    print("Accessing Blue Prism event log for Host BPIN038")
    returnString = "Accessing Blue Prism event log for Host BPIN038"

    while True:
            events = win32evtlog.ReadEventLog(hand, flags, 0)
            if events:
                for event in events:
                    data = event.StringInserts
                    searchWord = "System.OutOfMemoryException"
                    if (event.EventID == 0 and searchWord in data[0]) :
                        start_index = data[0].find(searchWord)
                        end_index = min(start_index + len(searchWord) + 100, len(data[0]))

                        message = searchWord + data[0][start_index + len(searchWord):end_index]
                        #message = data[0]
                        computer = event.ComputerName
                        user = event.SourceName

                       # event_time = str(event.TimeGenerated)[3:5] + "/" + str(event.TimeGenerated)[0:2] + "/20" + str(event.TimeGenerated)[6:]
                       # event_time = str(datetime.strptime(event_time, "%d/%m/%Y %H:%M:%S"))
                        event_time = event.TimeGenerated
                        event_line = str(event_no)+ ' : Event Time -' + str(event_time) + " Event Description - " + message + "-" + user + "-" + "Blueprism event log" + " in Runtime hostname-" + computer
                        print(event_line)
                        returnString = returnString + " \n" + event_line
                    event_no += 1
            if event_no >= total:
                print ("Finished data gathered from Blue Prism event log.")
                returnString = returnString + "\n" + " Finished data gathered from Blue Prism event log."
                kb = float(1024)
                mb = float(kb ** 2)
                gb = float(kb ** 3)
                memTotal = int(psutil.virtual_memory()[0] / gb)
                memFree = int(psutil.virtual_memory()[1] / gb)
                memUsed = int(psutil.virtual_memory()[3] / gb)
                memPercent = int(memUsed / memTotal * 100)
                print("RAM Used         : ", memUsed, "GiB /", memTotal, "GiB", "(", memPercent, "%", ")")
                returnString = returnString + "\n" + str(memUsed) + "GiB /" +  str(memTotal) + "GiB" + "("+ str(memPercent)+ "%"+ ")"
                storageTotal = int(psutil.disk_usage('/')[0] / gb)
                storageUsed = int(psutil.disk_usage('/')[1] / gb)
                storageFree = int(psutil.disk_usage('/')[2] / gb)
                storagePercent = int(storageUsed / storageTotal * 100)
                print("Disk Used        : ", storageUsed, "GiB /", storageTotal, "GiB", "(", storagePercent, "%", ")")
                returnString = returnString + "\n" + "Disk Used        : " + str(storageUsed) + " GiB /" + str(storageTotal) + " GiB" + "(" + str(storagePercent) + "%" + ")"
                print("Load avg (15 mins)  :", round(psutil.getloadavg()[2], 2))
                returnString = returnString + "\n" + "Load avg (15 mins)  :" + str(round(psutil.getloadavg()[2], 2))
                print("Current instantaneous CPU usage:" , psutil.cpu_percent() )
                returnString = returnString + "\n" + "Current instantaneous CPU usage:" + str(psutil.cpu_percent())
                #print ("CPU Used Percentage : ", psutil.cpu_percent() , " - Memory used percentage :" , psutil.virtual_memory().percent)

                return returnString


