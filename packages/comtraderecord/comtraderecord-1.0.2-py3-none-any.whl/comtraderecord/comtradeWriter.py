import os
import numpy as np
import struct
import datetime

class comtradeWriter:
    """
    A python Class for read and write IEEE Comtrade files. 
    
    This is the main class of pyComtrade.
    """

    def __init__(self,filename,data,samplingFreq = 1000, RatedFreq = 50, Number_D = 0):
        """
        pyComtrade constructor: 
            Prints a message. 
            Clear the variables
            Check if filename exists.
            If so, read the CFG file.

        filename: string with the path for the .cfg file.        
        
        """       
        self.filename = filename
        self.data = data        
        self.dataLen = len(data[0])
        self.totalChannelNum = len(data)
        self.Number_D = Number_D
        self.Number_A = self.totalChannelNum - self.Number_D
        self.ch_id = ['']*self.dataLen
        self.ph_id = ['']*self.dataLen
        self.uu_unit = ['']*self.dataLen
        self.primary = [1.0]*self.dataLen
        self.secondary = [1.0]*self.dataLen

        self.samplingFreq = samplingFreq
        self.RatedFreq = RatedFreq
        self.nrates = 1

    def createFile(self):
        """
        create the Comtrade header file (.cfg).
        """

        station_name = 'HSBT'
        rec_dev_id = 'Simu'
        rev_year='2010'

        f = open(self.filename+'.cfg', 'w')
        f.write(f'{station_name},{rec_dev_id},{rev_year}\n')
        f.write(f'{self.totalChannelNum},{self.Number_A}A,{self.Number_D}D\n')

        An_min = -99999
        An_max = 99998

        endsamp = len(self.data[0])
        xdata = [0]*(self.Number_A+2)
        xdata[0] = np.arange(1,self.dataLen+1)
        xdata[1] = xdata[0]*1e6/self.samplingFreq

        for i in range(0,self.Number_A):
            channelStr = str(i+1) + ','
            channelStr += self.ch_id[i] + ','
            channelStr += self.ph_id[i] + ','    
            channelStr += str(i+1) + ','
            channelStr += self.uu_unit[i] + ','
            maxA = max(self.data[i])
            minA = min(self.data[i])
            a_multiplier = (maxA - minA)/(An_max-An_min)
            b_offset = (minA*An_max-maxA*An_min)/(An_max-An_min)
            xdata[i+2] = (self.data[i] - b_offset)/a_multiplier
            channelStr += str(a_multiplier) + ','
            channelStr += str(b_offset) + ','
            channelStr += '0,'
            channelStr += str(An_min) + ','
            channelStr += str(An_max) + ','    
            channelStr += str(self.primary[i]) + ','
            channelStr += str(self.secondary[i]) + ','        
            channelStr += 'S'
            f.write(channelStr+'\n')

        f.write(f'{self.RatedFreq}\n')
        f.write(f'{self.nrates}\n')

        f.write(f'{self.samplingFreq},{endsamp}\n')
        start_time = datetime.datetime.now().strftime('%d/%m/%Y,%H:%M:%S.%f')
        f.write(f'{start_time}\n')
        trigger_time = start_time
        f.write(f'{start_time}\n')
        f.write('ASCII\n')
        f.write('1.0\n')
        
        f.close()

        fileData = np.asarray(xdata)
        np.savetxt(self.filename+'.dat', fileData.T, fmt='%d',delimiter=',')

    def setChannelID(self,ch_id):
        self.ch_id = ch_id

    def setPhaseID(self,ph_id):
        self.ph_id = ph_id

    def setUnit(self,uu_unit):
        self.uu_unit = uu_unit

    def setPrimary(self,primary):
        self.primary = primary

    def setSecondary(self,secondary):
        self.secondary = secondary            