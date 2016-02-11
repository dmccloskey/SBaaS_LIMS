from SBaaS_base.postgresql_orm_base import *
from .lims_lcMethod_postgresql_models import *
from .lims_msMethod_postgresql_models import *
from .lims_autosamplerMethod_postgresql_models import *

#acquisition_method
class acquisition_method(Base):
    #__table__ = make_table('acquisition_method')
    __tablename__ = 'acquisition_method'
    id = Column(String(50), nullable = False);
    ms_method_id = Column(String(50));
    autosampler_method_id = Column(String(50));
    lc_method_id = Column(String(50))
    __table_args__ = (PrimaryKeyConstraint('id'),
            ForeignKeyConstraint(['lc_method_id'],['lc_method.id'], onupdate="CASCADE"),
            ForeignKeyConstraint(['ms_method_id'],['ms_method.id'], onupdate="CASCADE"),
            )

    def __init__(self,data_dict_I):
        self.ms_method_id=data_dict_I['ms_method_id'];
        self.id=data_dict_I['id'];
        self.autosampler_method_id=data_dict_I['autosampler_method_id'];
        self.lc_method_id=data_dict_I['lc_method_id'];

    def __set__row__(self,id_I, ms_method_id_I,autosampler_method_id_I,lc_method_id_I):
        self.id = id_I;
        self.ms_method_id = ms_method_id_I;
        self.autosampler_method_id = autosampler_method_id_I;
        self.lc_method_id = lc_method_id_I;