from SBaaS_base.postgresql_orm_base import *

#quantitation_method
class quantitation_method(Base):
    #__table__ = make_table('quantitation_method')
    __tablename__ = 'quantitation_method'
    id = Column(String(50), nullable = False);
    q1_mass = Column(Float);
    q3_mass = Column(Float);
    met_id = Column(String(50));
    component_name = Column(String(100), nullable = False);
    is_name = Column(String(100))
    fit = Column(String(20));
    weighting = Column(String(20));
    intercept = Column(Float);
    slope = Column(Float);
    correlation = Column(Float);
    use_area = Column(Boolean, default = False)
    lloq = Column(Float);
    uloq = Column(Float);
    points = Column(Integer)

    __table_args__ = (PrimaryKeyConstraint('id','component_name'),
            #ForeignKeyConstraint(['id'],['quantitation_method_list.quantitation_method_id'], ondelete="CASCADE"),
            )

    def __init__(self,data_dict_I):
        self.q1_mass=data_dict_I['q1_mass'];
        self.slope=data_dict_I['slope'];
        self.intercept=data_dict_I['intercept'];
        self.weighting=data_dict_I['weighting'];
        self.fit=data_dict_I['fit'];
        self.component_name=data_dict_I['component_name'];
        self.met_id=data_dict_I['met_id'];
        self.q3_mass=data_dict_I['q3_mass'];
        self.correlation=data_dict_I['correlation'];
        self.id=data_dict_I['id'];
        self.use_area=data_dict_I['use_area'];
        self.is_name=data_dict_I['is_name'];
        self.points=data_dict_I['points'];
        self.uloq=data_dict_I['uloq'];
        self.lloq=data_dict_I['lloq'];

    def __set__row__(self,id_I, q1_mass_I,q3_mass_I,met_id_I,component_name_I,is_name_I,fit_I,
                 weighting_I,intercept_I,slope_I,correlation_I,use_area_I,lloq_I,uloq_I,
                 points_I):
        self.id = id_I;
        self.q1_mass = q1_mass_I;
        self.q3_mass = q3_mass_I;
        self.met_id = met_id_I;
        self.component_name = component_name_I;
        self.is_name = is_name_I;
        self.fit = fit_I;
        self.weighting = weighting_I;
        self.intercept = intercept_I;
        self.slope = slope_I;
        self.correlation = correlation_I;
        self.use_area = use_area_I;
        self.lloq = lloq_I;
        self.uloq = uloq_I;
        self.points = points_I;

    def __repr__dict__(self):
        return {'id':self.id,
                'q1_mass':self.q1_mass,
                'q3_mass':self.q3_mass,
                'met_id':self.met_id,
                'component_name':self.component_name,
                'is_name':self.is_name,
                'fit':self.fit,
                'weighting':self.weighting,
                'intercept':self.intercept,
                'slope':self.slope,
                'correlation':self.correlation,
                'use_area':self.use_area,
                'lloq':self.lloq,
                'uloq':self.uloq,
                'points':self.points,
                }
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

#quantitation_method_list
class quantitation_method_list(Base):
    #__table__ = make_table('quantitation_method_list')
    __tablename__ = 'quantitation_method_list'
    quantitation_method_id = Column(String(50), nullable = False)
    __table_args__ = (PrimaryKeyConstraint('quantitation_method_id'),
            )

    def __init__(self,data_dict_I):
        self.quantitation_method_id=data_dict_I['quantitation_method_id'];

    def __set__row__(self,quantitation_method_id_I):
        self.quantitation_method_id = quantitation_method_id_I;

    def __repr__dict__(self):
        return {'quantitation_method_id':self.quantitation_method_id,
                }
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
