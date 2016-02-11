# sbaas
from .lims_msMethod_postgresql_models import *
from SBaaS_base.postgresql_dataType_converter import postgresql_dataType_converter
from SBaaS_base.sbaas_base_query_update import sbaas_base_query_update
from SBaaS_base.sbaas_base_query_drop import sbaas_base_query_drop
from SBaaS_base.sbaas_base_query_initialize import sbaas_base_query_initialize
from SBaaS_base.sbaas_base_query_insert import sbaas_base_query_insert
from SBaaS_base.sbaas_base_query_select import sbaas_base_query_select
from SBaaS_base.sbaas_base_query_delete import sbaas_base_query_delete

from SBaaS_base.sbaas_template_query import sbaas_template_query

class lims_msMethod_query(sbaas_template_query):
    
    def initialize_supportedTables(self):
        '''Set the supported tables dict for 
        '''
        tables_supported = {'ms_component_list':MS_component_list,
                'ms_components':MS_components,
                'ms_information':MS_information,
                'ms_method':MS_method,
                'ms_sourceparameters':MS_sourceParameters,
                        };
        self.set_supportedTables(tables_supported);

    def update_componentNames(self):
        '''update component names for quant and isotopomer methods'''
        return
       
    #table initializations:
    def drop_lims_msMethod(self):
        try:
            MS_components.__table__.drop(self.engine,True);
            MS_sourceParameters.__table__.drop(self.engine,True);
            MS_information.__table__.drop(self.engine,True);
            MS_method.__table__.drop(self.engine,True);
            MS_component_list.__table__.drop(self.engine,True);

        except SQLAlchemyError as e:
            print(e);
    def reset_lims_msMethod(self):
        try:
            reset = self.session.query(MS_components).delete(synchronize_session=False);
            reset = self.session.query(MS_sourceParameters).delete(synchronize_session=False);
            reset = self.session.query(MS_information).delete(synchronize_session=False);
            reset = self.session.query(MS_method).delete(synchronize_session=False);
            reset = self.session.query(MS_component_list).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def initialize_lims_msMethod(self):
        try:
            MS_components.__table__.create(self.engine,True);
            MS_sourceParameters.__table__.create(self.engine,True);
            MS_information.__table__.create(self.engine,True);
            MS_method.__table__.create(self.engine,True);
            MS_component_list.__table__.create(self.engine,True);

        except SQLAlchemyError as e:
            print(e);
            
    def update_MSComponents_precursorFormulaAndMass(self,data_I):
        '''update rows of ms_components
        for columns of precursor_formula and precursor_exact_mass'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(MS_components).filter(
                           MS_components.met_id.like(d['met_id']),
                           MS_components.q1_mass == d['q1_mass'],
                           MS_components.q3_mass == d['q3_mass']).update(
                            {'precursor_formula':d['precursor_formula'],
                            'precursor_exactmass':d['precursor_exactmass']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def add_MSComponents(self, data_I):
        '''add rows of ms_components'''
        pgdatatypeconverter = postgresql_dataType_converter();
        if data_I:
            for d in data_I:
                try:
                    data_add = MS_components(d
                        #d['q1_mass'],
                        #d['q3_mass'],
                        #d['ms3_mass'],
                        #d['met_name'],
                        #d['dp'],
                        #d['ep'],
                        #d['ce'],
                        #d['cxp'],
                        #d['af'],
                        #d['quantifier'],
                        #d['ms_mode'],
                        #d['ion_intensity_rank'],
                        #d['ion_abundance'],
                        #d['precursor_formula'],
                        #d['product_ion_reference'],
                        #d['product_formula'],
                        #d['production_ion_notes'],
                        #d['met_id'],
                        #d['external_reference'],
                        #d['q1_mass_units'],
                        #d['q3_mass_units'],
                        #d['ms3_mass_units'],
                        #d['threshold_units'],
                        #d['dp_units'],
                        #d['ep_units'],
                        #d['ce_units'],
                        #d['cxp_units'],
                        #d['af_units'],
                        #d['ms_group'],
                        #d['threshold'],
                        #d['dwell_weight'],
                        #d['component_name'],
                        #pgdatatypeconverter.convert_text2PostgresqlDataType(d['ms_include']),
                        #pgdatatypeconverter.convert_text2PostgresqlDataType(d['ms_is']),
                        #pgdatatypeconverter.convert_text2List(d['precursor_fragment']),
                        #pgdatatypeconverter.convert_text2List(d['product_fragment']),
                        #d['precursor_exactmass'],
                        #d['product_exactmass'],
                        #d['ms_methodtype'],
                        #pgdatatypeconverter.convert_text2List(d['precursor_fragment_elements']),
                        #pgdatatypeconverter.convert_text2List(d['product_fragment_elements'])
                        );
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def add_MSInformation(self, data_I):
        '''add rows of ms_information'''
        if data_I:
            for d in data_I:
                try:
                    data_add = MS_information(d
                        );
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def add_MSSourceParameters(self, data_I):
        '''add rows of ms_sourceparameters'''
        if data_I:
            for d in data_I:
                try:
                    data_add = MS_sourceParameters(d
                        );
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def add_MSComponentList(self, data_I):
        '''add rows of ms_component_list'''
        if data_I:
            for d in data_I:
                try:
                    data_add = MS_component_list(d
                        #d['ms_method_id'],
                        #d['q1_mass'],
                        #d['q3_mass'],
                        #d['met_id'],
                        #d['component_name'],
                        #d['ms_methodtype']
                        );
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def add_MSMethod(self, data_I):
        '''add rows of ms_method'''
        if data_I:
            for d in data_I:
                try:
                    data_add = MS_method(d
                        #d['id'],
                        #d['ms_sourceparameters_id'],
                        #d['ms_information_id'],
                        #d['ms_experiment_id']
                                         );
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def get_Q1AndQ3MassAndMode_MSComponents(self,met_id_I):
        '''Querry q1 mass, q3 mass, and ms_mode from ms_components'''
        try:
            mscomponents = self.session.query(MS_components.q1_mass,
                    MS_components.q3_mass,
                    MS_components.ms_mode).filter(
                    MS_components.met_id.like(met_id_I)).order_by(
                    MS_components.ms_mode.asc(),
                    MS_components.q1_mass.asc(),
                    MS_components.q3_mass.asc()).all();
            mscomponents_O = [];
            for msc in mscomponents: 
                mscomponents_1 = {};
                mscomponents_1['met_id'] = met_id_I;
                mscomponents_1['q1_mass'] = msc.q1_mass;
                mscomponents_1['q3_mass'] = msc.q3_mass;
                mscomponents_1['ms_mode'] = msc.ms_mode;
                mscomponents_O.append(mscomponents_1);
            return mscomponents_O;
        except SQLAlchemyError as e:
            print(e);

    def get_row_MSComponents(self,met_id_I,ms_mode_I,ms_methodtype_I):
        '''Querry row from ms_components by met_id, ms_mode, and ms_methodtype'''
        try:
            mscomponents = self.session.query(MS_components.q1_mass,MS_components.q3_mass,
                    MS_components.ms3_mass,MS_components.met_name,MS_components.dp,
                    MS_components.ep,MS_components.ce,MS_components.cxp,MS_components.af,
                    MS_components.quantifier,MS_components.ms_mode,MS_components.ion_intensity_rank,
                    MS_components.ion_abundance,MS_components.precursor_formula,
                    MS_components.product_ion_reference,MS_components.product_formula,
                    MS_components.production_ion_notes,MS_components.met_id,
                    MS_components.external_reference,MS_components.q1_mass_units,
                    MS_components.q3_mass_units,MS_components.ms3_mass_units,
                    MS_components.threshold_units,MS_components.dp_units,
                    MS_components.ep_units,MS_components.ce_units,
                    MS_components.cxp_units,MS_components.af_units,
                    MS_components.ms_group,MS_components.threshold,
                    MS_components.dwell_weight,MS_components.component_name,
                    MS_components.ms_include,MS_components.ms_is,MS_components.precursor_fragment,
                    MS_components.product_fragment,MS_components.precursor_exactmass,
                    MS_components.product_exactmass,MS_components.ms_methodtype).filter(
                    MS_components.met_id.like(met_id_I),
                    MS_components.ms_mode.like(ms_mode_I),
                    MS_components.ms_methodtype.like(ms_methodtype_I)).all();
            mscomponents_O = [];
            if not mscomponents:
                print('bad query for row in ms_components: ')
                print('met_id: ' + met_id_I + ', ms_mode_I: ' + ms_mode_I + ', ms_methodtype_I: ' + ms_methodtype_I);
                exit(-1)
            for msc in mscomponents: 
                mscomponents_1 = {};
                mscomponents_1["q1_mass"] = msc.q1_mass;
                mscomponents_1["q3_mass"] = msc.q3_mass;
                mscomponents_1["ms3_mass"] = msc.ms3_mass;
                mscomponents_1["met_name"] = msc.met_name;
                mscomponents_1["dp"] = msc.dp;
                mscomponents_1["ep"] = msc.ep;
                mscomponents_1["ce"] = msc.ce;
                mscomponents_1["cxp"] = msc.cxp;
                mscomponents_1["af"] = msc.af;
                mscomponents_1["quantifier"] = msc.quantifier;
                mscomponents_1["ms_mode"] = msc.ms_mode;
                mscomponents_1["ion_intensity_rank"] = msc.ion_intensity_rank;
                mscomponents_1["ion_abundance"] = msc.ion_abundance;
                mscomponents_1["precursor_formula"] = msc.precursor_formula;
                mscomponents_1["product_ion_reference"] = msc.product_ion_reference;
                mscomponents_1["product_formula"] = msc.product_formula;
                mscomponents_1["production_ion_notes"] = msc.production_ion_notes;
                mscomponents_1["met_id"] = msc.met_id;
                mscomponents_1["external_reference"] = msc.external_reference;
                mscomponents_1["q1_mass_units"] = msc.q1_mass_units;
                mscomponents_1["q3_mass_units"] = msc.q3_mass_units;
                mscomponents_1["ms3_mass_units"] = msc.ms3_mass_units;
                mscomponents_1["threshold_units"] = msc.threshold_units;
                mscomponents_1["dp_units"] = msc.dp_units;
                mscomponents_1["ep_units"] = msc.ep_units;
                mscomponents_1["ce_units"] = msc.ce_units;
                mscomponents_1["cxp_units"] = msc.cxp_units;
                mscomponents_1["af_units"] = msc.af_units;
                mscomponents_1["ms_group"] = msc.ms_group;
                mscomponents_1["threshold"] = msc.threshold;
                mscomponents_1["dwell_weight"] = msc.dwell_weight;
                mscomponents_1["component_name"] = msc.component_name;
                mscomponents_1["ms_include"] = msc.ms_include;
                mscomponents_1["ms_is"] = msc.ms_is;
                mscomponents_1["precursor_fragment"] = msc.precursor_fragment;
                mscomponents_1["product_fragment"] = msc.product_fragment;
                mscomponents_1["precursor_exactmass"] = msc.precursor_exactmass;
                mscomponents_1["product_exactmass"] = msc.product_exactmass;
                mscomponents_1["ms_methodtype"] = msc.ms_methodtype;
                mscomponents_O.append(mscomponents_1);
            return mscomponents_O;
        except SQLAlchemyError as e:
            print(e);

    def get_row_MSComponents_metIDAndFormula(self,met_id_I,precursor_formula_I,
                                             product_formula_I,ms_methodtype_I):
        '''Querry row from ms_components by met_id, precursor_formula, product_formula'''
        try:
            mscomponents = self.session.query(MS_components.q1_mass,MS_components.q3_mass,
                    MS_components.ms3_mass,MS_components.met_name,MS_components.dp,
                    MS_components.ep,MS_components.ce,MS_components.cxp,MS_components.af,
                    MS_components.quantifier,MS_components.ms_mode,MS_components.ion_intensity_rank,
                    MS_components.ion_abundance,MS_components.precursor_formula,
                    MS_components.product_ion_reference,MS_components.product_formula,
                    MS_components.production_ion_notes,MS_components.met_id,
                    MS_components.external_reference,MS_components.q1_mass_units,
                    MS_components.q3_mass_units,MS_components.ms3_mass_units,
                    MS_components.threshold_units,MS_components.dp_units,
                    MS_components.ep_units,MS_components.ce_units,
                    MS_components.cxp_units,MS_components.af_units,
                    MS_components.ms_group,MS_components.threshold,
                    MS_components.dwell_weight,MS_components.component_name,
                    MS_components.ms_include,MS_components.ms_is,MS_components.precursor_fragment,
                    MS_components.product_fragment,MS_components.precursor_exactmass,
                    MS_components.product_exactmass,MS_components.ms_methodtype).filter(
                    MS_components.met_id.like(met_id_I),
                    MS_components.precursor_formula.like(precursor_formula_I),
                    MS_components.product_formula.like(product_formula_I),
                    MS_components.ms_methodtype.like(ms_methodtype_I)).all();
            mscomponents_O = [];
            if not mscomponents:
                print('bad query for row in ms_components: ')
                print('met_id: ' + met_id_I + ', precursor_formula_I: ' + precursor_formula_I + ', product_formula_I: ' + product_formula_I + ', ms_methodtype_I: ' + ms_methodtype_I);
                exit(-1)
            for msc in mscomponents: 
                mscomponents_1 = {};
                mscomponents_1["q1_mass"] = msc.q1_mass;
                mscomponents_1["q3_mass"] = msc.q3_mass;
                mscomponents_1["ms3_mass"] = msc.ms3_mass;
                mscomponents_1["met_name"] = msc.met_name;
                mscomponents_1["dp"] = msc.dp;
                mscomponents_1["ep"] = msc.ep;
                mscomponents_1["ce"] = msc.ce;
                mscomponents_1["cxp"] = msc.cxp;
                mscomponents_1["af"] = msc.af;
                mscomponents_1["quantifier"] = msc.quantifier;
                mscomponents_1["ms_mode"] = msc.ms_mode;
                mscomponents_1["ion_intensity_rank"] = msc.ion_intensity_rank;
                mscomponents_1["ion_abundance"] = msc.ion_abundance;
                mscomponents_1["precursor_formula"] = msc.precursor_formula;
                mscomponents_1["product_ion_reference"] = msc.product_ion_reference;
                mscomponents_1["product_formula"] = msc.product_formula;
                mscomponents_1["production_ion_notes"] = msc.production_ion_notes;
                mscomponents_1["met_id"] = msc.met_id;
                mscomponents_1["external_reference"] = msc.external_reference;
                mscomponents_1["q1_mass_units"] = msc.q1_mass_units;
                mscomponents_1["q3_mass_units"] = msc.q3_mass_units;
                mscomponents_1["ms3_mass_units"] = msc.ms3_mass_units;
                mscomponents_1["threshold_units"] = msc.threshold_units;
                mscomponents_1["dp_units"] = msc.dp_units;
                mscomponents_1["ep_units"] = msc.ep_units;
                mscomponents_1["ce_units"] = msc.ce_units;
                mscomponents_1["cxp_units"] = msc.cxp_units;
                mscomponents_1["af_units"] = msc.af_units;
                mscomponents_1["ms_group"] = msc.ms_group;
                mscomponents_1["threshold"] = msc.threshold;
                mscomponents_1["dwell_weight"] = msc.dwell_weight;
                mscomponents_1["component_name"] = msc.component_name;
                mscomponents_1["ms_include"] = msc.ms_include;
                mscomponents_1["ms_is"] = msc.ms_is;
                mscomponents_1["precursor_fragment"] = msc.precursor_fragment;
                mscomponents_1["product_fragment"] = msc.product_fragment;
                mscomponents_1["precursor_exactmass"] = msc.precursor_exactmass;
                mscomponents_1["product_exactmass"] = msc.product_exactmass;
                mscomponents_1["ms_methodtype"] = msc.ms_methodtype;
                mscomponents_O.append(mscomponents_1);
            return mscomponents_O[0];
        except SQLAlchemyError as e:
            print(e);
    def get_msGroup_componentName_MSComponents(self,component_name_I):
        '''Query component group names from the component name
        NOTE: intended to be used within a for loop'''
        try:
            component_group_name = self.session.query(MS_components.ms_group).filter(
                    MS_components.component_name.like(component_name_I)).group_by(
                    MS_components.ms_group).all();
            if len(component_group_name)>1:
                print('more than 1 component_group_name retrieved per component_name')
            component_group_name_O = component_group_name[0].ms_group;
            return component_group_name_O;
        except SQLAlchemyError as e:
            print(e);
    # Query data from ms_components
    def get_precursorFormulaAndProductFormulaAndCMapsAndPositions_metID(self,met_id_I,ms_mode_I,ms_methodtype_I):
        '''Querry precursor formulas for the ms_mode and ms_methodtype experiment'''
        try:
            component_names = self.session.query(MS_components.precursor_formula,
                    MS_components.product_formula,
                    MS_components.precursor_fragment,
                    MS_components.product_fragment,
                    MS_components.precursor_fragment_elements,
                    MS_components.product_fragment_elements).filter(
                    MS_components.met_id.like(met_id_I),
                    MS_components.ms_methodtype.like(ms_methodtype_I),
                    MS_components.ms_mode.like(ms_mode_I)).group_by(
                    MS_components.precursor_formula,
                    MS_components.product_formula,
                    MS_components.precursor_fragment,
                    MS_components.product_fragment,
                    MS_components.precursor_fragment_elements,
                    MS_components.product_fragment_elements).all();
            data_O = {};
            if not component_names: exit('bad query result: get_precursorFormulaAndProductFormulaAndCMaps_metID');
            for cn in component_names:
                data_O[cn.product_formula] = {'fragment':cn.product_fragment,
                                              'fragment_elements':cn.product_fragment_elements};
                data_O[cn.precursor_formula] = {'fragment':cn.precursor_fragment,
                                              'fragment_elements':cn.precursor_fragment_elements};
            return data_O;
        except SQLAlchemyError as e:
            print(e);

    # query precursor and product formulas from MS_components
    def get_precursorAndProductFormulas_metID(self,met_id_I,ms_mode_I,ms_methodtype_I):
        '''Querry precursor product formulas for the ms_mode and ms_methodtype experiment'''
        try:
            component_names = self.session.query(MS_components.precursor_formula,
                    MS_components.product_formula).filter(
                    MS_components.met_id.like(met_id_I),
                    MS_components.ms_methodtype.like(ms_methodtype_I),
                    MS_components.ms_mode.like(ms_mode_I)).group_by(
                    MS_components.precursor_formula,
                    MS_components.product_formula).order_by(
                    MS_components.precursor_formula.asc(),
                    MS_components.product_formula.asc()).all();
            precursor_formulas_O = [];
            product_formulas_O = [];
            if not component_names: exit('bad query result: get_productFormulas_metID');
            for cn in component_names:
                if cn.product_formula: # skip unknown fragments
                    precursor_formulas_O.append(cn.precursor_formula);
                    product_formulas_O.append(cn.product_formula);
            return precursor_formulas_O, product_formulas_O;
        except SQLAlchemyError as e:
            print(e);
    # query precursor formula from MS_components
    def get_precursorFormula_metID(self,met_id_I,ms_mode_I,ms_methodtype_I):
        '''Querry precursor formulas for the ms_mode and ms_methodtype experiment'''
        try:
            component_names = self.session.query(MS_components.precursor_formula).filter(
                    MS_components.met_id.like(met_id_I),
                    MS_components.ms_methodtype.like(ms_methodtype_I),
                    MS_components.ms_mode.like(ms_mode_I)).group_by(
                    MS_components.precursor_formula).all();
            precursor_formula_O = None;
            if not component_names: exit('bad query result: get_precursorFormula_metID');
            for cn in component_names:
                precursor_formula_O = cn[0];
            return precursor_formula_O;
        except SQLAlchemyError as e:
            print(e);
    def get_precursorFormulaAndProductFormulaAndCMaps_metID(self,met_id_I,ms_mode_I,ms_methodtype_I):
        '''Querry precursor/product formulas and fragments for the ms_mode and ms_methodtype experiment'''
        try:
            component_names = self.session.query(MS_components.precursor_formula,
                    MS_components.product_formula,
                    MS_components.precursor_fragment,
                    MS_components.product_fragment).filter(
                    MS_components.met_id.like(met_id_I),
                    MS_components.ms_methodtype.like(ms_methodtype_I),
                    MS_components.ms_mode.like(ms_mode_I)).group_by(
                    MS_components.precursor_formula,
                    MS_components.product_formula,
                    MS_components.precursor_fragment,
                    MS_components.product_fragment).all();
            data_O = {};
            if not component_names: exit('bad query result: get_precursorFormulaAndProductFormulaAndCMaps_metID');
            for cn in component_names:
                data_O[cn.product_formula] = cn.product_fragment;
                data_O[cn.precursor_formula] = cn.precursor_fragment;
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_precursorFormulaAndProductFormula_metID(self,met_id_I,ms_mode_I,ms_methodtype_I):
        '''Query the first precursor/product formula for the ms_mode and ms_methodtype experiment'''
        try:
            component_names = self.session.query(MS_components.precursor_formula,
                    MS_components.product_formula,
                    MS_components.q1_mass,
                    MS_components.q3_mass).filter(
                    MS_components.met_id.like(met_id_I),
                    MS_components.ms_methodtype.like(ms_methodtype_I),
                    MS_components.ms_mode.like(ms_mode_I)).group_by(
                    MS_components.precursor_formula,
                    MS_components.product_formula,
                    MS_components.q1_mass,
                    MS_components.q3_mass).order_by(
                    MS_components.q1_mass.asc(),
                    MS_components.q3_mass.asc(),
                    MS_components.precursor_formula.desc(),
                    MS_components.product_formula.desc()).all();
            data_O = {};
            product_formula_O = None;
            precursor_formula_O = None;
            if not component_names: exit('bad query result: get_precursorFormulaAndProductFormula');
            # only need the first precursor and product formulas (i.e. monoisotopic)
            product_formula_O = component_names[0].product_formula;
            precursor_formula_O = component_names[0].precursor_formula;
            for cn in component_names:
                data_O[cn.product_formula] = cn.q1_mass;
                data_O[cn.precursor_formula] = cn.q3_mass;
            return precursor_formula_O,product_formula_O;
        except SQLAlchemyError as e:
            print(e);
    def get_metIDs_msModeAndMsMethodType(self,ms_mode_I,ms_methodtype_I):
        '''Query met ids for the ms_mode and ms_methodtype experiment'''
        try:
            component_names = self.session.query(MS_components.met_id).filter(
                    MS_components.ms_methodtype.like(ms_methodtype_I),
                    MS_components.ms_mode.like(ms_mode_I)).group_by(
                    MS_components.met_id).order_by(
                    MS_components.met_id.asc()).all();
            met_id_O = [];
            if not component_names: exit('bad query result: get_metIDs_msModeAndMsMethodType');
            for cn in component_names:
                met_id_O.append(cn.met_id);
            return met_id_O;
        except SQLAlchemyError as e:
            print(e);