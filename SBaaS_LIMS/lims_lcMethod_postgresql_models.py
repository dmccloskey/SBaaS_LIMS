from SBaaS_base.postgresql_orm_base import *

#LC_information
class lc_information(Base):
    __tablename__ = 'lc_information'
    manufacturer = Column(String(100), nullable = False);
    id = Column(String(100), nullable = False);
    serial_number = Column(String(100), nullable = False)
    __table_args__ = (PrimaryKeyConstraint('id'),
            )

    def __init__(self,data_dict_I):
        self.manufacturer=data_dict_I['manufacturer'];
        self.id=data_dict_I['id'];
        self.serial_number=data_dict_I['serial_number'];

#LC_gradient
class lc_gradient(Base):
    __tablename__ = 'lc_gradient'
    id = Column(String(50), nullable = False);
    lc_event = Column(postgresql.ARRAY(Integer), nullable = False);
    lc_time = Column(postgresql.ARRAY(Float), nullable = False);
    percent_b = Column(postgresql.ARRAY(Float), nullable = False);
    flow_rate = Column(postgresql.ARRAY(Float), nullable = False);
    lc_time_units = Column(String(25), nullable = False);
    flow_rate_units = Column(String(25), nullable = False)
    __table_args__ = (PrimaryKeyConstraint('id'),
            ForeignKeyConstraint(['id'],['lc_gradient.id'], onupdate="CASCADE"),
            )

    def __init__(self,data_dict_I):
        self.lc_time=data_dict_I['lc_time'];
        self.lc_event=data_dict_I['lc_event'];
        self.id=data_dict_I['id'];
        self.flow_rate_units=data_dict_I['flow_rate_units'];
        self.lc_time_units=data_dict_I['lc_time_units'];
        self.flow_rate=data_dict_I['flow_rate'];
        self.percent_b=data_dict_I['percent_b'];

#LC_parameters
class lc_parameters(Base):
    __tablename__ = 'lc_parameters'
    id = Column(String(50), nullable = False);
    column_name = Column(String(100), nullable = False);
    dimensions_and_particle_size = Column(String(100), nullable = False);
    mobile_phase_a = Column(String(100), nullable = False);
    mobile_phase_b = Column(String(100), nullable = False);
    oven_temperature = Column(String(100), nullable = False);
    notes = Column(Text)
    __table_args__ = (PrimaryKeyConstraint('id'),
            )

    def __init__(self,data_dict_I):
        self.mobile_phase_b=data_dict_I['mobile_phase_b'];
        self.mobile_phase_a=data_dict_I['mobile_phase_a'];
        self.dimensions_and_particle_size=data_dict_I['dimensions_and_particle_size'];
        self.column_name=data_dict_I['column_name'];
        self.id=data_dict_I['id'];
        self.notes=data_dict_I['notes'];
        self.oven_temperature=data_dict_I['oven_temperature'];

#LC_method
class lc_method(Base):
    __tablename__ = 'lc_method'
    id = Column(String(50), nullable = False);
    lc_information_id = Column(String(100), nullable = False);
    lc_gradient_id = Column(String(50), nullable = False);
    lc_parameters_id = Column(String(50), nullable = False)
    __table_args__ = (PrimaryKeyConstraint('id'),
            ForeignKeyConstraint(['lc_information_id'],['lc_information.id'], onupdate="CASCADE"),
            ForeignKeyConstraint(['lc_parameters_id'],['lc_parameters.id'], onupdate="CASCADE"),
            )

    def __init__(self,data_dict_I):
        self.lc_information_id=data_dict_I['lc_information_id'];
        self.id=data_dict_I['id'];
        self.lc_parameters_id=data_dict_I['lc_parameters_id'];
        self.lc_gradient_id=data_dict_I['lc_gradient_id'];

#LC_elution
class lc_elution(Base):
    __tablename__ = 'lc_elution'
    id=Column(String(length=50), nullable = False, primary_key=True)
    met_id=Column(String(length=50), nullable = False)
    rt=Column(Float, default = 0.0)
    ms_window=Column(Float, default = 60.0)
    rt_units=Column(String(length=20))
    window_units=Column(String(length=20))
    __table_args__ = (PrimaryKeyConstraint('id'),
            ForeignKeyConstraint(['id'],['lc_method.id'], onupdate="CASCADE"),
            )

    def __init__(self,data_dict_I):
        self.met_id=data_dict_I['met_id'];
        self.lc_method_id=data_dict_I['lc_method_id'];
        self.rt_units=data_dict_I['rt_units'];
        self.window_units=data_dict_I['window_units'];
        self.rt=data_dict_I['rt'];
        self.ms_window=data_dict_I['ms_window'];
