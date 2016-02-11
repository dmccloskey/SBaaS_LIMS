from .lims_calibratorsAndMixes_postgresql_models import *
from .lims_calibratorsAndMixes_query import lims_calibratorsAndMixes_query
from SBaaS_base.sbaas_template_io import sbaas_template_io

# Resources
from io_utilities.base_importData import base_importData
from io_utilities.base_exportData import base_exportData

class lims_calibratorsAndMixes_io(lims_calibratorsAndMixes_query,sbaas_template_io):

    def import_calibratorConcentrations_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_calibratorConcentrations(data.data);
        data.clear_data();

    def export_calibratorConcentrations_csv(self,filename,met_ids_I=[]):
        '''export calibrator concentrations'''
        data_O = [];
        if met_ids_I:
            met_ids = met_ids_I;
        else:
            met_ids = [];
            met_ids = self.get_metIDs_calibratorConcentrations();
        for met_id in met_ids:
            rows = [];
            rows = self.get_rows_metID_calibratorConcentrations(met_id);
            data_O.extend(rows);

        export = base_exportData(data_O);
        export.write_dict2csv(filename);


