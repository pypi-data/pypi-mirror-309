import arcpy
import sys
import os
from datetime import datetime, timedelta

info = "Module that contains edit classes and functions."
metadata = {
  "owner": "Works Consulting LLC",
  "creationDate": "6/10/2024",
  "creator": "Gabriel Morin",
  "lastEditDate": "6/10/2024",
  "lastEditor": "Gabriel Morin"}

class tracker:
    """-------------------
    This class holds the track attributes functions for the LrsTools outputs
    -------------------
    """

    trackEdits = False
    def changeStatus(status):
        tracker.trackEdits = status
    editTrackerExists = False
    trackComment = None
    trackData = None
    objectClassName = None
    dataIsSde = False
    userName = None
    versionName = None
    updateInfo_List = []
    updateFields_List = []
    status = "Closed"

    def __init__(self):
        self.trackEdits = False
        self.editTrackerExists = False
        self.trackComment = None
        self.trackData = None
        self.objectClassName = None
        self.dataIsSde = False
        self.userName = None
        self.versionName = None
        self.updateInfo_List = []
        self.updateFields_List = []
        self.status = "Closed"
        self.info = "Class that tracks edits"

    class fields:
        """-------------------
        Class that holds the field info for a Works Consulting ET table
        -------------------
        """

        objectClassName = {"name":"ObjectClassName","type":"TEXT"}
        versionName = {"name":"VersionName","type":"TEXT"}
        recordId = {"name":"RecordID","type":"DOUBLE"}
        editType = {"name":"EditType","type":"TEXT"}
        columnName = {"name":"ColumnName","type":"TEXT"}
        origValue = { "name":"OriginalValue","type":"TEXT"}
        newValue = {"name":"NewValue","type":"TEXT"}
        modifiedDate = {"name":"ModifiedDate","type":"DATE"}
        userName = {"name":"UserName","type":"TEXT"}
    
    def listFields():
        """-------------------
        Function that list the fields expected in a Works Consulting edit tracker feature class
        -------------------
        """

        fieldDict = {}
        for attrName in dir(tracker.fields):
            attrVal = getattr(tracker.fields,attrName)
            if type(attrVal) == dict:
                try:
                    fieldDict[attrVal["name"]] = attrVal["type"]
                except:
                    pass
        return fieldDict
    
    def startTrack(inputData,suffix="_ET",comment="Script Tool Automatic Updates"):
        """-------------------
        Function that should be run at beginning of script and intakes input data and starts to track edits
        -------------------
        """

        path = arcpy.Describe(inputData).catalogPath
        if path.endswith(".sde"):
            tracker.dataIsSde = True
            descWorkspace = arcpy.da.Describe(path)
            descWorkspace["connectionProperties"]["version"]
            tracker.versionName = descWorkspace["connectionProperties"]["version"]
            try:
                tracker.userName = descWorkspace["connectionProperties"]["user"]
            except:
                tracker.userName = None
        tracker.objectClassName = arcpy.Describe(inputData).baseName
        ET_path = path + suffix
        etExists = arcpy.Exists(ET_path)

        if tracker.trackEdits:
            if etExists:
                tracker.editTrackerExists = True
                tracker.trackComment = comment
                tracker.trackData = ET_path
                tracker.status = "Open"
                arcpy.AddMessage("  *Edit Tracker found and will track edits")
            else:
                arcpy.AddWarning("Tracking Edits is set to True but could not find ET Table: [{0}]".format(ET_path))
        else:
            tracker.status = "Closed"

    def cursorUpdates(updateFields,OID,featureRowBefore,featureRowAfter):
        """-------------------
        Function that should be run after each "cursor".udpateRow("cursorRow") and intakes the update fields,
        and before and after attributes, as well as the ObjectID
        -------------------
        """

        assert len(featureRowBefore) == len(featureRowAfter), "Expected before and after value lists to have the same length, got {0} and {1} for before and after, repsectively".format(len(featureRowBefore),len(featureRowAfter))
        assert len(updateFields) == len(featureRowBefore), "Expected Update Fields List to have same length as the Update Attributes List."

        
        if tracker.editTrackerExists and tracker.trackEdits:
            if tracker.status == "Open":
                trackData = tracker.trackData
                dataBaseName = tracker.objectClassName
                comment = tracker.trackComment
                for field in updateFields:
                    if field not in tracker.updateFields_List:
                        tracker.updateFields_List.append(field)
                versionName = None
                userName = None
                if tracker.dataIsSde:
                    versionName = tracker.versionName
                    userName = tracker.userName

                #check for changes
                for i,attrBefore in enumerate(featureRowBefore):
                    attrAfter = featureRowAfter[i]
                    if attrBefore != attrAfter:
                        updateField = updateFields[i]
                        runtime = datetime.now()
                        #['ColumnName', 'EditType', 'ModifiedDate', 'NewValue', 'ObjectClassName', 'OriginalValue', 'RecordID', 'UserName', 'VersionName']
                        updateInfo = [updateField,"Update",runtime,attrAfter,dataBaseName,attrBefore,OID,userName,versionName]
                        tracker.updateInfo_List.append(updateInfo)

    def updateET():
        """-------------------
        Function that updates the ET table with values grabbed from a list generated within the "cursorUpdates" function
        -------------------
        """
        
        if tracker.trackEdits:
            if tracker.status == "Open":
                updateFields = []
                for attrName in dir(tracker.fields):
                    attrVal = getattr(tracker.fields,attrName)
                    if type(attrVal) == dict:
                        try:
                            updateFields.append(attrVal["name"])
                        except:
                            pass
                et_table = tracker.trackData
                updateList = tracker.updateInfo_List
                with arcpy.da.InsertCursor(et_table,updateFields) as featureClass:
                    for info in updateList:
                        featureClass.insertRow(info)

                arcpy.AddMessage("[ET] Inserted {0} update rows into the ET Table".format(len(updateList)))
            



         
        
        
        


    