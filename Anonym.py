import numpy as np
import os
from utils import printLogs, initLogs
import glob
import argparse


def UN():  
    #unanonymiser edf et resu (nom et données)  
    EDFList=glob.glob("RawAnonyme*.EDF")
    resuList=glob.glob("resuAnonyme*.resu")
    try:
        matriceEDF=np.loadtxt(EDFDB,delimiter='\t',comments=None,encoding='utf-8',dtype='U',skiprows=1,ndmin=2)
        matriceresu=np.loadtxt(resuDB,delimiter='\t',comments=None,encoding='utf-8',dtype='U',skiprows=1,ndmin=2)
    except Exception as e:
        printLogs("Les matrices EDF et resu ne sont pas chargées : " + str(e))
    for i in range(len(resuList)):
        #1 récupérer ID du fichier
        resuAnonymeName=resuList[i]
        resuAnonymeName=resuAnonymeName.replace(".resu","")
        IDFichierAnonyme=resuAnonymeName[11:]
        #2 voir où se trouve le fichier dans datafile
        posEDF=CheckInDataFile(matriceEDF,IDFichierAnonyme)
        posResu=CheckInDataFile(matriceresu,IDFichierAnonyme)
        #3 changer les noms anonymes et les données des edf et resu
        terminasonEDF='.EDF'
        terminaisonResu='.resu'
        originalEDFName=glob.glob('RawAnonyme'+IDFichierAnonyme+terminasonEDF)
        originalResuName=glob.glob('resuAnonyme'+IDFichierAnonyme+terminaisonResu)
        print(originalEDFName)
        print(originalResuName)
        posEDF=int(posEDF)
        print(posEDF)
        posResu=int(posResu)
        print(posResu)
        originalsNames=ChangeAnonymeToName(originalResuName[0],originalEDFName[0], matriceEDF,matriceresu,posResu, posEDF)
        UnAnonymiseEDF(originalsNames[1],matriceEDF,posEDF)
        UnAnonymiseResu(originalsNames[0],matriceresu,posResu)
        posEDF=int(posEDF)
        posResu=int(posResu)
    return

def AN(EDFDB, resuDB, directory):    
    try:
        bEDF=WriteFirstLine(EDFDB, "EDF/EDFHeader/champs identification/Date/ID\n")
    except:
        printLogs("Problème chargement EDFDB")
        return
    try:
        bResu=WriteFirstLine(resuDB, "resuName/Date/Chambre/EDFName/FileNumber/Name/FirstName/BirthDate/Sex/ID\n")
    except:
        printLogs("Problème chargement resuDB")
        return
    if bResu and bEDF :
        ID = 1
    else :
        ID = CheckID(EDFDB,resuDB)
    EDFList=glob.glob("*.EDF")
    resuList=glob.glob("*.resu")
    for resu in resuList:
        try:
            var=saveDataresu(resu,resuDB,ID)
        except : 
            print("error with saveDataResu")
            return
        if var:
            #1. récupérer edfname
            try:
                fid = open(resu, "rb")
            except:
                printLogs("Problème ouverture resu") 
                return
            fid.seek(144)
            RawFileName= fid.read(22).decode('unicode_escape')
            RawFileNameStrip=RawFileName.replace(" ","")
            fid.close()
            #2. trouver l'edf 
            term='.EDF'
            RawFileNameStripTerm=RawFileNameStrip + term
            EDFName=glob.glob(RawFileNameStripTerm)
            if EDFName:
                #3 savedataedf
                saveDataEDF(RawFileNameStripTerm,EDFDB,ID)
                #4 Anonymise edf et resu (nom et données)
                try:
                    AnonymiseEDF(RawFileNameStripTerm)
                except:
                    printLogs("Problème anonymisation EDF")
                try:
                    AnonymiseResu(resu)
                except:
                    printLogs("Problème anonymisation resu")

                anonymeNames=ChangeNameToAnonyme(resu,RawFileNameStripTerm,ID)
            else : 
                printLogs("Pas de fichier EDF associé à ce resu.")
            #5 incrémenter l'ID
            ID=int(ID)
            ID=ID+1
    return

