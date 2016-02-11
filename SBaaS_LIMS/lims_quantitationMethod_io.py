#from .lims_msMethod_query import lims_msMethod_query
from SBaaS_LIMS.lims_calibratorsAndMixes_query import lims_calibratorsAndMixes_query
from SBaaS_LIMS.lims_sample_query import lims_sample_query
from .lims_quantitationMethod_query import lims_quantitationMethod_query
from SBaaS_base.sbaas_template_io import sbaas_template_io

# Resources
from io_utilities.base_importData import base_importData
from io_utilities.base_exportData import base_exportData

class lims_quantitationMethod_io(lims_quantitationMethod_query,
                                 lims_calibratorsAndMixes_query,
                                #lims_msMethod_query,
                                lims_sample_query,
                                sbaas_template_io
                                ):
        
    def export_calibrationConcentrations(self, data, filename):
        '''export calibration curve concentrations'''

        # write calibration curve concentrations to file
        export = base_exportData(data);
        export.write_dict2csv(filename);

    def import_quantitationMethod_add(self,QMethod_id_I, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_quantitationMethod(QMethod_id_I, data.data);
        data.clear_data();