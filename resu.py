import numpy as np
from pyrsistent import v
import copy
from operator import itemgetter, attrgetter
from utils import printLogs 

class Point:
    def __init__(self):
        self.min = 0
        self.sao2 = 0
        self.temps = 0
        self.ecg = 0
    def __repr__(self):  
        return str(self.__class__) + ": " + str(self.__dict__)
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

class Event:
    def __init__(self):
        self.type = 0
        self.sous_type = 0
        self.sous_type2 = 0
        self.Area = 0
        self.free = 0
        self.debut = Point()
        self.reprise = Point()
        self.minsao2 = Point()
        self.fin = Point()
    def __repr__(self):  
        return str(self.__class__) + ": " + str(self.__dict__) + "\n"
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__) + "\n"


def readResu(resuName):
    fid = open(resuName, "rb")
    resu = {}
    resu['LastRecord'] = fid.read(6)
    resu['FileStruct'] = fid.read(6)
    resu['AASoft'] = fid.read(6)
    resu['CorrectionSoft'] = fid.read(6)
    resu['ExamDate'] = fid.read(10)
    resu['BeginningHour'] = fid.read(8)
    resu['pPatient'] = fid.read(6)
    resu['Room'] = fid.read(4)
    resu['RawType'] = fid.read(2)
    resu['pDescription'] = int(fid.read(6))
    resu['pEvents'] = int(fid.read(6))
    resu['EventsNumber'] = int(fid.read(6))
    resu['RecordType'] = fid.read(1)
    resu['EpochLength'] = fid.read(2)
    resu['epochsNumber'] = int(fid.read(5))
    resu['lastEpoch'] =  int(fid.read(5))
    resu['FFTWindowsN'] =  int(fid.read(2))
    resu['Channels'] = fid.read(8)
    resu['signalsValidity'] =  fid.read(1)
    resu['myo1Description'] =  fid.read(1)
    resu['myo2Description'] =  fid.read(1)
    resu['myo3Description'] =  fid.read(1)
    resu['myo4Description'] =  fid.read(1)
    resu['CreationDate'] =  fid.read(10)
    resu['EndymionVersion'] =  fid.read(10)
    resu['Examinator'] =  fid.read(24)
    resu['RawFileName'] =  fid.read(22)
    print(resu['RawFileName'])
    resu['DeviceNumber'] =  fid.read(2)
    resu['MiscBools'] =  fid.read(4)
    resu['Free1'] =  fid.read(20)
    resu['Free2'] =  fid.read(24)
    resu['Free3'] =  fid.read(24)
    resu['Free4'] =  fid.read(24)
    resu['Flags'] =  fid.read(384) #648
    resu['SleepVar'] =  fid.read(1200)
    resu['Free6'] =  fid.read(72)
    resu['A'] =  fid.read(2)
    resu['FileNumber'] =  fid.read(22)
    resu['Name'] =  fid.read(27)
    resu['FirstName'] =  fid.read(27)
    resu['BirthDate'] =  fid.read(10)
    resu['Sex'] =  fid.read(1)
    resu['Free7'] =  fid.read(7)
    fid.close()
    resu['Int32Begin'] = int((resu['pDescription']-1)*24*8/32)
    resu['Int32End'] = resu['Int32Begin']+12*resu['epochsNumber']
    values=np.fromfile(resuName,dtype=np.uintc)
    resu['Full'] = values
    
    Mot=values[resu['Int32Begin']:resu['Int32End']:12]
    resu['stages']=np.bitwise_and(Mot, 0x0f)
    resu['Mor']=np.bitwise_and(Mot >> 4, 0x1f)
    resu['Mol']=np.bitwise_and(Mot >> 9, 0x0f)
    resu['Tfs']=np.bitwise_and(Mot >> 13, 0x1f)
    resu['Kcp']=np.bitwise_and(Mot >> 18, 0x0f)
    resu['Tfd']=np.bitwise_and(Mot >> 22, 0x1f)
    resu['Tfa']=np.bitwise_and(Mot >> 27, 0x1f)
    
    Mot=values[resu['Int32Begin']+1:resu['Int32End']:12]
    resu['Del']=np.bitwise_and(Mot, 0xff)
    resu['The']=np.bitwise_and(Mot >> 8, 0xff)
    resu['Alp']=np.bitwise_and(Mot >> 16, 0xff)
    resu['Sig']=np.bitwise_and(Mot >> 24, 0xff)
    
    Mot=values[resu['Int32Begin']+2:resu['Int32End']:12]
    resu['Tfb']=np.bitwise_and(Mot, 0x1f)
    resu['Tar']=np.bitwise_and(Mot >> 5, 0x1f)
    resu['Art']=np.bitwise_and(Mot >> 10, 0x1f)
    resu['Ton']=np.bitwise_and(Mot >> 15, 0xffff)
    resu['2FV']=np.bitwise_and(Mot >> 31, 0x01)
    
    Mot=values[resu['Int32Begin']+3:resu['Int32End']:12]
    resu['Sao']=np.bitwise_and(Mot, 0x7f)
    resu['Res']=np.bitwise_and(Mot >> 7, 0xff)
    resu['Fca']=np.bitwise_and(Mot >> 15, 0xff)
    resu['Tpr']=np.bitwise_and(Mot >> 23, 0x1ff)
    
    Mot=values[resu['Int32Begin']+4:resu['Int32End']:12]
    resu['Myo']=np.bitwise_and(Mot, 0x0f)
    resu['Myo2']=np.bitwise_and(Mot >> 4, 0x0f)
    resu['MyoE']=np.bitwise_and(Mot >> 8, 0x0f)
    resu['Tft']=np.bitwise_and(Mot >> 12, 0x1f)
    resu['Ads']=np.bitwise_and(Mot >> 17, 0x1f)
    resu['Nse']=np.bitwise_and(Mot >> 22, 0x3ff)
    
    Mot=values[resu['Int32Begin']+5:resu['Int32End']:12]
    resu['Flg']=np.bitwise_and(Mot, 0xffff)
    resu['Fc2']=np.bitwise_and(Mot >> 16, 0xff)
    resu['Pcp']=np.bitwise_and(Mot >> 24, 0xff)
    
    Mot=values[resu['Int32Begin']+6:resu['Int32End']:12]
    resu['Msv']=np.bitwise_and(Mot, 0xffff)
    resu['Res2']=np.bitwise_and(Mot >> 16, 0xffff)
    
    Mot=values[resu['Int32Begin']+7:resu['Int32End']:12]
    resu['Pow']=np.bitwise_and(Mot, 0xffff)
    resu['Vft']=np.bitwise_and(Mot >> 16, 0x3f)
    resu['V2f']=np.bitwise_and(Mot >> 22, 0x3f)
    resu['Mev']=np.bitwise_and(Mot >> 28, 0x0f)

    Mot=values[resu['Int32Begin']+8:resu['Int32End']:12]
    resu['S5s']=np.bitwise_and(Mot, 0x0f)
    resu['S5sp2']=np.bitwise_and(Mot >> 4, 0x0f)
    resu['S5sp3']=np.bitwise_and(Mot >> 8, 0x0f)
    resu['S5sp4']=np.bitwise_and(Mot >> 12, 0x0f)
    resu['S5sp5']=np.bitwise_and(Mot >> 16, 0x0f)
    resu['S5sp6']=np.bitwise_and(Mot >> 20, 0x0f)
    resu['2sa']=np.bitwise_and(Mot >> 24, 0x01)
    resu['Sa2']=np.bitwise_and(Mot >> 25, 0x7f)
    
    Mot=values[resu['Int32Begin']+9:resu['Int32End']:12]
    resu['Myo3']=np.bitwise_and(Mot, 0x0f)
    resu['Myo4']=np.bitwise_and(Mot >> 4, 0x0f)
    resu['MySi']=np.bitwise_and(Mot >> 8, 0x0f)
    resu['POS']=np.bitwise_and(Mot >> 12, 0x0f)
    resu['Res3']=np.bitwise_and(Mot >> 16, 0xffff)
    
    Mot=values[resu['Int32Begin']+10:resu['Int32End']:12]
    resu['Res4']=Mot
    
    Mot=values[resu['Int32Begin']+11:resu['Int32End']:12]
    resu['Res5']=Mot
    
    
    Events = []
    a=int(resu['Int32End']+(resu['EventsNumber'])*192/32)
    tempEvents=values[resu['Int32End']:a]


    for i in range(resu['EventsNumber']):
        event = Event()
        event.type = np.bitwise_and(tempEvents[i*6], 0x0f)
        event.debut.sao2 =  np.bitwise_and(tempEvents[i*6] >> 4, 0x3f)
        if event.type == 7 : # Neuro
            event.sous_type = event.debut.sao2
            event.debut.sao2 = 0
        else :
            event.debut.sao2 += 37
            event.sous_type = 0
        if (event.sous_type >= 3 and event.sous_type <= 8) or (event.sous_type >= 11 and event.sous_type <= 15) or (event.sous_type >= 25 and event.sous_type <= 26): #BLA
            event.type = 9
            event.debut.temps = np.bitwise_and(tempEvents[i*6] >> 10, 0x003fffff) * 4
            tempString = ''
            for s in range(5):
                tempString = tempString + (tempEvents[i*6+1+s]).tobytes().decode('raw_unicode_escape')
            event.texte = tempString
            event.reprise.temps = event.debut.temps
            event.minsao2.temps = event.debut.temps
            event.fin.temps = event.debut.temps + 25
        elif event.sous_type == 24 : #EXTRAIT
            event.type = 11
            event.debut.temps = np.bitwise_and(tempEvents[i*6] >> 10, 0x3fffff) * 4
            event.reprise.temps = np.bitwise_and(tempEvents[i*6+1] , 0xffff)
            event.reprise.temps += event.debut.temps
            event.minsao2.temps = np.bitwise_and(tempEvents[i*6+1] >> 16 , 0xffff)
            event.fin.temps = event.reprise.temps
            event.control1 = tempEvents[i*6+2]
            event.control2 = tempEvents[i*6+3]
            event.free1 = tempEvents[i*6+4]
            event.free2 = tempEvents[i*6+5]
        elif (event.sous_type == 9 or event.sous_type == 10) : #SON
            event.type = 10
            event.debut.temps = np.bitwise_and(tempEvents[i*6] >> 10, 0x3fffff) * 4
            event.reprise.temps = event.debut.temps
            event.minsao2.temps = np.bitwise_and(tempEvents[i*6+1] , 0xffff) 
            event.minsao2.temps += event.debut.temps
            event.fin.temps = event.debut.temps + 25
            tempstring = ''
            tempstring = np.bitwise_and(tempEvents[i*6+1] >> 16 , 0xffff).tobytes().decode('unicode_escape') 
            for s in range(4):
                tempstring = tempstring + (tempEvents[i*6+2+s]).tobytes().decode('unicode_escape')
            event.texte = tempstring
        else : #EVENT
            event.debut.temps = np.bitwise_or(np.bitwise_and(tempEvents[i*6] >> 10, 0xffffff), np.bitwise_and(tempEvents[i*6+1] , 0x03)<<22)
            event.debut.ecg = np.bitwise_and(tempEvents[i*6+1] >> 2, 0xff)
            event.sous_type2 = np.bitwise_and(tempEvents[i*6+1] >> 10, 0x3f)
            event.reprise.temps = np.bitwise_or(np.bitwise_and(tempEvents[i*6+1] >> 16, 0xffff), np.bitwise_and(tempEvents[i*6+2] , 0x03)<<16)
            event.reprise.temps += event.debut.temps
            event.reprise.sao2 = np.bitwise_and(tempEvents[i*6+2] >> 2, 0x3f) +37
            event.reprise.ecg = np.bitwise_and(tempEvents[i*6+2] >> 8, 0xff)
            event.minsao2.temps = np.bitwise_or(np.bitwise_and(tempEvents[i*6+2] >> 16, 0xffff), np.bitwise_and(tempEvents[i*6+3] , 0x03)<<16)
            event.minsao2.temps += event.debut.temps
            event.minsao2.sao2 = np.bitwise_and(tempEvents[i*6+3] >> 2, 0x3f) +37
            event.minsao2.ecg = np.bitwise_and(tempEvents[i*6+3] >> 8, 0xff)
            event.fin.temps = np.bitwise_or(np.bitwise_and(tempEvents[i*6+3] >> 16, 0xffff), np.bitwise_and(tempEvents[i*6+4] , 0x03)<<16)
            event.fin.temps += event.debut.temps
            event.fin.sao2 = np.bitwise_and(tempEvents[i*6+4] >> 2, 0x3f) +37
            event.fin.ecg = np.bitwise_and(tempEvents[i*6+4] >> 8, 0xff)
            event.Area = np.bitwise_or(np.bitwise_and(tempEvents[i*6+4] >> 16, 0xffff), np.bitwise_and(tempEvents[i*6+5] , 0xffff)<<16)
            event.free = np.bitwise_and(tempEvents[i*6+5] >> 16, 0xffff)       
        if event.type == 4 :
            event.sous_type = event.sous_type2
        if event.type == 6:
            if event.minsao2.temps == event.debut.temps:
                event.minsao2 = event.fin
        else :
            event.Area = 0
        Events.append(event)
    resu['Events'] = Events
    
    print("-----------------------------------------------Test Guillaume-------------------------------------------------------------")
    #print(Events)
    print(len(Events))
    
    eventSeven=filter(lambda event : event.type ==7, Events)
    microEveil=filter(lambda event : event.sous_type == 1, eventSeven)

    # for me in microEveil:
    #     times=me.debut.temps




    #print(type(microEveil))
    
    aaa=list(microEveil)
    #print(aaa[0])
    print("vecvec")
    # vec = open("resu" + '.vec', 'a')
    zeros=np.zeros((8388608,1),dtype=int)
    np.savetxt('resu.vec',zeros,fmt='%i')
    # for item in aaa:
    #     print(type(aaa))
    #     print(type(item))
    #     vec.write(str(aaa[0])) 
    #     vec.write("\n")
    # vec.close()
    return resu
