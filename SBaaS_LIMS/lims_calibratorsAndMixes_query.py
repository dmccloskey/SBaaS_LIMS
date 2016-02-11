from .lims_calibratorsAndMixes_postgresql_models import *

from SBaaS_base.sbaas_base_query_update import sbaas_base_query_update
from SBaaS_base.sbaas_base_query_drop import sbaas_base_query_drop
from SBaaS_base.sbaas_base_query_initialize import sbaas_base_query_initialize
from SBaaS_base.sbaas_base_query_insert import sbaas_base_query_insert
from SBaaS_base.sbaas_base_query_select import sbaas_base_query_select
from SBaaS_base.sbaas_base_query_delete import sbaas_base_query_delete

from SBaaS_base.sbaas_template_query import sbaas_template_query

class lims_calibratorsAndMixes_query(sbaas_template_query):
    def initialize_supportedTables(self):
        '''Set the supported tables dict for 
        '''
        tables_supported = {'calibrator':calibrator,
            'calibrator_calculations':calibrator_calculations,
            'calibrator_concentrations':calibrator_concentrations,
            'calibrator_levels':calibrator_levels,
            'calibrator_met_parameters':calibrator_met_parameters,
            'calibrator_met2mix_calculations':calibrator_met2mix_calculations,
            'calibrator2mix':calibrator2mix,
            'mix_calculations':mix_calculations,
            'mix_description':mix_description,
            'mix_parameters':mix_parameters,
            'mix_storage':mix_storage,
            'mix2met_id':mix2met_id,
                        };
        self.set_supportedTables(tables_supported);
        #table initializations:
    def drop_lims_calibratorsAndMixes(self):
        try:
            mix_storage.__table__.drop(self.engine,True);
            mix_description.__table__.drop(self.engine,True);
            mix_parameters.__table__.drop(self.engine,True);
            calibrator_met_parameters.__table__.drop(self.engine,True);
            calibrator2mix.__table__.drop(self.engine,True);
            mix2met_id.__table__.drop(self.engine,True);
            calibrator.__table__.drop(self.engine,True);
            calibrator_concentrations.__table__.drop(self.engine,True);
            calibrator_calculations.__table__.drop(self.engine,True);
            calibrator_met2mix_calculations.__table__.drop(self.engine,True);
            mix_calculations.__table__.drop(self.engine,True);
            calibrator_levels.__table__.drop(self.engine,True);

        except SQLAlchemyError as e:
            print(e);
    def reset_lims_calibratorsAndMixes(self):
        try:
            reset = self.session.query(mix_storage).delete(synchronize_session=False);
            reset = self.session.query(mix_description).delete(synchronize_session=False);
            reset = self.session.query(mix_parameters).delete(synchronize_session=False);
            reset = self.session.query(calibrator_met_parameters).delete(synchronize_session=False);
            reset = self.session.query(calibrator2mix).delete(synchronize_session=False);
            reset = self.session.query(mix2met_id).delete(synchronize_session=False);
            reset = self.session.query(calibrator).delete(synchronize_session=False);
            reset = self.session.query(calibrator_concentrations).delete(synchronize_session=False);
            reset = self.session.query(calibrator_calculations).delete(synchronize_session=False);
            reset = self.session.query(calibrator_met2mix_calculations).delete(synchronize_session=False);
            reset = self.session.query(mix_calculations).delete(synchronize_session=False);
            reset = self.session.query(calibrator_levels).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def initialize_lims_calibratorsAndMixes(self):
        try:
            mix_storage.__table__.create(self.engine,True);
            mix_description.__table__.create(self.engine,True);
            mix_parameters.__table__.create(self.engine,True);
            calibrator_met_parameters.__table__.create(self.engine,True);
            calibrator2mix.__table__.create(self.engine,True);
            mix2met_id.__table__.create(self.engine,True);
            calibrator.__table__.create(self.engine,True);
            calibrator_concentrations.__table__.create(self.engine,True);
            calibrator_calculations.__table__.create(self.engine,True);
            calibrator_met2mix_calculations.__table__.create(self.engine,True);
            mix_calculations.__table__.create(self.engine,True);
            calibrator_levels.__table__.create(self.engine,True);

        except SQLAlchemyError as e:
            print(e);

    def add_calibratorConcentrations(self, data_I):
        '''add rows of calibrator_concentrations'''
        if data_I:
            for d in data_I:
                try:
                    data_add = calibrator_concentrations(d['met_id'],
                                                d['calibrator_level'],
                                                d['dilution_factor'],
                                                d['calibrator_concentration'],
                                                d['concentration_units']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def get_calibratorConcentrationAndUnit_metIDAndCalibratorIDAndLevel_calibratorConcentrations(self, met_id_I, calibrator_id_I, calibrator_level_I):
        '''Query calibrator id and level from metabolomics sample'''
        concentration_O = 0.0;
        unit_O = None;
        # 1. query the calibrator id for the metabolite
        try:
            calibratorID = self.session.query(
                    calibrator2mix.calibrator_id).filter(
                    mix2met_id.met_id.like(met_id_I),
                    mix2met_id.mix_id.like(calibrator2mix.mix_id)).all();
            calibrator_id_O = None;
            if calibratorID:
                calibrator_id_O = calibratorID[0][0];
            else: 
                print('no calibrator ID nor unit found for met_id ' + met_id_I);
        except SQLAlchemyError as e:
            print(e);
        # 2. check if the calibrator id matches
        if calibrator_id_O == calibrator_id_I:
            # 3. query the concentration and units
            try:
                calibratorInfo = self.session.query(
                        calibrator_concentrations.calibrator_concentration,
                        calibrator_concentrations.concentration_units).filter(
                        calibrator_concentrations.met_id.like(met_id_I),
                        calibrator_concentrations.calibrator_level == calibrator_level_I).all();
                if calibratorInfo:
                    concentration_O = calibratorInfo[0][0];
                    unit_O = calibratorInfo[0][1];
                else: 
                    print('no calibrator concentration nor unit found for met_id/calibrator_id/calibrator_level ' + met_id_I + ' / ' + str(calibrator_id_I) + ' / ' + str(calibrator_level_I));
                return concentration_O, unit_O
            except SQLAlchemyError as e:
                print(e);
        else: 
            return concentration_O, unit_O
    def get_rows_metID_calibratorConcentrations(self, met_id_I):
        '''Query rows by met_id from calibrator_concentrations'''
        try:
            calibratorInfo = self.session.query(
                    calibrator_concentrations).filter(
                    calibrator_concentrations.met_id.like(met_id_I)).order_by(
                    calibrator_concentrations.met_id.asc(),
                    calibrator_concentrations.calibrator_level.asc()).all();
            rows_O = [];
            if calibratorInfo:
                for c in calibratorInfo:
                    rows_O.append(c.__repr__dict__());
            else: 
                print('no calibrator concentration nor unit found for met_id' + met_id_I);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_metIDs_calibratorConcentrations(self):
        '''Query met_ids from calibrator_concentrations'''
        try:
            calibratorInfo = self.session.query(
                    calibrator_concentrations.met_id).order_by(
                    calibrator_concentrations.met_id.asc()).all();
            met_ids_O = [];
            if calibratorInfo:
                for c in calibratorInfo:
                    met_ids_O.append(c.met_id);
            return met_ids_O;
        except SQLAlchemyError as e:
            print(e);