from .lims_sample_postgresql_models import *
from .lims_sample_query import lims_sample_query
from .lims_biologicalMaterial_query import lims_biologicalMaterial_query
from SBaaS_base.sbaas_template_io import sbaas_template_io

# Resources
from io_utilities.base_importData import base_importData
from io_utilities.base_exportData import base_exportData

class lims_sample_io(lims_sample_query,
                     lims_biologicalMaterial_query,
                     sbaas_template_io):

    def import_sampleDescription_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_sampleDescription(data.data);
        data.clear_data();

    def import_sampleDescription_update(self, filename):
        '''table updates'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_sampleDescription(data.data);
        data.clear_data();

    def export_sampleStorage_csv(self, sample_ids_I, filename_O):
        """Export sample storage to .csv
        INPUT:
        sample_ids_I = [] of string, sample_id
        filename_O = string, filename for export"""

        data_O = [];
        for sample_id in sample_ids_I:
            data_tmp =[];
            data_tmp = self.get_rows_sampleID_limsSampleStorage(sample_id);
            data_O.extend(data_tmp);
        if data_O:
            io = base_exportData(data_O);
            io.write_dict2csv(filename_O);