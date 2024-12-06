try:
    import arcpy
    from arcpy import env
except:
    pass
import os, string, logging, re, sys, math
from datetime import datetime, timedelta, parser

def addOne(number):
    import time
    newNum = number+1
    time.sleep(1)
    return [number,newNum]

# def executeMulti(inputData):
#     import concurrent.futures
#     import multiprocessing
#     import psutil
#     import tempfile
#     from netCDF4 import Dataset
#     import sys
#     import os
#     multiprocessing.set_executable(os.path.join(sys.exec_prefix, 'pythonw.exe'))

#     #Simple
#     #processes=multiprocessing.cpu_count() - 1
#     pool = multiprocessing.Pool(4, maxtasksperchild=10)
#     result_numbers = pool.map(addOne,inputData,chunksize=len(inputData)/4)

#     pool.close()
#     pool.join()
#     return result_numbers

# def executeMulti(inputData,function):
#     try:
#         import concurrent.futures
#         import multiprocessing
#         import psutil
#         import tempfile
#         from netCDF4 import Dataset


#         #Complex
#         cpuCount = psutil.cpu_count(logical=False)
#         multiprocessing.set_executable(os.path.join(sys.exec_prefix,'pythonw.exe'))
#         multiManager = multiprocessing.Manager()
#         lock = multiManager.Lock()
#         #logger = create_log_handler()
#         taskCount = len(inputData) #maybe need to submit dictionaries/lists
#         processedTaskCount = 0 
#         failedTaskIds_list = []

#         chunkSize = cpuCount*10
#         chunkSizeData = [inputData[x:x + chunkSize] for x in range(0,taskCount,chunkSize)]
#         for task in chunkSizeData:
#             with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
#                 #submit a callable to be executed, session had "processHydroTrace" (assuming its like a user defined function the holds the main process)
#                 future_to_result = {executor.submit(function,row,lock):row for row in task}
#             for future in concurrent.futures.as_completed(future_to_result):
#                 if future.result()[0] == 0:
#                     processedTaskCount += 1
#                     arcpy.AddMessage("Success {0} of {1}".format(processedTaskCount,taskCount))
#                 elif future.result()[0] == 1:
#                     arcpy.AddMessage("Failed ")
#     except:
#         raise