def AnonymiseEDF(EDFName):                                 
    x='xxxxxxxxxxxxxxxxxxxxxx.EDF'
    if x in EDFName:
        print("Fichier EDF déjà anonyme")
    else:
        EDF = open(EDFName, "r+")
        EDF.seek(8)                                             
        sss = "x" * 168
        EDF.write(sss)
        EDF.close()
    return 

def AnonymiseResu(resuName):                                                                     
    x='resuAnonyme'
    if x in resuName:
        print("Fichier resu déjà anonyme")
    else:
        resu=open(resuName,'r+')
        resu.seek(24)                                           
        sss = "x"*10
        resu.write(sss)
        resu.seek(48)                                         
        sss="x"*4
        resu.write(sss)
        resu.seek(144)
        sss = "x" * 22
        resu.write(sss)
        resu.seek(1922)
        sss = "x" * 87
        resu.write(sss)
        resu.close()
    return      

def UnAnonymiseEDF(EDFName,matriceEDF,a):                    
    try:
        EDF = open(EDFName, "r+")
    except:
        printLogs("Problème ouverture fichier EDF")
    A = [8,88,168]
    for i in range(len(A)):
        EDF.seek(A[i])
        EDF.write(matriceEDF[a][i+1])
    EDF.close()
    return

def UnAnonymiseResu(resuName,matriceresu,a):                  
    try:
        resu=open(resuName,'r+')
    except:
        printLogs("Problème ouverture fichier resu")
    A = [24, 48, 144, 1922, 1944, 1971, 1998, 2008,2009] 
    for i in range(len(A)):
        resu.seek(A[i])
        resu.write(matriceresu[a][i+1])
    resu.close() 
    return
                                         
def saveDataresu(resuName,resuDB,ID):
    matriceresu=np.loadtxt(resuDB,delimiter='\t',comments=None,encoding='utf-8',dtype='U',skiprows=1,ndmin=2)
    if 'resuAnonyme' in resuName:
        print("Fichier resu déjà sauvé")
        return False
    else:
        dataFile = open(resuDB, 'a')
        dataFile.write(resuName) 
        dataFile.write('\t')
        fid = open(resuName, "rb")
        resu = {}
        fid.seek(24)
        resu['ExamDate'] = fid.read(10).decode('unicode_escape')
        dataFile.write(resu['ExamDate'])
        dataFile.write('\t')
        fid.seek(48)
        resu['Room'] = fid.read(4).decode('unicode_escape')  
        dataFile.write(resu['Room'])
        dataFile.write('\t')
        fid.seek(144)
        resu['RawFileName'] = fid.read(22).decode('unicode_escape') 
        dataFile.write(resu['RawFileName'])
        dataFile.write('\t')
        fid.seek(1922)
        resu['FileNumber'] =  fid.read(22).decode('unicode_escape')  
        dataFile.write(resu['FileNumber'])
        dataFile.write('\t')
        resu['Name'] =  fid.read(27).decode('unicode_escape')  
        dataFile.write(resu['Name'])
        dataFile.write('\t')
        resu['FirstName'] =  fid.read(27).decode('unicode_escape')  
        dataFile.write(resu['FirstName']) 
        dataFile.write('\t')
        resu['BirthDate'] =  fid.read(10).decode('unicode_escape')  
        dataFile.write(resu['BirthDate'])
        dataFile.write('\t')
        resu['Sex'] = fid.read(1).decode('unicode_escape')
        dataFile.write(resu['Sex'])
        dataFile.write('\t')
        dataFile.write(str(ID))
        dataFile.write('\n')
        fid.close()
        dataFile.close()
    return True

