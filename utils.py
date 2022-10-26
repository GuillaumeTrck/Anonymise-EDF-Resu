import argparse
from datetime import datetime
import glob
import os
def initLogs(logs):
    global logName
    if (logs):
        print("Logs activated")
        logName = logs
    else :
        print("Missing logs name. Procedure will goes on without logs")
        logName = ""
    if logName :
        try : 
            fid = open(logName, "a")
        except : 
            fid = open(logName, "w")
            fid.close()
            fid = open(logName, "a")
        else: 
            fid.write("{0} -- Start of logs \n".format(datetime.now().strftime("%Y-%m-%d %H:%M")))
            fid.close()
            printLogs('Logs initialisés')
    return

def printLogs(txt):
    if logName :
        fid = open(logName, "a")
        fid.write(txt + "\n")
        fid.close() 
    print(txt)
    return
            
def parseArguments(): 
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--edf", required=True, help="Edf file name")
    parser.add_argument("-r", "--resu", required=True, help="Edf file name")
    parser.add_argument("-s", "--stages", required=False, action="store_true", help="Activation of stages analysis")
    parser.add_argument("-sp", "--spindles", required=False, action="store_true", help="Activation of spindles analysis")
    parser.add_argument("-l", "--logs", required=False,help="Logs file name")
    parser.add_argument("-eo", "--eog", required=False,help="Eog channel name")
    parser.add_argument("-ee", "--eeg", required=False,help="Eeg channel name")
    parser.add_argument("-em", "--emg", required=False,help="Emg channel name")
    parser.add_argument("-ar", "--arousal", required=False,action="store_true",help="Activation of arousal analysis")
    args = parser.parse_args()
    return args

def initPaths(mainFile):
    global CURRENT_PATH
    global DEEPSLEEP_PATH
    global DATA_PATH
    global FEATURE_PATH
    global TRAINING_PATH
    global TESTTEST_PATH
    global AA_PATH
    global NONAA_PATH
    
    CURRENT_PATH = os.path.dirname(os.path.realpath(mainFile))

    #For Testpredict.py
    DEEPSLEEP_PATH = os.path.join(CURRENT_PATH, 'DeepSleep')
    DATA_PATH = os.path.join(DEEPSLEEP_PATH, 'dataEDF')
    FEATURE_PATH = os.path.join(DATA_PATH, 'featureEDF_8m')
    TRAINING_PATH=os.path.join(DATA_PATH, 'training')
    TESTTEST_PATH=os.path.join(CURRENT_PATH, 'TestTest')
    AA_PATH=os.path.join(CURRENT_PATH, 'ComparaisonAA\AA')
    NONAA_PATH=os.path.join(CURRENT_PATH, 'ComparaisonAA\POURTEST')
    return

def checkAnonymisation() :
    EDFListRef=glob.glob("*.EDF")
    EDFListNew=glob.glob("New/*.EDF")
    resuListNew=glob.glob("New/*.resu")  
    resuListRef=glob.glob("*.resu") 

    for edfRef in EDFListRef:
        fid = open(edfRef, "rb")
        stringRef = fid.read()    
        fid.close()
        fid = open("New/" + edfRef.upper(), "rb")
        stringNew = fid.read()    
        fid.close()
        if stringRef != stringNew:
            print("diff avec " + edfRef)
    return

