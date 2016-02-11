from .lims_lcMethod_postgresql_models import *
from SBaaS_base.sbaas_base_query_update import sbaas_base_query_update
from SBaaS_base.sbaas_base_query_drop import sbaas_base_query_drop
from SBaaS_base.sbaas_base_query_initialize import sbaas_base_query_initialize
from SBaaS_base.sbaas_base_query_insert import sbaas_base_query_insert
from SBaaS_base.sbaas_base_query_select import sbaas_base_query_select
from SBaaS_base.sbaas_base_query_delete import sbaas_base_query_delete

from SBaaS_base.sbaas_template_query import sbaas_template_query

class lims_lcMethod_query(sbaas_template_query):

    def initialize_supportedTables(self):
        '''Set the supported tables dict for 
        '''
        tables_supported = {'lc_elution':lc_elution,
            'lc_gradient':lc_gradient,
            'lc_information':lc_information,
            'lc_method':lc_method,
            'lc_parameters':lc_parameters,
                        };
        #table initializations:
    def drop_lcMethod_tables(self):
        try:
            lc_information.__table__.drop(self.engine,True);
            lc_gradient.__table__.drop(self.engine,True);
            lc_parameters.__table__.drop(self.engine,True);
            lc_method.__table__.drop(self.engine,True);
            lc_elution.__table__.drop(self.engine,True);
        except SQLAlchemyError as e:
            print(e);
    def reset_lcMethod_tables(self):
        try:
            reset = self.session.query(lc_information).delete(synchronize_session=False);
            reset = self.session.query(lc_gradient).delete(synchronize_session=False);
            reset = self.session.query(lc_parameters).delete(synchronize_session=False);
            reset = self.session.query(lc_method).delete(synchronize_session=False);
            reset = self.session.query(lc_elution).delete(synchronize_session=False);

            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def initialize_lcMethod_tables(self):
        try:
            lc_information.__table__.create(self.engine,True);
            lc_gradient.__table__.create(self.engine,True);
            lc_parameters.__table__.create(self.engine,True);
            lc_method.__table__.create(self.engine,True);
            lc_elution.__table__.create(self.engine,True);

        except SQLAlchemyError as e:
            print(e);