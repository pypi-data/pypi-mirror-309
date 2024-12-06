try:
    import arcpy
except:
    pass
import sys
import os
from datetime import datetime, timedelta

info = "Module that contains data check classes and functions."
metadata = {
  "owner": "Works Consulting LLC",
  "creationDate": "3/18/2024",
  "creator": "Gabriel Morin",
  "lastEditDate": "10/29/2024",
  "lastEditor": "Gabriel Morin"}

class fields:
    """-------------------
    This class holds the field attributes functions for the LrsTools outputs
    -------------------
    """

    
    #need to make class attributes only readable
    class referent:
        """-------------------
        This subclass holds the field attributes for the LrsTools Referent output
        -------------------
        """
        intName = {"name":"INTERSECTIONNAME","type":"TEXT"}
        intId = {"name":"INTERSECTIONID","type":"GUID"}
        routeId = {"name":"ROUTEID","type":"TEXT"}
        xrouteId = {"name":"FEATUREID","type":"TEXT"}
        measure = {"name":"Measure","type":"DOUBLE"}
        lrsType = { "name":"LrsType","type":"SHORT"}
        lrsTypeOn = {"name":"LrsType_Onroad","type":"SHORT"}
        brng = {"name":"PosMsBrng","type":"DOUBLE"}
        qual = {"name":"Qual","type":"SHORT"}
        x = {"name":"X","type":"DOUBLE"}
        y = {"name":"Y","type":"DOUBLE"}
        bMeas = {"name":"BMeas","type":"DOUBLE"}
        eMeas = {"name":"EMeas","type":"DOUBLE"}
        alpha = {"name":"Alphabetised","type":"TEXT"}
        atGrade = {"name":"AtGrade","type":"SHORT"}
        avgX = {"name":"AvgX","type":"DOUBLE"}
        avgY = {"name":"AvgY","type":"DOUBLE"}
        avgDistTo = {"name":"DistToParent","type":"DOUBLE"}
        avgMeas = {"name":"AvgIntersectionMeas","type":"TEXT"}
        junctionId = {"name":"M110_JunctionID","type":"TEXT"}
        eventRteId = {"name":"EventRouteId","type":"TEXT"}
        eventXRteId = {"name":"EventXRouteId","type":"TEXT"}
        fcName = {"name":"FEATURECLASSNAME","type":"TEXT"}
        fromDate = {"name":"FROMDATE","type":"DATE"}
        toDate = {"name":"TODATE","type":"DATE"}
        runtime = {"name":"RunTime","type":"DATE"}

        def listFields():
            fieldDict = {}
            for attrName in dir(fields.referent):
                attrVal = getattr(fields.referent,attrName)
                if type(attrVal) == dict:
                    try:
                        fieldDict[attrVal["name"]] = attrVal["type"]
                    except:
                        pass
            return fieldDict

    class segments:
        """-------------------
        This subclass holds the field attributes for the LrsTools Segments output
        -------------------
        """
        segmentId = {"name":"M12_SegmentID","type":"TEXT"}
        routeId = {"name":"M9_RouteName","type":"TEXT"}
        fromMeas = {"name":"FromMeasure","type":"DOUBLE"}
        toMeas = {"name":"ToMeasure","type":"DOUBLE"}
        fromId =  {"name":"M10_BegJunctionID","type":"TEXT"}
        toId = {"name":"M11_EndJunctionID","type":"TEXT"}

    class legs:
        """-------------------
        This subclass holds the field attributes for the LrsTools Legs output
        -------------------
        """
        approachId = {"name":"M129_ApproachID","type":"TEXT"}
        routeId = {"name":"ROUTEID","type":"TEXT"}
        fromMeas = {"name":"FromMeasure","type":"DOUBLE"}
        toMeas = {"name":"ToMeasure","type":"DOUBLE"}
        dir = {"name":"Direction","type":"TEXT"}
        junctionId = {"name":"M128_JunctionID","type":"TEXT"}

    class centroids:
        """-------------------
        This subclass holds the field attributes for the LrsTools Centroids output
        -------------------
        """
        minDist = {"name":"minDist","type":"TEXT"}
        maxDist = {"name":"maxDist","type":"TEXT"}
        x = {"name":"X","type":"DOUBLE"}
        y = {"name":"Y","type":"DOUBLE"}

    class mire:
        """-------------------
        This subclass holds the field names for LrsTools MIRE feture classes
        -------------------
        """
        dataItem = {"name":"DataItem","type":"TEXT"}
        valueText = {"name":"ValueText","type":"TEXT"}
        valueParent = {"name":"ValueParent","type":"TEXT"}
        comment = {"name":"Comment","type":"TEXT"}

    def validate(inputData,fieldNameList,cont=False):
        """-------------------
        Function that intakes input data and checks for fields against a provided list and returns the fields not found
        -------------------
        """

        assert arcpy.Exists(inputData), "Excpected input data to exist, could not find it"
        assert type(fieldNameList) == list, "Expected a list for third parameter, got {0}".format(type(fieldNameList))
        assert type(cont) == bool, "Expected a bool for third parameter, got {0}".format(type(cont))

        fieldsFound = [f.name for f in arcpy.ListFields(inputData) if f.name in fieldNameList]
        fieldsSearchCound = len(fieldNameList)
        fieldsFoundCount = len(fieldsFound)
        fieldsNotFound = []
        if fieldsSearchCound < fieldsFoundCount:
            fieldsNotFound = [field for field in fieldNameList if field not in fieldsFound]
            if cont:
                arcpy.AddWarning("    Field Validation caught {0} missing fields within [{1}].".format(len(fieldsNotFound),inputData))
            else:
                arcpy.AddError("    Field Validation caught {0} missing fields within [{1}].".format(len(fieldsNotFound),inputData))
        return fieldsNotFound
    
    def addComplex(inputData,fieldInfo,overwrite):
        """-------------------
        Function that adds fields to a feature class with the added option if it already exists to overwrite or add a qualifier
        The fieldInfo parameter is a list of arguments that follow suit with the regular AddField_management arguments:
        [field_name, field_type, {field_precision}, {field_scale}, {field_length}, {field_alias}, {field_is_nullable}, {field_is_required}, {field_domain}]
        -------------------
        """
        assert len(fieldInfo) >= 2, "Expected at least two arguments for the second parameters, got {0}".format(len(fieldInfo))

        fieldName,fieldType = fieldInfo[0],fieldInfo[1]
        fieldPrecision =  fieldInfo[2] if len(fieldInfo) > 2 else ""
        fieldScale =  fieldInfo[3] if len(fieldInfo) > 3 else ""
        fieldLength =  fieldInfo[4] if len(fieldInfo) > 4 else ""
        fieldAlias =  fieldInfo[5] if len(fieldInfo) > 5 else ""
        fieldNullable =  fieldInfo[6] if len(fieldInfo) > 6 else "NULLABLE"
        fieldRequired =  fieldInfo[7] if len(fieldInfo) > 7 else "NON_REQUIRED"
        fieldDomain =  fieldInfo[8] if len(fieldInfo) > 8 else ""

        addFieldExists = [f.name for f in arcpy.ListFields(inputData) if f.name == fieldName]
        try:
            if len(addFieldExists) == 0:
                arcpy.AddField_management(inputData,fieldName,fieldType,
                                          fieldPrecision,fieldScale,fieldLength,
                                          fieldAlias,fieldNullable,fieldRequired,fieldDomain)
                return [fieldName,fieldType]
            else:
                if overwrite:
                    arcpy.AddWarning("  The field [{0}] already exists in [{1}] and will be overwritten.".format(fieldName,inputData))
                    endFieldName = fieldName
                else:
                    fieldNameFound = False
                    inputDataFieldsList = [f.name for f in arcpy.ListFields(inputData)]
                    while fieldNameFound == False:
                        for i in range(100):
                            arcpy.AddMessage(i)
                            qual = i + 1
                            newFieldName = fieldName + "_" + str(qual)
                            if newFieldName not in inputDataFieldsList:
                                fieldNameFound = True
                    arcpy.AddField_management(inputData,newFieldName,fieldType,
                                              fieldPrecision,fieldScale,fieldLength,
                                              fieldAlias,fieldNullable,fieldRequired,fieldDomain)
                    arcpy.AddWarning("  The field [{0}] already exists in [{1}] and will be renamed to [{2}].".format(fieldName,inputData,newFieldName))
                    endFieldName = newFieldName
                return [endFieldName,fieldType]
        except:
            arcpy.AddWarning("Unable to add the field [{0}] into [{1}]. Printing out errors.".format(fieldName,inputData))
            raise

    def convertFieldType(fieldType):
        fieldTypeConversionDict = {"OID":"DOUBLE","SmallInteger":"SHORT","Double":"DOUBLE","String":"TEXT","Integer":"FLOAT","GlobalID":"TEXT","Date":"DATE","Single":"FLOAT"}
        return fieldTypeConversionDict[fieldType]
    
    def convertFieldObj(fieldObj):
        """-----------------
        Converts a field obj from arcpy.ListFields into a list of values ready for Add Fields (multiple)
        """
        fieldInfoList = []
        for key in dir(fieldObj):
            if "_" != key[0]:
                fieldInfoList.append([key,getattr(fieldObj,key)])
        #[Field Name, Field Type, {Field Alias}, {Field Length}, {Default Value}, {Field Domain}]
        fieldTypeConversionDict = {"OID":"DOUBLE","SmallInteger":"SHORT","Double":"DOUBLE","String":"TEXT","Integer":"FLOAT","GlobalID":"TEXT","Date":"DATE","Single":"FLOAT"}
        fieldName = [values[1] for values in  fieldInfoList if values[0] == "baseName"][0]
        fieldType = [fieldTypeConversionDict[values[1]] for values in  fieldInfoList if values[0] == "type"][0]
        fieldAlias = [values[1] for values in  fieldInfoList if values[0] == "aliasName"][0]
        fieldLength = [values[1] for values in  fieldInfoList if values[0] == "length"][0]
        fieldDefault = [values[1] for values in  fieldInfoList if values[0] == "defaultValue"][0]
        fieldDomain = [values[1] for values in  fieldInfoList if values[0] == "domain"][0]
        newFieldInfoList = [fieldName,fieldType,fieldAlias,fieldLength,fieldDefault,fieldDomain]
        return newFieldInfoList

        
