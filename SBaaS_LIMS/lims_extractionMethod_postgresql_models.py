from SBaaS_base.postgresql_orm_base import *

#extraction_method
class extraction_method(Base):
    #__table__ = make_table('extraction_method')
    __tablename__ = 'extraction_method'
    id = Column(String(500), nullable = False);
    extraction_method_reference = Column(String(100), nullable = False);
    notes = Column(Text)
    
    __table_args__ = (PrimaryKeyConstraint('id'),
            )
    
    def __init__(self,data_dict_I):
        self.extraction_method_reference=data_dict_I['extraction_method_reference'];
        self.id=data_dict_I['id'];
        self.notes=data_dict_I['notes'];

    #TODO:
    #define relations

    #define representation
    def __repr__(self):
        return "extraction_method: %s" % (self.id)

    #JSON representation
    def __repr__dict__(self):
        return {"id":self.id,"extraction_method_reference":self.extraction_method_reference,"notes":self.notes}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())