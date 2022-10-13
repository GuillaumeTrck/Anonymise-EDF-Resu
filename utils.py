import argparse
from datetime import datetime

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
    args = parser.parse_args()
    return args