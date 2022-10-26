import numpy as np
import os
from utils import printLogs, initLogs
import glob
import argparse


def UN():  
    #unanonymiser edf et resu (nom et données)  
    try:
        matriceEDF=np.loadtxt(EDFDB,delimiter='\t',comments=None,encoding='utf-8',dtype='U',skiprows=1,ndmin=2)
        matriceresu=np.loadtxt(resuDB,delimiter='\t',comments=None,encoding='utf-8',dtype='U',skiprows=1,ndmin=2)
    except Exception as e:
        printLogs("Error with EDF or resu loading in UN() : " + str(e) + "\n End of the procedure")
        return
    EDFList=glob.glob("RawAnonyme*.EDF")
    resuList=glob.glob("resuAnonyme*.resu")
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
        originalsNames=ChangeAnonymeToName(originalResuName[0],originalEDFName[0], matriceEDF,matriceresu,posResu, posEDF)
        try:
            UnAnonymiseEDF(originalsNames[1],matriceEDF,posEDF)
            UnAnonymiseResu(originalsNames[0],matriceresu,posResu)
        except Exception as e : 
            print("error with unanonymiseEdf/Resu() : " + str(e) + "\n End of the procedure")
    return

def AN(EDFDB, resuDB, directory):    
    try:
        bEDF=WriteFirstLine(EDFDB, "EDF/EDFHeader/champs identification/Date/ID\n")
    except Eception as e:
        printLogs("Error with WriteFirstLine(EDFDB) :" + str(e) + "\n End of the procedure")
        return
    try:
        bResu=WriteFirstLine(resuDB, "resuName/Date/Chambre/EDFName/FileNumber/Name/FirstName/BirthDate/Sex/ID\n")
    except Exception as e:
        printLogs("Error with WriteFirstLine(resuDB) :" + str(e) + "\n End of the procedure")
        return
    if bResu and bEDF :
        ID = 1
    else :
        try:
            ID = CheckID(EDFDB,resuDB)
        except Exception as e :
            printLogs("Error with CheckID :" + str(e) + "\n End of the procedure")
            return
    EDFList=glob.glob(os.path.join(directory, "*.EDF"))
    resuList=glob.glob(os.path.join(directory, "*.resu"))
    for resu in resuList:
        try:
            RawFileName=saveDataresu(resu,resuDB,ID)
        except Exception as e: 
            printLogs("Error with saveDataresu() :" + str(e) + "\n End of the procedure")
            return
        try:
            AnonymiseResu(resu)
        except:
            printLogs("Error with AnonymiseResu() :" + str(e) + "\n End of the procedure")
            return
        ChangeNameToAnonyme(resu,ID, 'resu')    
        if RawFileName:
            #1. récupérer edfname
            RawFileName=RawFileName.replace(" ","")
            #2. trouver l'edf 
            RawFileName=RawFileName + '.EDF'
            if glob.glob(RawFileName):
                #3 savedataedf
                try :
                    bOK=saveDataEDF(RawFileNameStripTerm,EDFDB,ID) # if false : already saved
                except Exception as e:
                    printLogs("Error with saveDataEDF() :" + str(e) + "\n End of the procedure")
                    return
                #4 Anonymise edf et resu (nom et données)
                if bOK:
                    try:
                        AnonymiseEDF(RawFileNameStripTerm)
                    except:
                        printLogs("Error with AnonymiseEDF() :" + str(e) + "\n End of the procedure")
                        return
                    ChangeNameToAnonyme(RawFileName,ID, 'edf')
            else : 
                printLogs("No EDF file with this resu.")
            #5 incrémenter l'ID
            ID=int(ID)
            ID=ID+1
    return

def AnonymiseEDF(EDFName):                                 
    EDF = open(EDFName, "r+")
    EDF.seek(8)                                             
    sss = "x" * 168
    EDF.write(sss)
    EDF.close()
    return 

def AnonymiseResu(resuName):                                                                     
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
    return resu['RawFileName']

def saveDataEDF(RawFileName, EDFDB,ID):
    matriceEDF=np.loadtxt(EDFDB,delimiter='\t',comments=None,encoding='utf-8',dtype='U',skiprows=1,ndmin=2)
    if 'xxxxxxxxxxxxxxxxxxxxxx.EDF' in RawFileName:
        print("Fichier EDF déjà sauvé")
        return False
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
    return True

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

def ChangeNameToAnonyme(Name, ID, type):
    if type == 'resu':
        NewName="resuAnonyme{0}.resu".format(ID)          
    elif type== 'edf':
        NewName="RawAnonyme{0}.resu".format(ID)     
    else : 
        return False
    os.rename(Name, NewName)
    return True

def ChangeAnonymeToName(resuAnonyme,rawAnonyme, matriceEDF,matriceresu,iResu,iEDF) :
    resuFileName=matriceresu[iResu][0]
    os.rename(resuAnonyme,resuFileName)
    EDFFileName=matriceEDF[iEDF][0]
    os.rename(rawAnonyme,EDFFileName)
    return [resuFileName,EDFFileName] 

def CheckInDataFile(matriceData,IDFichierAnonyme):
    i=np.where(matriceData==IDFichierAnonyme)
    return int(i[0])

if __name__ == '__main__':
    initLogs("LogsAnonyme.txt")
    parser=argparse.ArgumentParser(description='Anomyse/Unanomyse EDF and resu')
    parser.add_argument('-d','--dir',required=True,help="Directory containing EDF and resu files")
    parser.add_argument('-a','--anonym', required=False,action="store_true", help="Anonymise edf and resu")
    parser.add_argument('-e','--EDFDB', required=False, help="Edf data text name")
    parser.add_argument('-r','--resuDB', required=False, help="resu data text name")
    parser.add_argument('-u','--unanonym', required=False,action="store_true", help="Unanonymise edf and resu")
    args=parser.parse_args()

    if args.EDFDB:
        EDFDB=args.EDFDB
    else:
        try:
            EDFDB="EDFDatadefault.txt"
            fid=open(EDFDB,'a')
            fid.close()
        except Exception as e:
            printLogs("Error with EDFDatadefault.txt creation : " + str(e) + "\n End f the procedure")
            exit()
    if args.resuDB:
        resuDB=args.resuDB
    else:
        try:
            resuDB="resuDataDefault.txt"
            fid=open(resuDB,'a')
            fid.close()
        except Exception as e:
            printLogs("Error with resuDatadefault.txt creation : " + str(e) + "\n End f the procedure")
    if (args.unanonym):
        UN(EDFDB, resuDB, args.dir)
    elif(args.anonym):
        AN(EDFDB, resuDB, args.dir)
