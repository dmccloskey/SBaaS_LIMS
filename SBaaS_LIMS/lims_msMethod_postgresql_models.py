from SBaaS_base.postgresql_orm_base import *
from SBaaS_base.postgresql_dataType_converter import postgresql_dataType_converter

#MS_components
class MS_components(Base):
    #__table__ = make_table('ms_components')
    __tablename__ = 'ms_components'
    id = Column(Integer, Sequence('ms_components_id_seq'))
    q1_mass = Column(Float, nullable = False);
    q3_mass = Column(Float, nullable = False);
    ms3_mass = Column(Float);
    met_name = Column(Text);
    dp = Column(Float);
    ep = Column(Float);
    ce = Column(Float);
    cxp = Column(Float);
    af = Column(Float);
    quantifier = Column(Integer);
    ms_mode = Column(String(1));
    ion_intensity_rank = Column(Integer);
    ion_abundance = Column(Float);
    precursor_formula = Column(Text);
    product_ion_reference = Column(Text);
    product_formula = Column(Text);
    production_ion_notes = Column(Text);
    met_id = Column(String(50), nullable = False);
    external_reference = Column(Text);
    q1_mass_units = Column(String(20));
    q3_mass_units = Column(String(20));
    ms3_mass_units = Column(String(20));
    threshold_units = Column(String(20));
    dp_units = Column(String(20));
    ep_units = Column(String(20));
    ce_units = Column(String(20));
    cxp_units = Column(String(20));
    af_units = Column(String(20));
    ms_group = Column(String(100));
    threshold = Column(Float, default = 5000)
    dwell_weight = Column(Float, default = 1)
    component_name = Column(String(500));
    ms_include = Column(Boolean, default = False);
    ms_is = Column(Boolean, default = False);
    precursor_fragment = Column(postgresql.ARRAY(Boolean))
    product_fragment = Column(postgresql.ARRAY(Boolean))
    precursor_exactmass = Column(Float);
    product_exactmass = Column(Float);
    ms_methodtype = Column(String(20), default = 'tuning')
    precursor_fragment_elements = Column(postgresql.ARRAY(String(3)))
    product_fragment_elements = Column(postgresql.ARRAY(String(3)))

    __table_args__ = (UniqueConstraint('component_name','ms_include'),
                      PrimaryKeyConstraint('met_id','q1_mass','q3_mass','ms_methodtype'),
            )
    def __init__(self,data_dict_I):
        self.ion_abundance=data_dict_I['ion_abundance'];
        self.q1_mass=data_dict_I['q1_mass'];
        self.q3_mass=data_dict_I['q3_mass'];
        self.ms3_mass=data_dict_I['ms3_mass'];
        self.met_name=data_dict_I['met_name'];
        self.dp=data_dict_I['dp'];
        self.ep=data_dict_I['ep'];
        self.ce=data_dict_I['ce'];
        self.cxp=data_dict_I['cxp'];
        self.af=data_dict_I['af'];
        self.quantifier=data_dict_I['quantifier'];
        self.q1_mass_units=data_dict_I['q1_mass_units'];
        self.product_formula=data_dict_I['product_formula'];
        self.q3_mass_units=data_dict_I['q3_mass_units'];
        self.ms3_mass_units=data_dict_I['ms3_mass_units'];
        self.production_ion_notes=data_dict_I['production_ion_notes'];
        self.met_id=data_dict_I['met_id'];
        self.threshold_units=data_dict_I['threshold_units'];
        self.dp_units=data_dict_I['dp_units'];
        self.ep_units=data_dict_I['ep_units'];
        self.ce_units=data_dict_I['ce_units'];
        self.cxp_units=data_dict_I['cxp_units'];
        self.af_units=data_dict_I['af_units'];
        self.ms_group=data_dict_I['ms_group'];
        self.component_name=data_dict_I['component_name'];
        self.precursor_fragment=pgdatatypeconverter.convert_text2List(data_dict_I['precursor_fragment']);
        self.product_fragment=pgdatatypeconverter.convert_text2List(data_dict_I['product_fragment']);
        self.precursor_exactmass=data_dict_I['precursor_exactmass'];
        self.product_exactmass=data_dict_I['product_exactmass'];
        self.threshold=data_dict_I['threshold'];
        self.dwell_weight=data_dict_I['dwell_weight'];
        self.ms_include=pgdatatypeconverter.convert_text2PostgresqlDataType(data_dict_I['ms_include']);
        self.ms_is=pgdatatypeconverter.convert_text2PostgresqlDataType(data_dict_I['ms_is']);
        self.ms_methodtype=data_dict_I['ms_methodtype'];
        self.id=data_dict_I['id'];
        self.precursor_fragment_elements=pgdatatypeconverter.convert_text2List(data_dict_I['precursor_fragment_elements']);
        self.product_fragment_elements=pgdatatypeconverter.convert_text2List(data_dict_I['product_fragment_elements']);
        self.external_reference=data_dict_I['external_reference'];
        self.ms_mode=data_dict_I['ms_mode'];
        self.product_ion_reference=data_dict_I['product_ion_reference'];
        self.precursor_formula=data_dict_I['precursor_formula'];
        self.ion_intensity_rank=data_dict_I['ion_intensity_rank'];

    def __set__row__(self,q1_mass_I,q3_mass_I,ms3_mass_I,
                 met_name_I,dp_I,ep_I,ce_I,cxp_I,af_I,
                 quantifier_I,ms_mode_I,ion_intensity_rank_I,
                 ion_abundance_I,precursor_formula_I,
                 product_ion_reference_I,product_formula_I,
                 production_ion_notes_I,met_id_I,external_reference_I,
                 q1_mass_units_I,q3_mass_units_I,ms3_mass_units_I,
                 threshold_units_I,dp_units_I,ep_units_I,ce_units_I,
                 cxp_units_I,af_units_I,ms_group_I,threshold_I,
                 dwell_weight_I,component_name_I,ms_include_I,
                 ms_is_I,precursor_fragment_I,product_fragment_I,
                 precursor_exactmass_I,product_exactmass_I,
                 ms_methodtype_I,
                 precursor_fragment_elements_I,
                 product_fragment_elements_I):
        self.q1_mass=q1_mass_I
        self.q3_mass=q3_mass_I
        self.ms3_mass=ms3_mass_I
        self.met_name=met_name_I
        self.dp=dp_I
        self.ep=ep_I
        self.ce=ce_I
        self.cxp=cxp_I
        self.af=af_I
        self.quantifier=quantifier_I
        self.ms_mode=ms_mode_I
        self.ion_intensity_rank=ion_intensity_rank_I
        self.ion_abundance=ion_abundance_I
        self.precursor_formula=precursor_formula_I
        self.product_ion_reference=product_ion_reference_I
        self.product_formula=product_formula_I
        self.production_ion_notes=production_ion_notes_I
        self.met_id=met_id_I
        self.external_reference=external_reference_I
        self.q1_mass_units=q1_mass_units_I
        self.q3_mass_units=q3_mass_units_I
        self.ms3_mass_units=ms3_mass_units_I
        self.threshold_units=threshold_units_I
        self.dp_units=dp_units_I
        self.ep_units=ep_units_I
        self.ce_units=ce_units_I
        self.cxp_units=cxp_units_I
        self.af_units=af_units_I
        self.ms_group=ms_group_I
        self.threshold=threshold_I
        self.dwell_weight=dwell_weight_I
        self.component_name=component_name_I
        self.ms_include=ms_include_I
        self.ms_is=ms_is_I
        self.precursor_fragment=precursor_fragment_I
        self.product_fragment=product_fragment_I
        self.precursor_exactmass = precursor_exactmass_I
        self.product_exactmass = product_exactmass_I
        self.ms_methodtype = ms_methodtype_I
        self.precursor_fragment_elements = precursor_fragment_elements_I
        self.product_fragment_elements = product_fragment_elements_I

