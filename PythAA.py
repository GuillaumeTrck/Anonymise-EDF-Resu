OUTDATED_IGNORE=1
import mne
#import yasa
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
#from yasa.hypno import hypno_str_to_int_Erasme, hypno_upsample_to_data
from edf import *
from resu import *
import sys
import os
from datetime import datetime
from utils import *
from Testuniform import uniformEDF
#from Testpredict import predictEDF
    
def AA(args):
    # 1.Reading header
    try :
        header = readEDFHeader(args.edf)  
    except : 
        printLogs("Error with readEDFHeader(). End of the procedure.")
        return
    else :
        printLogs("readEDFHeader() ok")
    # 2.Reading EDF
    if header['version'] == '0       ' : # Regular EDF
        printLogs("Version 0. No Decompression needed")
        try :
            raw = readEDF(args.edf)
        except : 
            printLogs("Error with readEDF(). End of the procedure.")
            return
        else :
             printLogs("readEDF() ok")
    elif header['version'] == '0-1     ' : # Compressed EDF
        printLogs("Decompression is needed")
        newEDFName = os.path.dirname(args.edf) + '\\x' + os.path.basename(args.edf)
        print(newEDFName)
        unzipEDF(args.edf, newEDFName, header)
        printLogs("Error with unzipEDF(). End of the procedure.")
        printLogs("unzipEDF() ok")
        try: 
            raw = readEDF(newEDFName)
        except:
            printLogs("Error with readEDF(). End of the procedure.")
            return 
        else: 
            printLogs("readEDF() ok")  
        
        #try :
            #os.remove(newEDFName)
        #except: 
         #   printLogs("Error while removing " + newEDFName+". But the procedure goes on")
        #else: 
         #   printLogs(newEDFName + " has been removed")    
    else : 
        printLogs("Unknown version format. End of the procedure") 
        return
    # 3.Reading resu
    try:
        resu = readResu(args.resu)    
    except: 
        printLogs("Error with readResu(). End of the procedure")
    else: 
        printLogs("readResu() ok")

    # 4.Selecting channels stages
    if (args.stages):
        def StagesAnalysis(resu,raw):
            if 'EEG C4'in header['labels']:
                printLogs("EEG C4 selected")
                EEGChan = 'EEG C4' 
            elif 'EEG F4' in header['labels']: 
                printLogs("EEG F4 selected ") 
                EEGChan = 'EEG F4'      
            elif 'EEG O2' in header['labels']: 
                printLogs("EEG O2 selected") 
                EEGChan = 'EEG O2'
            elif 'EEG Cz'in header['labels']:
                printLogs("EEG Cz selected")
                EEGChan = 'EEG Cz' 
            elif 'EEG Fz' in header['labels']:  
                printLogs("EEG Fz selected")
                EEGChan = 'EEG Fz'      
            elif 'EEG Oz' in header['labels']:  
                printLogs("EEG Oz selected")
                EEGChan = 'EEG Oz'
            else : 
                printLogs("EEG not selected. end of the procedure ")
                return
            if 'EOG Droit'in header['labels']:
                printLogs("EOG Droit selected")
                EOGChan = 'EOG Droit' 
            elif 'EOG Gauche' in header['labels']:  
                printLogs("EOG Gauche selected")
                EOGChan = 'EOG Gauche'      
            else : 
                printLogs("EOG not selected")
                EOGChan =None
            if 'EMG menton'in header['labels']:
                printLogs("EMG menton selected")
                EMGChan = 'EMG menton'    
            else : 
                printLogs("MG not selected")
                EMGChan = None
            raw.pick_channels([EEGChan, EMGChan, EOGChan])

            # 4.Preprocessing
            raw.resample(100) # Downsample the data to 100 Hz
            raw.filter(0.1, 40) # Apply a bandpass filter from 0.1 to 40 Hz
            # 5. Sleep staging
            try : 
                sls = yasa.SleepStaging(raw, eeg_name=EEGChan, eog_name=EOGChan, emg_name=EMGChan)
                y_pred = sls.predict()
            except :
                printLogs("Erreur durant l'analyse par yasa") 
            else : 
                printLogs("AA terminée. Il reste à sauvegarder le fichier résumé")
            confidence = sls.predict_proba().max(1)
            # 6. Formatting data and saving resu
            resu['stages'] = hypno_str_to_int_Erasme(y_pred)
            while len(resu['stages']) < resu['epochsNumber']:
                resu['stages']=np.append(resu['stages'], 0)
            while len(resu['stages']) > resu['epochsNumber']:
                resu['stages'] = resu['stages'][:-1]
            saveResu(resu, args.resu)
            return
        StageAA=StagesAnalysis(resu,raw)
    #select chanels for arousals analysis
    elif(args.arousal):
        def ArousalAnalysis(raw):

            #Uniform 
            chanels=[]
            if 'EEG F4' and 'EEG C4' and 'EEG O2' and 'EOG Droit' and 'EMG menton'and 'Amp Abd'and 'Amp Thx'and 'Flux Nas'and 'Sao2'and 'ECG' in header['labels']:
                chanels=('EEG F4','EEG C4','EEG O2','EOG Droit','EMG menton','Amp Abd','Amp Thx','Flux Nas','Sao2','ECG')
                printLogs("All chanels for arousal analysis selected")
                print (chanels[0:])
            else : 
                printLogs("Prob chanels for arousal analysis")
            
            raw.pick_channels(chanels)
            info = raw.info
            print(info)
            print(info['ch_names'])
            new_raw=raw.get_data()
            print("info raw" +str(new_raw.shape))
            a = uniformEDF(new_raw)
            print(a.shape)

            #Predict
            




            return
        ArousalAA=ArousalAnalysis(raw)

         
args = parseArguments()
initPaths(__file__)
initLogs(args.logs)
printLogs("AA - EDFName = " + args.edf + ", ResuName = " + args.resu +"\n")
if (args.stages):
    AA(args)
elif(args.arousal):
    AA(args)