from .lims_oligos_query import lims_oligos_query
from SBaaS_base.sbaas_template_io import sbaas_template_io

class lims_oligos_io(lims_oligos_query,sbaas_template_io):

    def import_oligosStorage_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_oligosStorage(data.data);
        data.clear_data();

    def import_oligosDescription_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_oligosDescription(data.data);
        data.clear_data();