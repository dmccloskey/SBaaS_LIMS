from .lims_experiment_query import lims_experiment_query
from .lims_experimentor_query import lims_experimentor_query
from .lims_sample_query import lims_sample_query
from .lims_extractionMethod_query import lims_extractionMethod_query
from .lims_acquisitionMethod_query import lims_acquisitionMethod_query
#from .lims_quantitationMethod_query import lims_quantitationMethod_query
from SBaaS_base.sbaas_template_io import sbaas_template_io

# Resources
from io_utilities.base_importData import base_importData
from io_utilities.base_exportData import base_exportData
from ddt_python.ddt_container_table import ddt_container_table

class lims_experiment_io(lims_experiment_query,
                              lims_experimentor_query,
                              lims_sample_query,
                              lims_extractionMethod_query,
                              lims_acquisitionMethod_query,
                              #lims_quantitationMethod_query,
                              sbaas_template_io):
    def import_sampleFile_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        # split into seperate data structures based on the destined table add
        sampleDescription_data = [];
        samplePhysiologicalParameters_data = [];
        sampleStorage_data = [];
        sample_data = [];
        experiment_data = [];
        for d in data.data:
            sampleDescription_data.append({'sample_id':d['sample_id'],
                                        'sample_name_short':d['sample_name_short'],
                                        'sample_name_abbreviation':d['sample_name_abbreviation'],
                                        'sample_date':d['sample_date'],
                                        'time_point':d['time_point'],
                                        'sample_condition':d['sample_condition'],
                                        'extraction_method_id':d['extraction_method_id'],
                                        'biological_material':d['biological_material'],
                                        'sample_desc':d['sample_description'],
                                        'sample_replicate':d['sample_replicate'],
                                        'is_added':d['is_added'],
                                        'is_added_units':d['is_added_units'],
                                        'reconstitution_volume':d['reconstitution_volume'],
                                        'reconstitution_volume_units':d['reconstitution_volume_units'],
                                        #'sample_replicate_biological':d['sample_replicate'],
                                        #'istechnical':False});
                                        'sample_replicate_biological':d['sample_replicate_biological'],
                                        'istechnical':d['istechnical'],
                                        'notes':d['notes']});
            samplePhysiologicalParameters_data.append({'sample_id':d['sample_id'],
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
                                        'wcw_units':d['wcw_units']});
            sampleStorage_data.append({'sample_id':d['sample_id'],
                                        'sample_label':d['sample_label'],
                                        'ph':d['ph'],
                                        'box':d['box'],
                                        'pos':d['pos']});
            sample_data.append({'sample_name':d['sample_id'],
                                        #'sample_name':d['sample_name'],
                                        'sample_type':d['sample_type'],
                                        #'sample_type':'Unknown',
                                        'calibrator_id':None,
                                        'calibrator_level':None,
                                        #'calibrator_id':d['calibrator_id'],
                                        #'calibrator_level':d['calibrator_level'],
                                        'sample_id':d['sample_id'],
                                        'sample_dilution':1.0});
                                        #'sample_dilution':d['sample_dilution']});
            experiment_data.append({'exp_type_id':d['exp_type_id'],
                                        'id':d['experiment_id'],
                                        'sample_name':d['sample_id'],
                                        #'sample_name':d['sample_name'],
                                        'experimentor_id':d['experimentor_id'],
                                        'extraction_method_id':d['extraction_method_id'],
                                        'acquisition_method_id':d['acquisition_method_id'],
                                        'quantitation_method_id':d['quantitation_method_id'],
                                        'internal_standard_id':d['is_id']});
        # add data to the database:
        self.add_sampleDescription(sampleDescription_data);
        self.add_samplePhysiologicalParameters(samplePhysiologicalParameters_data);
        self.add_sampleStorage(sampleStorage_data);
        self.add_sample(sample_data);
        self.add_experiment(experiment_data);
        # deallocate memory
        data.clear_data();

        return sampleDescription_data,samplePhysiologicalParameters_data,sampleStorage_data,sample_data,experiment_data;
    def import_sampleFile_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        # split into seperate data structures based on the destined table add
        sampleDescription_data = [];
        samplePhysiologicalParameters_data = [];
        sampleStorage_data = [];
        sample_data = [];
        experiment_data = [];
        for d in data.data:
            sampleDescription_data.append({'sample_id':d['sample_id'],
                                        'sample_name_short':d['sample_name_short'],
                                        'sample_name_abbreviation':d['sample_name_abbreviation'],
                                        'sample_date':d['sample_date'],
                                        'time_point':d['time_point'],
                                        'sample_condition':d['sample_condition'],
                                        'extraction_method_id':d['extraction_method_id'],
                                        'biological_material':d['biological_material'],
                                        'sample_desc':d['sample_description'],
                                        'sample_replicate':d['sample_replicate'],
                                        'is_added':d['is_added'],
                                        'is_added_units':d['is_added_units'],
                                        'reconstitution_volume':d['reconstitution_volume'],
                                        'reconstitution_volume_units':d['reconstitution_volume_units'],
                                        #'sample_replicate_biological':d['sample_replicate'],
                                        #'istechnical':False});
                                        'sample_replicate_biological':d['sample_replicate_biological'],
                                        'istechnical':d['istechnical'],
                                        'notes':d['notes']});
            samplePhysiologicalParameters_data.append({'sample_id':d['sample_id'],
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
                                        'wcw_units':d['wcw_units']});
            sampleStorage_data.append({'sample_id':d['sample_id'],
                                        'sample_label':d['sample_label'],
                                        'ph':d['ph'],
                                        'box':d['box'],
                                        'pos':d['pos']});
            sample_data.append({'sample_name':d['sample_id'],
                                        #'sample_name':d['sample_name'],
                                        'sample_type':d['sample_type'],
                                        #'sample_type':'Unknown',
                                        'calibrator_id':None,
                                        'calibrator_level':None,
                                        #'calibrator_id':d['calibrator_id'],
                                        #'calibrator_level':d['calibrator_level'],
                                        'sample_id':d['sample_id'],
                                        'sample_dilution':1.0});
                                        #'sample_dilution':d['sample_dilution']});
            experiment_data.append({'exp_type_id':d['exp_type_id'],
                                        'id':d['experiment_id'],
                                        'sample_name':d['sample_id'],
                                        #'sample_name':d['sample_name'],
                                        'experimentor_id':d['experimentor_id'],
                                        'extraction_method_id':d['extraction_method_id'],
                                        'acquisition_method_id':d['acquisition_method_id'],
                                        'quantitation_method_id':d['quantitation_method_id'],
                                        'internal_standard_id':d['is_id']});
        # add data to the database:
        self.update_sampleDescription(sampleDescription_data);
        self.update_samplePhysiologicalParameters(samplePhysiologicalParameters_data);
        self.update_sampleStorage(sampleStorage_data);
        self.update_sample(sample_data);
        self.update_experiment(experiment_data);
        # deallocate memory
        data.clear_data();

        return sampleDescription_data,samplePhysiologicalParameters_data,sampleStorage_data,sample_data,experiment_data;
    def export_batchFile(self, data_I, header_I, filename):
        export = base_exportData(data_I)
        export.write_headersAndElements2txt(header_I,filename)
        return;
    def import_calibrationFile_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        # split into seperate data structures based on the destined table add
        sample_data = [];
        experiment_data = [];
        for d in data.data:
            sample_data.append({'sample_name':d['sample_name'],
                                        'sample_type':d['sample_type'],
                                        'calibrator_id':d['calibrator_id'],
                                        'calibrator_level':d['calibrator_level'],
                                        'sample_id':d['sample_id'],
                                        'sample_dilution':d['sample_dilution']});
            experiment_data.append({'exp_type_id':d['exp_type_id'],
                                        'id':d['experiment_id'],
                                        'sample_name':d['sample_name'],
                                        'experimentor_id':d['experimentor_id'],
                                        'extraction_method_id':d['extraction_method_id'],
                                        'acquisition_method_id':d['acquisition_method_id'],
                                        'quantitation_method_id':d['quantitation_method_id'],
                                        'internal_standard_id':d['is_id']});
        # add data to the database:
        self.add_sample(sample_data);
        self.add_experiment(experiment_data);
        # deallocate memory
        data.clear_data();
    def import_calibration_sampleAndComponents(self, filename):
        '''import calibration curve sample and component information'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        # split into separate data structures
        samplesComponents_data = [];
        for d in data.data:
            samplesComponents_data.append({'sample_name':d['Sample Name'],
                                           'sample_type':d['Sample Type'],
                                           'met_id':d['Component Group Name']});

        data.clear_data();
        return samplesComponents_data;

    def export_rows_experimentID_sample_csv(self, experiment_id_I,filename_O):
        '''export rows of table sample by experiment_id'''
        data_O = [];
        data_O = self.get_rows_experimentID_sample('ALEsKOs01');
        if data_O:
            baseo = base_exportData(data_O);
        else:
            print('no rows found.');
    def export_rows_experimentID_sample_js(self, experiment_id_I,data_dir_I='tmp'):
        '''export rows of table sample by experiment_id
        INPUT:
        experiment_id_I = string
        data_dir_I = data directory to write to
        '''

        data_O = [];
        data_O = self.get_rows_experimentID_sample(experiment_id_I);

        # dump chart parameters to a js files
        data1_keys = list(data_O[0].keys());
        data1_nestkeys = ['sample_id'];
        data1_keymap = {'xdata':'',
                        'ydata':'',
                        'serieslabel':'',
                        'featureslabel':''};

        ddttable = ddt_container_table()
        ddttable.make_container_table(data_O,data1_keys,data1_nestkeys,data1_keymap,tabletype='responsivetable_01');

        if data_dir_I=='tmp':
            filename_str = self.settings['visualization_data'] + '/tmp/ddt_data.js'
        elif data_dir_I=='data_json':
            data_json_O = ddttable.get_allObjects_js();
            return data_json_O;
        with open(filename_str,'w') as file:
            file.write(ddttable.get_allObjects());
    def export_rows_experimentID_sampleDescription_js(self, experiment_id_I,data_dir_I='tmp'):
        '''export rows of table sample_description by experiment_id
        INPUT:
        experiment_id_I = string
        data_dir_I = data directory to write to
        '''

        data_O = [];
        data_O = self.get_rows_experimentID_sampleDescription(experiment_id_I);

        # dump chart parameters to a js files
        data1_keys = list(data_O[0].keys());
        data1_nestkeys = ['sample_id'];
        data1_keymap = {'xdata':'',
                        'ydata':'',
                        'serieslabel':'',
                        'featureslabel':''};

        ddttable = ddt_container_table()
        ddttable.make_container_table(data_O,data1_keys,data1_nestkeys,data1_keymap,tabletype='responsivetable_01');

        if data_dir_I=='tmp':
            filename_str = self.settings['visualization_data'] + '/tmp/ddt_data.js'
        elif data_dir_I=='data_json':
            data_json_O = ddttable.get_allObjects_js();
            return data_json_O;
        with open(filename_str,'w') as file:
            file.write(ddttable.get_allObjects());
    def export_rows_experimentID_sampleStorage_js(self, experiment_id_I,data_dir_I='tmp'):
        '''export rows of table sample_storage by experiment_id
        INPUT:
        experiment_id_I = string
        data_dir_I = data directory to write to
        '''

        data_O = [];
        data_O = self.get_rows_experimentID_sampleStorage(experiment_id_I);

        # dump chart parameters to a js files
        data1_keys = list(data_O[0].keys());
        data1_nestkeys = ['sample_id'];
        data1_keymap = {'xdata':'',
                        'ydata':'',
                        'serieslabel':'',
                        'featureslabel':''};

        ddttable = ddt_container_table()
        ddttable.make_container_table(data_O,data1_keys,data1_nestkeys,data1_keymap,tabletype='responsivetable_01');

        if data_dir_I=='tmp':
            filename_str = self.settings['visualization_data'] + '/tmp/ddt_data.js'
        elif data_dir_I=='data_json':
            data_json_O = ddttable.get_allObjects_js();
            return data_json_O;
        with open(filename_str,'w') as file:
            file.write(ddttable.get_allObjects());
    def export_rows_experimentID_samplePhysiologicalParameters_js(self, experiment_id_I,data_dir_I='tmp'):
        '''export rows of table sample_physiologicalParameters by experiment_id
        INPUT:
        experiment_id_I = string
        data_dir_I = data directory to write to
        '''

        data_O = [];
        data_O = self.get_rows_experimentID_samplePhysiologicalParameters(experiment_id_I);

        # dump chart parameters to a js files
        data1_keys = list(data_O[0].keys());
        data1_nestkeys = ['sample_id'];
        data1_keymap = {'xdata':'',
                        'ydata':'',
                        'serieslabel':'',
                        'featureslabel':''};

        ddttable = ddt_container_table()
        ddttable.make_container_table(data_O,data1_keys,data1_nestkeys,data1_keymap,tabletype='responsivetable_01');

        if data_dir_I=='tmp':
            filename_str = self.settings['visualization_data'] + '/tmp/ddt_data.js'
        elif data_dir_I=='data_json':
            data_json_O = ddttable.get_allObjects_js();
            return data_json_O;
        with open(filename_str,'w') as file:
            file.write(ddttable.get_allObjects());
    def export_rows_experimentID_experiment_js(self,experiment_id_I,data_dir_I='tmp'):
        
        tables = ['experiment'];
        query = {};
        query['select'] = {tables[0]:None};
        query['where'] = {tables[0]:{
	        'id':{
		        'value':self.convert_string2StringString(experiment_id_I),
		        'operator':'LIKE',
		        },
	        },
        };
        self.export_rows_tables_table_js(
                tables_I=tables,
                query_I=query,
                data_dir_I=data_dir_I);
