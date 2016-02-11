from .lims_acquisitionMethod_io import lims_acquisitionMethod_io

class lims_acquisitionMethod_execute(lims_acquisitionMethod_io):
    def execute_exportAcqusitionMethod(self,lc_method_I,ms_mode_I,ms_methodtype_I,filename_I):
        '''export the current acqusition method'''
        # get the data
        amethod = [];
        amethod = self.get_acqusitionMethod(lc_method_I,ms_mode_I,ms_methodtype_I);
        # export the data to csv
        self.export_acquisitionMethod(amethod, filename_I);