class inputs:
    """--------------------
    Contains initialChecks() functions to assist in data checks and attributes.
    -------------------
    """
    
    info = "Class that helps with checking input feature classes"
    showMessages = True
    def changeStatus(status):
        inputs.showMessages = status
    inputCount = 0
    allowedTypesAttr =  {'Table':False,'TableView':False,'FeatureClass':True,'FeatureLayer':True}
    stateDotDict = {"puerto":"PRHTA","rhode":"RIDOT","arizona":"ADOT","NAD_1983_UTM_Zone_13N":"NMDOT","oregon":"ODOT"}
    inputDataDict = {}
        
    def initialChecks(inputData,requireShape=False):
        """-------------------
        Intakes a input data and runs checks on them and spits out describe object attributes. Second parameter defines whether to check for shape or not.
        --------------------
        """

        assert arcpy.Exists(inputData), "The input data {0} cannot be found.".format(inputData)

        showMessages = inputs.showMessages
        allowedTypesAttr = inputs.allowedTypesAttr
        stateDotDict = inputs.stateDotDict
        allowedTypes = [dataType for dataType,shape in allowedTypesAttr.items()]
        shape_types = [dataType for dataType,shape in allowedTypesAttr.items() if shape]
        
        fc_desc,fc_desc_type = arcpy.Describe(inputData),arcpy.Describe(inputData).dataType
        if requireShape:
            assert fc_desc_type in shape_types, "Expected shape got {0}.".format(fc_desc_type)
        
        assert fc_desc_type in allowedTypes, "The Input Features type of {0} is not supported. Please contact Gabe to add in compatability.".format(fc_desc_type)
            
        fc_desc_path,fc_desc_baseName = fc_desc.path,fc_desc.baseName
        try:
            fc_desc_sr = fc_desc.spatialreference
            stateDot = []
            for keyWord,state in stateDotDict.items():
                if keyWord in fc_desc_sr.name.lower() or keyWord == fc_desc_sr.name:
                    stateDot.append(state)
        except:
            stateDot = []
            fc_desc_sr = None
            stateDot.append(None)

        assert len(stateDot) == 1,"Expected one State DOT got {0}".format(len(stateDot))
        if stateDot[0] is None:
            arcpy.AddWarning("Could not determine State DOT from this input: [{0}].".format(inputData))

        fullpath = os.path.join(fc_desc_path,fc_desc_baseName)
        fc_count_path = int(float((arcpy.GetCount_management(fullpath)).getOutput(0)))
        fc_count = int(float((arcpy.GetCount_management(inputData)).getOutput(0)))
        fc_sel_count = 0
        try:
            fidSet = fc_desc.fidSet
            if len(fidSet) > 0:
                fc_sel_count = len(fidSet.split(";")) if ";" in fidSet else 1
        except:
            pass
        if fc_count < fc_count_path:
            fc_sel_count = fc_count
        if showMessages:
            if inputs.inputCount == 0:
                arcpy.AddMessage("Record Count (Selection)   | Layer/Feature/Table Name")
                arcpy.AddMessage("-----------------------------------------------------------")
            firstIng = "{0} ({1})".format(fc_count_path,fc_sel_count)
            firstIngFill = firstIng.ljust(26," ")
            arcpy.AddMessage("{0} | {1}".format(firstIngFill,fc_desc_baseName))
            #arcpy.AddMessage("{0} ({1})                 | {2}".format(fc_count_path,fc_sel_count,fc_desc_baseName))

        try:
            fc_desc_shapeType = fc_desc.shapeType
        except:
            fc_desc_shapeType = None
        inputDataDict = inputs.inputDataDict
        if fc_desc_baseName not in inputDataDict:
            inputDataDict[fc_desc_baseName] = {}
        inputDataDict[fc_desc_baseName] = {"descObj": fc_desc,
                         "dataType": fc_desc_type,
                         "baseName": fc_desc_baseName,
                         "path": fc_desc_path,
                         "spatialReference": fc_desc_sr,
                         "recordCount": fc_count_path,
                         "selectionCount": fc_sel_count,
                         "stateDOT":stateDot[0],
                         "iterCount":fc_count,
                         "shapeType":fc_desc_shapeType}
        inputs.inputDataDict = inputDataDict
        inputs.inputCount += 1
        return inputDataDict[fc_desc_baseName]

class measures:
    """--------------------
    Contains forceLowHigh() functions to assist in data checks and attributes.
    -------------------
    """

    def forceLowHigh(Measures,error=False):
        low = min(Measures)
        high = max(Measures)
        if error:
            assert low == Measures[0], "Expected measures to be increasing"
        return [low,high]
        
