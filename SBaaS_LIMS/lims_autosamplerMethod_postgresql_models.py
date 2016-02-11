from SBaaS_base.postgresql_orm_base import *

#Autosampler_parameters
class autosampler_parameters(Base):
    __tablename__ = 'autosampler_parameters'
    id = Column(String(50), nullable = False);
    injvolume_ul = Column(Float);
    washsolvent1 = Column(String(500));
    washsolvent2 = Column(String(500))
    __table_args__ = (PrimaryKeyConstraint('id'),
            )

    def __init__(self,data_dict_I):
        self.washsolvent1=data_dict_I['washsolvent1'];
        self.id=data_dict_I['id'];
        self.washsolvent2=data_dict_I['washsolvent2'];
        self.injvolume_ul=data_dict_I['injvolume_ul'];

#Autosampler_information
class autosampler_information(Base):
    __tablename__ = 'autosampler_information'
    manufacturer = Column(String(100), nullable = False);
    id = Column(String(100), nullable = False);
    serial_number = Column(String(100), nullable = False)
    __table_args__ = (PrimaryKeyConstraint('id'),
            )

    def __init__(self,data_dict_I):
        self.manufacturer=data_dict_I['manufacturer'];
        self.serial_number=data_dict_I['serial_number'];
        self.id=data_dict_I['id'];

#Autosampler_method
class autosampler_method(Base):
    __tablename__ = 'autosampler_method'
    id = Column(String(50), nullable = False);
    autosampler_parameters_id = Column(String(50), nullable = False);
    autosampler_information_id = Column(String(50), nullable = False)
    __table_args__ = (PrimaryKeyConstraint('id'),
            ForeignKeyConstraint(['id'],['autosampler_method.id'], onupdate="CASCADE"),
            ForeignKeyConstraint(['autosampler_information_id'],['autosampler_information.id'], onupdate="CASCADE"),
            ForeignKeyConstraint(['autosampler_parameters_id'],['autosampler_parameters.id'], onupdate="CASCADE"),
            )

    def __init__(self,data_dict_I):
        self.autosampler_parameters_id=data_dict_I['autosampler_parameters_id'];
        self.autosampler_information_id=data_dict_I['autosampler_information_id'];
        self.id=data_dict_I['id'];
