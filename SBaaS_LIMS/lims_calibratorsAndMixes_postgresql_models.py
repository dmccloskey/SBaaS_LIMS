#base orm
from SBaaS_base.postgresql_orm_base import *
#dependent orm models
from .lims_standards_postgresql_models import *

#Calibrators and mixes
#mix_storage
class mix_storage(Base):
    __tablename__ = 'mix_storage'
    mix_id = Column(String(25), nullable = False);
    mixdate= Column(Date);
    box = Column(postgresql.ARRAY(Integer));
    posstart = Column(postgresql.ARRAY(Integer));
    posend = Column(postgresql.ARRAY(Integer))
    __table_args__ = (PrimaryKeyConstraint('mix_id'),
            )
    def __init__(self,data_dict_I):
        self.posstart=data_dict_I['posstart'];
        self.mixdate=data_dict_I['mixdate'];
        self.box=data_dict_I['box'];
        self.posend=data_dict_I['posend'];
        self.mix_id=data_dict_I['mix_id'];

#mix_description
class mix_description(Base):
    __tablename__ = 'mix_description'
    mix_id = Column(String(25), nullable = False);
    mix_description = Column(Text, nullable = False)
    __table_args__ = (PrimaryKeyConstraint('mix_id'),
            )
    def __init__(self,data_dict_I):
        self.mix_id=data_dict_I['mix_id'];
        self.mix_description=data_dict_I['mix_description'];

#mix_parameters
class mix_parameters(Base):
    __tablename__ = 'mix_parameters'
    mix_id = Column(String(25), nullable = False);
    number_of_aliquots = Column(Float, nullable = False);
    mix_volume = Column(Float, nullable = False);
    number_of_aliquiots = Column(Integer, nullable = False)
    __table_args__ = (PrimaryKeyConstraint('mix_id'),
            )
    def __init__(self,data_dict_I):
        self.mix_id=data_dict_I['mix_id'];
        self.number_of_aliquiots=data_dict_I['number_of_aliquiots'];
        self.mix_volume=data_dict_I['mix_volume'];
        self.number_of_aliquots=data_dict_I['number_of_aliquots'];

#calibrator_met_parameters
class calibrator_met_parameters(Base):
    __tablename__ = 'calibrator_met_parameters'
    met_id = Column(String(50), nullable = False);
    dilution = Column(Integer, nullable = False)
    __table_args__ = (PrimaryKeyConstraint('met_id'),
            )
    def __init__(self,data_dict_I):
        self.met_id=data_dict_I['met_id'];
        self.dilution=data_dict_I['dilution'];

#calibrator2mix
class calibrator2mix(Base):
    #__table__ = make_table('calibrator2mix')
    __tablename__ = 'calibrator2mix'
    calibrator_id = Column(Integer, nullable = False);
    mix_id = Column(String(25), nullable = False)
    __table_args__ = (PrimaryKeyConstraint('mix_id'),
            )

    def __init__(self,data_dict_I):
        self.mix_id=data_dict_I['mix_id'];
        self.calibrator_id=data_dict_I['calibrator_id'];

    def __set__row__(self,calibrator_id_I,mix_id_I):
        self.calibrator_id=calibrator_id_I
        self.mix_id=mix_id_I
#mix2met_ID
class mix2met_id(Base):
    #__table__ = make_table('mix2met_id')
    __tablename__ = 'mix2met_id'
    mix_id = Column(String(25), nullable = False);
    met_id = Column(String(50), nullable = False);
    met_name = Column(String(500), nullable = False)
    __table_args__ = (PrimaryKeyConstraint('met_id','mix_id'),
            #ForeignKeyConstraint(['mix_id'],['mix_storage.mix_id']),
            #ForeignKeyConstraint(['mix_id'],['calibrator2mix.mix_id']),
            #ForeignKeyConstraint(['mix_id'],['mix_description.mix_id']),
            )
    
    def __init__(self,data_dict_I):
        self.mix_id=data_dict_I['mix_id'];
        self.met_id=data_dict_I['met_id'];
        self.met_name=data_dict_I['met_name'];

    def __set__row__(self,mix_id_I,met_id_I,met_name_I):
        self.mix_id=mix_id_I
        self.met_id=met_id_I
        self.met_name=met_name_I
#calibrator
class calibrator(Base):
    __tablename__ = 'calibrator'
    met_id = Column(String(50), nullable = False);
    lloq = Column(Float);
    uloq = Column(Float);
    uloq_working = Column(Float);
    concentration_units = Column(String(25));
    stockdate= Column(Date)
    __table_args__ = (UniqueConstraint('met_id','stockdate'),
            PrimaryKeyConstraint('met_id'),
            #ForeignKeyConstraint(['met_id','stockdate'],['standards_storage.met_id','standards_storage.stockdate']),
            )
    
    def __init__(self,data_dict_I):
        self.met_id=data_dict_I['met_id'];
        self.stockdate=data_dict_I['stockdate'];
        self.uloq=data_dict_I['uloq'];
        self.lloq=data_dict_I['lloq'];
        self.concentration_units=data_dict_I['concentration_units'];
        self.uloq_working=data_dict_I['uloq_working'];

