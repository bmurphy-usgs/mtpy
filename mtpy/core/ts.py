# -*- coding: utf-8 -*-
"""
Created on Thu Jul 06 14:24:18 2017

@author: jpeacock
"""

#==============================================================================
# Imports
#==============================================================================
import time
import datetime

import numpy as np
import pandas as pd

import mtpy.utils.gis_tools as gis_tools

#==============================================================================

#==============================================================================
class MT_TS(object):
    """
    MT time series object that will read/write data in different formats
    including hdf5, txt, miniseed.
    
    The foundations are based on Pandas Python package.
    
    Input ts as a numpy.ndarray or Pandas DataFrame
    
    Metadata
    -----------
    
        ==================== ==================================================
        Name                 Description        
        ==================== ==================================================
        azimuth              clockwise angle from coordinate system N (deg)
        calibration_fn       file name for calibration data
        component            component name [ 'ex' | 'ey' | 'hx' | 'hy' | 'hz']
        coordinate_system    [ geographic | geomagnetic ]
        datum                datum of geographic location ex. WGS84
        declination          geomagnetic declination (deg)
        dipole_length        length of dipole (m)
        data_logger          data logger type
        instrument_id        ID number of instrument for calibration
        lat                  latitude of station in decimal degrees
        lon                  longitude of station in decimal degrees
        n_samples            number of samples in time series
        sampling_rate        sampling rate in samples/second
        start_time_epoch_sec start time in epoch seconds
        start_time_utc       start time in UTC
        station              station name
        units                units of time series
        ==================== ==================================================
    
    .. note:: Currently only supports hdf5 and text files
    
    Methods
    ------------
    
        ======================= ===============================================
        Method                  Description        
        ======================= ===============================================
        read_hdf5               read an hdf5 file
        write_hdf5              write an hdf5 file
        write_ascii_file        write an ascii file
        read_ascii_file         read an ascii file
        ======================= ===============================================
        
    
    .. example:: 
    
        >>> import mtpy.core.ts as ts
        >>> import numpy as np
        >>> mt_ts = ts.MT_TS()
        >>> mt_ts.ts = np.random.randn(1024)
        >>> mt_ts.station = 'test'
        >>> mt_ts.lon = 30.00
        >>> mt_ts.lat = -122.00
        >>> mt_ts.component = 'HX'
        >>> mt_ts.units = 'counts'
        >>> mt_ts.write_hdf5(r"/home/test.h5")
        
        
    """
    
    def __init__(self, **kwargs):
        
        self.station = 'mt00'
        self.sampling_rate = 1
        self._start_time_epoch_sec = 0.0
        self._start_time_utc = '1980-01-01,00:00:00'
        self.n_samples = 0
        self.component = None
        self.coordinate_system = 'geomagnetic'
        self.dipole_length = 0
        self.azimuth = 0
        self.units = 'mV'
        self._lat = 0.0
        self._lon = 0.0
        self._elev = 0.0
        self.datum = 'WGS84'
        self.data_logger = 'Zonge Zen'
        self.instrument_id = None
        self.calibration_fn = None
        self.declination = 0.0
        self._ts = pd.DataFrame() 
        self.fn_hdf5 = None
        self.fn_ascii = None
        
        self._date_time_fmt = '%Y-%m-%d,%H:%M:%S'
        self._attr_list = ['station',
                           'sampling_rate',
                           'start_time_epoch_sec',
                           'start_time_utc',
                           'n_samples',
                           'component',
                           'coordinate_system',
                           'dipole_length',
                           'elev',
                           'azimuth',
                           'units',
                           'lat', 
                           'lon',
                           'datum',
                           'data_logger',
                           'instrument_id',
                           'calibration_fn',
                           'declination']
        
        for key in kwargs.keys():
            setattr(self, key, kwargs[key])
            
    ###-------------------------------------------------------------
    ## make sure some attributes have the correct data type
    # make sure that the time series is a pandas data frame
    @property
    def ts(self):
        return self._ts
    
    @ts.setter
    def ts(self, ts_arr):
        if type(ts_arr) is np.ndarray:
            self._ts = pd.DataFrame(ts_arr)
        elif type(ts_arr) is pd.core.frame.DataFrame:
            self._ts = ts_arr
        else:
            raise MT_TS_Error('Data type {0} not supported'.format(type(ts_arr))+\
                              ', ts needs to be a numpy.ndarray or pandas DataFrame')
    
    ##--> Latitude
    @property
    def lat(self):
        return self._lat
        
    @lat.setter
    def lat(self, latitude):
        self._lat = gis_tools.assert_lat_value(latitude)
        
    ##--> Longitude
    @property
    def lon(self):
        return self._lon
        
    @lon.setter
    def lon(self, longitude):
        self._lon = gis_tools.assert_lon_value(longitude)
        
    ##--> elevation
    @property
    def elev(self):
        return self._elev
        
    @elev.setter
    def elev(self, elevation):
        self._elev = gis_tools.assert_elevation_value(elevation)
        
    ## time
    @property
    def start_time_utc(self):
        return self._start_time_utc
    
    @start_time_utc.setter
    def start_time_utc(self, start_time):
        try:
            dt = datetime.datetime.strptime(start_time, self._date_time_fmt)
            self._start_time_utc = datetime.datetime.strftime(dt,
                                                              self._date_time_fmt)
              
            # these should be mutually self consistent
            epoch_sec = time.mktime(time.strptime(start_time,
                                                  self._date_time_fmt))
            if self.start_time_epoch_sec != epoch_sec:                                                
                self.start_time_epoch_sec = epoch_sec
                print 'Changed start_time_epoch_sec to {0}'.format(epoch_sec)
        except:
            raise MT_TS_Error('Time not input correctly, input as {0}'.format(self._date_time_fmt)+\
                              ', or change MT_TS._date_time_fmt')
        
    ## epoch seconds
    @property
    def start_time_epoch_sec(self):
        return self._start_time_epoch_sec
        
    @start_time_epoch_sec.setter
    def start_time_epoch_sec(self, epoch_sec):
        self._start_time_epoch_sec = float(epoch_sec)
        
        # these should be self cosistent
        dt_utc = time.strftime(self._date_time_fmt, time.localtime(epoch_sec))
        if self.start_time_utc != dt_utc:
            self.start_time_utc = dt_utc
            print 'Changed start_time_utc to {0}'.format(dt_utc)
        
    
    
    ###------------------------------------------------------------------
    ### read and write file types
    def write_hdf5(self, fn_hdf5):
        """
        use pandas to write the hdf5 file
        """        
        
        self.fn_hdf5 = fn_hdf5
        
        hdf5_store = pd.HDFStore(self.fn_hdf5, 'w')
        hdf5_store['time_series'] = self.ts
        
        # add in attributes
        hdf5_store.get_storer('time_series').attrs.station = self.station
        hdf5_store.get_storer('time_series').attrs.sampling_rate = self.sampling_rate
        hdf5_store.get_storer('time_series').attrs.start_time_epoch_sec = self.start_time_epoch_sec 
        hdf5_store.get_storer('time_series').attrs.start_time_utc = self.start_time_utc
        hdf5_store.get_storer('time_series').attrs.n_samples = self.n_samples
        hdf5_store.get_storer('time_series').attrs.component = self.component
        hdf5_store.get_storer('time_series').attrs.coordinate_system = self.coordinate_system
        hdf5_store.get_storer('time_series').attrs.dipole_length = self.dipole_length
        hdf5_store.get_storer('time_series').attrs.azimuth = self.azimuth
        hdf5_store.get_storer('time_series').attrs.units = self.units
        hdf5_store.get_storer('time_series').attrs.lat = self.lat
        hdf5_store.get_storer('time_series').attrs.lon = self.lon
        hdf5_store.get_storer('time_series').attrs.datum = self.datum
        hdf5_store.get_storer('time_series').attrs.data_logger = self.data_logger
        hdf5_store.get_storer('time_series').attrs.instrument_id = self.instrument_id
        hdf5_store.get_storer('time_series').attrs.calibration_fn = self.calibration_fn
        hdf5_store.get_storer('time_series').attrs.declination = self.declination
        
        hdf5_store.flush()
        hdf5_store.close()
        
    def read_hdf5(self, fn_hdf5):
        """
        read using pandas
        """
        
        self.fn_hdf5 = fn_hdf5

        hdf5_store = pd.HDFStore(self.fn_hdf5, 'r')
        
        self.ts = hdf5_store['time_series']
        
        for attr in self._attr_list:
            value = getattr(hdf5_store.get_storer('time_series').attrs, attr)
            setattr(self, attr, value)
            
        hdf5_store.close()     
        
    def write_ascii_file(self, fn_ascii=None, chunk_size=4096):
        """
        write an ascii format file
        """
        
        st = time.time()
        
        if fn_ascii is not None:
            self.fn_ascii = fn_ascii
        
        if self.fn_ascii is None:
            self.fn_ascii = self.fn_hdf5[:-2]+'txt'
            
        if self.ts is None:
            self.read_hdf5(self.fn_hdf5)

        # get the number of chunks to write        
        chunks = self.ts.shape[0]/chunk_size
            
        # make header lines
        header_lines = ['# MT time series text file for {0}'.format(self.station)]
        header_lines += ['# {0} = {1}'.format(attr, getattr(self, attr)) 
                        for attr in sorted(self._attr_list)]

        # write to file in chunks
        with open(self.fn_ascii, 'w') as fid:
            # write header lines first
            fid.write('\n'.join(header_lines))
    
            # write time series indicator
            fid.write('\n# *** time_series ***\n')
            
            # write in chunks
            for cc in range(chunks):
                # changing the dtype of the array is faster than making
                # a list of strings
                try:
                    ts_lines = np.array(self.ts[cc*chunk_size:(cc+1)*chunk_size][0],
                                        dtype='S20')
                except IndexError:
                    ts_lines = np.array(self.ts[cc*chunk_size:(cc+1)*chunk_size],
                                        dtype='S20')
                fid.write('\n'.join(list(ts_lines)))
                # be sure to write a new line after each chunk otherwise
                # they run together
                fid.write('\n')
             
            # be sure to write the last little bit
            try:
                fid.write('\n'.join(list(np.array(self.ts[(cc+1)*chunk_size:][0],
                                                  dtype='S20'))))
            except IndexError:
                fid.write('\n'.join(list(np.array(self.ts[(cc+1)*chunk_size:],
                                                  dtype='S20'))))
                
        # get an estimation of how long it took to write the file    
        et = time.time()
        time_diff = et-st
        
        print '--> Wrote {0}'.format(self.fn_ascii)
        print '    Took {0:.2f} seconds'.format(time_diff)

    def read_ascii(self, fn_ascii):
        """
        Read in an ascii
        """
        
        self.fn_ascii = fn_ascii
        
        with open(self.fn_ascii, 'r') as fid:
            line = fid.readline()
            count = 0
            while line.find('#') == 0:
                line_list = line[1:].strip().split('=')
                if len(line_list) == 2:
                    key = line_list[0].strip()
                    try:
                        value = float(line_list[1].strip())
                    except ValueError:
                        value = line_list[1].strip()
                    setattr(self, key, value)
                count +=1
                line = fid.readline()
        
        self.ts = pd.read_csv(self.fn_ascii, sep='\n', skiprows=count,
                              memory_map=True)
        
        print 'Read in {0}'.format(self.fn_ascii)
                
#==============================================================================
# Error classes
#==============================================================================
class MT_TS_Error(Exception):
    pass        
 
#==============================================================================
#  
#==============================================================================





