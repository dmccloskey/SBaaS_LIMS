
from .lims_msMethod_query import lims_msMethod_query
from SBaaS_base.sbaas_template_io import sbaas_template_io

# Resources
from io_utilities.base_importData import base_importData
from io_utilities.base_exportData import base_exportData

class lims_msMethod_io(lims_msMethod_query,sbaas_template_io):
    def import_MSComponents_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_MSComponents(data.data);
        data.clear_data();

    def import_MSComponentList_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_MSComponentList(data.data);
        data.clear_data();

    def import_MSMethod_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_MSMethod(data.data);
        data.clear_data();

    def import_MSSourceParameters_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_MSSourceParameters(data.data);
        data.clear_data();

    def import_MSInformation_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_MSInformation(data.data);
        data.clear_data();