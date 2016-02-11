from SBaaS_base.postgresql_orm_base import *

#experiments
#experiment_types
class experiment_types(Base):
    #__table__ = make_table('experiment_types')
    __tablename__ = 'experiment_types'
    id = Column(Integer, nullable = False);
    experiment_name = Column(String(100))
    __table_args__ = (PrimaryKeyConstraint('id'),
            )
    
    def __init__(self,data_dict_I):
        self.id=data_dict_I['id'];
        self.experiment_name=data_dict_I['experiment_name'];

    def __set__row__(self,id_I,experiment_type_I):
        self.id=id_I;
        self.experiment_type=experiment_type_I;
#experiment
class experiment(Base):
    #__table__ = make_table('experiment')
    __tablename__ = 'experiment'
    ##TODO:
    #wid = Column(Integer, Sequence('experiment_id_seq'),nullable=False,)
    wid = Column(Integer, Sequence('wids'),nullable=False,)
    exp_type_id=Column(Integer);
    id=Column(String(50),nullable=False);
    sample_name=Column(String(500),nullable=False);
    experimentor_id=Column(String(50));
    extraction_method_id=Column(String(50));
    acquisition_method_id=Column(String(50),nullable=False);
    quantitation_method_id=Column(String(50));
    internal_standard_id=Column(Integer);
    
    __table_args__ = (
            PrimaryKeyConstraint('id','sample_name'),
            #ForeignKeyConstraint(['acquisition_method_id'], ['acquisition_method.id'], onupdate="CASCADE"),
            #ForeignKeyConstraint(['exp_type_id'], ['experiment_types.id'], ondelete="CASCADE"),
            #ForeignKeyConstraint(['experimentor_id'], ['experimentor_list.experimentor_id']),
            #ForeignKeyConstraint(['extraction_method_id'], ['extraction_method.id']),
            #ForeignKeyConstraint(['internal_standard_id'], ['internal_standard.is_id']),
            #ForeignKeyConstraint(['quantitation_method_id'], ['quantitation_method_list.quantitation_method_id']),
            #ForeignKeyConstraint(['sample_name'], ['sample.sample_name']),
            UniqueConstraint('wid'),
            )

    def __init__(self,data_dict_I):
        self.experimentor_id=data_dict_I['experimentor_id'];
        self.exp_type_id=data_dict_I['exp_type_id'];
        self.id=data_dict_I['id'];
        self.sample_name=data_dict_I['sample_name'];
        self.extraction_method_id=data_dict_I['extraction_method_id'];
        self.acquisition_method_id=data_dict_I['acquisition_method_id'];
        self.quantitation_method_id=data_dict_I['quantitation_method_id'];
        self.internal_standard_id=data_dict_I['internal_standard_id'];

    def __set__row__(self,exp_type_id_I,id_I,sample_name_I,
                 experimentor_id_I,extraction_method_id_I,
                 acquisition_method_id_I,quantitation_method_id_I,
                 internal_standard_id_I):
        self.exp_type_id=exp_type_id_I;
        self.id=id_I;
        self.sample_name=sample_name_I;
        self.experimentor_id=experimentor_id_I;
        self.extraction_method_id=extraction_method_id_I;
        self.acquisition_method_id=acquisition_method_id_I;
        self.quantitation_method_id=quantitation_method_id_I;
        self.internal_standard_id=internal_standard_id_I;
    #TODO:
    #define relations

    #define representation
    def __repr__(self):
        return "experiment: %s" % (self.id)

    #JSON representation
    def __repr__dict__(self):
        return {"id":self.id,
                "sample_name":self.sample_name,
                "experimentor_id":self.experimentor_id,
                "extraction_method_ide":self.extraction_method_id,
                "acquisition_method_id":self.acquisition_method_id,
                "quantitation_method_id":self.quantitation_method_id,
                "internal_standard_id":self.internal_standard_id}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())