from .lims_standards_postgresql_models import *
from SBaaS_base.sbaas_base_query_update import sbaas_base_query_update
from SBaaS_base.sbaas_base_query_drop import sbaas_base_query_drop
from SBaaS_base.sbaas_base_query_initialize import sbaas_base_query_initialize
from SBaaS_base.sbaas_base_query_insert import sbaas_base_query_insert
from SBaaS_base.sbaas_base_query_select import sbaas_base_query_select
from SBaaS_base.sbaas_base_query_delete import sbaas_base_query_delete

from SBaaS_base.sbaas_template_query import sbaas_template_query

class lims_standards_query(sbaas_template_query):
    def initialize_supportedTables(self):
        '''Set the supported tables dict for 
        '''
        tables_supported = {'standards':standards,
            'standards_ordering':standards_ordering,
            'standards_storage':standards_storage,
            'standards2material':standards2material,
                        };
        self.set_supportedTables(tables_supported);
    #table initializations:
    def drop_lims_standards(self):
        try:
            standards.__table__.drop(self.engine,True);
            standards_ordering.__table__.drop(self.engine,True);
            standards2material.__table__.drop(self.engine,True);
            standards_storage.__table__.drop(self.engine,True);
        except SQLAlchemyError as e:
            print(e);
    def reset_lims_standards(self):
        try:
            reset = self.session.query(standards).delete(synchronize_session=False);
            reset = self.session.query(standards_ordering).delete(synchronize_session=False);
            reset = self.session.query(standards2material).delete(synchronize_session=False);
            reset = self.session.query(standards_storage).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def initialize_lims_standards(self):
        try:
            standards.__table__.create(self.engine,True);
            standards_ordering.__table__.create(self.engine,True);
            standards2material.__table__.create(self.engine,True);
            standards_storage.__table__.create(self.engine,True);

        except SQLAlchemyError as e:
            print(e);

    def add_standards(self, data_I):
        '''add rows of metabolomics_standard'''
        if data_I:
            for d in data_I:
                try:
                    data_add = standards(d
                        #d['met_id'],
                        #d['met_name'],
                        #d['formula'],
                        #d['hmdb'],
                        #d['solubility'],
                        #d['solubility_units'],
                        #d['mass'],
                        #d['cas_number'],
                        #d['keggid'],
                        #d['structure_file'],
                        #d['structure_file_extention']
                        );
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def update_standards(self,data_I):
        '''update rows of standards'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(standards).filter(
                            standards.met_id.like(d['met_id'])).update(
                            {'met_id':d['met_id'],
                            'met_name':d['met_name'],
                            'formula':d['formula'],
                            'hmdb':d['hmdb'],
                            'solubility':d['solubility'],
                            'solubility_units':d['solubility_units'],
                            'mass':d['mass'],
                            'cas_number':d['cas_number'],
                            'keggid':d['keggid'],
                            'structure_file':d['structure_file'],
                            'structure_file_extention':d['structure_file_extention']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def update_standards_structureFile(self,data_I):
        '''update rows of standards'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(standards).filter(
                            standards.met_id.like(d['met_id'])).update(
                            {'structure_file':d['structure_file'],
                            'structure_file_extention':d['structure_file_extention']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def update_standards_formulaAndMass(self,data_I):
        '''update rows of standards'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(standards).filter(
                            standards.met_id.like(d['met_id'])).update(
                            {'formula':d['formula'],
                            'mass':d['mass'],
                            'exactmass':d['exactmass']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def add_standardsOrdering(self, data_I):
        '''add rows of standards_ordering'''
        if data_I:
            for d in data_I:
                try:
                    data_add = standards_ordering(d
                        #d['met_id'],
                        #d['met_name'],
                        #d['hillcrest'],
                        #d['provider'],
                        #d['provider_reference'],
                        #d['price'],
                        #d['amount'],
                        #d['amount_units'],
                        #d['purity'],
                        #d['mw'],
                        #d['notes'],
                        #d['powderdate_received'],
                        #d['powderdate_opened'],
                        #d['order_standard'],
                        #d['standards_storage'],
                        #d['purchase']
                        );
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def update_standardsOrdering(self,data_I):
        '''update rows of standards_ordering'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(standards_ordering).filter(
                           standards_ordering.met_id.like(d['met_id'])).update(
                            {'met_id':d['met_id'],
                            'met_name':d['met_name'],
                            'hillcrest':d['hillcrest'],
                            'provider':d['provider'],
                            'provider_reference':d['provider_reference'],
                            'price':d['price'],
                            'amount':d['amount'],
                            'amount_units':d['amount_units'],
                            'purity':d['purity'],
                            'mw':d['mw'],
                            'notes':d['notes'],
                            'powderdate_received':d['powderdate_received'],
                            'powderdate_opened':d['powderdate_opened'],
                            'order_standard':d['order_standard'],
                            'standards_storage':d['standards_storage'],
                            'purchase':d['purchase']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def get_structureFile_standards(self,met_id_I):
        '''Querry structure file and extension from metabolomics standards'''
        try:
            structure = self.session.query(standards.structure_file,
                    standards.structure_file_extention).filter(
                    standards.met_id.like(met_id_I)).all();
            struct_file_O = '';
            struct_file_ext_O = '';
            if structure:
                struct_file_O = structure[0][0];
                struct_file_ext_O = structure[0][1];
            else: 
                print('no structure file found for ' + met_id_I);
                exit(-1);
            return struct_file_O, struct_file_ext_O
        except SQLAlchemyError as e:
            print(e);

    def get_exactMassAndFormula_standards(self,met_id_I):
        '''Querry exact mass and formula from metabolomics standards'''
        try:
            massformula = self.session.query(standards.exactmass,
                    standards.formula).filter(
                    standards.met_id.like(met_id_I)).all();
            mass_O = '';
            formula_O = '';
            if massformula:
                mass_O = massformula[0][0];
                formula_O = massformula[0][1];
            else: 
                print('no mass and formula found for ' + met_id_I);
                exit(-1);
            return mass_O, formula_O
        except SQLAlchemyError as e:
            print(e);