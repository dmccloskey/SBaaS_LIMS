from SBaaS_base.postgresql_orm_base import *

#oligos_description
class oligos_description(Base):
    __tablename__ = 'oligos_description'
    oligos_id = Column(String(100), primary_key=True)
    oligos_sequence = Column(Text)
    oligos_purification = Column(String(100))
    oligos_description = Column(Text) #need to rename column to "oligos_desc"
    oligos_notes = Column(Text)

    def __init__(self,data_dict_I):
        self.oligos_description=data_dict_I['oligos_description'];
        self.oligos_purification=data_dict_I['oligos_purification'];
        self.oligos_sequence=data_dict_I['oligos_sequence'];
        self.oligos_id=data_dict_I['oligos_id'];
        self.oligos_notes=data_dict_I['oligos_notes'];

    def __set__row__(self,oligos_id_I,oligos_sequence_I,
                 oligos_purification_I,oligos_description_I,
                 oligos_notes_I):
        self.oligos_id = oligos_id_I
        self.oligos_sequence = oligos_sequence_I
        self.oligos_purification = oligos_purification_I
        self.oligos_description = oligos_description_I
        self.oligos_notes = oligos_notes_I
#oligos_storage
class oligos_storage(Base):
    __tablename__ = 'oligos_storage'
    oligos_id = Column(String(100), primary_key=True)
    oligos_label = Column(String(100))
    oligos_box = Column(Integer)
    oligos_posstart = Column(Integer)
    oligos_posend = Column(Integer)
    oligos_date = Column(DateTime)
    oligos_storagebuffer = Column(String(100))
    oligos_concentration = Column(Float)
    oligos_concentration_units = Column(String(20))

    def __init__(self,data_dict_I):
        self.oligos_box=data_dict_I['oligos_box'];
        self.oligos_label=data_dict_I['oligos_label'];
        self.oligos_id=data_dict_I['oligos_id'];
        self.oligos_concentration=data_dict_I['oligos_concentration'];
        self.oligos_concentration_units=data_dict_I['oligos_concentration_units'];
        self.oligos_storagebuffer=data_dict_I['oligos_storagebuffer'];
        self.oligos_date=data_dict_I['oligos_date'];
        self.oligos_posend=data_dict_I['oligos_posend'];
        self.oligos_posstart=data_dict_I['oligos_posstart'];

    def __set__row__(self,oligos_id_I,oligos_label_I,oligos_box_I,
                 oligos_posstart_I,oligos_posend_I,oligos_date_I,
                 oligos_storagebuffer_I,oligos_concentration_I,
                 oligos_concentration_units_I):
        self.oligos_id = oligos_id_I
        self.oligos_label = oligos_label_I
        self.oligos_box = oligos_box_I
        self.oligos_posstart = oligos_posstart_I
        self.oligos_posend = oligos_posend_I
        self.oligos_date = oligos_date_I
        self.oligos_storagebuffer = oligos_storagebuffer_I
        self.oligos_concentration = oligos_concentration_I
        self.oligos_concentration_units = oligos_concentration_units_I