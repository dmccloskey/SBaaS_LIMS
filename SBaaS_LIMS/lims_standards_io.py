from .lims_standards_query import lims_standards_query
# Resources
from io_utilities.base_importData import base_importData
from io_utilities.base_exportData import base_exportData
from SBaaS_base.sbaas_template_io import sbaas_template_io

class lims_standards_io(lims_standards_query,sbaas_template_io):
    def import_standards_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_standards(data.data);
        data.clear_data();
    def import_standards_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_standards(data.data);
        data.clear_data();
    def import_standardsOrdering_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_standardsOrdering(data.data);
        data.clear_data();
    def import_standardsOrdering_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_standardsOrdering(data.data);
        data.clear_data();