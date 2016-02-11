from SBaaS_base.postgresql_orm_base import *
from time import mktime,strftime

#sample
class sample(Base):
    #__table__ = make_table('sample')
    __tablename__ = 'sample'
    #id = Column(Integer, Sequence('sample_id_seq'))
    sample_name = Column(String(500), nullable = False);
    sample_type = Column(String(100), nullable = False);
    calibrator_id = Column(Integer);
    calibrator_level = Column(Integer);
    sample_id = Column(String(500));
    sample_dilution = Column(Float, default = 1.0)
    
    __table_args__ = (PrimaryKeyConstraint('sample_name'),
            #ForeignKeyConstraint(['sample_id'],['sample_storage.sample_id']),
            #ForeignKeyConstraint(['sample_id'],['sample_physiologicalparameters.sample_id']),
            #ForeignKeyConstraint(['sample_id'],['sample_description.sample_id']),
            #UniqueConstraint('id'),
            )

    def __init__(self,data_dict_I):
        self.sample_dilution=data_dict_I['sample_dilution'];
        self.sample_name=data_dict_I['sample_name'];
        self.calibrator_level=data_dict_I['calibrator_level'];
        self.calibrator_id=data_dict_I['calibrator_id'];
        self.sample_type=data_dict_I['sample_type'];
        self.sample_id=data_dict_I['sample_id'];

    def __set__row__(self,sample_name_I,sample_type_I,calibrator_id_I,calibrator_level_I,sample_id_I,sample_dilution_I):
        self.sample_name=sample_name_I;
        self.sample_type=sample_type_I;
        self.calibrator_id=calibrator_id_I;
        self.calibrator_level=calibrator_level_I;
        self.sample_id=sample_id_I;
        self.sample_dilution=sample_dilution_I;

    def __repr__dict__(self):
        return {
        'sample_dilution':self.sample_dilution,
        'sample_name':self.sample_name,
        'calibrator_level':self.calibrator_level,
        'calibrator_id':self.calibrator_id,
        'sample_type':self.sample_type,
        'sample_id':self.sample_id,
        };
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
#sample_storage
class sample_storage(Base):
    #__table__ = make_table('sample_storage')
    __tablename__ = 'sample_storage'
    sample_id=Column(String(500),nullable=False, primary_key=True)
    sample_label=Column(String(50), nullable = False)
    #sample_dateAndTime=Column(DateTime)
    ph=Column(Float)
    box=Column(Integer)
    pos=Column(Integer)

    def __init__(self,data_dict_I):
        self.sample_label=data_dict_I['sample_label'];
        self.ph=data_dict_I['ph'];
        self.box=data_dict_I['box'];
        self.pos=data_dict_I['pos'];
        self.sample_id=data_dict_I['sample_id'];

    def __set__row__(self,sample_id_I,
                 #sample_dateAndTime_I,
                 sample_label_I,ph_I,box_I,pos_I):
        self.sample_id = sample_id_I
        self.sample_label = sample_label_I
        #self.sample_dateAndTime = sample_dateAndTime_I
        self.ph = ph_I
        self.box = box_I
        self.pos = pos_I
    

    def __repr__dict__(self):
        return {'sample_id':self.sample_id,
                'sample_label':self.sample_label,
        'ph':self.ph,
        'box':self.box,
        'pos':self.pos}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

