from .lims_acquisitionMethod_postgresql_models import *
from .lims_lcMethod_postgresql_models import *
from .lims_autosamplerMethod_postgresql_models import *
from .lims_msMethod_postgresql_models import *

from SBaaS_base.sbaas_base_query_update import sbaas_base_query_update
from SBaaS_base.sbaas_base_query_drop import sbaas_base_query_drop
from SBaaS_base.sbaas_base_query_initialize import sbaas_base_query_initialize
from SBaaS_base.sbaas_base_query_insert import sbaas_base_query_insert
from SBaaS_base.sbaas_base_query_select import sbaas_base_query_select
from SBaaS_base.sbaas_base_query_delete import sbaas_base_query_delete

from SBaaS_base.sbaas_template_query import sbaas_template_query

class lims_acquisitionMethod_query(sbaas_template_query):

    def initialize_supportedTables(self):
        '''Set the supported tables dict for 
        '''
        tables_supported = {
            'acquisition_method':acquisition_method
                        };
        self.set_supportedTables(tables_supported);
        #table initializations:
    def drop_lims_acqusitionMethod(self):
        try:
            acquisition_method.__table__.drop(self.engine,True);
        except SQLAlchemyError as e:
            print(e);
    def reset_lims_acqusitionMethod(self):
        try:
            reset = self.session.query(acquisition_method).delete(synchronize_session=False);

            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def initialize_lims_acqusitionMethod(self):
        try:
            acquisition_method.__table__.create(self.engine,True);

        except SQLAlchemyError as e:
            print(e);
    def add_AcquisitionMethod(self, data_I):
        '''add rows of acquisition_method'''
        if data_I:
            for d in data_I:
                try:
                    data_add = acquisition_method(d['id'],
                                         d['ms_method_id'],
                                         d['autosampler_method_id'],
                                         d['lc_method_id']);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def get_acqusitionMethod(self,lc_method_I,ms_mode_I,ms_methodtype_I):
        '''Querry acqusition method (i.e., join tables lc_elution and ms_components)'''
        try:
            mscomponents = self.session.query(MS_components.component_name, 
                    MS_components.met_id, 
                    MS_components.met_name, 
                    MS_components.q1_mass, 
                    MS_components.q3_mass, 
                    MS_components.dp, 
                    MS_components.ep, 
                    MS_components.ce, 
                    MS_components.cxp, 
                    MS_components.precursor_formula, 
                    MS_components.product_formula, 
                    MS_components.quantifier, 
                    MS_components.ms_group, 
                    MS_components.threshold, 
                    MS_components.dwell_weight, 
                    lc_elution.rt, 
                    lc_elution.ms_window, 
                    lc_elution.rt_units, 
                    lc_elution.window_units).filter(
                    lc_elution.lc_method_id.like(lc_method_I),
                    MS_components.ms_mode.like(ms_mode_I),
                    MS_components.ms_methodtype.like(ms_methodtype_I),
                    MS_components.met_id.like(lc_elution.met_id),
                    MS_components.ms_include).group_by( # query only components that are included in the method
                    MS_components.component_name, 
                    MS_components.met_id, 
                    MS_components.met_name, 
                    MS_components.q1_mass, 
                    MS_components.q3_mass, 
                    MS_components.dp, 
                    MS_components.ep, 
                    MS_components.ce, 
                    MS_components.cxp, 
                    MS_components.precursor_formula, 
                    MS_components.product_formula, 
                    MS_components.quantifier, 
                    MS_components.ms_group, 
                    MS_components.threshold, 
                    MS_components.dwell_weight, 
                    lc_elution.rt, 
                    lc_elution.ms_window, 
                    lc_elution.rt_units, 
                    lc_elution.window_units).order_by(
                    lc_elution.rt.asc(),
                    MS_components.component_name.asc()).all();
            mscomponents_O = [];
            if not mscomponents:
                print('bad query for row in ms_components: ')
                print('lc_method_I: ' + lc_method_I + ', ms_mode_I: ' + ms_mode_I + ', ms_methodtype_I: ' + ms_methodtype_I);
                exit(-1)
            for msc in mscomponents: 
                mscomponents_1 = {};
                mscomponents_1["q1_mass"] = msc.q1_mass;
                mscomponents_1["q3_mass"] = msc.q3_mass;
                mscomponents_1["met_name"] = msc.met_name;
                mscomponents_1["dp"] = msc.dp;
                mscomponents_1["ep"] = msc.ep;
                mscomponents_1["ce"] = msc.ce;
                mscomponents_1["cxp"] = msc.cxp;
                mscomponents_1["quantifier"] = msc.quantifier;
                mscomponents_1["met_id"] = msc.met_id;
                mscomponents_1["ms_group"] = msc.ms_group;
                mscomponents_1["threshold"] = msc.threshold;
                mscomponents_1["dwell_weight"] = msc.dwell_weight;
                mscomponents_1["component_name"] = msc.component_name;
                mscomponents_1["rt"] = msc.rt;
                mscomponents_1["ms_window"] = msc.ms_window;
                mscomponents_1["rt_units"] = msc.rt_units;
                mscomponents_1["window_units"] = msc.window_units;
                mscomponents_O.append(mscomponents_1);
            return mscomponents_O;
        except SQLAlchemyError as e:
            print(e);