def saveDataEDF(RawFileName, EDFDB,ID):
    matriceEDF=np.loadtxt(EDFDB,delimiter='\t',comments=None,encoding='utf-8',dtype='U',skiprows=1,ndmin=2)
    if 'xxxxxxxxxxxxxxxxxxxxxx.EDF' in RawFileName:
        print("Fichier EDF déjà sauvé")
        return
    else:
    # Writing datae
        dataFile = open(EDFDB, "a")
        dataFile.write(RawFileName)
        dataFile.write('\t')
        EDF = open(RawFileName, "rb")
        printLogs("Problème ouverture EDF")       
        EDF.read(8)
        EDFText = EDF.read(168).decode('unicode_escape')    
        EDF.close()
        dataFile.write(EDFText[0:80])
        dataFile.write('\t')
        dataFile.write(EDFText[80:160])
        dataFile.write('\t')
        dataFile.write(EDFText[160:168])
        dataFile.write('\t')
        dataFile.write(str(ID))
        dataFile.write('\n')
        dataFile.close()
    return

def WriteFirstLine(DB, Firstline):
    #return -1 if error; 1 if ID must be one and 0 if ID must be identified
    dataFile = open(DB, 'rb')
    line1=dataFile.readlines(1)
    dataFile.close()
    if not line1:    
        dataFile = open(DB, 'w')
        dataFile.write(FirstLine)
        dataFile.close()
        return True
    else:
        return False

def CheckID(EDFDB,resuDB):
    matriceEDFID=np.loadtxt(EDFDB,delimiter='\t',comments=None,encoding='utf-8',skiprows=1,usecols=4,ndmin=2)
    EDFID = int(max(matriceEDFID) +1)
    matriceresuID=np.loadtxt(resuDB,delimiter='\t',comments=None,encoding='utf-8',skiprows=1,usecols=9,ndmin=2)
    resuID = int(max(matriceresuID) +1)
    return max([EDFID,resuID])

def ChangeNameToAnonyme(resuName, rawFileName, ID): 
    
    x='resuAnonyme'
    if x in resuName:
        print("Noms resu déjà anonyme")
        return
    else:
        resuAnonymeFileName="resuAnonyme{0}.resu".format(ID)                      
        os.rename(resuName,resuAnonymeFileName)   
        rawAnonymeFileName = "RawAnonyme{0}.EDF".format(ID)               
        os.rename(rawFileName,rawAnonymeFileName)
        print("J'ai bien changé le nom")
    return [resuAnonymeFileName,rawAnonymeFileName]

def ChangeAnonymeToName(resuAnonyme,rawAnonyme, matriceEDF,matriceresu,iResu,iEDF) :
    resuFileName=matriceresu[iResu][0]
    os.rename(resuAnonyme,resuFileName)
    EDFFileName=matriceEDF[iEDF][0]
    os.rename(rawAnonyme,EDFFileName)

    return [resuFileName,EDFFileName] 

def CheckInDataFile(matriceData,IDFichierAnonyme):
    i=np.where(matriceData==IDFichierAnonyme)
    #print("i= {}".format(i))
    return i[0]

if __name__ == '__main__':
    initLogs("LogsAnonyme.txt")
    parser=argparse.ArgumentParser(description='Anomyse/Unanomyse EDF and resu')
    parser.add_argument('-d','--dir',required=True,help="Directory containing EDF and resu files")
    parser.add_argument('-a','--anonym', required=False,action="store_true", help="Anonymise edf and resu")
    parser.add_argument('-e','--EDFDB', required=False, help="Edf data text name")
    parser.add_argument('-r','--resuDB', required=False, help="resu data text name")
    parser.add_argument('-u','--unanonym', required=False,action="store_true", help="Unanonymise edf and resu")
    args=parser.parse_args()
    os.chdir(args.dirfile) #TODO Try to avoid this

    if args.EDFDB:
        EDFDB=args.EDFDB
    else:
        try:
            EDFDB="EDFDatadefault.txt"
            fid=open(EDFDB,'a')
            fid.close()
        except:
            printLogs("Le fichier txt n'a pas été créé")
    if args.resuDB:
        resuDB=args.resuDB
    else:
        try:
            resuDB="resuDataDefault.txt"
            fid=open(resuDB,'a')
            fid.close()
        except:
            printLogs("Le fichier txt n'a pas été créé")
    if (args.unanonym):
        UN(EDFDB, resuDB, args.dir)
    elif(args.anonym):
        AN(EDFDB, resuDB, args.dir)
