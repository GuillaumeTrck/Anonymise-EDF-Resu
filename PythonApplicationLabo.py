from os import read
import mne
import numpy as np
import matplotlib.pyplot as plt
from Anonym import *
import glob
import argparse


parser=argparse.ArgumentParser(description='Save Data EDF and resu')
parser.add_argument('-f','--file', required=True, help="File name with EDF and resu")
parser.add_argument('-d','--EDFData', required=False, help="Edf data text name")
parser.add_argument('-v','--resuData', required=False, help="resu data text name")
args=parser.parse_args()


file=args.file
EDFData=args.EDFData
resuData=args.resuData

os.chdir(file)

files=glob.glob("*.EDF")
resuList=glob.glob("*.resu")
print(type(resuList))
print(resuList)

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

    #5 unanonymiser edf et resu (nom et données)
    matriceEDF=np.loadtxt(EDFData,delimiter='\t',comments=None,encoding='utf-8',dtype='U',skiprows=1,ndmin=2)
    matriceresu=np.loadtxt(resuData,delimiter='\t',comments=None,encoding='utf-8',dtype='U',skiprows=1,ndmin=2)
    terminasonEDF='.EDF'
    terminaisonResu='.resu'
    ID=str(ID)
    originalEDFName=glob.glob('RawAnonyme'+ID+terminasonEDF)
    originalResuName=glob.glob('resuAnonyme'+ID+terminaisonResu)
    ID=int(ID)
    originalsNames=ChangeAnonymeToName(originalResuName[0],originalEDFName[0], matriceEDF,matriceresu,ID)
    UnAnonymiseEDF(originalsNames[1],matriceEDF)
    UnAnonymiseResu(originalsNames[0],matriceresu)
    

    #6 incrémenter l'ID
    ID=ID+1
    










 