#MS_sourceParameters
class MS_sourceParameters(Base):
    #__table__ = make_table('ms_sourceParameters')
    __tablename__ = 'ms_sourceparameters'
    id = Column(String(50), nullable = False);
    ms_cur = Column(Float, nullable = False);
    ms_cad = Column(String(10), nullable = False)
    ms_is = Column(Float, nullable = False);
    ms_tem = Column(Float, nullable = False);
    ms_gs1 = Column(Float, nullable = False);
    ms_gs2 = Column(Float, nullable = False)
    __table_args__ = (PrimaryKeyConstraint('id'),
            )

    def __init__(self,data_dict_I):
        self.ms_gs1=data_dict_I['ms_gs1'];
        self.ms_gs2=data_dict_I['ms_gs2'];
        self.ms_cur=data_dict_I['ms_cur'];
        self.ms_cad=data_dict_I['ms_cad'];
        self.ms_is=data_dict_I['ms_is'];
        self.ms_tem=data_dict_I['ms_tem'];
        self.id=data_dict_I['id'];

#MS_information
class MS_information(Base):
    #__table__ = make_table('ms_information')
    __tablename__ = 'ms_information'
    manufacturer = Column(String(100), nullable = False);
    id = Column(String(100), nullable = False);
    serial_number = Column(String(100), nullable = False)
    __table_args__ = (PrimaryKeyConstraint('id'),
            )

    def __init__(self,data_dict_I):
        self.serial_number=data_dict_I['serial_number'];
        self.id=data_dict_I['id'];
        self.manufacturer=data_dict_I['manufacturer'];

