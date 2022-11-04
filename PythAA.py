OUTDATED_IGNORE=1
import mne
#import yasa
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#from sklearn.metrics import confusion_matrix
#from yasa.hypno import hypno_str_to_int_Erasme, hypno_upsample_to_data
from edf import *
from resu import *
import sys
import os
from datetime import datetime
from utils import * 
from Testuniform import uniformEDF
from Testpredict import predictEDF
import utils as u
from sklearn import metrics
#from sklearn.metrics import f1_score
from sklearn.metrics import *
#from Testpredict import predictEDF
    
def AA(args):
    # 1.Reading header
    try :
        header = readEDFHeader(args.edf)  
    except Exception as e: 
        printLogs("Error with readEDFHeader() : " + str(e)+ "\nEnd of the procedure.")
        return
    else :
        printLogs("readEDFHeader() ok")
    # 2.Reading EDF
    if header['version'] == '0       ' : # Regular EDF
        printLogs("Version 0. No Decompression needed")
        try :
            raw = readEDF(args.edf)
        except Exception as e: 
            printLogs("Error with regular readEDF() : " + str(e) + "\nEnd of the procedure.")
            return
        else :
             printLogs("readEDF() ok")
    elif header['version'] == '0-1     ' : # Compressed EDF
        printLogs("Decompression is needed")
        newEDFName = os.path.dirname(args.edf) + '\\x' + os.path.basename(args.edf)
        print(newEDFName)
        try:
            unzipEDF(args.edf, newEDFName, header)
        except Exception as e:
            printLogs("Error with unzipEDF() : " + str(e) +"\nEnd of the procedure.")
        else:
            printLogs("unzipEDF() ok")
        try: 
            raw = readEDF(newEDFName)
        except Exception as e:
            printLogs("Error with unzipped readEDF(): " + str(e) + "\nEnd of the procedure.")
            return 
        else: 
            printLogs("readEDF() ok")  
        
        try :
            os.remove(newEDFName)
        except Exception as e: 
           printLogs("Error while removing " + newEDFName + " : " + str(e) + "\nBut the procedure goes on")
        else: 
           printLogs(newEDFName + " has been removed")    
    else : 
        printLogs("Unknown version format. End of the procedure") 
        return
    # 3.Reading resu
    try:
        print(args.resu)
        resu = readResu(args.resu)    
    except Exception as e: 
        printLogs("Error with readResu(): " + str(e) + "\nEnd of the procedure")
    else: 
        printLogs("readResu() ok")

    # 4.Selecting channels stages
    if (args.stages):
        StageAA=StagesAnalysis(resu,raw,header)
    #select chanels for arousals analysis
    elif(args.arousal):
        ArousalAA=ArousalAnalysis(resu,raw,header)
     

def StagesAnalysis(resu,raw,header):
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
    except Exception as e:
        printLogs("Erreur durant l'analyse par yasa : " + str(e) + "\nEnd of the procedure.") 
        return
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

def ArousalAnalysis(resu,raw,header):
        print(header['labels'])
        print(resu['Events'])
        #Uniform
        

        chanels=[]
        if 'EEG F4' and 'EEG C4' and 'EEG O2' and 'EOG Droit' and 'EMG menton'and 'Amp Abd'and 'Amp Thx'and 'Flux Nas'and 'Sao2'and 'ECG' and 'Frq.car.' and 'EMG jamb.1' and 'EMG jamb.2' in header['labels']:
            chanels=('EEG F4','EEG C4','EEG O2','EOG Droit','EMG menton','Amp Abd','Amp Thx','Flux Nas','Sao2','ECG','Frq.car.','EMG jamb.1','EMG jamb.2')
            printLogs("All chanels for arousal analysis selected")
            # print (chanels[0:])
        else : 
            printLogs("Prob chanels for arousal analysis")
        
        # if 'EEG F4' and 'EEG C4' and 'EEG O2' in header['labels']:
        #      chanels=('EEG F4','Amp Abd','ECG','Flux Nas','EMG menton')
        raw.pick_channels(chanels)
        #printEDFGraph(raw)
        info = raw.info
        #print(info)
        print(info['ch_names'])
        new_raw=raw.get_data()
        print("info raw" +str(new_raw.shape))
        #uniform = uniformEDF(new_raw) 
        #print(a.shape)

        #Predict
        #b= predictEDF(uniform,args.edf,new_raw)

        
        #comparaison
        label=np.loadtxt("resu.vec", dtype=int)
        print("labelshape"+str(label.shape))
        prediction=np.loadtxt(os.path.join(u.NONAA_PATH,'BR515010.EDF.vec'),dtype=float)
        print("predictionshape"+str(prediction.shape))
        auc = metrics.roc_auc_score(label,prediction)
        print(auc)
        fpr, tpr, _ = metrics.roc_curve(label,prediction)
        plt.plot(fpr, tpr)
        plt.ylabel('True Positive Rate')
        plt.xlabel('False Positive Rate')
        plt.show()


        #Trouver les vraies micro-éveils
        recordsNumber=(header['recordsNumber'])
        recordDuration=(header['recordDuration'])
        Events=(resu['Events'])
        eventSeven=filter(lambda event : event.type ==7, Events)
        TrueMicroEveil=filter(lambda event : event.sous_type == 1, eventSeven)
        

        abcd=F1ScoreBetweenResuAndAA(recordsNumber,recordDuration,TrueMicroEveil)
        matricescoreuse=abcd[1]
        matriceAA=abcd[2]
        ReadFalseResu=abcd[3]
        ResuAAName=abcd[4]
        print(matriceAA.shape)
        print(matriceAA)
        
        # bbbb=F1ScoreBetweenResuAndDeepsleep(matricescoreuse,prediction)
        # print(bbbb)
        matriceDeepSleep=predictionToVecWithThreshold(prediction)


        New_matriceDeepSleep=assambleArousals(matriceDeepSleep)
        New_matriceDeepSleep=selectGoodArousals(New_matriceDeepSleep)
        
        listeMEDeepSleep=New_matriceDeepSleep[1]
        print(listeMEDeepSleep)
        
        
        
        #Check la taille du fichier resu
        print(f'File Size in Bytes is {file_stats.st_size}')
        print(type(ReadFalseResu))


        #check le nb d'event header
        print("voici le nb events ds header")
        fid=open('BOUNRED0-20220115.resu','rb')
        resu = {}
        fid.seek(60)
        resu['pEvents'] = fid.read(6)
        fid.seek(66)
        resu['EventsNumber'] = fid.read(6)
        fid.close()

        print(resu['pEvents'])
        print(resu['EventsNumber'])

        #delete ME AA and add ME Deepsleep
        delMEAA=transposeVecToResu(ReadFalseResu,listeMEDeepSleep)

        #Change valeur dans header
        ReadFalseResu['EventsNumber']=1
        print(ReadFalseResu['EventsNumber'])

        #saveResu
        veriff=saveResu(ReadFalseResu,'BOUNRED0-20220115.resu')


        #verif si nouvel event dans le header
        print("voici le nb events ds header")
        fid=open('BOUNRED0-20220115.resu','rb')
        ReadFalseResu = {}
        fid.seek(60)
        ReadFalseResu['pEvents'] = fid.read(6)
        fid.seek(66)
        ReadFalseResu['EventsNumber'] = fid.read(6)
        fid.close()

        print(ReadFalseResu['pEvents'])
        print(ReadFalseResu['EventsNumber'])

        #Check la taille du fichier resu
        file_stats = os.stat('BOUNRED0-20220115.resu')
        print(f'File Size in Bytes is {file_stats.st_size}')
        
        
        # plt.plot(label)
        # plt.show()

        # plt.plot(prediction)
        # plt.show()

        # auc = metrics.roc_auc_score(label,prediction)
        # print(auc)
        # fpr, tpr, _ = metrics.roc_curve(label,prediction)
        # plt.plot(fpr, tpr)
        # plt.ylabel('True Positive Rate')
        # plt.xlabel('False Positive Rate')
        # plt.show()


        return
            