#Ev = a['Events']
#print(Ev)
#print(len(a['Events']))
#Ev.sort(key=lambda e: e['reprise']['temps'])
#newEv = Event()
#newEv.type = 1
#newEv.debut.temps = 1000
#newEv.reprise.temps = 10000
#newEv.minsao2.temps = 10000
#newEv.fin.temps = 10000
#a['Events'].append(newEv)
#print(a['Events'])
#a['Events'].sort(key=lambda e: e.reprise.temps)
#print(a['Events'])
#print(len(a['Events']))


# a=readResu("TestTest//resuAnonyme7.resu")
# a["Events"] = 0
# print(a)
# a=readResu("TestTest//ROSSMON0-20220131.resu")
# a["Events"] = 0
#print(a)

def saveResu(resu, resuName):
    Mot = []
    nMots = 12
    for i in range(nMots):
        Mot.append(np.array(np.zeros(resu['epochsNumber'], dtype='uintc')))
    Mot[0] = np.bitwise_or(resu['stages'], resu['Mor'] << 4)
    Mot[0] = np.bitwise_or(Mot[0], resu['Mol'] << 9)
    Mot[0] = np.bitwise_or(Mot[0], resu['Tfs'] << 13)
    Mot[0] = np.bitwise_or(Mot[0], resu['Kcp'] << 18)
    Mot[0] = np.bitwise_or(Mot[0], resu['Tfd'] << 22)
    Mot[0] = np.bitwise_or(Mot[0], resu['Tfa'] << 27)

    Mot[1] = np.bitwise_or(resu['Del'], resu['The'] << 8)
    Mot[1] = np.bitwise_or(Mot[1], resu['Alp'] << 16)
    Mot[1] = np.bitwise_or(Mot[1], resu['Sig'] << 24)
    
    Mot[2] = np.bitwise_or(resu['Tfb'], resu['Tar'] >> 5)
    Mot[2] = np.bitwise_or(Mot[2], resu['Art'] << 10)
    Mot[2] = np.bitwise_or(Mot[2], resu['Ton'] << 15)
    Mot[2] = np.bitwise_or(Mot[2], resu['2FV'] << 31)
    
    Mot[3] = np.bitwise_or(resu['Sao'], resu['Res'] << 7)
    Mot[3] = np.bitwise_or(Mot[3], resu['Fca'] << 15)
    Mot[3] = np.bitwise_or(Mot[3], resu['Tpr'] << 23)
    
    Mot[4] = np.bitwise_or(resu['Myo'], resu['Myo2']  << 4)
    Mot[4] = np.bitwise_or(Mot[4], resu['MyoE'] << 8)
    Mot[4] = np.bitwise_or(Mot[4], resu['Tft'] << 12)
    Mot[4] = np.bitwise_or(Mot[4], resu['Ads'] << 17)
    Mot[4] = np.bitwise_or(Mot[4], resu['Nse'] << 22)
    
    Mot[5] = np.bitwise_or(resu['Flg'], resu['Fc2'] << 16)
    Mot[5] = np.bitwise_or(Mot[5], resu['Pcp'] << 24)
    
    Mot[6] = np.bitwise_or(resu['Msv'], resu['Res2'] << 16)

    Mot[7] = np.bitwise_or(resu['Pow'], resu['Vft'] << 16)
    Mot[7] = np.bitwise_or(Mot[7], resu['V2f'] << 22)
    Mot[7] = np.bitwise_or(Mot[7], resu['Mev'] << 28)
    
    Mot[8] = np.bitwise_or(resu['S5s'], resu['S5sp2'] << 4)
    Mot[8] = np.bitwise_or(Mot[8], resu['S5sp3'] << 8)
    Mot[8] = np.bitwise_or(Mot[8], resu['S5sp4'] << 12)
    Mot[8] = np.bitwise_or(Mot[8], resu['S5sp5'] << 16)
    Mot[8] = np.bitwise_or(Mot[8], resu['S5sp6'] << 20)
    Mot[8] = np.bitwise_or(Mot[8], resu['2sa'] << 24)
    Mot[8] = np.bitwise_or(Mot[8], resu['Sa2'] << 25)
    
    Mot[9] = np.bitwise_or(resu['Myo3'], resu['Myo4'] << 4)
    Mot[9] = np.bitwise_or(Mot[9], resu['MySi'] << 8)
    Mot[9] = np.bitwise_or(Mot[9], resu['POS'] << 12)
    Mot[9] = np.bitwise_or(Mot[9], resu['Res3'] << 16)
    
    Mot[10] = resu['Res4']
    
    Mot[11] = resu['Res5']

    MotEvent = np.array([], dtype='uintc')
    Events = resu['Events']
    Event0 = np.zeros(6, dtype='uintc')
    for i in range(0, len(Events)):
        event = Events[i]
        Event0 = np.zeros(6, dtype='uintc')
        sous_type2 = event.sous_type2
        if event.type == 7 : # Neuro
            Type = event.type
            sao2 = event.sous_type
        elif (event.type == 9 ): #BLA
            Type = 7
            sao2 = event.sous_type
        elif (event.type == 10) : #SON
            Type = 7
            sao2 = event.sous_type
        elif (event.type == 11) :
            Type = 7
            sao2 = event.sous_type
        else :
            sao2 = event.debut.sao2
            if sao2 > 37 :
                sao2 = sao2 - 37
            else : 
                sao2 = 0
            Type = event.type
            sous_type2 = event.sous_type
            sao2 = sao2
        Event0[0] = np.bitwise_or(Type, sao2 << 4)
        if event.type == 9 :
            tps_deb = int(event.debut.temps / 4)
            Event0[0] = np.bitwise_or(Event0[0], tps_deb << 10)
            bla = event.texte
            for s in range(5):
                temp = bla[s*4:(s+1)*4]
                temp = temp.encode(encoding = 'raw_unicode_escape')
                temp  = int.from_bytes(temp, "little")
                Event0[s+1] = temp 
        elif event.type == 10 :
            tps_deb = int(event.debut.temps / 4)
            Event0[0] = np.bitwise_or(Event0[0], tps_deb << 10)
            tps = int(event.reprise.temps - event.debut.temps)
            if tps < 0 :
                tps = 0
            if event.get('texte') :
                bla = event.texte
            else : 
                bla = '                    '
            temp = bla[0:2]    
            temp = temp.encode(encoding = 'raw_unicode_escape')
            temp  = int.from_bytes(temp, "little")
            Event0[1] = np.bitwise_or(temp, tps << 16)
            for s in range(4):
                temp = bla[2+s*4:2+(s+1)*4]    
                temp = temp.encode(encoding = 'raw_unicode_escape')
                temp  = int.from_bytes(temp, "little")
                Event0[s+2] = temp 
        elif event.type == 11 :
            tps_deb = int(event.debut.temps / 4)
            Event0[0] = np.bitwise_or(Event0[0], tps_deb << 10)
            tps = int(event.reprise.temps - event.debut.temps)
            if tps < 0 or tps > 3000:
                tps = int(event.debut.temps / 200 / 30)
            tps2 = int(event.minsao2.temps)
            if tps2 <= 0 :
                tps2 = 30
            Event0[1] = np.bitwise_or(tps, tps2 << 16)
            Event0[2] = event.control1 
            Event0[3] = event.control2  
            Event0[4] = event.free1   
            Event0[5] = event.free2   
        else : 
            tps_deb = event.debut.temps
            Event0[0] = np.bitwise_or(Event0[0], np.bitwise_and(tps_deb, 0x3fffff) << 10)
            Event0[1] = np.bitwise_or(tps_deb >> 22, event.debut.ecg << 2)
            if i==1:
                print(sous_type2)
            Event0[1] = np.bitwise_or(Event0[1], sous_type2 << 10)
            tps = int(event.reprise.temps - event.debut.temps)
            if tps < 0 :
                tps =0
            Event0[1] = np.bitwise_or(Event0[1], np.bitwise_and(tps, 0xffff) << 16)
           
            if event.reprise.sao2 > 37 :
                sao2 = int(event.reprise.sao2 - 37)
            else : 
                sao2 = 0
            Event0[2] = np.bitwise_or(tps >> 16, sao2 << 2)
            Event0[2] = np.bitwise_or(Event0[2], event.reprise.ecg << 8)
            tps = event.minsao2.temps - tps_deb
            if tps < 0 :
                tps = 0
            Event0[2] = np.bitwise_or(Event0[2], np.bitwise_and(tps, 0xffff) << 16)  
            if event.minsao2.sao2 > 37 :
                sao2 = event.minsao2.sao2 - 37
            else : 
                sao2 = 0
            Event0[3] = np.bitwise_or(tps >> 16, sao2 << 2)
            Event0[3] = np.bitwise_or(Event0[3], event.minsao2.ecg << 8)
            tps = event.fin.temps - tps_deb
            if tps < 0 :
                tps = 0
            Event0[3] = np.bitwise_or(Event0[3], np.bitwise_and(tps, 0xffff) << 16)  
            if event.fin.sao2 > 37 :
                sao2 = event.fin.sao2 - 37
            else : 
                sao2 = 0
            Event0[4] = np.bitwise_or(tps >> 16, sao2 << 2)
            Event0[4] = np.bitwise_or(Event0[4], event.fin.ecg << 8)
            Event0[4] = np.bitwise_or(Event0[4], np.bitwise_and(event.Area, 0xffff) << 16)
            Event0[5] = np.bitwise_or(event.Area >> 16, event.free << 16)  
        MotEvent = np.append(MotEvent, Event0)
    MotF = Mot[0]
    for i in range(nMots-1):
        MotF = np.vstack((MotF, Mot[i+1]))     
    values = (MotF.T).flatten()    
    values = np.concatenate((values, MotEvent), axis=0)
    resu['Full'] = resu['Full'][0:resu['Int32Begin']]
    values = np.concatenate((resu['Full'], values), axis=0)
    values.tofile(resuName)
