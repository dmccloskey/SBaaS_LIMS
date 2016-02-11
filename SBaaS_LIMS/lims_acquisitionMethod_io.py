
from .lims_lcMethod_query import lims_lcMethod_query
from .lims_autosamplerMethod_query import lims_autosamplerMethod_query
from .lims_msMethod_query import lims_msMethod_query
from .lims_acquisitionMethod_query import lims_acquisitionMethod_query
# Resources
from io_utilities.base_importData import base_importData
from io_utilities.base_exportData import base_exportData
from SBaaS_base.sbaas_template_io import sbaas_template_io

class lims_acquisitionMethod_io(
    lims_acquisitionMethod_query,
    lims_lcMethod_query,
    lims_autosamplerMethod_query,
    lims_msMethod_query,
    sbaas_template_io,
    ):

    def import_AcquisitionMethod_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_AcquisitionMethod(data.data);
        data.clear_data();

    def export_acquisitionMethod(self, data, filename):
        '''export acquisition method'''

        # write acquisition method to file
        export = base_exportData(data);
        export.write_dict2csv(filename);