def F1ScoreBetweenResuAndAA(recordsNumber,recordDuration,TrueMicroEveil):
    #1 trouver les fichiers
    TrueResu = os.path.join(u.NONAA_PATH+'\BOUNRED0-20220115.resu') #peut changer ca en mettant resu en args
    FalseResu = os.path.join(u.AA_PATH +'\BOUNRED0-20220115.resu')
    print(TrueResu)
    print(FalseResu)

    ReadFalseResu=readResu(FalseResu)
    AAEvents=(ReadFalseResu['Events'])
    AAeventSeven=filter(lambda event : event.type ==7, AAEvents)
    AAMicroEveil=filter(lambda event : event.sous_type == 1, AAeventSeven)

    #2 transformer les donnees en 0 et 1
    matricescoreuse=resuToVec(TrueResu,recordsNumber,recordDuration,TrueMicroEveil)
    print(str(len(matricescoreuse)))
    matriceAA=resuToVec(FalseResu,recordsNumber,recordDuration,AAMicroEveil)
    print("AAscore"+str(len(matriceAA)))

    #3 calculer f1score
    comparaison=f1_score(matricescoreuse,matriceAA)
    print(comparaison)
    #4plot
    plt.plot(matricescoreuse)
    plt.show()

    plt.plot(matriceAA)
    plt.show()
    return comparaison,matricescoreuse,matriceAA,ReadFalseResu,FalseResu

def F1ScoreBetweenResuAndDeepsleep(matricescoreuse,prediction):
    label=matricescoreuse
    print(type(label))
    print("shape label"+str(label.shape))
    #prediction = np.loadtxt(prediction,delimiter='\t',comments=None,encoding='utf-8',ndmin=1)
    print(type(prediction))
    print("shape predict"+str(prediction.shape))
    precision, recall, thresholds =metrics.precision_recall_curve(label,prediction)
    f1_scores = 2*recall*precision/(recall+precision)
    print(f1_scores)
    print('Best threshold: ', thresholds[np.argmax(f1_scores)])
    print('Best F1-Score: ', np.max(f1_scores))
    plt.plot(precision, recall)
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.show()
    return f1_score

def predictionToVecWithThreshold(prediction):

    print("predictionnnnnnn"+str(prediction))
    prediction[prediction<0.001]=0
    prediction[prediction>0.001]=1
    prediction=prediction.astype(int)
    # i=0
    # for points in prediction:
    #     if points<0.001:
    #         prediction[i]=0
    #         i+1
    #     elif points>0.001:
    #         prediction[i]=1
    #         i+1
    print("predictionnnnnnn"+str(prediction))
    # vec = open('Test.vec','w')
    # for item in prediction:
    #     vec.write('%d' % item)
    #     vec.write('\n')
    # vec.close()    
    return prediction



args = parseArguments()
initPaths(__file__)
initLogs(args.logs)
printLogs("AA - EDFName = " + args.edf + ", ResuName = " + args.resu +"\n")
BB=AA(args)
if (args.stages):
    AA(args)
elif(args.arousal):
    AA(args)