from .lims_oligos_postgresql_models import *

from SBaaS_base.sbaas_base_query_update import sbaas_base_query_update
from SBaaS_base.sbaas_base_query_drop import sbaas_base_query_drop
from SBaaS_base.sbaas_base_query_initialize import sbaas_base_query_initialize
from SBaaS_base.sbaas_base_query_insert import sbaas_base_query_insert
from SBaaS_base.sbaas_base_query_select import sbaas_base_query_select
from SBaaS_base.sbaas_base_query_delete import sbaas_base_query_delete

from SBaaS_base.sbaas_template_query import sbaas_template_query

class lims_oligos_query(sbaas_template_query):

    def initialize_supportedTables(self):
        '''Set the supported tables dict for 
        '''
        tables_supported = {'oligos_description':oligos_description,
                            'oligos_storage':oligos_storage
                        };
        self.set_supportedTables(tables_supported);
        #table initializations:
    def drop_oligos_tables(self):
        try:
            oligos_description.__table__.drop(self.engine,True);
            oligos_storage.__table__.drop(self.engine,True);

        except SQLAlchemyError as e:
            print(e);
    def reset_oligos_tables(self):
        try:
            reset = self.session.query(oligos_description).delete(synchronize_session=False);
            reset = self.session.query(oligos_storage).delete(synchronize_session=False);

            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def initialize_oligos_tables(self):
        try:
            oligos_description.__table__.create(self.engine,True);
            oligos_storage.__table__.create(self.engine,True);

        except SQLAlchemyError as e:
            print(e);

    def add_oligosStorage(self, data_I):
        '''add rows of oligos_storage'''
        if data_I:
            for d in data_I:
                try:
                    data_add = oligos_storage(d
                        #d['oligos_id'],
                        #d['oligos_label'],
                        #d['oligos_box'],
                        #d['oligos_posstart'],
                        #d['oligos_posend'],
                        #d['oligos_date'],
                        #d['oligos_storagebuffer'],
                        #d['oligos_concentration'],
                        #d['oligos_concentration_units']
                        );
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def add_oligosDescription(self, data_I):
        '''add rows of oligos_description'''
        if data_I:
            for d in data_I:
                try:
                    data_add = oligos_description(d
                        #d['oligos_id'],
                        #d['oligos_sequence'],
                        #d['oligos_purification'],
                        #d['oligos_description'],
                        #d['oligos_notes']
                                                    );
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();