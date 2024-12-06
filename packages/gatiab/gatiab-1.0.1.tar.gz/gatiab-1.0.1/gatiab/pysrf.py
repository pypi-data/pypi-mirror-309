#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import h5py
from glob import glob



def SRF(sensor=None, camera=None, dir_SRFs = './', minT = 0.005):
    '''
    Arguments:
        sensor : one sensor name in the list return by SRF()
        camera : eventually a camera name (str) for a sensor
        
    returns:
        (wvn_limits, wvl_limits, fwhm, wvl_central, rod_effective, srf_wvl, rsrf)
        with wvn in cm-1, wvl in nm, fwhm in nm, wvl_central in nm, 
        reference wavelegnth of the rsrf in nm, rsrf, name (string)
    '''

    dir_EUMETSAT_SRFs = dir_SRFs + 'EUMETSAT-SAF-SRFs/'
   
    if sensor is None: 
        list_sensor_eumetsat = np.sort([f.split('/')[-1][7:-8].upper() for f in glob(dir_EUMETSAT_SRFs+'*tar')])
        list_sensor_special  = ['SENTINEL3_1_OLCI', 'SENTINEL3_2_OLCI', 'VGT1', 'VGT2', 'Proba-V',\
                                'LANDSAT_8_OLI', 'EOS_1_MISR', 'ENVISAT_MERIS']
        a=''
        for s in list_sensor_eumetsat:
            if a=='': a=a+s
            else : a=a+','+s
        for s in list_sensor_special:
            a=a+','+s
            
        return a
    
    if (sensor=='Proba-V' and camera is None) : 
        print('{} sensor: camera needed : LEFT,RIGHT,CENTER,\ndefault CENTER'.format(sensor))
        camera='CENTER'
    xLimits = []
    fwhm    = []
    central_wvl = []
    srf_wvl = [] 
    srf     = []
    name    = []

    if 'LANDSAT' in sensor :
        platform = sensor[:8]
        fsrf   = dir_SRFs + 'OLI/LANDSAT8/Ball_BA_RSR.v1.2.xlsx'
        data   = pd.read_excel(fsrf, sheet_name='Band summary')
        bandnames = data['Band'][1:]
        for band in bandnames:
            if band=='CA' : band='CoastalAerosol'
            data = pd.read_excel(fsrf, sheet_name=band)
            srf_ = np.array(data['BA RSR [watts]'])
            srf_ = srf_/srf_.max() # normalize SRF
            ok   = srf_ > 0.005 # subset only minimum transmission
            srf_ = srf_[ok]
            srf_wvl_ = np.array(data['Wavelength'])
            srf_wvl_ = srf_wvl_[ok]
            fwhm .append(srf_wvl_[srf_>0.5][-1] - srf_wvl_[srf_>0.5][0])
            central_wvl.append((srf_wvl_[srf_>0.5][-1] + srf_wvl_[srf_>0.5][0]) * 0.5)
            xLimits.append([1e7/(srf_wvl_.max()+1.), 1e7/(srf_wvl_.min()-1.)])
            srf_wvl.append(srf_wvl_)
            srf.append(srf_)
            name.append(band)

    elif 'MISR' in sensor :
        platform = sensor[:5]
        f= dir_SRFs + 'MISR/Terra/MISR_SRF.txt'
        dat = np.loadtxt(f, skiprows=18, delimiter=',')
        nb  = dat[0,2:].size
        for i in np.arange(nb):
            srf_ = dat[:,i+2]/dat[:,i+2].max() # normalize SRF
            ok   = srf_ > 0.005 # subset only minimum transmission
            srf_ = srf_[ok]
            srf_wvl_ = dat[:,0]
            srf_wvl_ = srf_wvl_[ok]
            fwhm .append(srf_wvl_[srf_>0.5][-1] - srf_wvl_[srf_>0.5][0])
            central_wvl.append((srf_wvl_[srf_>0.5][-1] + srf_wvl_[srf_>0.5][0]) * 0.5)
            xLimits.append([1e7/(srf_wvl_.max()+1.), 1e7/(srf_wvl_.min()-1.)])
            srf_wvl.append(srf_wvl_ )
            srf.append(srf_)
            
    elif ('VGT' in sensor) or ('Proba' in sensor) :
        fsrfs  = glob(dir_SRFs + 'VGT/VGT_SRF.XLSX')
        data   = pd.read_excel(fsrfs[0], sheet_name=sensor)
        if sensor=='Proba-V' : 
            data.rename(index=str, columns={"NIR  CENTER": "NIR CENTER"}, inplace=True)
            sensor2 = sensor+'-'+camera
        else : sensor2 = sensor
        for band in ['BLUE','RED','NIR','SWIR']:
            if sensor2=='Proba-V-CENTER' :
                srf_wvl_     = np.array(data['wvl_{}'.format(band)].values)
                srf_         = np.array(data['{} CENTER'.format(band)].values)
            elif sensor2=='Proba-V-LEFT' :
                srf_wvl_     = np.array(data['wvl_{}'.format(band)].values)
                srf_         = np.array(data['{} LEFT'.format(band)].values)
            elif sensor2=='Proba-V-RIGHT' :
                srf_wvl_     = np.array(data['wvl_{}'.format(band)].values)
                srf_         = np.array(data['{} RIGHT'.format(band)].values)
            elif sensor2=='VGT1' :
                srf_wvl_     = np.array(data['wavelength'].values)*1e3
                srf_         = np.array(data['{} {}'.format(band, sensor)].values)
            else :
                srf_wvl_     = np.array(data['wavelength'].values)
                srf_         = np.array(data['{} {}'.format(band, sensor)].values)    
            srf_ /= np.nanmax(srf_) # normalize SRF
            ok = srf_ > 0.005 # subset only minimum transmission
            srf_ = srf_[ok]
            srf_wvl_ = srf_wvl_[ok]
            fwhm .append(srf_wvl_[srf_>0.5][-1] - srf_wvl_[srf_>0.5][0])
            central_wvl.append((srf_wvl_[srf_>0.5][-1] + srf_wvl_[srf_>0.5][0]) * 0.5)
            xLimits.append([1e7/(srf_wvl_.max()+1.), 1e7/(srf_wvl_.min()-1.)])
            srf_wvl.append(srf_wvl_ )
            srf.append(srf_)
            name.append(band)
            
    elif 'OLCI' in sensor:
        platform = sensor[:11]
        if platform=='SENTINEL3_1' : fsrf=h5py.File(dir_SRFs + 'OLCI/S3A/S3A_OL_SRF_20160713_mean_rsr.nc4', "r")
        else                       : fsrf=h5py.File(dir_SRFs + 'OLCI/S3B/S3B_OL_SRF_0_20180109_mean_rsr.nc4', "r")
        central_wvl_i = np.copy(fsrf[u'srf_centre_wavelength'])
        srf_wvl_i   = np.copy(fsrf[u"mean_spectral_response_function_wavelength"])
        srf_i       = np.copy(fsrf[u"mean_spectral_response_function"])
        fsrf.close()
        for i in np.arange(len(central_wvl_i)):
            srf_ = srf_i[i,:]/srf_i[i,:].max() # normalize SRF
            ok   = srf_ > minT # subset only minimum transmission
            srf_ = srf_[ok]
            srf_wvl_ = srf_wvl_i[i,:]
            srf_wvl_ = srf_wvl_[ok]
            fwhm .append(srf_wvl_[srf_>0.5][-1] - srf_wvl_[srf_>0.5][0])
            central_wvl.append((srf_wvl_[srf_>0.5][-1] + srf_wvl_[srf_>0.5][0]) * 0.5)
            xLimits.append([1e7/(srf_wvl_.max()+1.), 1e7/(srf_wvl_.min()-1.)])
            srf_wvl.append(srf_wvl_ )
            srf.append(srf_)
            name.append("band Oa{:02d}".format(i+1))

    elif 'MERIS' in sensor:
        platform = 'ENVISAT'
        fsrfs    = pd.read_excel(dir_SRFs + 'MERIS/MERIS_NominalSRF_Model2004.xls', sheet_name='NominalSRF Model2004', skiprows=1)
        for i in range(15):
            if i==0 : st=''
            else :  st='.'+str(i)
            srf_wvl_ = np.array(fsrfs['wavelength' + st])
            srf_wvl_ = srf_wvl_[np.isfinite(srf_wvl_)]
            srf_     = np.array(fsrfs['SRF' + st])
            srf_     = srf_[np.isfinite(srf_)]
            srf_ /= srf_.max() # normalize SRF
            ok = srf_ > minT # subset only minimum transmission
            srf_ = srf_[ok]
            srf_wvl_ = srf_wvl_[ok] 
            fwhm .append(srf_wvl_[srf_>0.5][-1] - srf_wvl_[srf_>0.5][0])
            central_wvl.append((srf_wvl_[srf_>0.5][-1] + srf_wvl_[srf_>0.5][0]) * 0.5)
            xLimits.append([1e7/(srf_wvl_.max()+1.), 1e7/(srf_wvl_.min()-1.)])
            srf_wvl.append(srf_wvl_ )
            srf.append(srf_)
            name.append('band %i'%i)
            
    else:
        fsrfs = glob(dir_EUMETSAT_SRFs + 'rtcoef_'+sensor.lower()+'_srf*.txt') 

        for f in np.sort(fsrfs):
            name.append(open(f,"r").readline()[:-1])
            fsrf         = np.loadtxt(f, skiprows=4)
            srf_wvl_     = np.float64(1e7)/np.float64(fsrf[:,0][::-1])
            srf_         = fsrf[:,1][::-1]
            srf_ /= srf_.max() # normalize SRF
            ok = srf_ > minT # subset only minimum transmission
            srf_ = srf_[ok]
            srf_wvl_ = srf_wvl_[ok] 
            fwhm .append(srf_wvl_[srf_>0.5][-1] - srf_wvl_[srf_>0.5][0])
            central_wvl.append((srf_wvl_[srf_>0.5][-1] + srf_wvl_[srf_>0.5][0]) * 0.5)
            xLimits.append([1e7/(srf_wvl_.max()+1.), 1e7/(srf_wvl_.min()-1.)])
            srf_wvl.append(srf_wvl_ )
            srf.append(srf_)
    
    # wavelengths intervals
    central_wvl = np.array(central_wvl)
    fwhm = np.array(fwhm)
    #srf = np.array(srf)
    #srf_wvl = np.array(srf_wvl)
    ODR = []

    return np.array(xLimits), 1e7/np.array(xLimits)[:,::-1], fwhm, central_wvl, srf_wvl, srf, np.array(name)