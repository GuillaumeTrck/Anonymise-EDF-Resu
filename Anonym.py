import numpy as np
import os
from utils import printLogs
import glob
import argparse
from utils import *

initLogs("LogsAnonyme.txt")
parser=argparse.ArgumentParser(description='Anomyse/Unanomyse EDF and resu')
parser.add_argument('-f','--file',required=True,help="File with EDF and resu")
parser.add_argument('-a','--anomyse', required=False,action="store_true", help="Anomyse edf and resu")
parser.add_argument('-d','--EDFData', required=False, help="Edf data text name")
parser.add_argument('-v','--resuData', required=False, help="resu data text name")
parser.add_argument('-u','--unAnomyse', required=False,action="store_true", help="Unanomyse edf and resu")

args=parser.parse_args()


anomyse=args.anomyse
unAnomyse=args.unAnomyse
file=args.file
os.chdir(file)

if args.EDFData:
    EDFData=args.EDFData
else:
    try:
        EDFData="EDFDatadefault.txt"
        fid=open(EDFData,'a')
        fid.close()
    except:
        printLogs("Le fichier txt n'a pas été créé")

if args.resuData:
    resuData=args.resuData
else:
    try:
        resuData="resuDataDefault.txt"
        fid=open(resuData,'a')
        fid.close()
    except:
        printLogs("Le fichier txt n'a pas été créé")


#6 unanonymiser edf et resu (nom et données)
def UN():    
    EDFList=glob.glob("RawAnonyme*.EDF")
    resuList=glob.glob("resuAnonyme*.resu")

    try:
        matriceEDF=np.loadtxt(EDFData,delimiter='\t',comments=None,encoding='utf-8',dtype='U',skiprows=1,ndmin=2)
        matriceresu=np.loadtxt(resuData,delimiter='\t',comments=None,encoding='utf-8',dtype='U',skiprows=1,ndmin=2)
    except:
        printLogs("Les matrices EDF et resu ne sont pas chargées")

    
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

def AN():    

    EDFList=glob.glob("*.EDF")
    resuList=glob.glob("*.resu")
    print(resuList)
    print(EDFList)

    test=FirstLineEDF(EDFData)

    try:
        test1=FirstLineresu(resuData)
    except:
        printLogs("Problème chargement resuData")

    if test and test1:
        ID = 1
    else :
        ID = CheckID(EDFData,resuData)

    for resu in resuList:
        var=saveDataresu(resu,resuData,ID)
        if var:
            
            #1. récupérer edfname
            try:
                fid = open(resu, "rb")
            except:
                printLogs("Problème ouverture resu") 

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
                saveDataEDF(RawFileNameStripTerm,EDFData,ID)
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
        sss = "x" * 8 + "##" + "xxxxxxxx" + "##"
        EDF.write(sss)
        EDF.seek(28)
        sss = "010101MX00             "+" "*38 #22 carac en tout 
        EDF.write(sss)
        EDF.seek(88)
        sss="Erasme-ULB-Endymion##C03.56##20##01/01/2001##000##P9&10#202#"
        EDF.write(sss)

        # EDF.seek(122)
        # sss = "01/01/2001" + " "*36
        
        EDF.seek(168)
        sss = "01/01/01"
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
        sss = "01/01/2001"
        resu.write(sss)
        resu.seek(48)                                         
        sss="0000"
        resu.write(sss)
        resu.seek(144)
        sss = "x" * 22
        resu.write(sss)
        resu.seek(1922)
        sss = "010101MX00" + " "*12
        resu.write(sss)
        resu.seek(1944)
        sss = "x" * 54
        resu.write(sss)
        resu.seek(1998)
        sss = "01/01/2001"
        resu.write(sss)
        resu.seek(2008)
        sss = "M" 
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
                                         
def saveDataresu(resuName,resuData,ID):
    x='resuAnonyme'
    try:
        matriceresu=np.loadtxt(resuData,delimiter='\t',comments=None,encoding='utf-8',dtype='U',skiprows=1,ndmin=2)
    except:
        printLogs("Problème chargement matrice resu")

    if x in resuName:
        print("Fichier resu déjà sauvé")
        return False
    else:
    # Writing data
        print("J'ai bien sauvé les données")
        try:
            dataFile = open(resuData, 'a')
        except:
            printLogs("Problème ouverture resuData")

        dataFile.write(resuName) 
        dataFile.write('\t')

        try :
            fid = open(resuName, "rb")
        except:
            printLogs("Problème ouverture resu")

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

def saveDataEDF(RawFileName, EDFData,ID):
    x='xxxxxxxxxxxxxxxxxxxxxx.EDF'
    try:
        matriceEDF=np.loadtxt(EDFData,delimiter='\t',comments=None,encoding='utf-8',dtype='U',skiprows=1,ndmin=2)
    except:
        printLogs("Problème chargement matrice EDF")

    if x in RawFileName:
        print("Fichier EDF déjà sauvé")
        return
    else:
    # Writing data
        try:
            dataFile = open(EDFData, "a")
        except:
            printLogs("Problème ouverture EDFData")
        dataFile.write(RawFileName)
        dataFile.write('\t')
        
        try:
            EDF = open(RawFileName, "rb")
        except:
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

def FirstLineEDF(EDFData):

    try:
        dataFile = open(EDFData, 'rb')
    except:
        printLogs("Problème ouverture fichier EDFData")
    
    ligne1=dataFile.readlines(1)

    # Writting the first line
    if not ligne1:
        try:    
            dataFile = open(EDFData, 'w')
        except:
            printLogs("Problème ouverture fichier EDFData")

        dataFile.write("EDF/EDFHeader/champs identification/Date/ID")
        dataFile.write('\n')
        dataFile.close()

        return True
    else:
        return False 

def FirstLineresu(resuData):

    dataFile = open(resuData, 'rb') 
    ligne2=dataFile.readlines(1)

    # Writting the first line
    if not ligne2:
        dataFile = open(resuData, 'w')
        dataFile.write("resuName/Date/Chambre/EDFName/FileNumber/Name/FirstName/BirthDate/Sex/ID")
        dataFile.write('\n')
        dataFile.close()
        
        return True
    else:
        return False 

def CheckID(EDFData,resuData):

    matriceEDFID=np.loadtxt(EDFData,delimiter='\t',comments=None,encoding='utf-8',skiprows=1,usecols=4,ndmin=2)
    EDFID = int(max(matriceEDFID) +1)

    matriceresuID=np.loadtxt(resuData,delimiter='\t',comments=None,encoding='utf-8',skiprows=1,usecols=9,ndmin=2)
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

if (args.unAnomyse):
    UN()

elif(args.anomyse):
    AN()