#calibrator_concentrations
class calibrator_concentrations(Base):
    #__table__ = make_table('calibrator_concentrations')
    __tablename__ = 'calibrator_concentrations'
    met_id = Column(String(50), nullable = False);
    calibrator_level = Column(Integer, nullable = False);
    dilution_factor = Column(Float);
    calibrator_concentration = Column(Float);
    concentration_units = Column(String(25))
    __table_args__ = (PrimaryKeyConstraint('met_id','calibrator_level'),
            )

    def __init__(self,data_dict_I):
        self.concentration_units=data_dict_I['concentration_units'];
        self.dilution_factor=data_dict_I['dilution_factor'];
        self.calibrator_concentration=data_dict_I['calibrator_concentration'];
        self.calibrator_level=data_dict_I['calibrator_level'];
        self.met_id=data_dict_I['met_id'];

    def __set__row__(self,met_id_I,calibrator_level_I,dilution_factor_I,
                 calibrator_concentration_I,concentration_units_I):
        self.met_id=met_id_I
        self.calibrator_level=calibrator_level_I
        self.dilution_factor=dilution_factor_I
        self.calibrator_concentration=calibrator_concentration_I
        self.concentration_units=concentration_units_I
    def __repr__dict__(self):
        return {"met_id":self.met_id,
                "calibrator_level":self.calibrator_level,
                "dilution_factor":self.dilution_factor,
                "calibrator_concentration":self.calibrator_concentration,
                "concentration_units":self.concentration_units}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
#calibrator_calculations
class calibrator_calculations(Base):
    __tablename__ = 'calibrator_calculations'
    met_id = Column(String(50), nullable = False);
    calcstart_concentration = Column(Float);
    start_concentration = Column(Float)
    
    __table_args__ = (PrimaryKeyConstraint('met_id'),
            #ForeignKeyConstraint(['met_id'],['calibrator.met_id']),
            )
    def __init__(self,data_dict_I):
        self.met_id=data_dict_I['met_id'];
        self.calcstart_concentration=data_dict_I['calcstart_concentration'];
        self.start_concentration=data_dict_I['start_concentration'];

#calibrator_met2mix_calculations
class calibrator_met2mix_calculations(Base):
    __tablename__ = 'calibrator_met2mix_calculations'
    met_id = Column(String(50), nullable = False);
    mix_id = Column(String(25), nullable = False);
    working_concentration = Column(Float);
    total_volume = Column(Float);
    add_volume = Column(Float)
    __table_args__ = (PrimaryKeyConstraint('met_id'),
            #ForeignKeyConstraint(['met_id'],['calibrator_met_parameters.met_id']),
            #ForeignKeyConstraint(['met_id'],['calibrator_calculations.met_id']),
            #ForeignKeyConstraint(['mix_id'],['mix_calculations.mix_id']),
            #ForeignKeyConstraint(['mix_id'],['mix_parameters.mix_id']),
            )
    def __init__(self,data_dict_I):
        self.mix_id=data_dict_I['mix_id'];
        self.total_volume=data_dict_I['total_volume'];
        self.working_concentration=data_dict_I['working_concentration'];
        self.add_volume=data_dict_I['add_volume'];
        self.met_id=data_dict_I['met_id'];

#mix_calculations
class mix_calculations(Base):
    __tablename__ = 'mix_calculations'
    mix_id = Column(String(25), nullable = False);
    number_of_compounds = Column(Integer);
    total_volume_actual = Column(Float);
    aliquot_volume = Column(Float);
    add_to_make_aliquot_volume_even = Column(Float);
    corrected_aliquot_volume = Column(Float);
    volume_units = Column(String(25))
    __table_args__ = (PrimaryKeyConstraint('mix_id'),
            #ForeignKeyConstraint(['mix_id'],['mix_parameters.mix_id']),
            )
    def __init__(self,data_dict_I):
        self.mix_id=data_dict_I['mix_id'];
        self.number_of_compounds=data_dict_I['number_of_compounds'];
        self.total_volume_actual=data_dict_I['total_volume_actual'];
        self.aliquot_volume=data_dict_I['aliquot_volume'];
        self.add_to_make_aliquot_volume_even=data_dict_I['add_to_make_aliquot_volume_even'];
        self.corrected_aliquot_volume=data_dict_I['corrected_aliquot_volume'];
        self.volume_units=data_dict_I['volume_units'];

#calibrator_levels
class calibrator_levels(Base):
    __tablename__ = 'calibrator_levels'
    calibrator_level = Column(Integer, nullable = False);
    dilution = Column(Float, nullable = False);
    injectionvolume = Column(Float);
    workingvolume = Column(Float);
    dilution_factor_from_the_previous_level = Column(Float);
    amount_from_previous_level = Column(Float);
    balance_h2o = Column(Float);
    dilution_concentration = Column(Float)
    __table_args__ = (PrimaryKeyConstraint('calibrator_level'),
            )
    def __init__(self,data_dict_I):
        self.injectionvolume=data_dict_I['injectionvolume'];
        self.dilution_concentration=data_dict_I['dilution_concentration'];
        self.balance_h2o=data_dict_I['balance_h2o'];
        self.amount_from_previous_level=data_dict_I['amount_from_previous_level'];
        self.dilution_factor_from_the_previous_level=data_dict_I['dilution_factor_from_the_previous_level'];
        self.workingvolume=data_dict_I['workingvolume'];
        self.dilution=data_dict_I['dilution'];
        self.calibrator_level=data_dict_I['calibrator_level'];
