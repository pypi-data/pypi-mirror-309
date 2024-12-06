try:
    import arcpy
except:
    pass
import sys
from datetime import datetime, timedelta

info = "Module that contains time classes and functions."
metadata = {
  "owner": "Works Consulting LLC",
  "creationDate": "3/15/2024",
  "creator": "Gabriel Morin",
  "lastEditDate": "5/3/2024",
  "lastEditor": "Gabriel Morin"}

class tracking:
    """--------------------
    Contains start(), live() and end() functions to assist in runtime logging and tracking attributes.
    --------------------
    """

    #info = "Class that helps with recording process runtimes."
    showMetrics = True
    def changeStatus(status):
        tracking.showMetrics = status
    ProcessNumber = 0
    startList = []
    timeTuple = []
    iterationTuple = []
    openSession = False
    currentLabel = None
    run = True
    itemize = True

    processCountList = []
    totalIterPreCount = 0
    liveReset = True
    unknownProcessCounts = 0
    processTotal = 0

    def __init__(self):
        self.showMetrics = True
        self.openSession = False
        self.run = True
        self.startList = []
        self.timeTuple = []
        self.iterationTuple = []
        self.info = "Class that helps with recording process runtimes."
    
    def startFull(ProcessCountList):
        """--------------------
        Intakes a list of counts to run a tracker on all processes. Opens a session.
        --------------------
        """
        if not tracking.itemize:
            assert type(ProcessCountList) == list, "Expected a list, got a {0}".format(type(ProcessCountList))

            ProcessLabel = "Script Running..."
            arcpy.SetProgressorLabel(ProcessLabel)
            tracking.currentLabel = ProcessLabel
            tracking.totalIterPreCount = sum([count for count in ProcessCountList if count is not None])
            tracking.unknownProcessCounts = len([count for count in ProcessCountList if count is None])
            tracking.processCountList = ProcessCountList
            tracking.processTotal = len(ProcessCountList)
            tracking.startList.append(datetime.now())
            tracking.timeTuple.append([])
            tracking.iterationTuple.append(0)
            tracking.openSession = True


    def start(ProcessLabel,iterCount=1):
        """--------------------
        Intakes a process label and updates the tracking class for process runtimes and live tracking. Opens a session.
        --------------------
        """

        if tracking.run:
            assert type(ProcessLabel) == str, "ArgumentDataTypeError - expected a {0} got a {1}".format(str,type(ProcessLabel))
            
            if tracking.itemize:
                assert tracking.openSession == False, "A tracking session is already open. Reconfigure and close tracking sessions before starting another one."
                iterCount = 1
                arcpy.SetProgressorLabel(ProcessLabel)
                tracking.currentLabel = ProcessLabel
                ProcessNumber = tracking.ProcessNumber
                tracking.startList.append(datetime.now())
                tracking.timeTuple.append([])
                tracking.iterationTuple.append(0)
                tracking.openSession = True
            
            else:
                tracking.currentLabel = ProcessLabel
                #arcpy.AddMessage(ProcessLabel)


    
    def live(iterCount):
        """--------------------
        Intakes the total number of iterations for process and updates the Progressor Label with ETA's and ETR's.
        --------------------
        """

        if tracking.run:
            assert type(iterCount) == int, "ArgumentDataTypeError - expected a {0} got a {1}".format(int,type(iterCount))
            assert tracking.openSession == True, "No tracking session is open. Reconfigure and open a tracking session before."
            
            if tracking.itemize:
            
                ProcessLabel = tracking.currentLabel
                ProcessNumber = tracking.ProcessNumber
                start = tracking.startList[ProcessNumber]
                time = tracking.timeTuple[ProcessNumber]
                iteration = tracking.iterationTuple[ProcessNumber]
                now = datetime.now()
                time.append(now)
                diff = time[iteration] - start
                rate = (diff.total_seconds())/len(time)
                eta = rate*iterCount/60
                etr = eta - (diff.total_seconds())/60
                units = "sec(s)" if etr < 1 else "min(s)"
                etr = etr*60 if etr < 1 else etr
                newProgressorLabel = "{0}\nEstimated total time in min(s): {1} | Estimate remaining time in {2}: {3}".format(ProcessLabel,round(eta,1),units,round(etr,1))
                arcpy.SetProgressor("step",newProgressorLabel,0,iterCount,iteration)
                arcpy.SetProgressorPosition(iteration)
                tracking.iterationTuple[ProcessNumber] += 1
            else:

                ProcessLabel = tracking.currentLabel
                ProcessNumber = tracking.ProcessNumber
                ProcessIterCount = tracking.processCountList[ProcessNumber]
                start = tracking.startList[0]
                time = tracking.timeTuple[0]
                iteration = tracking.iterationTuple[0]
                if ProcessIterCount is None:
                    if tracking.liveReset:
                        newIterCount = tracking.totalIterPreCount + iterCount
                        tracking.liveReset = False
                    else:
                        newIterCount = tracking.totalIterPreCount
                else:
                    newIterCount = tracking.totalIterPreCount
                now = datetime.now()
                time.append(now)
                diff = time[iteration] - start
                rate = (diff.total_seconds())/len(time)
                eta = rate*newIterCount/60
                etr = eta - (diff.total_seconds())/60
                units = "sec(s)" if etr < 1 else "min(s)"
                etr = etr*60 if etr < 1 else etr
                newProgressorLabel = "{0}\nEstimated total time in min(s): {1} | Estimate remaining time in {2}: {3}".format(ProcessLabel,round(eta,1),units,round(etr,1))
                arcpy.SetProgressor("step",newProgressorLabel,0,newIterCount,iteration)
                arcpy.SetProgressorPosition(iteration)
                tracking.iterationTuple[0] += 1
                tracking.totalIterPreCount = newIterCount
                #arcpy.AddMessage(tracking.iterationTuple)
                #arcpy.AddMessage(tracking.totalIterPreCount)
    
    def end():
        """--------------------
        Displays process runtimes through arcpy's AddMessage function. Closes a session.
        --------------------
        """

        if tracking.run:
            assert tracking.openSession == True, "No tracking session is open. Reconfigure and open a tracking session before."

            if tracking.itemize:
                
                showMetrics = tracking.showMetrics
                ProcessLabel = tracking.currentLabel
                ProcessNumber = tracking.ProcessNumber
                start = tracking.startList[ProcessNumber]
                end = datetime.now()
                date_str = end.strftime("%H:%M:%S")
                diff = end - start
                diff2 = diff.total_seconds() if diff.total_seconds() < 60 else diff.total_seconds()/60
                diff_str = str(round(diff2,2)) + " seconds" if diff.total_seconds() < 60 else str(round(diff2,2)) + " minutes"
                if showMetrics:
                    arcpy.AddMessage("[{0}] {1} took {2} and finished at {3}.".format(ProcessNumber+1,ProcessLabel,diff_str,date_str))
                tracking.ProcessNumber +=1
                tracking.openSession = False
            else:

                showMetrics = False
                ProcessLabel = tracking.currentLabel
                ProcessNumber = tracking.ProcessNumber
                iteration = tracking.iterationTuple[0]
                newIterCount = tracking.totalIterPreCount
                start = tracking.startList[0]
                end = datetime.now()
                time = tracking.timeTuple[0]
                time.append(end)
                diff = time[iteration] - start
                rate = (diff.total_seconds())/len(time)
                eta = rate*newIterCount/60
                etr = eta - (diff.total_seconds())/60
                units = "sec(s)" if etr < 1 else "min(s)"
                etr = etr*60 if etr < 1 else etr
                newProgressorLabel = "{0}\nEstimated total time in min(s): {1} | Estimate remaining time in {2}: {3}".format(ProcessLabel,round(eta,1),units,round(etr,1))
                arcpy.SetProgressor("step",newProgressorLabel,0,newIterCount,iteration)
                arcpy.SetProgressorPosition(iteration)
                tracking.iterationTuple[0] += 1
                tracking.ProcessNumber += 1
                tracking.openSession = True
                tracking.liveReset = True


