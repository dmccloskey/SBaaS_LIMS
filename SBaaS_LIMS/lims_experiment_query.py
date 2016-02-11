from SBaaS_base.sbaas_base import sbaas_base
from .lims_experiment_postgresql_models import *
from .lims_experimentor_postgresql_models import *
from .lims_sample_postgresql_models import *
from .lims_extractionMethod_postgresql_models import *
from .lims_acquisitionMethod_postgresql_models import *

from SBaaS_base.sbaas_base_query_update import sbaas_base_query_update
from SBaaS_base.sbaas_base_query_drop import sbaas_base_query_drop
from SBaaS_base.sbaas_base_query_initialize import sbaas_base_query_initialize
from SBaaS_base.sbaas_base_query_insert import sbaas_base_query_insert
from SBaaS_base.sbaas_base_query_select import sbaas_base_query_select
from SBaaS_base.sbaas_base_query_delete import sbaas_base_query_delete

from SBaaS_base.sbaas_template_query import sbaas_template_query

class lims_experiment_query(sbaas_template_query):
    def initialize_supportedTables(self):
        '''Set the supported tables dict for 
        '''
        tables_supported = {"experiment_types":experiment_types,
                            "experiment":experiment,
                        };
        self.set_supportedTables(tables_supported);
    def get_CVSAndCVSUnitsAndODAndDilAndDilUnits_sampleNameShort(self,experiment_id_I,sample_name_short_I,exp_type_I=4):
        '''Querry culture volume sampled, culture volume sampled units, and OD600 from sample name
        NOTE: intended to be used within a for loop'''
        try:
            physiologicalParameters = self.session.query(sample_physiologicalParameters.culture_volume_sampled,
                    sample_physiologicalParameters.culture_volume_sampled_units,
                    sample_physiologicalParameters.od600,
                    sample_description.reconstitution_volume,
                    sample_description.reconstitution_volume_units).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),
                    sample_description.sample_name_short.like(sample_name_short_I),
                    sample_description.sample_id.like(sample_physiologicalParameters.sample_id)).all();
            cvs_O = physiologicalParameters[0][0];
            cvs_units_O = physiologicalParameters[0][1];
            od600_O = physiologicalParameters[0][2];
            dil_O = physiologicalParameters[0][3];
            dil_units_O = physiologicalParameters[0][4];
            return cvs_O, cvs_units_O, od600_O, dil_O, dil_units_O;
        except SQLAlchemyError as e:
            print(e);

    # query description from sample_description
    def get_description_experimentIDAndSampleID_sampleDescription(self,experiment_id_I,sample_id_I):
        '''Query description by sample id from sample_description'''
        try:
            data = self.session.query(sample_description).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_id_I),
                    sample.sample_id.like(sample_description.sample_id)).first();
            desc = {};
            if data: 
                desc['sample_id']=data.sample_id;
                desc['sample_name_short']=data.sample_name_short;
                desc['sample_name_abbreviation']=data.sample_name_abbreviation;
                desc['sample_date']=data.sample_date;
                desc['time_point']=data.time_point;
                desc['sample_condition']=data.sample_condition;
                desc['extraction_method_id']=data.extraction_method_id;
                desc['biological_material']=data.biological_material;
                desc['sample_desc']=data.sample_desc;
                desc['sample_replicate']=data.sample_replicate;
                desc['is_added']=data.is_added;
                desc['is_added_units']=data.is_added_units;
                desc['reconstitution_volume']=data.reconstitution_volume;
                desc['reconstitution_volume_units']=data.reconstitution_volume_units;
                desc['istechnical']=data.istechnical;
                desc['sample_replicate_biological']=data.sample_replicate_biological;
                desc['notes']=data.notes;
            return desc;
        except SQLAlchemyError as e:
            print(e);
            
    def drop_lims_experimentTypes(self):
        try:
            experiment_types.__table__.drop(self.engine,True);

        except SQLAlchemyError as e:
            print(e);
    def reset_lims_experimentTypes(self):
        try:
            reset = self.session.query(experiment_types).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def initialize_lims_experimentTypes(self):
        try:
            experiment_types.__table__.create(self.engine,True);

        except SQLAlchemyError as e:
            print(e);
            
    def drop_lims_experiment(self):
        try:
            experiment.__table__.drop(self.engine,True);

        except SQLAlchemyError as e:
            print(e);
    def reset_lims_experiment(self,experiment_id_I=None):
        try:
            if experiment_id_I:
                reset = self.session.query(experiment).filter(experiment.id.like(experiment_id_I)).delete(synchronize_session=False);
            else:
                reset = self.session.query(experiment).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def initialize_lims_experiment(self):
        try:
            experiment.__table__.create(self.engine,True);

        except SQLAlchemyError as e:
            print(e);
    def add_experiment(self, data_I):
        '''add rows of experiment'''
        if data_I:
            for d in data_I:
                try:
                    data_add = experiment(d
                        #d['exp_type_id'],
                        #d['id'],
                        #d['sample_name'],
                        #d['experimentor_id'],
                        #d['extraction_method_id'],
                        #d['acquisition_method_id'],
                        #d['quantitation_method_id'],
                        #d['internal_standard_id']
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
    def update_experiment(self,data_I):
        '''update rows of experiment'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(experiment).filter(
                           experiment.sample_name==d['sample_name'],
                           experiment.id==d['id']).update(
                            {#'wid ':d['wid '],
                            'exp_type_id':d['exp_type_id'],
                            #'id':d['id'],
                            #'sample_name':d['sample_name'],
                            'experimentor_id':d['experimentor_id'],
                            'extraction_method_id':d['extraction_method_id'],
                            'acquisition_method_id':d['acquisition_method_id'],
                            'quantitation_method_id':d['quantitation_method_id'],
                            'internal_standard_id':d['internal_standard_id']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def get_nMaxBioReps_sampleDescription(self,experiment_id_I):
        '''Query the maximum number of biological replicates corresponding to a given experiment'''
        try:
            bioReps = self.session.query(sample_description.sample_replicate).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),
                    sample_description.istechnical != True).group_by(
                    sample_description.sample_replicate).order_by(
                    sample_description.sample_replicate.desc()).all();
            maxBioReps_O = 0;
            if bioReps:
                maxBioReps_O = max(bioReps[0]);
            else: 
                print('no biological replicates found for experiment ' + experiment_id_I);
                exit(-1);
            return maxBioReps_O;
        except SQLAlchemyError as e:
            print(e);
    def get_batchFileInfo_experimentID(self,experiment_id_I,sample_type_I):
        '''Query data from experiment and sample for batch file'''
        try:
            data = self.session.query(experiment.id,
                    sample.sample_name,
                    experiment.acquisition_method_id,
                    sample.sample_dilution,
                    sample.sample_type,
                    sample_description.sample_replicate,
                    sample_description.sample_desc,
                    sample_description.sample_name_abbreviation).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_type.like(sample_type_I),
                    sample.sample_id.like(sample_description.sample_id)).group_by(
                    experiment.id,
                    sample.sample_name,
                    experiment.acquisition_method_id,
                    sample.sample_dilution,
                    sample.sample_type,
                    sample_description.sample_replicate,
                    sample_description.sample_desc,
                    sample_description.sample_name_abbreviation).order_by(
                    experiment.id.asc(),
                    sample.sample_dilution.desc(),
                    sample_description.sample_name_abbreviation.asc(),
                    #sample.sample_name.asc(),
                    sample_description.sample_replicate.asc(),
                    sample_description.sample_desc.desc()).all();
            #.order_by(
            #        experiment.id.asc(),
            #        sample.sample_dilution.desc(),
            #        sample_description.sample_replicate.asc(),
            #        sample_description.sample_desc.desc(),
            #        sample.sample_name.asc()).all();
            data_O = [];
            if data:
                for d in data:
                    data_tmp = {};
                    data_tmp['id']=d.id;
                    data_tmp['sample_name']=d.sample_name;
                    data_tmp['sample_type']=d.sample_type;
                    data_tmp['acquisition_method_id']=d.acquisition_method_id;
                    data_tmp['sample_dilution']=d.sample_dilution;
                    data_tmp['sample_replicate']=d.sample_replicate;
                    data_O.append(data_tmp);
            else: 
                print('no data found for experiment ' + experiment_id_I + ' and sample_type' + sample_type_I);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_batchFileInfo_experimentIDAndExpType(self,experiment_id_I,sample_type_I,exp_type_I):
        '''Query data from experiment and sample for batch file'''
        try:
            data = self.session.query(experiment.id,
                    sample.sample_name,
                    experiment.acquisition_method_id,
                    sample.sample_dilution,
                    sample.sample_type,
                    sample_description.sample_replicate,
                    sample_description.sample_desc,
                    sample_description.sample_name_abbreviation).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id==exp_type_I,
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_type.like(sample_type_I),
                    sample.sample_id.like(sample_description.sample_id)).group_by(
                    experiment.id,
                    sample.sample_name,
                    experiment.acquisition_method_id,
                    sample.sample_dilution,
                    sample.sample_type,
                    sample_description.sample_replicate,
                    sample_description.sample_desc,
                    sample_description.sample_name_abbreviation).order_by(
                    experiment.id.asc(),
                    sample.sample_dilution.desc(),
                    sample_description.sample_name_abbreviation.asc(),
                    #sample.sample_name.asc(),
                    sample_description.sample_replicate.asc(),
                    sample_description.sample_desc.desc()).all();
            #.order_by(
            #        experiment.id.asc(),
            #        sample.sample_dilution.desc(),
            #        sample_description.sample_replicate.asc(),
            #        sample_description.sample_desc.desc(),
            #        sample.sample_name.asc()).all();
            data_O = [];
            if data:
                for d in data:
                    data_tmp = {};
                    data_tmp['id']=d.id;
                    data_tmp['sample_name']=d.sample_name;
                    data_tmp['sample_type']=d.sample_type;
                    data_tmp['acquisition_method_id']=d.acquisition_method_id;
                    data_tmp['sample_dilution']=d.sample_dilution;
                    data_tmp['sample_replicate']=d.sample_replicate;
                    data_O.append(data_tmp);
            else: 
                print('no data found for experiment ' + experiment_id_I + ' and sample_type' + sample_type_I);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def delete_sample_experimentIDAndSampleName_experiment(self,dataListDelete_I):
        '''Delete specific samples from an experiment by their sample name from experiment'''
        deletes = [];
        for d in dataListDelete_I:
            try:
                delete = self.session.query(experiment).filter(
                        experiment.id.like(d['experiment_id']),
                        experiment.sample_name.like(d['sample_name'])).delete(
                        synchronize_session=False);
                if delete == 0:
                    print('row not found')
                    print(d);
                deletes.append(delete);
            except SQLAlchemyError as e:
                print(e);
        self.session.commit();
    def delete_sample_sampleName_sample(self,dataListDelete_I):
        '''Delete specific samples from an experiment by their sample name'''
        deletes = [];
        for d in dataListDelete_I:
            try:
                delete = self.session.query(sample).filter(
                        sample.sample_name.like(d['sample_name'])).delete(
                        synchronize_session=False);
                if delete == 0:
                    print('row not found')
                    print(d);
                deletes.append(delete);
            except SQLAlchemyError as e:
                print(e);
        self.session.commit();
    def delete_sample_sampleID_sampleDescription(self,dataListDelete_I):
        '''Delete specific samples from an experiment by their sample ID from sample_description'''
        deletes = [];
        for d in dataListDelete_I:
            try:
                delete = self.session.query(sample_description).filter(
                        sample_description.sample_id.like(d['sample_id'])).delete(
                        synchronize_session=False);
                if delete == 0:
                    print('row not found')
                    print(d);
                deletes.append(delete);
            except SQLAlchemyError as e:
                print(e);
        self.session.commit();
    def delete_sample_sampleID_sampleStorage(self,dataListDelete_I):
        '''Delete specific samples from an experiment by their sample ID from sample_storage'''
        deletes = [];
        for d in dataListDelete_I:
            try:
                delete = self.session.query(sample_storage).filter(
                        sample_storage.sample_id.like(d['sample_id'])).delete(
                        synchronize_session=False);
                if delete == 0:
                    print('row not found')
                    print(d);
                deletes.append(delete);
            except SQLAlchemyError as e:
                print(e);
        self.session.commit();
    def delete_sample_sampleID_samplePhysiologicalParameters(self,dataListDelete_I):
        '''Delete specific samples from an experiment by their sample ID from sample_physiologicalparameters'''
        deletes = [];
        for d in dataListDelete_I:
            try:
                delete = self.session.query(sample_physiologicalParameters).filter(
                        sample_physiologicalParameters.sample_id.like(d['sample_id'])).delete(
                        synchronize_session=False);
                if delete == 0:
                    print('row not found')
                    print(d);
                deletes.append(delete);
            except SQLAlchemyError as e:
                print(e);
        self.session.commit();

    def delete_sample_experimentID_experiment(self,dataListDelete_I):
        '''Delete samples from an experiment from experiment'''
        deletes = [];
        for d in dataListDelete_I:
            try:
                delete = self.session.query(experiment).filter(
                        experiment.id.like(d['experiment_id'])).delete(
                        synchronize_session=False);
                if delete == 0:
                    print('row not found')
                    print(d);
                deletes.append(delete);
            except SQLAlchemyError as e:
                print(e);
        self.session.commit();

    def delete_sample_experimentID_sample(self,dataListDelete_I):
        '''Delete an experiment from sample'''
        deletes = [];
        for d in dataListDelete_I:
            try:
                delete = self.session.query(sample).filter(
                        experiment.id.like(d['experiment_id']),
                        experiment.sample_name.like(sample.sample_name)).delete(
                        synchronize_session=False);
                if delete == 0:
                    print('row not found')
                    print(d);
                deletes.append(delete);
            except SQLAlchemyError as e:
                print(e);
        self.session.commit();
  
    def get_nMaxBioReps_experimentIDAndSampleName_sampleDescription(self,experiment_id_I,sample_name_I):
        '''Query the maximum number of biological replicates corresponding to a given experiment'''
        try:
            bioReps = self.session.query(sample_description.sample_replicate).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample_name_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),
                    sample_description.istechnical != True).group_by(
                    sample_description.sample_replicate).order_by(
                    sample_description.sample_replicate.desc()).all();
            maxBioReps_O = 0;
            if bioReps:
                maxBioReps_O = max(bioReps[0]);
            else: 
                print('no biological replicates found for experiment ' + experiment_id_I);
                exit(-1);
            return maxBioReps_O;
        except SQLAlchemyError as e:
            print(e);

    def get_nMaxBioReps_experimentIDAndSampleID_sampleDescription(self,experiment_id_I,sample_id_I):
        '''Query the maximum number of biological replicates corresponding to a given experiment'''
        try:
            bioReps = self.session.query(sample_description.sample_replicate).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_id_I),
                    sample.sample_id.like(sample_description.sample_id),
                    sample_description.sample_desc.like('Broth'),
                    sample_description.istechnical != True).group_by(
                    sample_description.sample_replicate).order_by(
                    sample_description.sample_replicate.desc()).all();
            maxBioReps_O = 0;
            if bioReps:
                maxBioReps_O = max(bioReps[0]);
            else: 
                print('no biological replicates found for experiment ' + experiment_id_I);
                exit(-1);
            return maxBioReps_O;
        except SQLAlchemyError as e:
            print(e);

    def get_nMaxBioReps_experimentIDAndSampleNameAbbreviation_sampleDescription(self,experiment_id_I,sample_name_abbreviation_I):
        '''Query the maximum number of biological replicates corresponding to a given experiment'''
        try:
            bioReps = self.session.query(sample_description.sample_replicate).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),
                    sample_description.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    sample_description.sample_desc.like('Broth')
                    #sample_description.istechnical != True
                    ).group_by(
                    sample_description.sample_replicate).order_by(
                    sample_description.sample_replicate.desc()).all();
            maxBioReps_O = 0;
            if bioReps:
                maxBioReps_O = max(bioReps[0]);
            else: 
                print('no biological replicates found for experiment ' + experiment_id_I);
                exit(-1);
            return maxBioReps_O;
        except SQLAlchemyError as e:
            print(e);

    def get_nMaxBioReps_experimentIDAndSampleNameAbbreviationAndExpType_sampleDescription(self,experiment_id_I,sample_name_abbreviation_I,exp_type_I):
        '''Query the maximum number of biological replicates corresponding to a given experiment'''
        try:
            bioReps = self.session.query(sample_description.sample_replicate).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id==exp_type_I,
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),
                    sample_description.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    sample_description.sample_desc.like('Broth')
                    #sample_description.istechnical != True
                    ).group_by(
                    sample_description.sample_replicate).order_by(
                    sample_description.sample_replicate.desc()).all();
            maxBioReps_O = 0;
            if bioReps:
                maxBioReps_O = max(bioReps[0]);
            else: 
                print('no biological replicates found for experiment ' + experiment_id_I);
                exit(-1);
            return maxBioReps_O;
        except SQLAlchemyError as e:
            print(e);
       
    def get_sampleIDs_experimentID_experiment(self,experiment_id_I):
        '''Querry sample IDs that are used from the experiment'''
        try:
            sample_names = self.session.query(sample.sample_id).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name)).group_by(
                    sample.sample_id).order_by(
                    sample.sample_id.asc()).all();
            sample_names_O = [];
            for sn in sample_names: sample_names_O.append(sn.sample_id);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e);
       
    def get_sampleIDsAndSampleNames_experimentID_experiment(self,experiment_id_I):
        '''Querry sample IDs and sample namesthat are used from the experiment'''
        try:
            sample_names = self.session.query(sample.sample_id,sample.sample_name).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name)).group_by(
                    sample.sample_id,sample.sample_name).order_by(
                    sample.sample_name.asc(),
                    sample.sample_id.asc()).all();
            sample_names_O = [];
            sample_ids_O = [];
            for sn in sample_names: 
                sample_names_O.append(sn.sample_name);
                sample_ids_O.append(sn.sample_id);
            return sample_ids_O, sample_names_O;
        except SQLAlchemyError as e:
            print(e);
       
    def get_sampleIDsAndSampleNames_experimentIDAndSampleName_experiment(self,experiment_id_I,sample_name_I):
        '''Querry sample IDs and sample namesthat are used from the experiment'''
        try:
            sample_names = self.session.query(sample.sample_id,sample.sample_name).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample_name_I),
                    experiment.sample_name.like(sample.sample_name)).group_by(
                    sample.sample_id,sample.sample_name).order_by(
                    sample.sample_name.asc(),
                    sample.sample_id.asc()).all();
            sample_names_O = [];
            sample_ids_O = [];
            for sn in sample_names: 
                sample_names_O.append(sn.sample_name);
                sample_ids_O.append(sn.sample_id);
            return sample_ids_O, sample_names_O;
        except SQLAlchemyError as e:
            print(e);

    def get_sampleNameAbbreviation_experimentIDAndSampleID(self,experiment_id_I,sample_id_I):
        '''Querry sample name abbreviation from the experiment'''
        try:
            sample_name_abbreviations = self.session.query(sample_description.sample_name_abbreviation).filter(
                    sample.sample_id.like(sample_id_I),
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id)).group_by(
                    sample_description.sample_name_abbreviation).order_by(
                    sample_description.sample_name_abbreviation.asc()).all();
            sample_name_abbreviations_O = None;
            sample_name_abbreviations_O = sample_name_abbreviations[0][0];
            return sample_name_abbreviations_O;
        except SQLAlchemyError as e:
            print(e);

    def get_sampleNameAbbreviation_experimentIDAndSampleName(self,experiment_id_I,sample_name_I):
        '''Querry sample name abbreviation from the experiment'''
        try:
            sample_name_abbreviations = self.session.query(sample_description.sample_name_abbreviation).filter(
                    sample.sample_name.like(sample_name_I),
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id)).group_by(
                    sample_description.sample_name_abbreviation).order_by(
                    sample_description.sample_name_abbreviation.asc()).all();
            sample_name_abbreviations_O = None;
            sample_name_abbreviations_O = sample_name_abbreviations[0][0];
            return sample_name_abbreviations_O;
        except SQLAlchemyError as e:
            print(e);

    def get_sampleLabelAndBoxAndPos_experimentIDAndExperimentTypeID_sampleStorage(self,experiment_id_I,exp_type_id_I):
        '''Querry sample name abbreviation from the experiment'''
        try:
            data = self.session.query(sample_storage.sample_id,
                    sample_storage.sample_label,
                    sample_storage.box,
                    sample_storage.pos).filter(
                    experiment.exp_type_id == exp_type_id_I,
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_storage.sample_id)).group_by(
                    sample_storage.sample_id,
                    sample_storage.sample_label,
                    sample_storage.box,
                    sample_storage.pos).order_by(
                    sample_storage.sample_id.asc()).all();
            sampleStorage_O = [];
            if data:
                for d in data:
                    sampleStorage_O.append({'sample_id':d.sample_id,
                    'sample_label':d.sample_label,
                    'box':d.box,
                    'pos':d.pos});
            return sampleStorage_O;
        except SQLAlchemyError as e:
            print(e);
    # query physiological parameters and sample mass conversion
    def get_CVSAndCVSUnitsAndODAndDilAndDilUnits_sampleNameShort(self,experiment_id_I,sample_name_short_I,exp_type_I=4):
        '''Querry culture volume sampled, culture volume sampled units, and OD600 from sample name
        NOTE: intended to be used within a for loop'''
        try:
            physiologicalParameters = self.session.query(sample_physiologicalParameters.culture_volume_sampled,
                    sample_physiologicalParameters.culture_volume_sampled_units,
                    sample_physiologicalParameters.od600,
                    sample_description.reconstitution_volume,
                    sample_description.reconstitution_volume_units).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),
                    sample_description.sample_name_short.like(sample_name_short_I),
                    sample_description.sample_id.like(sample_physiologicalParameters.sample_id)).all();
            cvs_O = physiologicalParameters[0][0];
            cvs_units_O = physiologicalParameters[0][1];
            od600_O = physiologicalParameters[0][2];
            dil_O = physiologicalParameters[0][3];
            dil_units_O = physiologicalParameters[0][4];
            return cvs_O, cvs_units_O, od600_O, dil_O, dil_units_O;
        except SQLAlchemyError as e:
            print(e);
             
    # query sample ids from sample_physiologicalParameters
    def get_sampleIDs_experimentIDNoOD600_samplePhysiologicalParameters(self,experiment_id_I):
        '''Querry sample ids (i.e. unknowns) that are used from
        the experiment for all experiment types
        that do not have an OD600 but do have a time'''
        try:
            sample_names = self.session.query(sample_physiologicalParameters.sample_id).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_physiologicalParameters.sample_id),
                    #sample.sample_id.like(sample_description.sample_id),
                    sample_physiologicalParameters.od600 == None).group_by(
                    sample_physiologicalParameters.sample_id).order_by(
                    sample_physiologicalParameters.sample_id.asc()).all();
            sample_names_O = [];
            for sn in sample_names: sample_names_O.append(sn.sample_id);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleIDs_experimentIDAndSampleDescriptionNoOD600_samplePhysiologicalParameters(self,experiment_id_I,sample_description_I):
        '''Querry sample ids (i.e. unknowns) that are used from
        the experiment for all experiment types
        that do not have an OD600 but do have a time'''
        try:
            sample_names = self.session.query(sample_physiologicalParameters.sample_id).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_physiologicalParameters.sample_id),
                    sample.sample_id.like(sample_description.sample_id),
                    sample_description.sample_description.like(sample_description_I),
                    sample_physiologicalParameters.od600 == None).group_by(
                    sample_physiologicalParameters.sample_id).order_by(
                    sample_physiologicalParameters.sample_id.asc()).all();
            sample_names_O = [];
            for sn in sample_names: sample_names_O.append(sn.sample_id);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleIDs_experimentIDWithOD600NoCultureDensity_samplePhysiologicalParameters(self,experiment_id_I):
        '''Querry sample ids (i.e. unknowns) that are used from
        the experiment for all experiment types
        that do have an OD600 but do not have a culture density'''
        try:
            sample_names = self.session.query(sample_physiologicalParameters.sample_id).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_physiologicalParameters.sample_id),
                    sample_physiologicalParameters.od600 != None,
                    sample_physiologicalParameters.culture_density == None).group_by(
                    sample_physiologicalParameters.sample_id).order_by(
                    sample_physiologicalParameters.sample_id.asc()).all();
            sample_names_O = [];
            for sn in sample_names: sample_names_O.append(sn.sample_id);
            return sample_names_O;
        except SQLAlchemyError as e:
            print(e);
    # query physiologicalParameters from sample_physiologicalParameters
    def get_physiologicalParameters_experimentIDAndSampleID_samplePhysiologicalParameters(self,experiment_id_I,sample_id_I):
        '''Query physiologicalParameters by sample id from sample_physiologicalparameters'''
        try:
            data = self.session.query(sample_physiologicalParameters).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_id_I),
                    sample.sample_id.like(sample_physiologicalParameters.sample_id)).first();
            pp = {};
            if data: 
                pp['sample_id']=data.sample_id;
                pp['growth_condition_short']=data.growth_condition_short;
                pp['growth_condition_long']=data.growth_condition_long;
                pp['media_short']=data.media_short;
                pp['media_long']=data.media_long;
                pp['isoxic']=data.isoxic;
                pp['temperature']=data.temperature;
                pp['supplementation']=data.supplementation;
                pp['od600']=data.od600;
                pp['vcd']=data.vcd;
                pp['culture_density']=data.culture_density;
                pp['culture_volume_sampled']=data.culture_volume_sampled;
                pp['cells']=data.cells;
                pp['dcw']=data.dcw;
                pp['wcw']=data.wcw;
                pp['vcd_units']=data.vcd_units;
                pp['culture_density_units']=data.culture_density_units;
                pp['culture_volume_sampled_units']=data.culture_volume_sampled_units;
                pp['dcw_units']=data.dcw_units;
                pp['wcw_units']=data.wcw_units;
            return pp;
        except SQLAlchemyError as e:
            print(e);
    def get_rows_experimentID_samplePhysiologicalParameters(self,experiment_id_I):
        '''Query rows by experiment_id from sample_physiologicalParameters'''
        try:
            data = self.session.query(sample_physiologicalParameters,
                    experiment.id).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_physiologicalParameters.sample_id)).all();
            data_O = [];
            if data: 
                for d in data:
                    tmp = d.sample_physiologicalParameters.__repr__dict__();
                    tmp['experiment_id']=d.id;
                    data_O.append(tmp);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    # query OD600 values from sample_physiologicalParameters
    def get_OD600s_experimentIDAndSampleID_samplePhysiologicalParameters(self,experiment_id_I,sample_id_I):
        '''query OD600 values from biological broth replicates'''
        #1 query sample_name_abbreviation and exp_typ_id by experiment_id and sample_id
        try:
            sample_names = self.session.query(sample_description.sample_name_abbreviation,
                    experiment.exp_type_id).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id),
                    sample.sample_id.like(sample_id_I)).first();
            sample_name_abbreviation_O = None;
            exp_type_id_O = None;
            if sample_names:
                sample_name_abbreviation_O = sample_names.sample_name_abbreviation;
                exp_type_id_O = sample_names.exp_type_id
        except SQLAlchemyError as e:
            print(e);
        #2 query OD600 by sample_name_abbreviation, exp_type_id, sample_description, istechnical
        try:
            od600 = self.session.query(sample_physiologicalParameters.od600).filter(
                    sample_description.sample_name_abbreviation.like(sample_name_abbreviation_O),
                    sample_description.sample_description.like('Broth'),
                    sample_description.istechnical.is_(False),
                    sample_physiologicalParameters.od600 != None,
                    sample.sample_id.like(sample_description.sample_id),
                    sample_physiologicalParameters.sample_id.like(sample_description.sample_id),
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    experiment.exp_type_id == exp_type_id_O).group_by(
                    sample_physiologicalParameters.od600).all();
            od600_O = [];
            if od600: 
                for od in od600:
                    od600_O.append(od.od600);
            return od600_O;
        except SQLAlchemyError as e:
            print(e);
    # query OD600 and DCW values from sample_physiologicalParameters
    def get_OD600AndCultureDensity_experimentIDAndSampleNameShort_samplePhysiologicalParameters(self,experiment_id_I,exp_type_id_I,sample_name_short_I):
        '''query OD600 and culture density values sorted by time'''
        try:
            od600 = self.session.query(sample_physiologicalParameters.od600,
                    sample_physiologicalParameters.culture_density,
                    sample_description.sample_date).filter(
                    experiment.id.like(experiment_id_I),
                    sample_description.sample_name_short.like(sample_name_short_I),
                    sample.sample_id.like(sample_description.sample_id),
                    sample_physiologicalParameters.sample_id.like(sample.sample_id),
                    experiment.sample_name.like(sample.sample_name),
                    experiment.exp_type_id == exp_type_id_I).group_by(
                    sample_physiologicalParameters.od600,
                    sample_physiologicalParameters.culture_density,
                    sample_description.sample_date).order_by(
                    sample_description.sample_date.asc()).all();
            od600_O = [];
            culture_density_O = [];
            if od600: 
                for od in od600:
                    od600_O.append(od.od600);
                    culture_density_O.append(od.culture_density);
            return od600_O,culture_density_O;
        except SQLAlchemyError as e:
            print(e);
    # query OD600 and DCW values from sample_physiologicalParameters
    def get_OD600AndCultureDensity_experimentIDAndSampleID_samplePhysiologicalParameters(self,experiment_id_I,exp_type_id_I,sample_id_I):
        '''query OD600 and culture density values sorted by time'''
        try:
            od600 = self.session.query(sample_physiologicalParameters.od600,
                    sample_physiologicalParameters.culture_density,
                    sample_description.sample_date).filter(
                    experiment.id.like(experiment_id_I),
                    sample_description.sample_id.like(sample_id_I),
                    sample.sample_id.like(sample_id_I),
                    sample_physiologicalParameters.sample_id.like(sample_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    experiment.exp_type_id == exp_type_id_I).first();
            od600_O = None;
            culture_density_O = None;
            if od600: 
                od600_O=od600.od600;
                culture_density_O=od600.culture_density;
            return od600_O,culture_density_O;
        except SQLAlchemyError as e:
            print(e);
    # query sample_date from sample_description
    def get_sampleDate_experimentIDAndSampleID_sampleDescription(self,experiment_id_I,sample_id_I):
        '''Query sample_date by sample id'''
        try:
            data = self.session.query(sample_description.sample_date).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_id_I),
                    sample.sample_id.like(sample_description.sample_id)).first();
            sample_date_O = None;
            if data: 
                sample_date_O=data.sample_date;
            return sample_date_O;
        except SQLAlchemyError as e:
            print(e);

    # query description from sample_description
    def get_description_experimentIDAndSampleID_sampleDescription(self,experiment_id_I,sample_id_I):
        '''Query description by sample id from sample_description'''
        try:
            data = self.session.query(sample_description).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_id_I),
                    sample.sample_id.like(sample_description.sample_id)).first();
            desc = {};
            if data: 
                desc['sample_id']=data.sample_id;
                desc['sample_name_short']=data.sample_name_short;
                desc['sample_name_abbreviation']=data.sample_name_abbreviation;
                desc['sample_date']=data.sample_date;
                desc['time_point']=data.time_point;
                desc['sample_condition']=data.sample_condition;
                desc['extraction_method_id']=data.extraction_method_id;
                desc['biological_material']=data.biological_material;
                desc['sample_desc']=data.sample_desc;
                desc['sample_replicate']=data.sample_replicate;
                desc['is_added']=data.is_added;
                desc['is_added_units']=data.is_added_units;
                desc['reconstitution_volume']=data.reconstitution_volume;
                desc['reconstitution_volume_units']=data.reconstitution_volume_units;
                desc['istechnical']=data.istechnical;
                desc['sample_replicate_biological']=data.sample_replicate_biological;
                desc['notes']=data.notes;
            return desc;
        except SQLAlchemyError as e:
            print(e);
    def get_rows_experimentID_sampleDescription(self,experiment_id_I):
        '''Query description by experiment_id from sample_description'''
        try:
            data = self.session.query(sample_description,
                    experiment.id).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_description.sample_id)).all();
            data_O = [];
            if data: 
                for d in data:
                    tmp = d.sample_description.__repr__dict__();
                    tmp['experiment_id']=d.id;
                    data_O.append(tmp);
            return data_O;
        except SQLAlchemyError as e:
            print(e);

    # query storage from sample_storage
    def get_rows_experimentID_sampleStorage(self,experiment_id_I):
        '''Query rows by experiment_id from sample_storage'''
        try:
            data = self.session.query(sample_storage,
                    experiment.id).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name),
                    sample.sample_id.like(sample_storage.sample_id)).all();
            data_O = [];
            if data: 
                for d in data:
                    tmp = d.sample_storage.__repr__dict__();
                    tmp['experiment_id']=d.id;
                    data_O.append(tmp);
            return data_O;
        except SQLAlchemyError as e:
            print(e);

    # query storage from sample
    def get_rows_experimentID_sample(self,experiment_id_I):
        '''Query rows by experiment_id from sample'''
        try:
            data = self.session.query(sample,
                    experiment.id).filter(
                    experiment.id.like(experiment_id_I),
                    experiment.sample_name.like(sample.sample_name)).all();
            data_O = [];
            if data: 
                for d in data:
                    tmp = d.sample.__repr__dict__();
                    tmp['experiment_id']=d.id;
                    data_O.append(tmp);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
        
