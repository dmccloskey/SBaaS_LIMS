from SBaaS_base.postgresql_orm_base import *

#standards
class standards(Base):
    #__table__ = make_table('standards')
    
    __tablename__ = 'standards'
    met_id = Column(String(50), nullable = False);
    met_name = Column(String(500), nullable = False);
    formula = Column(String(100));
    hmdb = Column(String(500));
    solubility = Column(Float);
    solubility_units = Column(String(10));
    mass = Column(Float);
    cas_number = Column(String(100));
    keggid = Column(String(100));
    structure_file = Column(Text);
    structure_file_extention = Column(String(10));
    exactmass = Column(Float)
    __table_args__ = (PrimaryKeyConstraint('met_id'),
            )

    def __init__(self,data_dict_I):
        self.solubility=data_dict_I['solubility'];
        self.met_id=data_dict_I['met_id'];
        self.met_name=data_dict_I['met_name'];
        self.formula=data_dict_I['formula'];
        self.hmdb=data_dict_I['hmdb'];
        self.solubility_units=data_dict_I['solubility_units'];
        self.exactmass=data_dict_I['exactmass'];
        self.mass=data_dict_I['mass'];
        self.structure_file_extention=data_dict_I['structure_file_extention'];
        self.structure_file=data_dict_I['structure_file'];
        self.keggid=data_dict_I['keggid'];
        self.cas_number=data_dict_I['cas_number'];

    def __set__row__(self,met_id_I,met_name_I,formula_I,hmdb_I,
                solubility_I,solubility_units_I,mass_I,cas_number_I,
                keggid_I,structure_file_I,structure_file_extention_I,
                exactmass_I):
        self.met_id=met_id_I
        self.met_name=met_name_I
        self.formula=formula_I
        self.hmdb=hmdb_I
        self.solubility=solubility_I
        self.solubility_units=solubility_units_I
        self.mass=mass_I
        self.cas_number=cas_number_I
        self.keggid=keggid_I
        self.structure_file=structure_file_I
        self.structure_file_extention=structure_file_extention_I
        self.exactmass=exactmass_I

    #TODO:
    #define relations

    #define representation
    def __repr__(self):
        return "standards: %s" % (self.met_id)

    #JSON representation
    def __repr__dict__(self):
        return {"met_id":self.met_id}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
#standards_ordering
class standards_ordering(Base):
    #__table__ = make_table('standards_ordering')
    __tablename__ = 'standards_ordering'
    met_id = Column(String(50), nullable = False);
    met_name = Column(String(100), nullable = False);
    hillcrest = Column(Boolean);
    provider = Column(String(100), nullable = False);
    provider_reference = Column(String(100), nullable = False);
    price = Column(Float);
    amount = Column(Float);
    amount_units = Column(String(10));
    purity = Column(Float);
    mw = Column(Float);
    notes = Column(String(500));
    powderdate_received= Column(Date);
    powderdate_opened= Column(Date);
    order_standard = Column(Boolean);
    standards_storage = Column(Float);
    purchase = Column(Boolean)
    __table_args__ = (PrimaryKeyConstraint('met_id','provider','provider_reference'),
            )

    def __init__(self,data_dict_I):
        self.amount=data_dict_I['amount'];
        self.met_id=data_dict_I['met_id'];
        self.met_name=data_dict_I['met_name'];
        self.hillcrest=data_dict_I['hillcrest'];
        self.provider=data_dict_I['provider'];
        self.provider_reference=data_dict_I['provider_reference'];
        self.price=data_dict_I['price'];
        self.amount_units=data_dict_I['amount_units'];
        self.purity=data_dict_I['purity'];
        self.mw=data_dict_I['mw'];
        self.notes=data_dict_I['notes'];
        self.powderdate_received=data_dict_I['powderdate_received'];
        self.powderdate_opened=data_dict_I['powderdate_opened'];
        self.order_standard=data_dict_I['order_standard'];
        self.standards_storage=data_dict_I['standards_storage'];
        self.purchase=data_dict_I['purchase'];

    def __set__row__(self,met_id_I,met_name_I,hillcrest_I,
                 provider_I,provider_reference_I,price_I,
                 amount_I,amount_units_I,purity_I,mw_I,
                 notes_I,powderdate_received_I,
                 powderdate_opened_I,order_standard_I,
                 standards_storage_I,purchase_I):
        self.met_id=met_id_I
        self.met_name=met_name_I
        self.hillcrest=hillcrest_I
        self.provider=provider_I
        self.provider_reference=provider_reference_I
        self.price=price_I
        self.amount=amount_I
        self.amount_units=amount_units_I
        self.purity=purity_I
        self.mw=mw_I
        self.notes=notes_I
        self.powderdate_received=powderdate_received_I
        self.powderdate_opened=powderdate_opened_I
        self.order_standard=order_standard_I
        self.standards_storage=standards_storage_I
        self.purchase=purchase_I

    #TODO:
    #define relations

    #define representation
    def __repr__(self):
        return "standards_ordering: %s" % (self.met_id)

    #JSON representation
    def __repr__dict__(self):
        return {"met_id":self.met_id}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
#standards2material
class standards2material(Base):
    __tablename__ = 'standards2material'
    met_id = Column(String(50), nullable = False);
    provider = Column(String(100), nullable = False);
    provider_reference = Column(String(100), nullable = False)
    __table_args__ = (PrimaryKeyConstraint('met_id','provider','provider_reference'),
                      ForeignKeyConstraint(['met_id'],['standards.met_id']),
                      ForeignKeyConstraint(['met_id','provider','provider_reference'],['standards_ordering.met_id','standards_ordering.provider','standards_ordering.provider_reference']),
            )

    def __init__(self,data_dict_I):
        self.provider=data_dict_I['provider'];
        self.provider_reference=data_dict_I['provider_reference'];
        self.met_id=data_dict_I['met_id'];

#standards_storage
class standards_storage(Base):
    __tablename__ = 'standards_storage'
    met_id = Column(String(50), nullable = False);
    met_name = Column(String(500), nullable = False);
    provider = Column(String(100), nullable = False);
    provider_reference = Column(String(50), nullable = False);
    powderdate= Column(Date);
    stockdate= Column(Date, nullable = False);
    concentration = Column(Float);
    concentration_units = Column(String(10));
    aliquots = Column(Integer);
    solvent = Column(String(100));
    ph = Column(Float);
    box = Column(Integer);
    posstart = Column(Integer);
    posend = Column(Integer)
    __table_args__ = (UniqueConstraint('met_id','stockdate'),
            PrimaryKeyConstraint('met_id','provider','provider_reference','stockdate'),
            ForeignKeyConstraint(['met_id','provider','provider_reference'],['standards2material.met_id','standards2material.provider','standards2material.provider_reference']),
            )

    def __init__(self,data_dict_I):
        self.posend=data_dict_I['posend'];
        self.met_id=data_dict_I['met_id'];
        self.met_name=data_dict_I['met_name'];
        self.ph=data_dict_I['ph'];
        self.box=data_dict_I['box'];
        self.posstart=data_dict_I['posstart'];
        self.provider=data_dict_I['provider'];
        self.provider_reference=data_dict_I['provider_reference'];
        self.powderdate=data_dict_I['powderdate'];
        self.stockdate=data_dict_I['stockdate'];
        self.concentration=data_dict_I['concentration'];
        self.concentration_units=data_dict_I['concentration_units'];
        self.aliquots=data_dict_I['aliquots'];
        self.solvent=data_dict_I['solvent'];
