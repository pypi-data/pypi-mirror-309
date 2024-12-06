import os
import numpy as np
import pandas as pd
import struct
from datetime import * 
from .ComtradeParser import *


class ComtradeFile(object):
    """
    A python Class for read and write IEEE Comtrade files. 
    
    This is the main class of pyComtrade.
    """

    def __init__(self,filename):
        """
        pyComtrade constructor: 
            Clear the variables
            Check if filename exists. If so, read the CFG file.

        filename: string with the path for the .cfg file.        
        
        """
        self.__clear()
        
        if os.path.isfile(filename):
            self.filename = filename
            self.__ReadCfgFile()
            self.__ReadDatFile()            
        else:
            print("Error:  %s File not found." %(filename))
            return

    def __clear(self):
        """
        Clear the internal (private) variables of the class.
        """
        self.filename = ''
        # Resets the variables
        self.cfg_data = {}  # Config data
        # Data file type:
        self.fileType = 'ASCII'
        self.__DatFileContent = ''     
        # Line frequency:
        self.freq = 50

    def __ReadCfgFile(self):
        """
        Reads the Comtrade header file (.cfg).
        """

        # Try to open the config file
        cfgParser = ComtradeParser()
        with open(self.filename, 'r') as cfg_file:
            # For each argument
            for arg in cfgParser.arg_str:
                # Extracting and testing arguments
                if arg in ['A', 'D']:
                    # Number of channels
                    nchnn = self.cfg_data['#A']
                    if arg == 'D':
                        nchnn = self.cfg_data['#D']

                    # Reading analog/digital  channels
                    self.cfg_data[arg] = []
                    for i in range(nchnn):
                        # Read line and Process line
                        line = cfg_file.readline()
                        out_dct = cfgParser.proc_line(line, arg)
                        self.cfg_data[arg].append(out_dct.copy())
                elif arg in 'samples':
                    # Read samples line
                    line = cfg_file.readline()
                    nrate = int(self.cfg_data['nrates'])
                    if nrate < 1:
                        cfgParser.nrates = 1
                    else:
                        cfgParser.nrates = nrate
                        
                    out_dct = cfgParser.proc_line(line, arg)
                    self.cfg_data.update(out_dct)                
                else:
                    # Remaining channels
                    # Read line
                    line = cfg_file.readline()
                    if line.rstrip() == '':
                        break

                    # Process line
                    out_dct = cfgParser.proc_line(line, arg)
                    self.cfg_data.update(out_dct)

        # Read start/trigger date and time ([dd,mm,yyyy,hh,mm,ss.ssssss]):
        self.startTime = datetime.strptime(self.cfg_data['start_date']+','+self.cfg_data['start_time'], '%d/%m/%Y,%H:%M:%S.%f')
        self.triggerTime = datetime.strptime(self.cfg_data['trigger_date']+','+self.cfg_data['trigger_time'], '%d/%m/%Y,%H:%M:%S.%f')

        # Read file type:
        self.fileType = self.cfg_data['file_type']
        # get the sampling rate, sample point per period
        self.freq = self.cfg_data['line_freq'] 
        self.sampleRate = self.cfg_data['samp'][-1]
        self.numberOfSamples = self.cfg_data['endsamp'][-1]        
        self.samplePoint = round(self.sampleRate/self.freq)
        
        self.analog_id = [v['ch_id'] for v in self.cfg_data['A']]
        self.analog_An = [v['An'] for v in self.cfg_data['A']]
        self.digital_id = [v['ch_id'] for v in self.cfg_data['D']]
        self.digital_Dn = [v['Dn'] for v in self.cfg_data['D']]

    def __ReadDatFile(self):
        """
        Reads the contents of the Comtrade .dat file and store them in a
        private variable.
        
        For accessing a specific channel data, see methods getAnalogData and
        getDigitalData.
        """

        if self.filename.endswith(".cfg"):
            datFile = self.filename.replace(".cfg",".dat")
        elif self.filename.endswith(".CFG"):
            datFile = self.filename.replace(".CFG",".DAT")

        if not os.path.isfile(datFile):
            print("%s data File not found." %(datFile))
            return 0

        # Reading data file.
        if self.cfg_data['file_type'] == 'ASCII':
            # Read ASCII file
            self.__DatFileContent = pd.read_csv(datFile, header=None)
            self.__DatFileContent = self.__DatFileContent[:self.numberOfSamples].T.values
        else:
            # Read binary
            # Opens file and reads all data
            with open(datFile, 'rb') as bdata:
                bdata = bdata.read()

            # Fomating string for struct module:
            # Getting auxiliary variables
            nA = self.cfg_data['#A']
            nD = self.cfg_data['#D']
            nH = int(np.ceil(nD/16.0))
            nS = self.numberOfSamples

            # Setting struct string
            str_struct = "ii{0}h".format(nA + nH)
            str_struct = "ii{0}h{1}H".format(nA, nH)        
            # Number of bytes per sample        
            nbps = 4+4+nA*2+nH*2

            # Empty column vector:
            self.__DatFileContent = np.empty([nS, nA+nD+2])

            for i in range(nS):  # i: sample index
                data = bdata[i*nbps:(i+1)*nbps]            
                data = struct.unpack(str_struct, data)

                # parse digital channel
                data_D = data[(nA+2):]
                chl_D = ''
                for di in data_D:
                    bin_di = '{0:0b}'.format(di)
                    bin_di = '0'*(16 - len(bin_di)) + bin_di
                    chl_D += bin_di[::-1]

                chl_D = list(chl_D[:nD])
                chl_D = [int(i) for i in chl_D]
                self.__DatFileContent[i] = data[:(nA+2)] + tuple(chl_D)

            self.__DatFileContent = self.__DatFileContent.T
        
        # Set channel values for cfg_data
        self.__setChannelData()

        if self.sampleRate < 1:
            self.sampleRate = 1e6/(self.__DatFileContent[1][1] - self.__DatFileContent[1][0])
            self.samplePoint = round(self.sampleRate/self.freq)

    def __setChannelData(self):
        '''
        Set channel data for cfg_data.
        '''

        # Open data
        data = self.__DatFileContent[2:]
        # For each analog channel
        for cidx in range(self.cfg_data['#A']):
            # Reading channels
            values = data[cidx]
            values = values * self.cfg_data['A'][cidx]['a']
            values = values + self.cfg_data['A'][cidx]['b']
            self.cfg_data['A'][cidx]['values'] = values

        # Removing analog channels
        data = data[self.cfg_data['#A']:]

        # For each digital channel
        for cidx in range(self.cfg_data['#D']):
            # Reading channels
            self.cfg_data['D'][cidx]['values'] = data[cidx]


    def getTime(self):
        """
        Actually, this function creates a time stamp vector 
        based on the number of samples and sample rate.
        """
        t_interval = 1/self.sampleRate
        t_end = self.numberOfSamples * t_interval
        t = np.linspace(0,t_end,self.numberOfSamples+1)
        t = np.delete(t,-1)
        t = t - (self.triggerTime-self.startTime).total_seconds()
        
        return t

    def getAnalogData(self,Channel,type='S'):
        """
        Returns the sampling values, according to the channel id or channel number.    

        Parameters
        ----------
        Channel : channel number or channel name    
        type : 
            'S' get secondary analog
            'P' get primary analog    

        Examples
        --------
        >>> VA = comtradeFile.getAnalogData(1)   
        >>> VB = comtradeFile.getAnalogData('VB')

        """

        # Get channel number if use channel id
        if isinstance(Channel,str):
            ChNumber = self.analog_id.index(Channel)
        else:
            ChNumber = self.analog_An.index(Channel)
        
        if (ChNumber >= self.cfg_data['#A']):
            print("Channel number greater than the number of channels.")
            return 0        
        
        values = self.cfg_data['A'][ChNumber]['values']
        rtgPrimary = self.cfg_data['A'][ChNumber]['primary']
        rtgSecondary = self.cfg_data['A'][ChNumber]['secondary']
        
        if (((type=='S') or (type=='Secondary')) and ('P' in self.cfg_data['A'][ChNumber]['P_S'])):
            values = values * rtgSecondary/rtgPrimary

        if (((type=='P') or (type=='Primary')) and ('S' in self.cfg_data['A'][ChNumber]['P_S'])):
            values = values * rtgPrimary/rtgSecondary

        return values

    def getDigitalData(self,Channel):
        """
        Returns the digit channel data (0 or 1) .

        Parameters
        ----------
        Channel : channel number or channel name    
        """

        # Get channel number if use channel id
        if isinstance(Channel,str):
            ChNumber = self.digital_id.index(Channel)
        else:
            ChNumber = Channel - 1
        
        if (ChNumber >= self.cfg_data['#D']):
            print("Channel number greater than the number of channels.")
            return 0

        return self.cfg_data['D'][ChNumber]['values']


    def getAnalogID(self,num=None):
        """
        Returns the COMTRADE ID of a given channel number.
        The number to be given is the same of the COMTRADE header.
        Or Returns all analog channels ID
        """

        if num is None:
            return self.analog_id
        else:
            # Get the position of the channel number.
            listidx = self.analog_An.index(num) 
            return self.analog_id[listidx]

    def getDigitalID(self,num=None):
        """
        Returns the COMTRADE ID of a given channel number.
        The number to be given is the same of the COMTRADE header.
        Or Returns all analog channels ID
        """

        if num is None:
            return self.digital_Dn
        else:
            # Get the position of the channel number.
            listidx = self.digital_Dn.index(num) 
            return self.digital_id[listidx]

    def __getitem__(self, key):
        '''
        Returns a COMTRADE file key value.

        @param key target key.

        @return key value.
        '''
        return self.cfg_data[key]

    def __setitem__(self, key, item):
        '''
        Sets a COMTRADE file key value

        @param key target key.
        @param item target key value.
        '''
        self.cfg_data[key] = item


    def to_csv(self, path):
        '''
        Saves channels signals in a csv file.

        @param path csv file
        '''

        # Converting each channel signal into a dictionary
        values = {}
        values.update({v['ch_id']: v['values'] for v in self.cfg_data['A']})
        values.update({v['ch_id']: v['values'] for v in self.cfg_data['D']})

        # Saving into dataframe
        values = pd.DataFrame(values, self.getTime())
        values.to_csv(path, header=True, index_label='timestamp')

