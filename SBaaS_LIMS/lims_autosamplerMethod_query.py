from .lims_autosamplerMethod_postgresql_models import *

from SBaaS_base.sbaas_base_query_update import sbaas_base_query_update
from SBaaS_base.sbaas_base_query_drop import sbaas_base_query_drop
from SBaaS_base.sbaas_base_query_initialize import sbaas_base_query_initialize
from SBaaS_base.sbaas_base_query_insert import sbaas_base_query_insert
from SBaaS_base.sbaas_base_query_select import sbaas_base_query_select
from SBaaS_base.sbaas_base_query_delete import sbaas_base_query_delete

from SBaaS_base.sbaas_template_query import sbaas_template_query

class lims_autosamplerMethod_query(sbaas_template_query):
    def initialize_supportedTables(self):
        '''Set the supported tables dict for 
        '''
        tables_supported = {'autosampler_parameters':autosampler_parameters,
                            'autosampler_information':autosampler_information,
                            'autosampler_method':autosampler_method,
                        };
        self.set_supportedTables(tables_supported);
    
    #table initializations:
    def drop_lims_autosamplerMethod(self):
        try:
            autosampler_parameters.__table__.drop(self.engine,True);
            autosampler_information.__table__.drop(self.engine,True);
            autosampler_method.__table__.drop(self.engine,True);

        except SQLAlchemyError as e:
            print(e);
    def reset_lims_autosamplerMethod(self):
        try:
            reset = self.session.query(autosampler_parameters).delete(synchronize_session=False);
            reset = self.session.query(autosampler_information).delete(synchronize_session=False);
            reset = self.session.query(autosampler_method).delete(synchronize_session=False);

            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def initialize_lims_autosamplerMethod(self):
        try:
            autosampler_parameters.__table__.create(self.engine,True);
            autosampler_information.__table__.create(self.engine,True);
            autosampler_method.__table__.create(self.engine,True);

        except SQLAlchemyError as e:
            print(e);