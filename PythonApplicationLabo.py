from os import read
import mne
import numpy as np
import matplotlib.pyplot as plt
from Anonym import *
import glob
import argparse

parser=argparse.ArgumentParser(description='Save Data EDF and resu')
parser.add_argument('-a','--anomyse', required=False, help="File name with EDF and resu")
parser.add_argument('-d','--EDFData', required=True, help="Edf data text name")
parser.add_argument('-v','--resuData', required=True, help="resu data text name")
parser.add_argument('-u','--unAnomyse', required=False, help="File name with EDF and resu anomyse")

args=parser.parse_args()


file=args.anomyse
fileA=args.unAnomyse
EDFData=args.EDFData
resuData=args.resuData


#6 unanonymiser edf et resu (nom et données)
def UN():    
    os.chdir(fileA)
    EDFList=glob.glob("*.EDF")
    resuList=glob.glob("*.resu")

    matriceEDF=np.loadtxt(EDFData,delimiter='\t',comments=None,encoding='utf-8',dtype='U',skiprows=1,ndmin=2)
    matriceresu=np.loadtxt(resuData,delimiter='\t',comments=None,encoding='utf-8',dtype='U',skiprows=1,ndmin=2)
    i=0
    for id in EDFList:

        #1 récupérer ID du fichier
        
        
        EDFAnonymeName=EDFList[i]
        EDFAnonymeName=EDFAnonymeName.replace(".EDF","")
        IDFichierAnonyme=EDFAnonymeName[10:]
        #2 voir où se trouve le fichier dans datafile
        i=CheckInDataFile(matriceEDF,IDFichierAnonyme)
        
        
        #3 changer les noms anonymes et les données des edf et resu
        terminasonEDF='.EDF'
        terminaisonResu='.resu'
        originalEDFName=glob.glob('RawAnonyme'+IDFichierAnonyme+terminasonEDF)
        originalResuName=glob.glob('resuAnonyme'+IDFichierAnonyme+terminaisonResu)
        print(originalEDFName)
        print(originalResuName)
        i=int(i)
        originalsNames=ChangeAnonymeToName(originalResuName[0],originalEDFName[0], matriceEDF,matriceresu,i)
        UnAnonymiseEDF(originalsNames[1],matriceEDF)
        UnAnonymiseResu(originalsNames[0],matriceresu)
        i=int(i)
        print(type(i))
        i=i+1
        print(i)
    return

def AN():    
    os.chdir(file)

    EDFList=glob.glob("*.EDF")
    resuList=glob.glob("*.resu")
    print(type(resuList))
    print(resuList)
    print(EDFList)

    test=FirstLineEDF(EDFData)
    test1=FirstLineresu(resuData)
    if test and test1:
        ID = 1
    else :
        ID = CheckID()

    for resu in resuList:
        saveDataresu(resu,resuData,ID)
        
        #1. récupérer edfname
        fid = open(resu, "rb")                                                   
        fid.seek(144)
        RawFileName= fid.read(22).decode('unicode_escape')
        RawFileNameStrip=RawFileName.replace(" ","")
        fid.close()
        
        #2. trouver l'edf 
        term='.EDF'
        RawFileNameStripTerm=RawFileNameStrip + term
        EDFName=glob.glob(RawFileNameStripTerm)
        print(EDFName)
        #3 savedataedf
        saveDataEDF(RawFileNameStripTerm,EDFData,ID)

        #4 Anonymise edf et resu (nom et données)
        AnonymiseEDF(RawFileNameStripTerm)
        AnonymiseResu(resu)
        anonymeNames=ChangeNameToAnonyme(resu,RawFileNameStripTerm,ID)

        #5 incrémenter l'ID
        ID=int(ID)
        ID=ID+1
    return

if (args.unAnomyse):
    UN()

elif(args.anomyse):
    AN()

















 






