from .lims_extractionMethod_postgresql_models import *
from SBaaS_base.sbaas_base_query_update import sbaas_base_query_update
from SBaaS_base.sbaas_base_query_drop import sbaas_base_query_drop
from SBaaS_base.sbaas_base_query_initialize import sbaas_base_query_initialize
from SBaaS_base.sbaas_base_query_insert import sbaas_base_query_insert
from SBaaS_base.sbaas_base_query_select import sbaas_base_query_select
from SBaaS_base.sbaas_base_query_delete import sbaas_base_query_delete

from SBaaS_base.sbaas_template_query import sbaas_template_query

class lims_extractionMethod_query(sbaas_template_query):

    def initialize_supportedTables(self):
        '''Set the supported tables dict for 
        '''
        tables_supported = {'extraction_method':extraction_method
                        };
        self.set_supportedTables(tables_supported);
        #table initializations:
    def drop_lims_extractionMethod(self):
        try:
            extraction_method.__table__.drop(self.engine,True);

        except SQLAlchemyError as e:
            print(e);
    def reset_lims_extractionMethod(self):
        try:
            reset = self.session.query(extraction_method).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def initialize_lims_extractionMethod(self):
        try:
            extraction_method.__table__.create(self.engine,True);
        except SQLAlchemyError as e:
            print(e);