#MS_method
class MS_method(Base):
    #__table__ = make_table('ms_method')
    __tablename__ = 'ms_method'
    id = Column(String(50), nullable = False);
    ms_sourceparameters_id = Column(String(50), nullable = False);
    ms_information_id = Column(String(50), nullable = False);
    ms_experiment_id = Column(String(50))
    __table_args__ = (PrimaryKeyConstraint('id'),
            #ForeignKeyConstraint(['ms_information_id'],['ms_information.id'], onupdate="CASCADE", ondelete="CASCADE"),
            #ForeignKeyConstraint(['ms_sourceparameters_id'],['ms_sourceparameters.id'], onupdate="CASCADE", ondelete="CASCADE"),
            )

    def __init__(self,data_dict_I):
        self.ms_experiment_id=data_dict_I['ms_experiment_id'];
        self.ms_information_id=data_dict_I['ms_information_id'];
        self.ms_sourceparameters_id=data_dict_I['ms_sourceparameters_id'];
        self.id=data_dict_I['id'];

    def __set__row__(self,id_I, ms_sourceparameters_id_I,ms_information_id_I,ms_experiment_id_I):
        self.id = id_I;
        self.ms_sourceparameters_id = ms_sourceparameters_id_I;
        self.ms_information_id = ms_information_id_I;
        self.ms_experiment_id = ms_experiment_id_I;
#MS_component_list
class MS_component_list(Base):
    #__table__ = make_table('ms_component_list')
    __tablename__ = 'ms_component_list'
    ms_method_id = Column(String(50), nullable = False);
    q1_mass = Column(Float);
    q3_mass = Column(Float);
    met_id = Column(String(50));
    component_name = Column(String(500), nullable = False);
    ms_methodtype = Column(String(20), default = 'quantification')
    __table_args__ = (PrimaryKeyConstraint('ms_method_id','component_name'),
            #ForeignKeyConstraint(['ms_method_id'],['ms_method.id'], onupdate="CASCADE"),
            )
    
    def __init__(self,data_dict_I):
        self.ms_method_id=data_dict_I['ms_method_id'];
        self.q1_mass=data_dict_I['q1_mass'];
        self.q3_mass=data_dict_I['q3_mass'];
        self.met_id=data_dict_I['met_id'];
        self.component_name=data_dict_I['component_name'];
        self.ms_methodtype=data_dict_I['ms_methodtype'];

    def __set__row__(self,ms_method_id_I,q1_mass_I,q3_mass_I,
                 met_id_I,component_name_I,ms_methodtype_I):
        self.ms_method_id=ms_method_id_I
        self.q1_mass=q1_mass_I
        self.q3_mass=q3_mass_I
        self.met_id=met_id_I
        self.component_name=component_name_I
        self.ms_methodtype=ms_methodtype_I