from SBaaS_base.postgresql_orm_base import *

#IS
#internal_standard
class internal_standard(Base):
    #__table__ = make_table('internal_standard')
    __tablename__ = 'internal_standard'
    is_id = Column(Integer, nullable = False);
    is_date = Column(DateTime, nullable = False);
    experimentor_id = Column(String(50), nullable = False);
    extraction_method_id = Column(String(50))
    __table_args__ = (PrimaryKeyConstraint('is_id'),
            ForeignKeyConstraint(['is_id'],['internal_standard_storage.is_id']),
            )

    def __init__(self,data_dict_I):
        self.experimentor_id=data_dict_I['experimentor_id'];
        self.is_id=data_dict_I['is_id'];
        self.is_date=data_dict_I['is_date'];
        self.extraction_method_id=data_dict_I['extraction_method_id'];

#internal_standard_storage
class internal_standard_storage(Base):
    #__table__ = make_table('internal_standard_storage')
    __tablename__ = 'internal_standard_storage'
    is_id = Column(Integer, nullable = False);
    concentration = Column(Float);
    concentration_units = Column(String(10));
    aliquots = Column(Integer);
    aliquot_volume = Column(Float);
    aliquot_volume_units = Column(String(10));
    solvent = Column(String(100));
    ph = Column(Float);
    box = Column(Integer);
    posstart = Column(Integer);
    posend = Column(Integer)
    __table_args__ = (PrimaryKeyConstraint('is_id'),
            )

    def __init__(self,data_dict_I):
        self.ph=data_dict_I['ph'];
        self.is_id=data_dict_I['is_id'];
        self.concentration=data_dict_I['concentration'];
        self.concentration_units=data_dict_I['concentration_units'];
        self.aliquots=data_dict_I['aliquots'];
        self.aliquot_volume=data_dict_I['aliquot_volume'];
        self.posstart=data_dict_I['posstart'];
        self.aliquot_volume_units=data_dict_I['aliquot_volume_units'];
        self.posend=data_dict_I['posend'];
        self.solvent=data_dict_I['solvent'];
        self.box=data_dict_I['box'];
