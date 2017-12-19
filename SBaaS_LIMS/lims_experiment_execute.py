import re
import io,os
from copy import copy
# sbaas
from .lims_experiment_io import lims_experiment_io

class lims_experiment_execute(lims_experiment_io):
    
    def execute_makeBatchFileCalibrators(self, experiment_id_I, DateAcquisition_I, batch_fileName_I):
        '''Generate the acqusition batch file for the calibrators'''
        return;
    def execute_makeExperimentFromSampleFile(self, sample_fileName_I, nTechReps_I=0, dil_levels_I=[]):
        '''Populate experiment, samples, sample_physiologicalparameters, sample_description, and sample_storage tables
        NOTE: the sample_file should only contain samples for 1 experiment_id and 1 exp_type if multiple technical replicates
              and/or dilutions are to be made
        INPUT:
        sample_fileName_I = name of the .csv file with sample information
        nTechReps_I = the number of technical replicates per biological replicate that should be created
        dil_levels_I = additional dilution levels per sample'''

        #import sample file and split into respective tables
        sampleDescription_data,samplePhysiologicalParameters_data,\
            sampleStorage_data,sample_data,\
            experiment_data = self.import_sampleFile_add(sample_fileName_I);
        #make technical replicates and dilutions
        if nTechReps_I>0 or len(dil_levels_I)>0:
            # check that there is only 1 experiment_id and 1 exp_type
            experiment_ids = [v['id'] for v in experiment_data];
            experiment_ids_unique = list(set(experiment_ids));
            exp_types = [v['exp_type_id'] for v in experiment_data];
            exp_types_unique = list(set(exp_types));
            if len(experiment_ids_unique)!=1 or len(exp_types_unique)!=1:
                print('More than 1 experiment_id and/or more than 1 exp_type found');
                print('This should be changed in future iterations');
                print('Technical replicates and dilutions will not be made');
                return;
            # make the technical replicates and dilutions
            sampleDescription_data,samplePhysiologicalParameters_data,\
                sampleStorage_data,sample_data,\
                experiment_data = self.make_techRepsAndDils(nTechReps_I, dil_levels_I,
                                                                        sampleDescription_data,samplePhysiologicalParameters_data,
                                                                        sampleStorage_data,
                                                                        sample_data,experiment_data);
            # add the data in order
            self.add_sampleDescription(sampleDescription_data);
            self.add_samplePhysiologicalParameters(samplePhysiologicalParameters_data);
            self.add_sampleStorage(sampleStorage_data);
            self.add_sample(sample_data);
            self.add_experiment(experiment_data);
    def execute_makeBatchFile(self, experiment_id_I, DateAcquisition_I, batch_fileName_I, experiment_type_I=4):
        '''generate the acqusition batch file for the experiment

        Input:
        batch_fileName_I = name of the .txt batch file that will be created
        Output:
        batch_fileName_I.txt
        '''
        #query sample and experiment data
        #ordered dilutions.asc(), sample_replicate.asc();
        data_unknown = self.get_batchFileInfo_experimentIDAndExpType(experiment_id_I,'Unknown',exp_type_I=experiment_type_I);
        data_qc = self.get_batchFileInfo_experimentIDAndExpType(experiment_id_I,'QC',exp_type_I=experiment_type_I);
        #generate the batch file
        batchFile_data = []
        batchFile_header = [];
        batchFile_data,batchFile_header = self.make_batchFile(DateAcquisition_I,data_unknown,data_qc);
        self.export_batchFile(batchFile_data, batchFile_header, batch_fileName_I); #analyst cannot read in csv files for some reason, only txt files
    def execute_deleteSamplesFromExperiment(self,experiment_id_I, sample_ids_I):
        '''remove specific samples from an experiment by their sample ID

        NOTES: DELETE statement appears to be broken

        remove samples from
        1. experiment
        2. sample
        3. sample_description, sample_storage, sample_physiologicalparameters
        '''

        dataListDelete = [];
        for si in sample_ids_I:
            dataListDelete.append({'experiment_id':experiment_id_I,
                                   'sample_id':si});
        # remove samples in order
        self.delete_sample_experimentIDAndSampleID_experiment(dataListDelete);
        self.delete_sample_experimentIDAndSampleID_sample(dataListDelete);
        self.delete_sample_experimentIDAndSampleID_sampleDescription(dataListDelete);
        self.delete_sample_experimentIDAndSampleID_sampleStorage(dataListDelete);
        self.delete_sample_experimentIDAndSampleID_samplePhysiologicalParameters(dataListDelete);
    def execute_makeExperimentFromCalibrationFile(self, calibration_fileName_I):
        '''Populate experiment and samples'''

        # Input:
        #   calibration_fileName_I = name of the .csv file with calibrator information

        #import sample file and split into respective tables
        self.import_calibrationFile_add(calibration_fileName_I);
    def execute_deleteExperiments(self,experiment_ids_I=[],sample_names_I=[]):
        '''remove an experiment
        remove samples from the following tables:
        1. experiment
        2. sample
        3. sample_description, sample_storage, sample_physiologicalparameters
        INPUT:
        experiment_ids_I = [] of strings, experiment_id
        sample_names_I = [] of strings, sample_names
        '''

        dataListDelete = [];
        for experiment_id_I in experiment_ids_I:
            #query the sample IDs in the experiment
            #sample_ids = self.get_sampleIDs_experimentID_experiment(experiment_id_I);
            #for si in sample_ids:
            #    dataListDelete.append({'experiment_id':experiment_id_I,
            #                       'sample_id':si});
            if sample_names_I:
                sample_ids,sample_names = [],[];
                for sn in sample_names_I:
                    sample_ids_tmp,sample_names_tmp = [],[];
                    sample_ids_tmp,sample_names_tmp = self.get_sampleIDsAndSampleNames_experimentIDAndSampleName_experiment(experiment_id_I,sn);
                    sample_ids.extend(sample_ids_tmp);
                    sample_names.extend(sample_names_tmp);
            else:
                sample_ids,sample_names = [],[];
                sample_ids,sample_names= self.get_sampleIDsAndSampleNames_experimentID_experiment(experiment_id_I);
            for cnt,si in enumerate(sample_ids):
                dataListDelete.append({'experiment_id':experiment_id_I,
                                   'sample_id':si,
                                   'sample_name':sample_names[cnt]});
        # remove samples in order
        self.delete_sample_experimentIDAndSampleName_experiment(dataListDelete);
        self.delete_sample_sampleName_sample(dataListDelete);
        self.delete_sample_sampleID_sampleDescription(dataListDelete);
        self.delete_sample_sampleID_sampleStorage(dataListDelete);
        self.delete_sample_sampleID_samplePhysiologicalParameters(dataListDelete);
    def execute_makeDefaultExperimentTypes(self):
        '''make default experiment types'''
        experiment_types = [];

    #internal
    def make_batchFile(self,DateAcquisition_I,data_unknown_I,data_qc_I):
        '''make an acquisition batch file from sample_description'''
        batchFile_data_O = [];
        batchFile_header_O = [['% header=SampleName','SampleID',
                            'Comments','AcqMethod','ProcMethod',
                            'RackCode','PlateCode','VialPos',
                            'SmplInjVol','DilutFact','WghtToVol',
                            'Type','RackPos','PlatePos','SetName',
                            'OutputFile']];
        n_racks_max = 6; 
        n_pos_max = 51; # pos 52, 53, and 54 are reserved for a water blank;
        cnt_rack = 3;
        cnt_pos = 1;
        injection_order = [];
        cnt_sample = 0;
        cnt_qc = 0;
        cnt_blank = 0;
        cnt_blank_inj = 0;
        n_blank_max_inj = 20;
        vialPos_blank = 54;
        
        n_qc = len(data_qc_I);

        # injection order:
        # QC01
        # Blank
        # 9 samples in increasing dilution
        # QCx
        # Blank
        # ...
        if data_qc_I:
            vialPos = cnt_pos;
            rackPos = cnt_rack;
            platePos = 1;
            rackCode = 'CStk' + str(platePos) + '-0' + str(rackPos); #e.g. CStk1-01
            setName = DateAcquisition_I + '_' + data_qc_I[cnt_qc]['id'];
            outputFile = DateAcquisition_I + '02/' + DateAcquisition_I + '_' + data_qc_I[cnt_qc]['id'];
            row = [];
            row.append(data_qc_I[cnt_qc]['sample_name']);
            row.append('');
            row.append('');
            row.append(data_qc_I[cnt_qc]['acquisition_method_id']);
            row.append('none');
            row.append(rackCode);
            row.append('VT54')
            row.append(vialPos);
            row.append(10);
            row.append(1);
            row.append(0);
            row.append(data_qc_I[cnt_qc]['sample_type']);
            row.append(rackPos);
            row.append(platePos);
            row.append(setName);
            row.append(outputFile);
            batchFile_data_O.append(row);
            cnt_pos+=1;
            cnt_qc+=1;
        vialPos = cnt_pos;
        rackPos = cnt_rack;
        platePos = 1;
        rackCode = 'CStk' + str(platePos) + '-0' + str(rackPos); #e.g. CStk1-01
        setName = DateAcquisition_I + '_' + data_unknown_I[cnt_sample]['id'];
        outputFile = DateAcquisition_I + '02/' + DateAcquisition_I + '_' + data_unknown_I[cnt_sample]['id'];
        row = [];
        row.append(DateAcquisition_I + '_Blank' + str(cnt_blank));
        row.append('');
        row.append('');
        row.append(data_unknown_I[cnt_sample]['acquisition_method_id']);
        row.append('none');
        row.append(rackCode);
        row.append('VT54')
        row.append(vialPos_blank);
        row.append(10);
        row.append(1);
        row.append(0);
        row.append('Solvent');
        row.append(rackPos);
        row.append(platePos);
        row.append(setName);
        row.append(outputFile);
        batchFile_data_O.append(row);
        cnt_blank+=1;
        cnt_blank_inj+=1;
        for d in data_unknown_I:
            vialPos = cnt_pos;
            rackPos = cnt_rack;
            platePos = 1;
            #rackCode = CStk1-01;
            rackCode = 'CStk' + str(platePos) + '-0' + str(rackPos); #CStk1-01
            setName = DateAcquisition_I + '_' + d['id'];
            outputFile = DateAcquisition_I + '02/' + DateAcquisition_I + '_' + d['id'];
            row = [];
            row.append(d['sample_name']);
            row.append('');
            row.append('');
            row.append(d['acquisition_method_id']);
            row.append('none');
            row.append(rackCode);
            row.append('VT54')
            row.append(vialPos);
            row.append(10);
            row.append(1);
            row.append(0);
            row.append(d['sample_type']);
            row.append(rackPos);
            row.append(platePos);
            row.append(setName);
            row.append(outputFile);
            batchFile_data_O.append(row);

            #row['% header=SampleName']=
            #row['SampleID']=
            #row['Comments']=
            #row['AcqMethod']=
            #row['ProcMethod']=
            #row['RackCode']=
            #row['PlateCode']=
            #row['VialPos']=
            #row['SmplInjVol']=
            #row['DilutFact']=
            #row['WghtToVol']=
            #row['Type']=
            #row['RackPos']=
            #row['PlatePos']=
            #row['SetName']=
            #row['OutputFile']=

            #increment rack and vial positions
            cnt_pos+=1;
            if cnt_pos > n_pos_max:
                cnt_pos = 1;
                cnt_rack+=1;

            cnt_sample +=1;
            if cnt_sample >= 8:
                # add QC and blank
                if data_qc_I and cnt_qc<n_qc:
                    vialPos = cnt_pos;
                    rackPos = cnt_rack;
                    platePos = 1;
                    rackCode = 'CStk' + str(platePos) + '-0' + str(rackPos); #e.g. CStk1-01
                    setName = DateAcquisition_I + '_' + data_qc_I[cnt_qc]['id'];
                    outputFile = DateAcquisition_I + '02/' + DateAcquisition_I + '_' + data_qc_I[cnt_qc]['id'];
                    row = [];
                    row.append(data_qc_I[cnt_qc]['sample_name']);
                    row.append('');
                    row.append('');
                    row.append(data_qc_I[cnt_qc]['acquisition_method_id']);
                    row.append('none');
                    row.append(rackCode);
                    row.append('VT54')
                    row.append(vialPos);
                    row.append(10);
                    row.append(1);
                    row.append(0);
                    row.append(data_qc_I[cnt_qc]['sample_type']);
                    row.append(rackPos);
                    row.append(platePos);
                    row.append(setName);
                    row.append(outputFile);
                    batchFile_data_O.append(row);
                    cnt_pos+=1;
                    cnt_qc+=1;
                    if cnt_pos > n_pos_max:
                        cnt_pos = 1;
                        cnt_rack+=1;

                vialPos = cnt_pos;
                rackPos = cnt_rack;
                platePos = 1;
                rackCode = 'CStk' + str(platePos) + '-0' + str(rackPos); #e.g. CStk1-01
                setName = DateAcquisition_I + '_' + d['id'];
                outputFile = DateAcquisition_I + '02/' + DateAcquisition_I + '_' + d['id'];
                row = [];
                row.append(DateAcquisition_I + '_Blank' + str(cnt_blank));
                row.append('');
                row.append('');
                row.append(d['acquisition_method_id']);
                row.append('none');
                row.append(rackCode);
                row.append('VT54')
                row.append(vialPos_blank);
                row.append(10);
                row.append(1);
                row.append(0);
                row.append('Solvent');
                row.append(rackPos);
                row.append(platePos);
                row.append(setName);
                row.append(outputFile);
                batchFile_data_O.append(row);
                cnt_blank+=1;
                cnt_blank_inj+=1;
                if cnt_blank_inj > n_blank_max_inj:
                    vialPos_blank-=1;
                cnt_sample = 0;

        # add final QC and Blank
        if data_qc_I and cnt_qc<n_qc:
            vialPos = cnt_pos;
            rackPos = cnt_rack;
            platePos = 1;
            rackCode = 'CStk' + str(platePos) + '-0' + str(rackPos); #e.g. CStk1-01
            setName = DateAcquisition_I + '_' + data_qc_I[cnt_qc]['id'];
            outputFile = DateAcquisition_I + '02/' + DateAcquisition_I + '_' + data_qc_I[cnt_qc]['id'];
            row = [];
            row.append(data_qc_I[cnt_qc]['sample_name']);
            row.append('');
            row.append('');
            row.append(data_qc_I[cnt_qc]['acquisition_method_id']);
            row.append('none');
            row.append(rackCode);
            row.append('VT54')
            row.append(vialPos);
            row.append(10);
            row.append(1);
            row.append(0);
            row.append(data_qc_I[cnt_qc]['sample_type']);
            row.append(rackPos);
            row.append(platePos);
            row.append(setName);
            row.append(outputFile);
            batchFile_data_O.append(row);
            cnt_pos+=1;
            cnt_qc+=1;
        vialPos = cnt_pos;
        rackPos = cnt_rack;
        platePos = 1;
        rackCode = 'CStk' + str(platePos) + '-0' + str(rackPos); #e.g. CStk1-01
        setName = DateAcquisition_I + '_' + data_unknown_I[cnt_sample]['id'];
        outputFile = DateAcquisition_I + '02/' + DateAcquisition_I + '_' + data_unknown_I[cnt_sample]['id'];
        row = [];
        row.append(DateAcquisition_I + '_Blank' + str(cnt_blank));
        row.append('');
        row.append('');
        row.append(data_unknown_I[0]['acquisition_method_id']);
        row.append('none');
        row.append(rackCode);
        row.append('VT54')
        row.append(vialPos_blank);
        row.append(10);
        row.append(1);
        row.append(0);
        row.append('Solvent');
        row.append(rackPos);
        row.append(platePos);
        row.append(setName);
        row.append(outputFile);
        batchFile_data_O.append(row);
        cnt_blank+=1;
        cnt_blank_inj+=1;

        return batchFile_data_O, batchFile_header_O;
    def make_techRepsAndDils(self,nTechReps_I, dil_levels_I,
                             sampleDescription_data_I, samplePhysiologicalParameters_data_I, sampleStorage_data_I,
                             sample_data_I,experiment_data_I):
        '''expand experiment and sample tables
        to include technical replicates and dilutions'''

        sampleDescription_data_O = [];
        samplePhysiologicalParameters_data_O = [];
        sampleStorage_data_O = [];
        sample_data_O = [];
        experiment_data_O = [];

        # get the different metabolomics experiment ids:
        experiment_ids = [v['id'] for v in experiment_data_I];
        experiment_ids_unique = list(set(experiment_ids));
        exp_types = [v['exp_type_id'] for v in experiment_data_I];
        exp_types_unique = list(set(exp_types));
        for experiment_id in experiment_ids_unique:
            for exp_type in exp_types_unique:
                # get the bioRep sample names for the experiment
                sample_names = [v['sample_name'] for v in experiment_data_I];
                ## query the maximum number of technical reps based on the experiment id
                #nMaxBioReps = self.get_nMaxBioReps_sampleDescription(experiment_id); # breaks when the number of bio reps is not the same for all samples in an experiment
                for row in sampleDescription_data_I:
                    # query the maximum number of technical reps based on the experiment id and sample name
                    sample_name_abbreviation = self.get_sampleNameAbbreviation_experimentIDAndSampleID(experiment_id,row['sample_id']);
                    #nMaxBioReps = self.get_nMaxBioReps_experimentIDAndSampleNameAbbreviation_sampleDescription(experiment_id,sample_name_abbreviation); # does not take into account exp_type
                    nMaxBioReps = self.get_nMaxBioReps_experimentIDAndSampleNameAbbreviationAndExpType_sampleDescription(experiment_id,sample_name_abbreviation,exp_type);
                    for rep in range(1,nTechReps_I+1):
                        # add techReps to sample Description
                        # copy sample description fields to techReps
                        sample_id_new = '';
                        sample_id_list = row['sample_id'].split('-');
                        sample_dil = None #check for something else besides the replicate number
                        if any(let.isalpha() for let in sample_id_list[len(sample_id_list)-1]): 
                            sample_dil = sample_id_list[len(sample_id_list)-1]
                            sample_id_list = sample_id_list[:-1]
                        for l in range(len(sample_id_list)-1):  sample_id_new += sample_id_list[l] + '-';
                        replicate_number = int(sample_id_list[len(sample_id_list)-1]);
                        sample_id_new += str(nMaxBioReps*rep + replicate_number);
                        if sample_dil: sample_id_new += '-' + sample_dil;
                        sample_name_short_new = '';
                        sample_name_short_list = row['sample_name_short'].split('-');
                        sample_dil = None #check for something else besides the replicate number
                        if any(let.isalpha() for let in sample_name_short_list[len(sample_name_short_list)-1]): 
                            sample_dil = sample_name_short_list[len(sample_name_short_list)-1]
                            sample_name_short_list = sample_name_short_list[:-1]
                        for l in range(len(sample_name_short_list)-1):  sample_name_short_new += sample_name_short_list[l] + '-';
                        sample_name_short_new += str(nMaxBioReps*rep + replicate_number);
                        if sample_dil: sample_name_short_new += '-' + sample_dil;
                        sampleDescription_data_O.append({'sample_id':sample_id_new, #change sample_id
                                                'sample_name_short':sample_name_short_new, #change sample_name_short
                                                'sample_name_abbreviation':row['sample_name_abbreviation'],
                                                'sample_date':row['sample_date'],
                                                'time_point':row['time_point'],
                                                'sample_condition':row['sample_condition'],
                                                'extraction_method_id':row['extraction_method_id'],
                                                'biological_material':row['biological_material'],
                                                'sample_desc':row['sample_desc'],
                                                'sample_replicate':nMaxBioReps*rep + replicate_number,# modify sample_replicate_biological
                                                'is_added':row['is_added'],
                                                'is_added_units':row['is_added_units'],
                                                'reconstitution_volume':row['reconstitution_volume'],
                                                'reconstitution_volume_units':row['reconstitution_volume_units'],
                                                'sample_replicate_biological':row['sample_replicate_biological'],
                                                'istechnical':True,
                                                'notes':row['notes']});# modify istech (True)
                for row in samplePhysiologicalParameters_data_I:
                    # query the maximum number of technical reps based on the experiment id and sample name
                    sample_name_abbreviation = self.get_sampleNameAbbreviation_experimentIDAndSampleID(experiment_id,row['sample_id']);
                    #nMaxBioReps = self.get_nMaxBioReps_experimentIDAndSampleNameAbbreviation_sampleDescription(experiment_id,sample_name_abbreviation); # does not take into account exp_type
                    nMaxBioReps = self.get_nMaxBioReps_experimentIDAndSampleNameAbbreviationAndExpType_sampleDescription(experiment_id,sample_name_abbreviation,exp_type);
                    for rep in range(1,nTechReps_I+1):
                        # add techReps to physiological parameters
                        # copy physiological parameters fields to techReps
                        sample_id_new = '';
                        sample_id_list = row['sample_id'].split('-');
                        sample_dil = None #check for something else besides the replicate number
                        if any(let.isalpha() for let in sample_id_list[len(sample_id_list)-1]): 
                            sample_dil = sample_id_list[len(sample_id_list)-1]
                            sample_id_list = sample_id_list[:-1]
                        for l in range(len(sample_id_list)-1):  sample_id_new += sample_id_list[l] + '-';
                        replicate_number = int(sample_id_list[len(sample_id_list)-1]);
                        sample_id_new += str(nMaxBioReps*rep + replicate_number);
                        if sample_dil: sample_id_new += '-' + sample_dil;
                        samplePhysiologicalParameters_data_O.append({'sample_id':sample_id_new,
                                            'growth_condition_short':row['growth_condition_short'],
                                            'growth_condition_long':row['growth_condition_long'],
                                            'media_short':row['media_short'],
                                            'media_long':row['media_long'],
                                            'isoxic':row['isoxic'],
                                            'temperature':row['temperature'],
                                            'supplementation':row['supplementation'],
                                            'od600':row['od600'],
                                            'vcd':row['vcd'],
                                            'culture_density':row['culture_density'],
                                            'culture_volume_sampled':row['culture_volume_sampled'],
                                            'cells':row['cells'],
                                            'dcw':row['dcw'],
                                            'wcw':row['wcw'],
                                            'vcd_units':row['vcd_units'],
                                            'culture_density_units':row['culture_density_units'],
                                            'culture_volume_sampled_units':row['culture_volume_sampled_units'],
                                            'dcw_units':row['dcw_units'],
                                            'wcw_units':row['wcw_units']});
                for row in sampleStorage_data_I:
                    # query the maximum number of technical reps based on the experiment id and sample name
                    sample_name_abbreviation = self.get_sampleNameAbbreviation_experimentIDAndSampleID(experiment_id,row['sample_id']);
                    #nMaxBioReps = self.get_nMaxBioReps_experimentIDAndSampleNameAbbreviation_sampleDescription(experiment_id,sample_name_abbreviation); # does not take into account exp_type
                    nMaxBioReps = self.get_nMaxBioReps_experimentIDAndSampleNameAbbreviationAndExpType_sampleDescription(experiment_id,sample_name_abbreviation,exp_type);
                    for rep in range(1,nTechReps_I+1):
                        # add techReps to storage
                        # copy storage parameter fields to techReps
                        # modify box/pos (point back to the biological replicate)
                        sample_id_new = '';
                        sample_id_list = row['sample_id'].split('-');
                        sample_dil = None #check for something else besides the replicate number
                        if any(let.isalpha() for let in sample_id_list[len(sample_id_list)-1]): 
                            sample_dil = sample_id_list[len(sample_id_list)-1]
                            sample_id_list = sample_id_list[:-1]
                        for l in range(len(sample_id_list)-1):  sample_id_new += sample_id_list[l] + '-';
                        replicate_number = int(sample_id_list[len(sample_id_list)-1]);
                        sample_id_new += str(nMaxBioReps*rep + replicate_number);
                        if sample_dil: sample_id_new += '-' + sample_dil;
                        sampleStorage_data_O.append({'sample_id':sample_id_new,
                                            'sample_label':row['sample_label'],
                                            'ph':row['ph'],
                                            'box':row['box'],
                                            'pos':row['pos']});
                for row in sample_data_I:
                    # add techReps to sample
                    # copy sample fields to techReps
                    # add dilutions to sample
                    # copy sample fields for bio/techReps to dilutions
                    # modify sample_dilution field to reflect the dilution factor

                    # query the maximum number of technical reps based on the experiment id and sample name
                    sample_name_abbreviation = self.get_sampleNameAbbreviation_experimentIDAndSampleName(experiment_id,row['sample_name']);
                    #nMaxBioReps = self.get_nMaxBioReps_experimentIDAndSampleNameAbbreviation_sampleDescription(experiment_id,sample_name_abbreviation); # does not take into account exp_type
                    nMaxBioReps = self.get_nMaxBioReps_experimentIDAndSampleNameAbbreviationAndExpType_sampleDescription(experiment_id,sample_name_abbreviation,exp_type);
                    for dil in dil_levels_I:
                        sample_name_new_dil = copy(row['sample_name']);
                        sample_name_new_dil += '-' + str(dil) + 'x';
                        sample_data_O.append({'sample_name':sample_name_new_dil,
                                        'sample_type':row['sample_type'],
                                        'calibrator_id':None,
                                        'calibrator_level':None,
                                        'sample_id':row['sample_id'],
                                        'sample_dilution':dil});
                    for rep in range(1,nTechReps_I+1):
                        sample_id_new = '';
                        sample_id_list = row['sample_id'].split('-');
                        sample_dil = None #check for something else besides the replicate number
                        if any(let.isalpha() for let in sample_id_list[len(sample_id_list)-1]): 
                            sample_dil = sample_id_list[len(sample_id_list)-1]
                            sample_id_list = sample_id_list[:-1]
                        for l in range(len(sample_id_list)-1):  sample_id_new += sample_id_list[l] + '-';
                        replicate_number = int(sample_id_list[len(sample_id_list)-1]);
                        sample_id_new += str(nMaxBioReps*rep + replicate_number);
                        if sample_dil: sample_id_new += '-' + sample_dil;
                        sample_name_new = '';
                        sample_name_list = row['sample_name'].split('-');
                        sample_dil = None #check for something else besides the replicate number
                        if any(let.isalpha() for let in sample_name_list[len(sample_name_list)-1]): 
                            sample_dil = sample_name_list[len(sample_name_list)-1]
                            sample_name_list = sample_name_list[:-1]
                        for l in range(len(sample_name_list)-1):  sample_name_new += sample_name_list[l] + '-';
                        sample_name_new += str(nMaxBioReps*rep + replicate_number);
                        if sample_dil: sample_name_new += '-' + sample_dil;
                        sample_data_O.append({'sample_name':sample_name_new,
                                            'sample_type':row['sample_type'],
                                            'calibrator_id':None,
                                            'calibrator_level':None,
                                            'sample_id':sample_id_new,
                                            'sample_dilution':row['sample_dilution']});
                        for dil in dil_levels_I:
                            sample_name_new_dil = copy(sample_name_new);
                            sample_name_new_dil += '-' + str(dil) + 'x';
                            sample_data_O.append({'sample_name':sample_name_new_dil,
                                            'sample_type':row['sample_type'],
                                            'calibrator_id':None,
                                            'calibrator_level':None,
                                            'sample_id':sample_id_new,
                                            'sample_dilution':dil});
                        
                for row in experiment_data_I:
                    # query the maximum number of technical reps based on the experiment id and sample name
                    sample_name_abbreviation = self.get_sampleNameAbbreviation_experimentIDAndSampleName(experiment_id,row['sample_name']);
                    #nMaxBioReps = self.get_nMaxBioReps_experimentIDAndSampleNameAbbreviation_sampleDescription(experiment_id,sample_name_abbreviation); # does not take into account exp_type
                    nMaxBioReps = self.get_nMaxBioReps_experimentIDAndSampleNameAbbreviationAndExpType_sampleDescription(experiment_id,sample_name_abbreviation,exp_type);
                    # add techReps and dilutions to experiment
                    # copy experiment fields to techReps and dilutions
                    for dil in dil_levels_I:
                        sample_name_new_dil = copy(row['sample_name']);
                        sample_name_new_dil += '-' + str(dil) + 'x';
                        experiment_data_O.append({'exp_type_id':row['exp_type_id'],
                                            'id':row['id'],
                                            'sample_name':sample_name_new_dil,
                                            'experimentor_id':row['experimentor_id'],
                                            'extraction_method_id':row['extraction_method_id'],
                                            'acquisition_method_id':row['acquisition_method_id'],
                                            'quantitation_method_id':row['quantitation_method_id'],
                                            'internal_standard_id':row['internal_standard_id']});

                    for rep in range(1,nTechReps_I+1):
                        sample_name_new = '';
                        sample_name_list = row['sample_name'].split('-');
                        sample_dil = None #check for something else besides the replicate number
                        if any(let.isalpha() for let in sample_name_list[len(sample_name_list)-1]): 
                            sample_dil = sample_name_list[len(sample_name_list)-1]
                            sample_name_list = sample_name_list[:-1]
                        for l in range(len(sample_name_list)-1):  sample_name_new += sample_name_list[l] + '-';
                        replicate_number = int(sample_name_list[len(sample_name_list)-1]);
                        sample_name_new += str(nMaxBioReps*rep + replicate_number);
                        if sample_dil: sample_name_new += '-' + sample_dil;
                        experiment_data_O.append({'exp_type_id':row['exp_type_id'],
                                            'id':row['id'],
                                            'sample_name':sample_name_new,
                                            'experimentor_id':row['experimentor_id'],
                                            'extraction_method_id':row['extraction_method_id'],
                                            'acquisition_method_id':row['acquisition_method_id'],
                                            'quantitation_method_id':row['quantitation_method_id'],
                                            'internal_standard_id':row['internal_standard_id']});

                        for dil in dil_levels_I:
                            sample_name_new_dil = copy(sample_name_new);
                            sample_name_new_dil += '-' + str(dil) + 'x';
                            experiment_data_O.append({'exp_type_id':row['exp_type_id'],
                                            'id':row['id'],
                                            'sample_name':sample_name_new_dil,
                                            'experimentor_id':row['experimentor_id'],
                                            'extraction_method_id':row['extraction_method_id'],
                                            'acquisition_method_id':row['acquisition_method_id'],
                                            'quantitation_method_id':row['quantitation_method_id'],
                                            'internal_standard_id':row['internal_standard_id']});

        return sampleDescription_data_O, samplePhysiologicalParameters_data_O, sampleStorage_data_O, sample_data_O,experiment_data_O;
                                    
   