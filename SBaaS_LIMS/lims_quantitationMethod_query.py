#from SBaaS_LIMS.lims_quantitationMethod_postgresql_models import *
#from .lims_msMethod_query import lims_msMethod_query
from SBaaS_LIMS.lims_calibratorsAndMixes_query import lims_calibratorsAndMixes_query
class lims_quantitationMethod_query(lims_calibratorsAndMixes_query,
                                    #lims_msMethod_query,
                                    ):
    def initialize_supportedTables(self):
        '''Set the supported tables dict for 
        '''
        tables_supported = {'quantitation_method':quantitation_method,
            'quantitation_method_list':quantitation_method_list,
                        };
        self.set_supportedTables(tables_supported);
        #table initializations:
    def drop_lims_quantitationMethod(self):
        try:
            quantitation_method.__table__.drop(self.engine,True);
            quantitation_method_list.__table__.drop(self.engine,True);

        except SQLAlchemyError as e:
            print(e);
    def reset_lims_quantitationMethod(self,quantitation_method_id_I=None):
        try:
            if quantitation_method_id_I:
                reset = self.session.query(quantitation_method).filter(quantitation_method.id.like(quantitation_method_id_I)).delete(synchronize_session=False);
                reset = self.session.query(quantitation_method_list).filter(
                    quantitation_method_list.quantitation_method_id.like(quantitation_method_id_I)).delete(synchronize_session=False);
            else:
                reset = self.session.query(quantitation_method).delete(synchronize_session=False);
                reset = self.session.query(quantitation_method_list).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def initialize_lims_quantitationMethod(self):
        try:
            quantitation_method.__table__.create(self.engine,True);
            quantitation_method_list.__table__.create(self.engine,True);

        except SQLAlchemyError as e:
            print(e);

    def add_quantitationMethod(self, QMethod_id_I, data_I):
        '''add rows of quantitation_method'''
        if data_I:
            for d in data_I:
                if not d['IS'] or d['IS'] == 'False': # ignore internal standards
                    try:
                        d['id']=QMethod_id_I;
                        d['q1_mass']=d['Q1 Mass - 1']
                        d['q3_mass']=d['Q3 Mass - 1']
                        d['met_id']=d['Group Name']
                        d['component_name']=d['Name']
                        d['is_name']=d['IS Name']
                        d['fit']=d['Regression Type']
                        d['weighting']=d['Regression Weighting']
                        d['intercept']=None
                        d['slope']=None
                        d['correlation']=None
                        d['use_area']=d['Use Area']
                        d['lloq']=None
                        d['uloq']=None
                        d['points']=None

                        data_add = quantitation_method(d
                            #QMethod_id_I,
                            #d['Q1 Mass - 1'],
                            #d['Q3 Mass - 1'],
                            #d['Group Name'],
                            #d['Name'],
                            #d['IS Name'],
                            #d['Regression Type'],
                            #d['Regression Weighting'],
                            #None,
                            #None,
                            #None,
                            #d['Use Area'],
                            #None,
                            #None,
                            #None
                                                    );
                        self.session.add(data_add);
                    except SQLAlchemyError as e:
                        print(e);
            self.session.commit();

    def get_quantMethodIds(self):
        '''Query quantitation method IDs that do not have regression parameters
        Note: correlation==Null is used to identify which quantitation method
              IDs do not have regression parameters'''
        quant_method_ids = self.session.query(quantitation_method.id).filter(
                    quantitation_method.correlation.is_(None)).group_by(
                    quantitation_method.id).all();
        quant_method_ids_O = [];
        for id in quant_method_ids: quant_method_ids_O.append(id.id);
        return quant_method_ids_O;

    def get_quantSamplesAndComponents(self, quant_method_id_I):
        '''Query calibrator samples and components that were used
        for calibration
        NOTE: can be used within a loop if multiple
        there are multiple quantitation ids'''
        # input:
        #       quantitation_method_id
        # ouput:
        #       calibrators_samples
        #       calibrators_components
        # query experiment and samples that were used to create the given calibration method
        calibrators_samples = self.session.query(data_stage01_quantification_MQResultsTable.sample_name).filter(
                             quantitation_method.id==experiment.quantitation_method_id,
                             experiment.sample_name==data_stage01_quantification_MQResultsTable.sample_name,
                             data_stage01_quantification_MQResultsTable.sample_type.like('Standard'),
                             data_stage01_quantification_MQResultsTable.used_,
                             quantitation_method.id.like(quant_method_id_I)).group_by(
                             data_stage01_quantification_MQResultsTable.sample_name).subquery('calibrators_samples');
        # query components from quantitation method that were used to create the given calibration method
        calibrators_components = self.session.query(data_stage01_quantification_MQResultsTable.component_name).filter(
                            data_stage01_quantification_MQResultsTable.used_.is_(True),
                            data_stage01_quantification_MQResultsTable.is_.isnot(True), 
                            data_stage01_quantification_MQResultsTable.sample_name.like(calibrators_samples.c.sample_name)).group_by(
                            data_stage01_quantification_MQResultsTable.component_name).all(); #subquery('calibrators_components');
        #calibrators_components = self.session.query(quantitation_method.component_name).filter(
        #                    quantitation_method.id.like(quant_method_id_I)).group_by(
        #                    quantitation_method.component_name).all(); #subquery('calibrators_components');
        component_names_O = [];
        for cn in calibrators_components: 
            component_names_O.append(cn.component_name);
        return calibrator_samples, component_names_O;
    def get_quantMethodParameters(self, quant_method_id_I, component_name_I):
        '''Query calibration parameters for a given component
        from a specified quantitation method id
        NOTE: intended to be used in a loop'''
        # input:
        #       component_name
        #       quantitation_method_id
        # ouput:
        #       fit
        #       weighting
        #       use_area
        calibrators_parameters = self.session.query(quantitation_method.component_name,
                            quantitation_method.fit,quantitation_method.weighting,
                            quantitation_method.use_area).filter(
                            quantitation_method.id.like(quant_method_id_I),
                            quantitation_method.component_name.like(component_name_I)).first();
        fit_O = calibrators_parameters.fit;
        weighting_O = calibrators_parameters.weighting;
        use_area_O = calibrators_parameters.use_area;

        return fit_O, weighting_O, use_area_O;
    def update_quantitationMethod(self, quant_method_id_I, component_name_I, 
                                  slope_I, intercept_I, correlation_I, lloq_I, uloq_I, points_I):
        try:
            quant_method_update = self.session.query(quantitation_method).filter(
                 quantitation_method.id.like(quant_method_id_I),
                 quantitation_method.component_name.like(component_name_I)).update(
                 {'slope': slope_I,'intercept':intercept_I,'correlation':correlation_I,
                  'lloq':lloq_I,'uloq':uloq_I,'points':points_I},synchronize_session=False);
            self.session.commit(); # could possible move if efficiency is poor
        except SQLAlchemyError as e:
            print(e);
    
    def get_components(self,quant_method_id_I):
        '''Query calibrator components that are in the calibration method
        NOTE: can be used within a loop if multiple
        there are multiple quantitation ids'''
        # input:
        #       quantitation_method_id
        # ouput:
        #       calibrators_components
        # query experiment and samples that were used to create the given calibration method
        try:
            calibrators_components = self.session.query(quantitation_method.component_name).filter(
                                quantitation_method.id.like(quant_method_id_I)).group_by(
                                quantitation_method.component_name).all();
            component_names_O = [];
            for cn in calibrators_components: component_names_O.append(cn.component_name);
            return component_names_O;

        except SQLAlchemyError as e:
            print(e);
    def get_allComponents(self):
        '''Query calibrator components that are in all of the calibration methods
        NOTE: can be used within a loop if multiple
        there are multiple quantitation ids'''
        # input:
        #       quantitation_method_id
        # ouput:
        #       calibrators_components
        # query experiment and samples that were used to create the given calibration method
        try:
            calibrators_components = self.session.query(quantitation_method.component_name).group_by(
                                quantitation_method.component_name).all();
            component_names_O = [];
            for cn in calibrators_components: component_names_O.append(cn.component_name);
            return component_names_O;

        except SQLAlchemyError as e:
            print(e);
    def get_allQuantMethodIds(self):
        '''Query quantitation method IDs that do not have regression parameters
        Note: correlation==Null is used to identify which quantitation method
              IDs do not have regression parameters'''
        try:
            quant_method_ids = self.session.query(quantitation_method.id).group_by(
                        quantitation_method.id).all();
            quant_method_ids_O = [];
            for id in quant_method_ids: quant_method_ids_O.append(id.id);
            return quant_method_ids_O;
        except SQLAlchemyError as e:
            print(e);
    def get_quantMethodRegression(self, quant_method_id_I, component_name_I):
        '''Query calibration parameters for a given component
        from a specified quantitation method id
        NOTE: intended to be used in a loop'''
        # input:
        #       component_name
        #       quantitation_method_id
        # ouput:
        #       intercept
        #       slope
        #       correlation
        #       lloq
        #       uloq
        #       points
        try:
            calibrators_parameters = self.session.query(quantitation_method.intercept,
                                quantitation_method.slope,
                                quantitation_method.correlation,
                                quantitation_method.lloq,
                                quantitation_method.uloq,
                                quantitation_method.points,
                                quantitation_method.slope).filter(
                                quantitation_method.id.like(quant_method_id_I),
                                quantitation_method.component_name.like(component_name_I)).first();
                                #first(): primary key(quant_method_id,component_name)
            if calibrators_parameters:
                intercept_O = calibrators_parameters.intercept;
                slope_O = calibrators_parameters.slope;
                correlation_O = calibrators_parameters.correlation;
                lloq_O = calibrators_parameters.lloq;
                uloq_O = calibrators_parameters.uloq;
                points_O = calibrators_parameters.points;
                if (slope_O and intercept_O and correlation_O and lloq_O and uloq_O and points_O):
                    return slope_O, intercept_O, correlation_O, lloq_O, uloq_O, points_O;
                else:
                    return 0,0,0,0,0,0;
            else:
                return 0,0,0,0,0,0;

        except SQLAlchemyError as e:
            print(e);
    def get_quantMethodInfo(self,calibrator_samples,user_area_I):
        '''Query calibrators by calibrator_samples
        INPUT:
        calibrator_samples = calibrator_table object'''
        try:
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
            actual_concentration_O = [];
            ratio_O = [];
            dilution_factor_O = [];
            if calibrators:
                for c in calibrators:
                    actual_concentration_O.append(c.actual_concentration);
                    if use_area_I: ratio_O.append(c.area_ratio);
                    else: ratio_O.append(c.height_ratio);
                    dilution_factor.append(c.dilution_factor);
            return actual_concentration_O,ratio_O,dilution_factor_O;
        except SQLAlchemyError as e:
            print(e);