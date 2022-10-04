from os import read
import mne
import numpy as np
import matplotlib.pyplot as plt
from Anonym import *

def readEDF(EDFName):               #fonction permettant de lire les fichier EDF, le fichier doit se trouver dans le dossier du programme 
    ErasmeToMneEdf(EDFName)
    raw = mne.io.read_raw_edf(EDFName, preload=True)
    print(raw)
    print('Chan =', raw.ch_names)   #Ligne qui renvoit le nom de tous les EEG
    print('Sampling frequency =', raw.info['sfreq'])
    print('Data shape (channels, times) =', raw._data.shape)
    print(raw.info)
    #raw.pick_types(eeg=True, eog=False)
    raw.pick(raw.ch_names[5])                 #fonctionne
                  
    print('Chan =', raw.ch_names)
    #raw.plot(start=30, duration=10,scalings=dict(eeg=1e-4,resp=1e3,eog=1e-4,emg=1e-7,misc=1e-1))
    raw.plot(duration=30, start=10, n_channels=1, block=True,title='test') #affiche le graph des diff�rents capteurs
    MneToErasmeEdf(EDFName)
    return raw
def ErasmeToMneEdf(EDFName):        #fonction permettant de changer dans le format des caract�re par des points : format historique de erasme
    fid = open(EDFName, "r+")       #r pour (lecture) et + pour �crire dedans 
    fid.seek(170)                   #seek = chercher 
    fid.write(".")
    fid.seek(173)
    fid.write(".")
    fid.seek(178)
    fid.write(".")
    fid.seek(181)
    fid.write(".")
    fid.close()
    return
def MneToErasmeEdf(EDFName):        #fonction permettant de changer dans le format des caract�re par des points : format historique de erasme
    fid = open(EDFName, "r+")
    fid.seek(170)
    fid.write("/")
    fid.seek(173)
    fid.write("/")
    fid.seek(178)
    fid.write(":")
    fid.seek(181)
    fid.write(":")
    fid.close()
def readEDFHeader(EDFName):         #fonction permettant de lire l'ent�te (Header) ce qui donne les info sur le patient,...
    ErasmeToMneEdf(EDFName)
    EDF = open(EDFName, "rb")
    header = {}
    header['version'] = EDF.read(8).decode('unicode_escape')
    header['patient'] = EDF.read(80).decode('unicode_escape')
    header['recording'] = EDF.read(80).decode('unicode_escape')
    header['startDate'] = EDF.read(16).decode('unicode_escape')
    header['headerSize'] = int(EDF.read(8).decode('unicode_escape'))
    header['reserved'] = EDF.read(44).decode('unicode_escape')
    header['recordsNumber'] = int(EDF.read(8).decode('unicode_escape'))
    header['recordDuration'] = int(EDF.read(8).decode('unicode_escape'))
    header['signalsNumber'] = int(EDF.read(4).decode('unicode_escape'))
    header['labels'] = list(chunkPrint(EDF.read(header['signalsNumber']*16).decode('unicode_escape'), 16))
    header['transducers'] = list(chunkPrint(EDF.read(header['signalsNumber']*80).decode('unicode_escape'), 80))
    header['physDim'] = EDF.read(header['signalsNumber']*8).decode('unicode_escape')
    header['physMin'] = list(chunkPrint(EDF.read(header['signalsNumber']*8).decode('unicode_escape'), 8))
    header['physMin'] = np.array(header['physMin'], dtype=np.float32)
    header['physMax'] = list(chunkPrint(EDF.read(header['signalsNumber']*8).decode('unicode_escape'), 8))
    header['physMax'] = np.array(header['physMax'], dtype=np.float32)
    header['digMin'] = list(chunkPrint(EDF.read(header['signalsNumber']*8).decode('unicode_escape'), 8))
    header['digMin'] = np.array(header['digMin'], dtype=np.float32)
    header['digMax'] = list(chunkPrint(EDF.read(header['signalsNumber']*8).decode('unicode_escape'), 8))
    header['digMax'] = np.array(header['digMax'], dtype=np.float32)
    header['prefiltering'] = list(chunkPrint(EDF.read(header['signalsNumber']*80).decode('unicode_escape'), 80))
    header['samplesNumber'] = list(chunkPrint(EDF.read(header['signalsNumber']*8).decode('unicode_escape'), 8))
    header['reserved2'] = list(chunkPrint(EDF.read(header['signalsNumber']*32).decode('unicode_escape'), 32))
    EDF.close() 
    EDF = open(EDFName, "rb")
    header['fullHeader'] = EDF.read(header['headerSize']).decode('unicode_escape')
    EDF.close()
    print(header)
    return header       
def chunkPrint(string, length):     #fonction permettant de s�parer les labels et les mettre dans une liste
    return (string[0+i:length+i].strip() for i in range(0, len(string), length))


#readEDFHeader("PX428090.EDF")
#saveData("PERSONX0-20220928.resu","PX428090.EDF","Anonym")
#AnonymiseEDF("PX428090.EDF")
#AnonymiseResu("PERSONX0-20220928.resu")                             #REMARQUE : la date n'est pas anonymis�e dans le fichier resu
#ChangeNameToAnonyme("PERSONX0-20220928.resu","PX428090.EDF")
#UnAnonymiseEDF("RawAnonyme.EDF","Anonym.txt")
ChangeAnonymeToName("Anonym.txt")
