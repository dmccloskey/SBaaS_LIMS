from .lims_internalStandards_postgresql_models import *

from SBaaS_base.sbaas_base_query_update import sbaas_base_query_update
from SBaaS_base.sbaas_base_query_drop import sbaas_base_query_drop
from SBaaS_base.sbaas_base_query_initialize import sbaas_base_query_initialize
from SBaaS_base.sbaas_base_query_insert import sbaas_base_query_insert
from SBaaS_base.sbaas_base_query_select import sbaas_base_query_select
from SBaaS_base.sbaas_base_query_delete import sbaas_base_query_delete

from SBaaS_base.sbaas_template_query import sbaas_template_query

class lims_internalStandards_query(sbaas_template_query):

    def initialize_supportedTables(self):
        '''Set the supported tables dict for 
        '''
        tables_supported = {'internal_standard':internal_standard,
                            'internal_standard_storage':internal_standard_storage
                        };
        self.set_supportedTables(tables_supported);
        #table initializations:
    def drop_lims_internalStandards(self):
        try:
            internal_standard.__table__.drop(self.engine,True);
            internal_standard_storage.__table__.drop(self.engine,True);
        except SQLAlchemyError as e:
            print(e);
    def reset_lims_internalStandards(self):
        try:
            reset = self.session.query(internal_standard).delete(synchronize_session=False);
            reset = self.session.query(internal_standard_storage).delete(synchronize_session=False);

            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def initialize_lims_internalStandards(self):
        try:
            internal_standard.__table__.create(self.engine,True);
            internal_standard_storage.__table__.create(self.engine,True);

        except SQLAlchemyError as e:
            print(e);