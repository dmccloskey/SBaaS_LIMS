from SBaaS_base.postgresql_orm_base import *

#Experimentor
#experimentor_id2name
class experimentor_id2name(Base):
    #__table__ = make_table('experimentor_id2name')
    __tablename__ = 'experimentor_id2name'
    experimentor_id = Column(String(50), nullable = False);
    experimentor_name = Column(String(100), nullable = False);
    experimentor_role = Column(String(500), nullable = False)

    __table_args__ = (ForeignKeyConstraint(['experimentor_id'],['experimentor_list.experimentor_id'], onupdate="CASCADE"),
                ForeignKeyConstraint(['experimentor_name'],['experimentor.experimentor_name']),
                PrimaryKeyConstraint('experimentor_id','experimentor_name','experimentor_role'),
            )

    def __init__(self,data_dict_I):
        self.experimentor_role=data_dict_I['experimentor_role'];
        self.experimentor_id=data_dict_I['experimentor_id'];
        self.experimentor_name=data_dict_I['experimentor_name'];

    def __repr__(self):
        return "experimentor_id2name: %s, %s, %s" % (self.experimentor_id,self.experimentor_name,self.experimentor_role)

    def __repr__dict__(self):
        return {"experimentor_id":self.experimentor_id,"experimentor_name":self.experimentor_name,"experimentor_role":self.experimentor_role}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
#experimentor
class experimentor(Base):
    #__table__ = make_table('experimentor')
    __tablename__ = 'experimentor'
    experimentor_name = Column(String(100), nullable = False);
    contact_information = Column(String(100))
    __table_args__ = (PrimaryKeyConstraint('experimentor_name'),
            )

    #define relations
    experimentor_id2name = relationship(experimentor_id2name);

    def __init__(self,data_dict_I):
        self.contact_information=data_dict_I['contact_information'];
        self.experimentor_name=data_dict_I['experimentor_name'];

    def __repr__(self):
        return "experimentor: %s, %s" % (self.experimentor_name,self.contact_information)

    #TODO:
    #JSON representation
    def __repr__dict__(self):
        return {"experimentor_name":self.experimentor_name,"contact_information":self.contact_information}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
#experimentor_list
class experimentor_list(Base):
    #__table__ = make_table('experimentor_list')
    __tablename__ = 'experimentor_list'
    experimentor_id = Column(String(50), nullable = False)

    __table_args__ = (PrimaryKeyConstraint('experimentor_id'),
            )
    #define relations
    experimentor_id2name = relationship(experimentor_id2name);

    def __init__(self,data_dict_I):
        self.experimentor_id=data_dict_I['experimentor_id'];

    def __repr__(self):
        return "experimentor_list: %s" % (self.experimentor_id)

    #TODO:
    #JSON representation
    def __repr__dict__(self):
        return {"experimentor_list":self.experimentor_id}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())