import re
import io,os
from copy import copy
# resources
from molmass.molmass import Formula
from chemioinformatics_utilities.chemaxon import cxcalc_bin, RunCxcalc
from molmass.molmass import Formula
# sbaas
from .lims_msMethod_io import lims_msMethod_io

class lims_msMethod_execute(lims_msMethod_io):

    def execute_correctMassesFromFormula(self):
        '''Replace the q1_mass, q3_mass, and ms3_mass with the monoisotopic mass from formula'''
        return
    def execute_13CFluxMRM(self,met_ids_I):
        '''generate the MRMs for each compound for m + 0 to m + # carbons in the precursor
        and product formula'''
        # input: 
        #       met_ids_I = [{'met_id': , 'precursor_formula':, 'product_formula':},]
        # ouptput:
        #       dictionary of 13CFlux MRMs

        phosphates = ["O3P-","H2O4P-","HO6P2-"]

        mrms_O = [];
        # loop over each met_id
        for met in met_ids_I:
            # make mass ensemble for precursor
            precursor_Formula_str = re.sub('[+-]', '', met['precursor_formula']);
            precursor_Formula = Formula(precursor_Formula_str);
            precursor_ensemble = self.make_13CEnsemble(met['precursor_formula']);
            if 'C' in precursor_Formula._elements:
                nCpre = precursor_Formula._elements['C'][0]; # count the number of carbon;
            else: nCpre = 0;
            # make mass ensemble for product
            product_Formula_str = re.sub('[+-]', '', met['product_formula']);
            product_Formula = Formula(product_Formula_str);
            product_ensemble = self.make_13CEnsemble(met['product_formula']);
            if 'C' in product_Formula._elements:
                nCpro = product_Formula._elements['C'][0]; # count the number of carbon;
            else: nCpro = 0;

            # query transition from the tuning method
            trans = self.get_row_MSComponents_metIDAndFormula(met['met_id'],met['precursor_formula'],met['product_formula'],'tuning');

            # make component_name, group_name
            trans['ms_methodtype'] = 'isotopomer_13C';
            
            # match precursor to product and add to new mrms list
            for pre_m,pre_Formula in precursor_ensemble.items(): # loop over each precursor
                if nCpre-pre_m < nCpro: nUnlabeled = nCpre-pre_m;
                else: nUnlabeled = nCpro;
                if pre_m < nCpro: nLabeled = pre_m;
                else: nLabeled = nCpro;
                if nUnlabeled > 0 and nUnlabeled < nCpro: pro_m_start = nCpro - nUnlabeled;
                elif nUnlabeled > 0: pro_m_start = 0;
                else: pro_m_start = nCpro;
                for i in range(pro_m_start,nLabeled+1): # loop over each product        
                    trans13C = trans.copy();
                    # make 13C component_name, group_name,...
                    trans13C['component_name'] = trans13C['met_id'] + '.' + trans13C['met_id'] + '_m' + str(pre_m) + '-' + str(i);
                    trans13C['ms_group'] = trans['met_id'] + '.' + trans13C['met_id'] + '_m' + str(pre_m) + '-' + str(i);
                    trans13C['quantifier'] = 1;
                    trans13C['precursor_formula'] = pre_Formula._formula + trans13C['ms_mode'];
                    trans13C['precursor_exactmass'] = pre_Formula.isotope.mass;
                    trans13C['product_formula'] = product_ensemble[i]._formula + trans13C['ms_mode'];
                    trans13C['product_exactmass'] = product_ensemble[i].isotope.mass;
                    trans13C['met_name'] = trans['met_name'] + '-' + pre_Formula._formula + '_' + product_ensemble[i]._formula;
                    trans13C['q1_mass'] = pre_Formula.isotope.mass;
                    trans13C['q3_mass'] = product_ensemble[i].isotope.mass;
                    trans13C['ms3_mass'] = None;
                    trans13C['quantifier'] = None;
                    trans13C['ion_intensity_rank'] = None;
                    trans13C['ion_abundance'] = None;
                    trans13C['ms_include'] = True;

                    mrms_O.append(trans13C);
        
        self.add_MSComponents(mrms_O);       
    def execute_scheduledMRMPro_quant(self,met_ids_I):
        '''generate the MRMs for each compound for the scheduled MRM pro acquisition method'''
        # input: 
        #       met_ids_I = [{'met_id': , 'precursor_formula':, 'product_formula':},]
        # ouptput:
        #       dictionary of MRMs
        
        mrms_O = [];
        # loop over each met_id
        for met in met_ids_I:
            # query transition from the tuning method
            trans = self.get_row_MSComponents_metIDAndFormula(met['met_id'],met['precursor_formula'],met['product_formula'],'tuning');
            transUC13 = trans.copy();
            # make component_name, group_name
            trans['component_name'] = met['met_id'] + '.' + met['met_id'] + '_' + str(trans['quantifier']) + '.Light';
            trans['ms_group'] = met['met_id'];
            trans['ms_methodtype'] = 'quantification';

            # make UC13 component_name, group_name
            transUC13['component_name'] = met['met_id'] + '.' + met['met_id'] + '_' + str(trans['quantifier']) + '.Heavy';
            transUC13['met_ID'] = met['met_id'] + '-UC13';
            transUC13['met_name'] = transUC13['met_name'] + '-UC13';
            transUC13['ms_group'] = met['met_id'] + '-UC13';
            transUC13['ms_methodtype'] = 'quantification';
                
            # make UC13 equivalent: q1/q3_mass, precursor/product_formula, precursor/product_exactmass
            if trans['precursor_formula']:
                trans_precursor_formula = Formula(re.sub('[+-]', '', trans['precursor_formula'])) # remove '-' or '+'
                trans['precursor_formula'] = trans_precursor_formula.formula + trans['ms_mode'];
                trans['precursor_exactmass'] = trans_precursor_formula.isotope.mass;
                if 'C' in list(trans_precursor_formula._elements.keys()):
                    nC = trans_precursor_formula._elements['C'][0];
                    tmp = Formula(trans_precursor_formula.formula);
                    tmp._elements['C'] = {13:nC};
                    transUC13_precursor_formula = Formula(tmp.formula);
                else:
                    transUC13_precursor_formula = trans_precursor_formula;
                transUC13['precursor_formula'] = transUC13_precursor_formula.formula + trans['ms_mode'];
                transUC13['precursor_exactmass'] = transUC13_precursor_formula.isotope.mass;
                # substitute for algorithm that checks for unique q1_masses
                # therefore, must ensure that each q1_mass/q3_mass is unique for a given mode in ms_components
                transUC13['q1_mass'] = trans['q1_mass'] + transUC13_precursor_formula.isotope.mass - trans_precursor_formula.isotope.mass;

            if trans['product_formula']:
                trans_product_formula = Formula(re.sub('[+-]', '', trans['product_formula'])) # remove '-' or '+'
                trans['product_formula'] = trans_product_formula.formula + trans['ms_mode'];
                trans['product_exactmass'] = trans_product_formula.isotope.mass;
                if 'C' in list(trans_product_formula._elements.keys()):
                    nC = trans_product_formula._elements['C'][0];
                    tmp = Formula(trans_product_formula.formula);
                    tmp._elements['C'] = {13:nC};
                    transUC13_product_formula = Formula(tmp.formula);
                else:
                    transUC13_product_formula = trans_product_formula;
                transUC13['product_formula'] = transUC13_product_formula.formula + trans['ms_mode'];
                transUC13['product_exactmass'] = transUC13_product_formula.isotope.mass;
                # substitute for algorithm that checks for unique q1_masses
                # therefore, must ensure that each q1_mass/q3_mass is unique for a given mode in ms_components
                transUC13['q3_mass'] = trans['q3_mass'] + transUC13_product_formula.isotope.mass - trans_product_formula.isotope.mass;
            # set defaults: window = 120 sec, dwell = 1, priority, ms_include = False
            mrms_O.append(trans);
            mrms_O.append(transUC13);
        
        self.add_MSComponents(mrms_O);
    def execute_importStructureFile(self,data_I):
        '''import structure files for a list of metabolites and
        update metabolomics standards table
        
        NOTE: '''
        # input:
        #       data_I = [{met_id = list of metabolite ids,
        #                  file_directory = file directory for structure files
        #                       e.g. data/Compound Structure Files/
        #                  file_ext = extension of the file (e.g. .mol)}]
        # output:
        #       update to standards table
        
        data_O = [];
        for data in data_I:
            # generate the fileName
            fileName = data['file_directory'] + data['met_id'] + data['file_ext'];
            structureFile = '';
            # read in the structure file
            with open (fileName, "r") as myfile:
                structureFile=myfile.read()
            # update the standards table with the structure file
            data_O.append({'met_id':data['met_id'],
                           'structure_file':structureFile,
                           'structure_file_extention':data['file_ext']});
        # update standards table
        self.update_standards_structureFile(data_O);
    def execute_updateFormulaAndMassFromStructure(self, met_ids_I):
        '''update the molecular formula and exact mass of
        standards from imported structure file'''

        data_O = [];
        for met in met_ids_I:
            # query the structure file and extension
            struct_file, struct_file_ext = self.get_structureFile_standards(met);
            # write the structure file to a temporary directory
            struct_file_name = 'data/struct'+struct_file_ext
            with open(struct_file_name, 'w') as outfile:
                outfile.write(struct_file);
            # calculate the formula and exact mass using chemAxon cxcalc
            molfile = os.getcwd() + '/' + struct_file_name
            args = [molfile];
            cmd = 'exactmass';
            res = RunCxcalc(cxcalc_bin,cmd,args)
            res = res.split('\n')[1].split('\t')[1].split('\r')[0]
            exactmass_O = res;
            cmd = 'mass';
            res = RunCxcalc(cxcalc_bin,cmd,args)
            res = res.split('\n')[1].split('\t')[1].split('\r')[0]
            mass_O = res;
            cmd = 'formula';
            res = RunCxcalc(cxcalc_bin,cmd,args)
            res = res.split('\n')[1].split('\t')[1].split('\r')[0]
            formula_O = res;
            # update standards with the formula and exact mass
            data_O.append({'met_id':met,'exactmass':exactmass_O,'mass':mass_O,'formula':formula_O});
        # update standards table
        self.update_standards_formulaAndMass(data_O);
    def execute_updatePrecursorFormulaAndMass(self, met_ids_I):
        '''update the precusor formula and exact mass of
        ms_components from imported structure file'''
        
        # get the mass and exact mass for hydrogen
        # NOTE: mass is in aggrement with chemaxon
        exactmass_h = Formula('H').isotope.mass
        mass_h = Formula('H').mass
        data_O = [];
        for met in met_ids_I:
            # query exact mass and formula from standards
            exactMass_O, formula_O = self.get_exactMassAndFormula_standards(met);
            ## calculate the formula and exact mass using chemAxon cxcalc
            ## query the structure file and extension
            #struct_file, struct_file_ext = self.get_structureFile_standards(met);
            ## write the structure file to a temporary directory
            #struct_file_name = 'data/struct'+struct_file_ext
            #with open(struct_file_name, 'w') as outfile:
            #    outfile.write(struct_file);
            ## calculate the formula and exact mass using chemAxon cxcalc
            ## alternatively, one could query standards for the formula
            #molfile = os.getcwd() + '/' + struct_file_name
            #args = [molfile];
            #cmd = 'formula';
            #res = RunCxcalc(cxcalc_bin,cmd,args)
            #res = res.split('\n')[1].split('\t')[1].split('\r')[0]
            #formula_O = res;
            # query ms_components
            mscomponents = [];
            mscomponents = self.get_Q1AndQ3MassAndMode_MSComponents(met);
            if len(mscomponents)==0:
                print(('no component found for ' + met + ' in ms_components'))
                continue;
            # calculate the formula, exact mass, and average mass for the ms_mode
            data_tmp = {};
            for msc in mscomponents:
                if msc['ms_mode'] == '-':
                    if met == 'nad' or met == 'nadp': # correct for nad and nadp
                        precursor = Formula(formula_O) - Formula('H2')
                    else:
                        precursor = Formula(formula_O) - Formula('H')
                    data_O.append({'met_id':met,
                                   'q1_mass':msc['q1_mass'],
                                   'q3_mass':msc['q3_mass'],
                                   'precursor_exactmass':precursor.isotope.mass,
                                   'precursor_formula':precursor.formula + '-'});
                elif msc['ms_mode'] == '+':
                    precursor = Formula(formula_O) + Formula('H')
                    data_O.append({'met_id':met,
                                   'q1_mass':msc['q1_mass'],
                                   'q3_mass':msc['q3_mass'],
                                   'precursor_exactmass':precursor.isotope.mass,
                                   'precursor_formula':precursor.formula + '+'});
                else:
                    print(('no ms_mode specified for ' + met))
                    exit(-1);
        # update ms_components table
        self.update_MSComponents_precursorFormulaAndMass(data_O);

        return
    def execute_checkPrecursorFormulaAndMass(self, met_ids_I):
        '''check that the formula, q1_mass and precursor_exactmass are consistent'''
        return
    #internal functions
    def make_13CEnsemble(self,formula_str_I):
        '''Make formula for m + 0 to m + # carbons'''
        # input:
        #       formula_str_I = string of formula
        # output:
        #       mass_ensemble_O = ensemble of distributions
        formula_str = re.sub('[+-]', '', formula_str_I) # remove '-' or '+' 

        formula = Formula(formula_str);
        mass_ensemble_O = {};
        if 'C' in formula._elements:
            nC = formula._elements['C'][0]; # count the number of carbon;
            for c in range(nC+1):
                tmp = Formula(formula_str);
                if c==0:tmp._elements['C'] = {0:nC-c};
                elif nC-c==0:tmp._elements['C'] = {13:c};
                else:tmp._elements['C'] = {0:nC-c, 13:c};
                mass_ensemble_O[c] = Formula(tmp.formula);
            return mass_ensemble_O;
        else: 
            nC = 0;
            mass_ensemble_O = {0:formula};
            return mass_ensemble_O
    #TODO:
    def execute_MSComponents_consistencyCheck(self):
        '''
        All method types:
        check that q1 mass matches precursor formula
        check that q3 mas matches product formula
        check that precursor_exactmass matches precursor formula
        check that product_exactmass matches product formula
        Quantification:
        check that the component_name matches the priority
        check that no components have the same q1_mass
        '''