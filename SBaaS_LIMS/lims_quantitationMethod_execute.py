
from .lims_quantitationMethod_io import lims_quantitationMethod_io
from .lims_quantitationMethod_dependencies import lims_quantitationMethod_dependencies
#resources
from calculate_utilities.r import robjects,importr

class lims_quantitationMethod_execute(lims_quantitationMethod_io,
                                      lims_quantitationMethod_dependencies
                                    ):
    def execute_exportCalibrationConcentrations(self, sampleAndComponent_fileName_I, concentrations_fileName_O):
        '''export calibrator concentrations for "cut&paste" into Actual Concentration column in MultiQuant
        when filtering Analytes only'''

        #Input:
        #   sampleAndComponent_fileName_I = .csv file specifying sample_name, sample_type, and component_group_name
        #Output:
        #   concentrations_fileName_O = .csv file specifying sample_name, sample_type, component_group_name, and actual_concentration
        
        concentrations_O = [];
        met_id_conv_dict = {'Hexose_Pool_fru_glc-D':'glc-D',
                            'Pool_2pg_3pg':'3pg'};
        #import sampleAndComponents
        samplesComponents = [];
        samplesComponents = self.import_calibration_sampleAndComponents(sampleAndComponent_fileName_I);
        for sc in samplesComponents:
            # if met_id is a pool of metabolites, convert to the metabolite
            # that is logged in calibrator tables and standards tables
            if sc['met_id'] in list(met_id_conv_dict.keys()):
                met_id_conv = met_id_conv_dict[sc['met_id']];
            else:
                met_id_conv = sc['met_id'];
            #query calibrator_id and calibrator_level from sample
            calibrator_id,calibrator_level = None,None;
            calibrator_id,calibrator_level = self.get_calibratorIDAndLevel_sampleNameAndSampleType_sample(sc['sample_name'],sc['sample_type']);
            #query calibrator_concentration from calibrator_concentrations
            calibrator_concentration, concentration_units = 'N/A', None;
            if calibrator_id and calibrator_level:
                calibrator_concentration, concentration_units = self.get_calibratorConcentrationAndUnit_metIDAndCalibratorIDAndLevel_calibratorConcentrations(met_id_conv,calibrator_id,calibrator_level);
            concentrations_O.append({'sample_name':sc['sample_name'], 'sample_type':sc['sample_type'],'component_group_name':sc['met_id'], 'actual_concentration':calibrator_concentration});
        self.export_calibrationConcentrations(concentrations_O, concentrations_fileName_O)

    def execute_quantitationMethodUpdate(self, quant_method_ids_I = []):
        '''calculate regression parameters for all components
        that have not been determined'''

        if quant_method_ids_I:
            quant_method_ids = quant_method_ids_I;
        else:
            quant_method_ids = [];
            quant_method_ids = self.get_quantMethodIds();
        for id in quant_method_ids:
            # get the samples and components that make were used to make
            # the quantitation method
            print(id);
            calibrator_samples = None;
            component_names = [];
            component_names = self.get_quantSamplesAndComponents(id);
            for n in component_names:
                print(n);
                # get the quant method parameters for each component
                fit,weighting,use_area = self.get_quantMethodParameters(id,n);
                # get the quant method info
                actual_concentration,ratio,dilution_factor=self.get_quantMethodInfo(calibrator_samples,use_are);
                # calculate the quant regression parameters for each component
                slope,intercept,correlation,lloq,uloq,points = self.calculate_regressionParameters(fit,weighting,actual_concentration,ratio,dilution_factor);
                #slope,intercept,correlation,lloq,uloq,points = self.calculate_regressionParameters_v1(calibrator_samples,n,fit,weighting,use_area);
                # update the quantitation_method table
                self.update_quantitationMethod(id,n,slope,intercept,correlation,lloq,uloq,points);
    def calculate_regressionParameters_v1(self, calibrator_samples, component_name_I, fit_I, weighting_I, use_area_I):
        '''calculate regression parameters for a given component
        from a specified quantitation method id
        NOTE: intended to be used in a loop
        input:
            component_name
            calibrators_samples (class member) 
            fit
            weighting
            use_area
        ouput:
            slope
            intercept
            correlation
            lloq
            uloq
            points'''

        # query calibrators for specific component_name from specific experiment_id
        if use_area_I:
            calibrators = self.session.query(data_stage01_quantification_MQResultsTable.actual_concentration,
                                        data_stage01_quantification_MQResultsTable.area_ratio,
                                        data_stage01_quantification_MQResultsTable.dilution_factor).filter(
                                     data_stage01_quantification_MQResultsTable.sample_name.like(calibrator_samples.c.sample_name),
                                     data_stage01_quantification_MQResultsTable.used_.is_(True),
                                     data_stage01_quantification_MQResultsTable.is_.isnot(True),
                                     data_stage01_quantification_MQResultsTable.component_name.like(component_name_I)).all();
        else:
            calibrators = self.session.query(data_stage01_quantification_MQResultsTable.actual_concentration,
                                        data_stage01_quantification_MQResultsTable.height_ratio,
                                        data_stage01_quantification_MQResultsTable.dilution_factor).filter(
                                     data_stage01_quantification_MQResultsTable.sample_name.like(calibrator_samples.c.sample_name),
                                     data_stage01_quantification_MQResultsTable.used_.is_(True),
                                     data_stage01_quantification_MQResultsTable.is_.isnot(True),
                                     data_stage01_quantification_MQResultsTable.component_name.like(component_name_I)).all();
        # variable to check quantitation
        calc_regress = True;

        # extraction concentrations
        concentration = [];
        for c in calibrators: 
            if c.actual_concentration: concentration.append(c.actual_concentration);
            else: calc_regress = False;
        if len(concentration)==0:
            calc_regress = False;
        # extraction ratio
        ratio = [];
        if use_area_I:
            for c in calibrators: 
                if c.area_ratio: ratio.append(c.area_ratio);
                else: ratio.append(0.0);
        else:
            for c in calibrators:
                if c.height_ratio: ratio.append(c.height_ratio);
                else: ratio.append(0.0);
        if len(ratio)==0:
            calc_regress = False;
        # extraction diluton factor
        dilution_factor = [];
        for c in calibrators:
            if c.dilution_factor: dilution_factor.append(c.dilution_factor);
            else: dilution_factor.append(1.0);
        # correct the concentration for the dilution factor
        for n in range(len(concentration)):
            concentration[n] = concentration[n]/dilution_factor[n];

        if (not(calc_regress)):
            return 0,0,0,0,0,0;

        # lloq, uloq, points
        lloq_O = min(concentration);
        uloq_O = max(concentration);
        points_O = len(concentration);

        # Call to R
        try:
            stats = importr('stats');

            # generate weights:
            '''From MultiQuant Manual:
            Weighting type	Weight (w)
            None Always	1.0.
            1 / x	If |x| < 10-5 then w = 10e5; otherwise w = 1 / |x|.
            1 / x2	If |x| < 10-5 then w = 10e10; otherwise w = 1 / x2.
            1 / y	If |y| < 10-8 then w = 10e8; otherwise w = 1 / |y|.
            1 / y2	If |y| < 10-8 then w = 10e16; otherwise w = 1 / y2.
            ln x	If x < 0 an error is generated; otherwise if x < 10-5 then w = ln 105,
		            otherwise w = |ln x|.'''
            wts = []; 
            if weighting_I == 'ln (x)':
                for c in concentration:
                    if c<10e-5:
                        wts.append(log(10e5));
                    else:
                        wts.append(abs(log(c)));
            elif weighting_I == 'None':
                for c in concentration:
                    wts.append(1.0);
            elif weighting_I == '1 / x':
                for c in concentration:
                    if c<10e-5:
                        wts.append(1/10e5);
                    else:
                        wts.append(1/abs(c));
            elif weighting_I == '1 / y':
                for c in ratio:
                    if c<10e-8:
                        wts.append(1/10e8);
                    else:
                        wts.append(1/abs(c));

            else:
                print(("weighting " + weighting_I + " not yet supported"));
                print("linear weighting used instead");
                for c in concentration:
                    wts.append(1.0);
            
            # convert lists to R objects
            x = robjects.FloatVector(concentration);
            y = robjects.FloatVector(ratio);
            w = robjects.FloatVector(wts);
            if fit_I == 'Linear':
                fmla = robjects.Formula('y ~ x'); # generate the R formula for lm
            elif fit_I == 'Linear Through Zero':
                fmla = robjects.Formula('y ~ -1 + x'); # generate the R formula for lm
            elif fit_I == 'Quadratic':
                fmla = robjects.Formula('y ~ x + I(x^2)'); # generate the R formula for lm
            elif fit_I == 'Power':
                fmla = robjects.Formula('log(y) ~ log(x)'); # generate the R formula for lm
            else:
                print(("fit " + fit_I + " not yet supported"));
                print("linear model used instead");
                fmla = robjects.Formula('y ~ x');

            env = fmla.environment; # set the local environmental variables for lm
            env['x'] = x;
            env['y'] = y;
            #fit = r('lm(%s)' %fmla.r_repr()); # direct call to R
            fit = stats.lm(fmla, weights = w); # return the lm fitted model from R
            sum = stats.summary_lm(fit) # return the summary of the fit
            intercept_O = sum.rx2('coefficients')[0]; #intercept
            slope_O = sum.rx2('coefficients')[1]; #slope
            correlation_O = sum.rx2('r.squared')[0]; #r-squared

            return slope_O, intercept_O, correlation_O, lloq_O, uloq_O, points_O;
        except:
            print('error in R')

    def execute_quantitationMethodComparison(self):
        '''Query and write calibration regression parameters to file'''

        # get the components that are in all of the calibration methods
        component_names = [];
        component_names = self.get_allComponents();
        # get all the quantitation method IDs
        quant_method_ids = [];
        quant_method_ids = self.get_allQuantMethodIds();
        with open('quantitationMethodComparison.csv', 'wb') as csvfile:
            # write header to file
            csv_writer = csv.writer(csvfile)
            header = [];
            columns = [];
            column_names = ['slope','intercept','correlation','lloq','uloq','points'];
            for c in column_names:
                for i in quant_method_ids:
                    header.append(i);
                    columns.append(c);
            header.insert(0,'');
            columns.insert(0,'Component_Name');
            csv_writer.writerow(header);
            csv_writer.writerow(columns);
            # loop through each component
            for n in component_names:
                slopes = [];
                intercepts = [];
                correlations = [];
                lloqs = [];
                uloqs = [];
                points = [];
                for id in quant_method_ids:
                    # query regression parameters
                    slope = 0;
                    intercept = 0;
                    correlation = 0;
                    lloq = 0;
                    uloq = 0;
                    point = 0;
                    slope,intercept,correlation,lloq,uloq,point = self.get_quantMethodRegression(id,n);
                    slopes.append(slope);
                    intercepts.append(intercept);
                    correlations.append(correlation);
                    lloqs.append(lloq);
                    uloqs.append(uloq);
                    points.append(point);

                # write row to file
                row = [n];
                row.extend(slopes);
                row.extend(intercepts);
                row.extend(correlations);
                row.extend(lloqs);
                row.extend(uloqs);
                row.extend(points);
                csv_writer.writerow(row);