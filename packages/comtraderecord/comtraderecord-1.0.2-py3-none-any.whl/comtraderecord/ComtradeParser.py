
class ComtradeParser:

    def __init__(self):
        """
        Initializes a ComtradeRecord instance.
        """

        # Argument string
        self.arg_str = ['header', 'nchannels', 'A', 'D', 'line_freq', 'nrates',
                        'samples', 'start', 'trigger', 'file_type', 'timemult',
                        'time_code', 'tmq_code']

        # Function dictionary
        self.fun_dct = {
            'header': self.dct_header,
            'nchannels': self.dct_nchannels,
            'A': self.dct_analog,
            'D': self.dct_digital,
            'line_freq': self.dct_lf,
            'nrates': self.dct_nrates,
            'samples': self.dct_samples,
            'start': self.dct_start,
            'trigger': self.dct_trigger,
            'file_type': self.dct_ft,
            'timemult': self.dct_tml
        }

        self.nrate = 1

    def cast_data(self, data):
        '''
        Cast data to the correct type.

        @param data argument to be casted.

        @return data with the correctly parsed type.
        '''

        # Test each type
        try:
            # int
            return int(data)
        except ValueError:
            pass
        try:
            # float
            return float(data)
        except ValueError:
            pass
        if data in ['True', 'False']:
            # boolean
            return data == 'True'
        # A string
        # return _unicode(data)
        return data

    def proc_line(self, line, arg):
        '''
        Processes a COMTRADE config file line.

        @param line input line.
        @param arg type of line/argument.

        @return dictionary with the lines elements.
        '''

        # Stripe line from end data and split each property
        line = line.rstrip().split(',')

        # Parsing, if needed
        if arg == 'nchannels':
            line[1] = line[1][:-1]  # Removing the 'A' letter from the number
            line[2] = line[2][:-1]  # Removing the 'D' letter from the number

        # Casting
        line = [self.cast_data(l) for l in line]

        # Processing and returning dictionary
        return self.fun_dct[arg](line)

    def dct_header(self, data):
        '''
        Converts header line to dictionary form.

        @param data data to be converted.
        @return station name, recording device id, and standard revision year
        '''
        output = {}
        output['station_name'] = data[0]  # Station name
        output['rec_dev_id'] = data[1]  # Recording device ID
        if len(data) > 2:  # From 1999 revision
            output['rev_year'] = data[2]  # Standard revision year
        return output

    def dct_nchannels(self, data):
        '''
        Converts number of channels line to dictionary form.

        @param data data to be converted.
        @return number of channels info.
        '''
        output = {}
        output['TT'] = data[0]  # Number of channels (#A+#D)
        output['#A'] = data[1]  # Number of analogic channels
        output['#D'] = data[2]  # Number of analogic channels
        return output

    def dct_analog(self, data):
        '''
        Converts analog channel line to dictionary form.

        @param data data to be converted.
        @return analog channel data.
        '''

        # Setting initial output and properties string
        output = {}
        dt_str = [
            'An',         # analog channel index number
            'ch_id',      # station_name:channel_name
            'ph',         # channel phase identification (0 to 2)
            'ccbm',       # circuit component being monitored
            'uu',         # channel units
            'a',          # channel multiplier
            'b',          # channel offset
            'skew',       # time skew between channels
            'min',        # data range minimum value
            'max',        # data range maximum value
            'primary',    # PT/CT primary ratio factor
            'secondary',  # PT/CT scondary ratio factor
            'P_S'         # primary or secondary PT/CT scaling identifier. 'P' or 'S'
        ]

        # For each data property
        for dtidx, dt in enumerate(data):

            # Getting data
            dn = dt_str[dtidx]
            output[dn] = dt

        # Return output
        return output

    def dct_digital(self, data):
        '''
        Converts digital channel line to dictionary form.

        @param data data to be converted
        @return digital channel data.
        '''

        # Setting initial output and properties string
        output = {}
        dt_str = [
            'Dn',     # Digital channel index
            'ch_id',  # station_name:channel_name
            'ph',     # channel phase identification
            'ccbm',   # circuit component being monitore
            'y'       # normal state of the channel
        ]

        # For each data property
        for dtidx, dt in enumerate(data):

            # Getting data
            dn = dt_str[dtidx]
            output[dn] = dt

        # Return output
        return output

    def dct_lf(self, data):
        '''
        Converts line freq line to dictionary form.

        @param data data to be converted.
        @return line frequency.
        '''
        output = {}
        output['line_freq'] = data[0]  # Line frequency in Hz
        return output

    def dct_nrates(self, data):
        '''
        Converts nrates line to dictionary form.

        @param data data to be converted.
        @return number of sampling rates.
        '''
        output = {}
        output['nrates'] = data[0]  # Number of sampling rates in the file
        return output

    def dct_samples(self, data):
        '''
        Converts samples line to dictionary form.

        @param data data to be converted
        @return sampling rates and number of samples.
        '''
        output = {'samp': [], 'endsamp': []}

        # For each sample rate
        for i in range(self.nrate):
            output['samp'].append(data[0])     # Sample rates
            output['endsamp'].append(data[1])  # Number of samples
        return output

    def dct_start(self, data):
        '''
        Converts start date/time line to dictionary form.

        @param data data to be converted.
        @return start date/time data.
        '''
        output = {}
        output['start_date'] = data[0]  # Start date
        output['start_time'] = data[1]  # Start time
        return output

    def dct_trigger(self, data):
        '''
        Converts trigger date/time line to dictionary form.

        @param data data to be converted
        @return trigger date/time data.
        '''
        output = {}
        output['trigger_date'] = data[0]  # Trigger date
        output['trigger_time'] = data[1]  # Trigger time
        return output

    def dct_ft(self, data):
        '''
        Converts file type line to dictionary form.

        @param data data to be converted
        @return file type.
        '''
        output = {}
        output['file_type'] = data[0]  # File type
        return output

    def dct_tml(self, data):
        '''
        Converts timemult line to dictionary form.

        @param data data to be converted.
        @param time multiplication factor/scale.
        '''
        output = {}
        output['timemult'] = data[0]  # time multiplication factor/scale
        return output