#sample_physiologicalParameters
class sample_physiologicalParameters(Base):
    #__table__ = make_table('sample_physiologicalparameters')
    __tablename__ = 'sample_physiologicalparameters'
    sample_id=Column(String(500),nullable=False, primary_key=True)
    growth_condition_short=Column(Text)
    growth_condition_long=Column(Text)
    media_short=Column(Text)
    media_long=Column(Text)
    isoxic=Column(Boolean)
    temperature=Column(Float)
    supplementation=Column(String(100))
    od600=Column(Float)
    vcd=Column(Float)
    culture_density=Column(Float)
    culture_volume_sampled=Column(Float)
    cells=Column(Float)
    dcw=Column(Float)
    wcw=Column(Float)
    vcd_units=Column(String(10))
    culture_density_units=Column(String(10))
    culture_volume_sampled_units=Column(String(10))
    dcw_units=Column(String(10))
    wcw_units=Column(String(10))

    def __init__(self,data_dict_I):
        self.culture_density=data_dict_I['culture_density'];
        self.wcw_units=data_dict_I['wcw_units'];
        self.dcw_units=data_dict_I['dcw_units'];
        self.culture_volume_sampled_units=data_dict_I['culture_volume_sampled_units'];
        self.culture_density_units=data_dict_I['culture_density_units'];
        self.vcd_units=data_dict_I['vcd_units'];
        self.wcw=data_dict_I['wcw'];
        self.dcw=data_dict_I['dcw'];
        self.cells=data_dict_I['cells'];
        self.culture_volume_sampled=data_dict_I['culture_volume_sampled'];
        self.vcd=data_dict_I['vcd'];
        self.od600=data_dict_I['od600'];
        self.supplementation=data_dict_I['supplementation'];
        self.temperature=data_dict_I['temperature'];
        self.isoxic=data_dict_I['isoxic'];
        self.media_long=data_dict_I['media_long'];
        self.media_short=data_dict_I['media_short'];
        self.growth_condition_long=data_dict_I['growth_condition_long'];
        self.growth_condition_short=data_dict_I['growth_condition_short'];
        self.sample_id=data_dict_I['sample_id'];

    def __set__row__(self,sample_id_I,growth_condition_short_I,growth_condition_long_I,
                media_short_I,media_long_I,isoxic_I,temperature_I,supplementation_I,od600_I,
                vcd_I,culture_density_I,culture_volume_sampled_I,cells_I,dcw_I,wcw_I,vcd_units_I,
                culture_density_units_I,culture_volume_sampled_units_I,dcw_units_I,wcw_units_I):
        self.sample_id = sample_id_I
        self.growth_condition_short = growth_condition_short_I
        self.growth_condition_long = growth_condition_long_I
        self.media_short = media_short_I
        self.media_long = media_long_I
        self.isoxic = isoxic_I
        self.temperature = temperature_I
        self.supplementation = supplementation_I
        self.od600 = od600_I
        self.vcd = vcd_I
        self.culture_density = culture_density_I
        self.culture_volume_sampled = culture_volume_sampled_I
        self.cells = cells_I
        self.dcw = dcw_I
        self.wcw = wcw_I
        self.vcd_units = vcd_units_I
        self.culture_density_units = culture_density_units_I
        self.culture_volume_sampled_units = culture_volume_sampled_units_I
        self.dcw_units = dcw_units_I
        self.wcw_units = wcw_units_I

    def __repr__dict__(self):
        return {
        'culture_density':self.culture_density,
        'wcw_units':self.wcw_units,
        'dcw_units':self.dcw_units,
        'culture_volume_sampled_units':self.culture_volume_sampled_units,
        'culture_density_units':self.culture_density_units,
        'vcd_units':self.vcd_units,
        'wcw':self.wcw,
        'dcw':self.dcw,
        'cells':self.cells,
        'culture_volume_sampled':self.culture_volume_sampled,
        'vcd':self.vcd,
        'od600':self.od600,
        'supplementation':self.supplementation,
        'temperature':self.temperature,
        'isoxic':self.isoxic,
        'media_long':self.media_long,
        'media_short':self.media_short,
        'growth_condition_long':self.growth_condition_long,
        'growth_condition_short':self.growth_condition_short,
        'sample_id':self.sample_id,
        };
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
#sample_description
class sample_description(Base):
    #__table__ = make_table('sample_description')
    __tablename__ ='sample_description'
    sample_id=Column(String(500),nullable=False, primary_key=True);
    sample_name_short=Column(String(100));
    sample_name_abbreviation=Column(String(50));
    sample_date=Column(DateTime,nullable=False);
    time_point=Column(String(50),nullable=False);
    sample_condition=Column(String(100),nullable=False);
    extraction_method_id=Column(String(500));
    biological_material=Column(String(100),nullable=False);
    #sample_description=Column(String(100),nullable=False);
    sample_desc=Column(String(100),nullable=False);
    sample_replicate=Column(Integer);
    is_added=Column(Float);
    is_added_units=Column(String(10));
    reconstitution_volume=Column(Float);
    reconstitution_volume_units=Column(String(10));
    istechnical=Column(Boolean);
    sample_replicate_biological=Column(Integer);
    notes=Column(Text);

    def __init__(self,data_dict_I):
        self.time_point=data_dict_I['time_point'];
        self.sample_date=data_dict_I['sample_date'];
        self.sample_name_abbreviation=data_dict_I['sample_name_abbreviation'];
        self.sample_name_short=data_dict_I['sample_name_short'];
        self.sample_id=data_dict_I['sample_id'];
        self.notes=data_dict_I['notes'];
        self.sample_replicate_biological=data_dict_I['sample_replicate_biological'];
        self.istechnical=data_dict_I['istechnical'];
        self.reconstitution_volume_units=data_dict_I['reconstitution_volume_units'];
        self.is_added_units=data_dict_I['is_added_units'];
        self.reconstitution_volume=data_dict_I['reconstitution_volume'];
        self.is_added=data_dict_I['is_added'];
        self.sample_replicate=data_dict_I['sample_replicate'];
        self.sample_desc=data_dict_I['sample_desc'];
        self.biological_material=data_dict_I['biological_material'];
        self.extraction_method_id=data_dict_I['extraction_method_id'];
        self.sample_condition=data_dict_I['sample_condition'];

    def __set__row__(self,sample_id_I,sample_name_short_I,sample_name_abbreviation_I,
                 sample_date_I,time_point_I,sample_condition_I,extraction_method_id_I,
                 biological_material_I,sample_description_I,sample_replicate_I,
                 is_added_I,is_added_units_I,reconstitution_volume_I,reconstitution_volume_units_I,
                 sample_replicate_biological_I,istechnical_I,notes_I):
        self.sample_id=sample_id_I
        self.sample_name_short=sample_name_short_I
        self.sample_name_abbreviation=sample_name_abbreviation_I
        self.sample_date=sample_date_I
        self.time_point=time_point_I
        self.sample_condition=sample_condition_I
        self.extraction_method_id=extraction_method_id_I
        self.biological_material=biological_material_I
        self.sample_desc=sample_description_I
        self.sample_replicate=sample_replicate_I
        self.is_added=is_added_I
        self.is_added_units=is_added_units_I
        self.reconstitution_volume=reconstitution_volume_I
        self.reconstitution_volume_units=reconstitution_volume_units_I
        self.sample_replicate_biological=sample_replicate_biological_I
        self.istechnical=istechnical_I
        self.notes=notes_I

    def __repr__dict__(self):
        return {
        'time_point':self.time_point,
        'sample_date':self.sample_date.strftime('%Y-%m-%d %H:%M:%S'),
        'sample_name_abbreviation':self.sample_name_abbreviation,
        'sample_name_short':self.sample_name_short,
        'sample_id':self.sample_id,
        'notes':self.notes,
        'sample_replicate_biological':self.sample_replicate_biological,
        'istechnical':self.istechnical,
        'reconstitution_volume_units':self.reconstitution_volume_units,
        'is_added_units':self.is_added_units,
        'reconstitution_volume':self.reconstitution_volume,
        'is_added':self.is_added,
        'sample_replicate':self.sample_replicate,
        'sample_desc':self.sample_desc,
        'biological_material':self.biological_material,
        'extraction_method_id':self.extraction_method_id,
        'sample_condition':self.sample_condition,
        };
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())