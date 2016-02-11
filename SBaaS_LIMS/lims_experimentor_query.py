from .lims_experimentor_postgresql_models import *

from SBaaS_base.sbaas_base_query_update import sbaas_base_query_update
from SBaaS_base.sbaas_base_query_drop import sbaas_base_query_drop
from SBaaS_base.sbaas_base_query_initialize import sbaas_base_query_initialize
from SBaaS_base.sbaas_base_query_insert import sbaas_base_query_insert
from SBaaS_base.sbaas_base_query_select import sbaas_base_query_select
from SBaaS_base.sbaas_base_query_delete import sbaas_base_query_delete

from SBaaS_base.sbaas_template_query import sbaas_template_query

class lims_experimentor_query(sbaas_template_query):
    def initialize_supportedTables(self):
        '''Set the supported tables dict for 
        '''
        tables_supported = {"experimentor_id2name":experimentor_id2name,
                            "experimentor":experimentor,
                            "experimentor_list":experimentor_list,
                        };
        self.set_supportedTables(tables_supported);
    
    #table initializations:
    def drop_lims_experimentor(self):
        try:
            experimentor_id2name.__table__.drop(self.engine,True);
            experimentor.__table__.drop(self.engine,True);
            experimentor_list.__table__.drop(self.engine,True);
        except SQLAlchemyError as e:
            print(e);
    def reset_lims_experimentor(self):
        try:
            reset = self.session.query(experimentor_id2name).delete(synchronize_session=False);
            reset = self.session.query(experimentor).delete(synchronize_session=False);
            reset = self.session.query(experimentor_list).delete(synchronize_session=False);

            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def initialize_lims_experimentor(self):
        try:
            experimentor_id2name.__table__.create(self.engine,True);
            experimentor.__table__.create(self.engine,True);
            experimentor_list.__table__.create(self.engine,True);

        except SQLAlchemyError as e:
            print(e);