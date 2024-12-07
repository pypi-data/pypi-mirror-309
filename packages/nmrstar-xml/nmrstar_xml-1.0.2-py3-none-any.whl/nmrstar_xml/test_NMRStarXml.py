# !/usr/bin/env python3
from unittest import TestCase


import os.path
import pynmrstar
import sys
import xml.etree.ElementTree as ET
import xml.dom.minidom
from .translate import NMRStarXml


class TestNMRStarXml(TestCase):
    TFILE = "/tmp/example.nex"
    def setUp(self):
        with open(self.TFILE,'w') as f:
            print(self.__EXAMPLE,file=f)

    def test_star_entry(self):
        PRINT = False
        PY3 = (sys.version_info[0] == 3)
        e = pynmrstar.Entry.from_file(self.TFILE)
        ns = NMRStarXml()
        etree = ns.star_entry(e)
        root = etree.getroot()
        back = ns.xml_entry(root)
        if PRINT:
            if PY3:
                s = ET.tostring(root, encoding='unicode')
            else:
                s = ET.tostring(root)
            dom = xml.dom.minidom.parseString(s)
            print(dom.toprettyxml())
            print(back)
        delta = e.compare(back)
        if delta:
            print(delta)
            self.fail()


    __EXAMPLE = """data_NUS_schedule

##################################################
save_NEX_format_information

        _NEX.Sf_category                   NEX_information
        _NEX.Format_version                0.54
        _NEX.Format_date                   2017-02-21
	
save_
	
##################################################
save_FID_sampling

    _FID_sampling.Sf_category              FID_sampling                                    
    _FID_sampling.ID                       1     
    _FID_sampling.Software_ID		       2
    _FID_sampling.Software_name		'schedule generator'                          
    _FID_sampling.Experiment_name                          HN-HSQC
    _FID_sampling.Dimension_count                          2                                                
    _FID_sampling.Layout_hypercomplex_component_type       full                                            
    _FID_sampling.Layout_transient_type                    uniform                                         
    _FID_sampling.Expt_quadrature_class                    na                                              
    _FID_sampling.Expt_redfield_trick                      no                                             

  
    loop_            # Keep schedule base parameters and values in one loop.
        _FID_sampling_base.Spectral_dim       
        _FID_sampling_base.Parameter
        _FID_sampling_base.Parameter_value
        _FID_sampling_base.Param_tag

         2         time_series_type    linear          '_Schedule.Time_index_dim2'
         2         time_multiplier     0.000010         na 
         2         time_offset         0                na
         2         time_units          sec              na
         2         phase_series_type   linear          '_Schedule.Phase_index_dim2'
         2         phase_multiplier    90               na
         2         phase_offset        0                na
         2         phase_units         degree           na

    stop_

    
    loop_                                                                                               
        _Schedule.FID_ID                                                                                  
        _Schedule.Time_index_dim2
        _Schedule.Phase_index_dim2                                                                        
        _Schedule.Transient_count
        _Schedule.FID_weight

        1  0  0   16  1.0                                                                            
        2  0  1   16  1.0                                                       
                                                       
    stop_                                                                                               

save_


##################################################
save_NEX_converter

    _Software.Sf_category                             'software'                                        
    _Software.Type                                    'schedule converter'                              
    _Software.ID                                      1                                                 
    _Software.Name                                    'NUS schedule converter'                 
    _Software.Version                                 0.7                                               
    _Software.DOI                                     na                                               
    _Software.Details                                 
;
Text field used to report additional information relevant to the software.
;                              

    loop_                                                                                               
        _Vendor.Name                                                                                        
        _Vendor.Address                                                                                     
        _Vendor.Electronic_address                                                                                                                                                          

        'Adam Schuyler - NMRbox' 'UConn Health / UW' 'schuyler@uchc.edu'                                                 
    stop_                                                                                               

    loop_                                                                                               
        _Task.Task                                                                                                                                                                           

        'Convert NUS schedules into NMR-STAR standardized format'                                               
    stop_                                                                                               

save_

##################################################
save_schedule_generator

    _Software.Sf_category                             'software'                                        
    _Software.Type                                    'schedule generator'                              
    _Software.ID                                      2                                                 
    _Software.Name                                    'schedule generator'                                               
    _Software.Version                                 na                                               
    _Software.DOI                                     na                                               
    _Software.Details                                 na                                              

    loop_                                                                                               
        _Vendor.Name                                                                                        
        _Vendor.Address                                                                                     
        _Vendor.Electronic_address                                                                                  

        na na na                                                                                     
    stop_                                                                                               

    loop_                                                                                               
        _Task.Task                                                                                  

        na                                                                                              
    stop_                                                                                               

save_
"""
