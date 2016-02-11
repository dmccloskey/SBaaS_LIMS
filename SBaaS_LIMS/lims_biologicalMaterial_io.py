from .lims_biologicalMaterial_query import lims_biologicalMaterial_query
from SBaaS_base.sbaas_template_io import sbaas_template_io

# Resources
from io_utilities.base_importData import base_importData
from io_utilities.base_exportData import base_exportData

class lims_biologicalMaterial_io(lims_biologicalMaterial_query,sbaas_template_io):
    
    def import_biologicalMaterialDescription_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_biologicalMaterialDescription(data.data);
        data.clear_data();

    def import_biologicalMaterialGeneReferences_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_biologicalMaterialGeneReferences(data.data);
        data.clear_data();

    def import_biologicalMaterialGeneReferences_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_biologicalMaterialGeneReferences(data.data);
        data.clear_data();
        data.clear_data();

    def import_biologicalMaterialMassVolumeConversion_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_biologicalMaterialMassVolumeConversion(data.data);
        data.clear_data();

    def import_biologicalMaterialMassVolumeConversion_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_biologicalMaterialMassVolumeConversion(data.data);
        data.clear_data();