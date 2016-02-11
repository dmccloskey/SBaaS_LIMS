from .lims_sample_postgresql_models import *
from SBaaS_base.sbaas_base_query_update import sbaas_base_query_update
from SBaaS_base.sbaas_base_query_drop import sbaas_base_query_drop
from SBaaS_base.sbaas_base_query_initialize import sbaas_base_query_initialize
from SBaaS_base.sbaas_base_query_insert import sbaas_base_query_insert
from SBaaS_base.sbaas_base_query_select import sbaas_base_query_select
from SBaaS_base.sbaas_base_query_delete import sbaas_base_query_delete

from SBaaS_base.sbaas_template_query import sbaas_template_query

class lims_sample_query(sbaas_template_query):
    
    def initialize_supportedTables(self):
        '''Set the supported tables dict for 
        '''
        tables_supported = {'sample':sample,
            'sample_description':sample_description,
            'sample_physiologicalparameters':sample_physiologicalParameters,
            'sample_storage':sample_storage,
                        };
        self.set_supportedTables(tables_supported);
    #table initializations:
    def drop_lims_sample(self):
        try:
            sample.__table__.drop(self.engine,True);
            sample_storage.__table__.drop(self.engine,True);
            sample_physiologicalParameters.__table__.drop(self.engine,True);
            sample_description.__table__.drop(self.engine,True);

        except SQLAlchemyError as e:
            print(e);
    def reset_lims_sample(self):
        try:
            reset = self.session.query(sample).delete(synchronize_session=False);
            reset = self.session.query(sample_storage).delete(synchronize_session=False);
            reset = self.session.query(sample_physiologicalParameters).delete(synchronize_session=False);
            reset = self.session.query(sample_description).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def initialize_lims_sample(self):
        try:
            sample.__table__.create(self.engine,True);
            sample_storage.__table__.create(self.engine,True);
            sample_physiologicalParameters.__table__.create(self.engine,True);
            sample_description.__table__.create(self.engine,True);
        except SQLAlchemyError as e:
            print(e);

    def add_sample(self, data_I):
        '''add rows of sample'''
        if data_I:
            for d in data_I:
                try:
                    data_add = sample(d
                        #d['sample_name'],
                        #d['sample_type'],
                        #d['calibrator_id'],
                        #d['calibrator_level'],
                        #d['sample_id'],
                        #d['sample_dilution']
                        );
                    self.session.add(data_add);
                    self.session.commit();
                except IntegrityError as e:
                    print(e);
                    self.session.rollback();
                except SQLAlchemyError as e:
                    print(e);
                    self.session.rollback();
            self.session.commit();
    
    def update_sample(self,data_I):
        '''update rows of sample'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(sample).filter(
                            sample.sample_name.like(d['sample_name'])).update(
                            {'sample_type':d['sample_type'],
                            'calibrator_id':d['calibrator_id'],
                            'calibrator_level':d['calibrator_level'],
                            'sample_id':d['sample_id'],
                            'sample_dilution':d['sample_dilution']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def add_sampleDescription(self, data_I):
        '''add rows of sample_description'''
        if data_I:
            for d in data_I:
                try:
                    data_add = sample_description(d
                        #d['sample_id'],
                        #d['sample_name_short'],
                        #d['sample_name_abbreviation'],
                        #d['sample_date'],
                        #d['time_point'],
                        #d['sample_condition'],
                        #d['extraction_method_id'],
                        #d['biological_material'],
                        #d['sample_desc'],
                        #d['sample_replicate'],
                        #d['is_added'],
                        #d['is_added_units'],
                        #d['reconstitution_volume'],
                        #d['reconstitution_volume_units'],
                        #d['sample_replicate_biological'],
                        #d['istechnical'],
                        #d['notes']
                            );
                    self.session.add(data_add);
                    self.session.commit();
                except IntegrityError as e:
                    print(e);
                    self.session.rollback();
                except SQLAlchemyError as e:
                    print(e);
                    self.session.rollback();
            self.session.commit();
    
    def update_sampleDescription(self,data_I):
        '''update rows of sample_description'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(sample_description).filter(
                            sample_description.sample_id.like(d['sample_id'])).update(
                            {'sample_name_short':d['sample_name_short'],
                            'sample_name_abbreviation':d['sample_name_abbreviation'],
                            'sample_date':d['sample_date'],
                            'time_point':d['time_point'],
                            'sample_condition':d['sample_condition'],
                            'extraction_method_id':d['extraction_method_id'],
                            'biological_material':d['biological_material'],
                            'sample_desc':d['sample_desc'],
                            'sample_replicate':d['sample_replicate'],
                            'is_added':d['is_added'],
                            'is_added_units':d['is_added_units'],
                            'reconstitution_volume':d['reconstitution_volume'],
                            'reconstitution_volume_units':d['reconstitution_volume_units'],
                            'sample_replicate_biological':d['sample_replicate_biological'],
                            'istechnical':d['istechnical'],
                            'notes':d['notes']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def add_samplePhysiologicalParameters(self, data_I):
        '''add rows of sample_physiologicalparameters'''
        if data_I:
            for d in data_I:
                try:
                    data_add = sample_physiologicalParameters(d
                        #d['sample_id'],
                        #d['growth_condition_short'],
                        #d['growth_condition_long'],
                        #d['media_short'],
                        #d['media_long'],
                        #d['isoxic'],
                        #d['temperature'],
                        #d['supplementation'],
                        #d['od600'],
                        #d['vcd'],
                        #d['culture_density'],
                        #d['culture_volume_sampled'],
                        #d['cells'],
                        #d['dcw'],
                        #d['wcw'],
                        #d['vcd_units'],
                        #d['culture_density_units'],
                        #d['culture_volume_sampled_units'],
                        #d['dcw_units'],
                        #d['wcw_units']
                        );
                    self.session.add(data_add);
                    self.session.commit();
                except IntegrityError as e:
                    print(e);
                    self.session.rollback();
                except SQLAlchemyError as e:
                    print(e);
                    self.session.rollback();
            self.session.commit();

    def add_sampleStorage(self, data_I):
        '''add rows of sample_storage'''
        if data_I:
            for d in data_I:
                try:
                    data_add = sample_storage(d
                        #d['sample_id'],
                        #d['sample_label'],
                        #d['ph'],
                        #d['box'],
                        #d['pos']
                        );
                    self.session.add(data_add);
                    self.session.commit();
                except IntegrityError as e:
                    print(e);
                    self.session.rollback();
                except SQLAlchemyError as e:
                    print(e);
                    self.session.rollback();
            self.session.commit();

    def update_samplePhysiologicalParameters(self,data_I):
        '''update rows of sample_physiologicalParameters'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(sample_physiologicalParameters).filter(
                           sample_physiologicalParameters.sample_id==d['sample_id']).update(
                            {
                            'growth_condition_short':d['growth_condition_short'],
                            'growth_condition_long':d['growth_condition_long'],
                            'media_short':d['media_short'],
                            'media_long':d['media_long'],
                            'isoxic':d['isoxic'],
                            'temperature':d['temperature'],
                            'supplementation':d['supplementation'],
                            'od600':d['od600'],
                            'vcd':d['vcd'],
                            'culture_density':d['culture_density'],
                            'culture_volume_sampled':d['culture_volume_sampled'],
                            'cells':d['cells'],
                            'dcw':d['dcw'],
                            'wcw':d['wcw'],
                            'vcd_units':d['vcd_units'],
                            'culture_density_units':d['culture_density_units'],
                            'culture_volume_sampled_units':d['culture_volume_sampled_units'],
                            'dcw_units':d['dcw_units'],
                            'wcw_units':d['wcw_units']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def update_sampleStorage(self,data_I):
        '''update rows of sample_storage'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(sample_storage).filter(
                           sample_storage.sample_id==d['sample_id']).update(
                            {
                            'sample_label':d['sample_label'],
                            'ph':d['ph'],
                            'box':d['box'],
                            'pos':d['pos']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def get_calibratorIDAndLevel_sampleNameAndSampleType_sample(self,sample_name_I,sample_type_I):
        '''Querry calibrator id and level from metabolomics sample'''
        try:
            calibratorInfo = self.session.query(sample.calibrator_id,
                    sample.calibrator_level).filter(
                    sample.sample_name.like(sample_name_I),
                    sample.sample_type.like(sample_type_I)).all();
            id_O = None;
            level_O = None;
            if calibratorInfo:
                id_O = calibratorInfo[0][0];
                level_O = calibratorInfo[0][1];
            else: 
                print('no calibrator id nor level found for sample_name/sample_type ' + sample_name_I + ' / ' + sample_type_I);
            return id_O, level_O
        except SQLAlchemyError as e:
            print(e);
    def get_CVSAndCVSUnitsAndODAndDilAndDilUnits_sampleName(self,sample_name_I):
        '''Querry culture volume sampled, culture volume sampled units, and OD600 from sample name
        NOTE: intended to be used within a for loop'''
        try:
            physiologicalParameters = self.session.query(sample_physiologicalParameters.culture_volume_sampled,
                    sample_physiologicalParameters.culture_volume_sampled_units,
                    sample_physiologicalParameters.od600,
                    sample_description.reconstitution_volume,
                    sample_description.reconstitution_volume_units).filter(
                    sample.sample_name.like(sample_name_I),
                    sample.sample_id.like(sample_physiologicalParameters.sample_id),
                    sample.sample_id.like(sample_description.sample_id)).all();
            cvs_O = physiologicalParameters[0][0];
            cvs_units_O = physiologicalParameters[0][1];
            od600_O = physiologicalParameters[0][2];
            dil_O = physiologicalParameters[0][3];
            dil_units_O = physiologicalParameters[0][4];
            return cvs_O, cvs_units_O, od600_O, dil_O, dil_units_O;
        except SQLAlchemyError as e:
            print(e);

    # update physiologicalParameters 
    def update_data_samplePhysiologicalParameters(self,dataListUpdated_I):
        # update the sample_physiologicalParameters table
        updates = [];
        for d in dataListUpdated_I:
            try:
                data_update = self.session.query(sample_physiologicalParameters).filter(
                        sample_physiologicalParameters.sample_id.like(d['sample_id'])).update(		
                        {'growth_condition_short':d['growth_condition_short'],
                        'growth_condition_long':d['growth_condition_long'],
                        'media_short':d['media_short'],
                        'media_long':d['media_long'],
                        'isoxic':d['isoxic'],
                        'temperature':d['temperature'],
                        'supplementation':d['supplementation'],
                        'od600':d['od600'],
                        'vcd':d['vcd'],
                        'culture_density':d['culture_density'],
                        'culture_volume_sampled':d['culture_volume_sampled'],
                        'cells':d['cells'],
                        'dcw':d['dcw'],
                        'wcw':d['wcw'],
                        'vcd_units':d['vcd_units'],
                        'culture_density_units':d['culture_density_units'],
                        'culture_volume_sampled_units':d['culture_volume_sampled_units'],
                        'dcw_units':d['dcw_units'],
                        'wcw_units':d['wcw_units']},
                        synchronize_session=False);
                if data_update == 0:
                    print('row not found.')
                    print(d);
                updates.append(data_update);
            except SQLAlchemyError as e:
                print(e);
        self.session.commit();
    def get_rows_sampleID_limsSampleStorage(self,sample_id_I):
        '''Query rows of sample_storage by sample_id'''
        try:
            data = self.session.query(sample_storage).filter(
                    sample_storage.sample_id.like(sample_id_I)).order_by(
                    sample_storage.box.asc(),
                    sample_storage.pos.asc()).all();
            data_O = [];
            if data:
                for d in data:
                    data_O.append(d.__repr__dict__());
            return data_O;
        except SQLAlchemyError as e:
            print(e);