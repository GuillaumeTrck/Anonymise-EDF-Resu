import numpy as np
import os
from utils import printLogs, initLogs
import glob
import argparse


def UN(EDFDB, resuDB, directory):  
    #unanonymiser edf et resu (nom et données)  
    try:
        matriceEDF=np.loadtxt(EDFDB,delimiter='\t',comments=None,encoding='utf-8',dtype='U',skiprows=1,ndmin=2)
        matriceresu=np.loadtxt(resuDB,delimiter='\t',comments=None,encoding='utf-8',dtype='U',skiprows=1,ndmin=2)
    except Exception as e:
        printLogs("Error with EDF or resu loading in UN() : " + str(e) + "\n End of the procedure")
        return
    EDFList=glob.glob(os.path.join(directory, "RawAnonyme*.EDF"))
    resuList=glob.glob(os.path.join(directory, "resuAnonyme*.resu"))
    for i in range(len(resuList)):
        #1 récupérer ID du fichier
        resuAnonymeName=os.path.basename(resuList[i])
        resuAnonymeName=resuAnonymeName.replace(".resu","")
        IDFichierAnonyme=resuAnonymeName[11:]
        #2 voir où se trouve le fichier dans datafile
        posResu=CheckInDataFile(matriceresu,IDFichierAnonyme)
        originalResuName=resuList[i]
        
        originalResuName = ChangeAnonymeToName(originalResuName,matriceresu,posResu)
        #3 changer les noms anonymes et les données des edf et resu
        originalEDFName=glob.glob(os.path.join(os.path.dirname(resuList[i]),'RawAnonyme'+IDFichierAnonyme+'.EDF'))
        if originalEDFName:
            posEDF=CheckInDataFile(matriceEDF,IDFichierAnonyme)
            originalEDFName = ChangeAnonymeToName(originalEDFName[0],matriceEDF,posEDF)
            UnAnonymiseEDF(originalEDFName,matriceEDF,posEDF)
        try:
            UnAnonymiseResu(originalResuName,matriceresu,posResu)
        except Exception as e : 
            print("error with unanonymiseEdf/Resu() : " + str(e) + "\n End of the procedure")
    return

def AN(EDFDB, resuDB, directory):    
    try:
        bEDF=WriteFirstLine(EDFDB, "EDF/EDFHeader/champs identification/Date/ID\n")
    except Exception as e:
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
            RawFileName = os.path.join(directory, RawFileName)
            if glob.glob(RawFileName):
                #3 savedataedf
                try :
                    bOK=saveDataEDF(RawFileName,EDFDB,ID) # if false : already saved
                except Exception as e:
                    printLogs("Error with saveDataEDF() :" + str(e) + "\n End of the procedure")
                    return
                #4 Anonymise edf et resu (nom et données)
                if bOK:
                    try:
                        AnonymiseEDF(RawFileName)
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
                                         
def saveDataresu(resuName,resuDB,ID):
    if 'resuAnonyme' in resuName:
        print("Fichier resu déjà sauvé")
        return False
    else:
        matriceresu=np.loadtxt(resuDB,delimiter='\t',comments=None,encoding='utf-8',dtype='U',skiprows=1,ndmin=2)
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
    if 'RawAnonyme' in RawFileName:
        print("Fichier EDF déjà sauvé")
        return False
    else:
    # Writing datae
        dataFile = open(EDFDB, "a")
        dataFile.write(RawFileName)
        dataFile.write('\t')
        EDF = open(RawFileName, "rb")
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

def WriteFirstLine(DB, FirstLine):
    #return true  if ID must be one and false if ID must be identified
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
        NewName="RawAnonyme{0}.EDF".format(ID)     
    else : 
        NewName="UnknownAnonyme{0}.resu".format(ID)    
    NewName = os.path.join(os.path.dirname(Name), NewName)
    os.rename(Name, NewName)
    return 


def ChangeAnonymeToName(AnonymFile, matrix,ID) :
    FileName=matrix[ID][0]
    os.rename(AnonymFile,FileName)
    return FileName

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
