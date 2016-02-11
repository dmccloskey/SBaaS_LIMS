from SBaaS_base.postgresql_orm_base import *

#biologicalmaterial_storage
class biologicalMaterial_storage(Base):
    __tablename__ = 'biologicalmaterial_storage'
    biologicalmaterial_id = Column(String(100), primary_key=True)
    biologicalmaterial_label = Column(String(100))
    biologicalmaterial_box = Column(Integer)
    biologicalmaterial_posstart = Column(Integer)
    biologicalmaterial_posend = Column(Integer)
    biologicalmaterial_date = Column(DateTime)

    def __init__(self,data_dict_I):
        self.biologicalmaterial_posstart=data_dict_I['biologicalmaterial_posstart'];
        self.biologicalmaterial_label=data_dict_I['biologicalmaterial_label'];
        self.biologicalmaterial_id=data_dict_I['biologicalmaterial_id'];
        self.biologicalmaterial_posend=data_dict_I['biologicalmaterial_posend'];
        self.biologicalmaterial_date=data_dict_I['biologicalmaterial_date'];
        self.biologicalmaterial_box=data_dict_I['biologicalmaterial_box'];

    def __set__row__(self,biologicalmaterial_id_I,biologicalmaterial_label_I,biologicalmaterial_box_I,
                 biologicalmaterial_posstart_I,biologicalmaterial_posend_I,biologicalmaterial_date_I):
        self.biologicalmaterial_id = biologicalmaterial_id_I
        self.biologicalmaterial_label = biologicalmaterial_label_I
        self.biologicalmaterial_box = biologicalmaterial_box_I
        self.biologicalmaterial_posstart = biologicalmaterial_posstart_I
        self.biologicalmaterial_posend = biologicalmaterial_posend_I
        self.biologicalmaterial_date = biologicalmaterial_date_I
#biologicalmaterial_description
class biologicalMaterial_description(Base):
    __tablename__ = 'biologicalmaterial_description'
    biologicalmaterial_id = Column(String(100), primary_key=True)
    biologicalmaterial_strain = Column(String(100))
    biologicalmaterial_description = Column(Text)
    biologicalmaterial_notes = Column(Text)

    def __init__(self,data_dict_I):
        self.biologicalmaterial_id=data_dict_I['biologicalmaterial_id'];
        self.biologicalmaterial_strain=data_dict_I['biologicalmaterial_strain'];
        self.biologicalmaterial_notes=data_dict_I['biologicalmaterial_notes'];
        self.biologicalmaterial_description=data_dict_I['biologicalmaterial_description'];

    def __set__row__(self,biologicalmaterial_id_I,biologicalmaterial_strain_I,biologicalmaterial_description_I,
                biologicalmaterial_notes_I):
        self.biologicalmaterial_id = biologicalmaterial_id_I
        self.biologicalmaterial_strain = biologicalmaterial_strain_I
        self.biologicalmaterial_description = biologicalmaterial_description_I
        self.biologicalmaterial_notes = biologicalmaterial_notes_I
#biologicalmaterial_description
class biologicalMaterial_geneReferences(Base):
    __tablename__ = 'biologicalmaterial_genereferences'
    id = Column(Integer, Sequence('biologicalmaterial_genereferences_id_seq'), primary_key=True)
    biologicalmaterial_id = Column(String(100))
    ordered_locus_name = Column(String(20))
    ordered_locus_name2 = Column(String(100))
    swissprot_entry_name = Column(String(20))
    ac = Column(String(20))
    ecogene_accession_number = Column(String(20))
    gene_name = Column(String(20))

    def __init__(self,data_dict_I):
        self.gene_name=data_dict_I['gene_name'];
        self.biologicalmaterial_id=data_dict_I['biologicalmaterial_id'];
        self.ordered_locus_name=data_dict_I['ordered_locus_name'];
        self.ordered_locus_name2=data_dict_I['ordered_locus_name2'];
        self.swissprot_entry_name=data_dict_I['swissprot_entry_name'];
        self.ac=data_dict_I['ac'];
        self.ecogene_accession_number=data_dict_I['ecogene_accession_number'];

    def __set__row__(self,biologicalmaterial_id_I,
                ordered_locus_name_I,
                ordered_locus_name2_I,
                swissprot_entry_name_I,
                ac_I,
                ecogene_accession_number_I,
                gene_name_I):
        self.biologicalmaterial_id=biologicalmaterial_id_I
        self.ordered_locus_name=ordered_locus_name_I
        self.ordered_locus_name2=ordered_locus_name2_I
        self.swissprot_entry_name=swissprot_entry_name_I
        self.ac=ac_I
        self.ecogene_accession_number=ecogene_accession_number_I
        self.gene_name=gene_name_I

    #TODO:
    #define relations

    def __repr__dict__(self):
        return {'biologicalmaterial_id':self.biologicalmaterial_id,
                'ordered_locus_name':self.ordered_locus_name,
                'ordered_locus_name2':self.ordered_locus_name2,
                'swissprot_entry_name':self.swissprot_entry_name,
                'ac':self.ac,
                'ecogene_accession_number':self.ecogene_accession_number,
                'gene_name':self.gene_name}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
#TODO:
#biologicalMaterial_massVolumeConversion
class biologicalMaterial_massVolumeConversion(Base):
    __tablename__ = 'biologicalmaterial_massvolumeconversion'
    biological_material=Column(String(100),nullable=False, primary_key=True);
    conversion_name=Column(String(50),nullable=False, primary_key=True);
    conversion_factor=Column(Float);
    conversion_units=Column(String(50),nullable=False);
    conversion_reference=Column(String(500),nullable=False);

    def __init__(self,data_dict_I):
        self.conversion_name=data_dict_I['conversion_name'];
        self.conversion_factor=data_dict_I['conversion_factor'];
        self.conversion_reference=data_dict_I['conversion_reference'];
        self.conversion_units=data_dict_I['conversion_units'];
        self.biological_material=data_dict_I['biological_material'];

    def __set__row__(self,biological_material_I,
        conversion_name_I,
        conversion_factor_I,
        conversion_units_I,
        conversion_reference_I):
        self.biological_material=biological_material_I
        self.conversion_name=conversion_name_I
        self.conversion_factor=conversion_factor_I
        self.conversion_units=conversion_units_I
        self.conversion_reference=conversion_reference_I

    #TODO:
    #define relations

    def __repr__dict__(self):
        return {'biological_material':self.biological_material,
            'conversion_name':self.conversion_name,
            'conversion_factor':self.conversion_factor,
            'conversion_units':self.conversion_units,
            'conversion_reference':self.conversion_reference,}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())