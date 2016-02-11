from .lims_biologicalMaterial_postgresql_models import *

from SBaaS_base.sbaas_base_query_update import sbaas_base_query_update
from SBaaS_base.sbaas_base_query_drop import sbaas_base_query_drop
from SBaaS_base.sbaas_base_query_initialize import sbaas_base_query_initialize
from SBaaS_base.sbaas_base_query_insert import sbaas_base_query_insert
from SBaaS_base.sbaas_base_query_select import sbaas_base_query_select
from SBaaS_base.sbaas_base_query_delete import sbaas_base_query_delete

from SBaaS_base.sbaas_template_query import sbaas_template_query

class lims_biologicalMaterial_query(sbaas_template_query):

    def initialize_supportedTables(self):
        '''Set the supported tables dict for 
        '''
        tables_supported = {
            'biologicalmaterial_storage':biologicalMaterial_storage,
            'biologicalmaterial_description':biologicalMaterial_description,
            'biologicalmaterial_genereferences':biologicalMaterial_geneReferences,
            'biologicalmaterial_massvolumeconversion':biologicalMaterial_massVolumeConversion,
                        };
        self.set_supportedTables(tables_supported);
    
    # query gene names from biologicalMaterial_geneReferences
    def get_orderedLocusName_biologicalmaterialIDAndGeneName_biologicalMaterialGeneReferences(self,biologicalmaterial_id_I,gene_name_I):
        '''Query ordered locus name from gene name'''
        try:
            data = self.session.query(biologicalMaterial_geneReferences.biologicalmaterial_id,
                    biologicalMaterial_geneReferences.gene_name,
                    biologicalMaterial_geneReferences.ordered_locus_name).filter(
                    biologicalMaterial_geneReferences.biologicalmaterial_id.like(biologicalmaterial_id_I),
                    biologicalMaterial_geneReferences.gene_name.like(gene_name_I)).all();
            data_O = [];
            for d in data: 
                data_dict = {};
                data_dict['ordered_locus_name'] = d.ordered_locus_name;
                data_O.append(data_dict);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_ecogeneAccessionNumber_biologicalmaterialIDAndGeneName_biologicalMaterialGeneReferences(self,biologicalmaterial_id_I,gene_name_I):
        '''Query ecogene accession number from gene name'''
        try:
            data = self.session.query(biologicalMaterial_geneReferences.biologicalmaterial_id,
                    biologicalMaterial_geneReferences.gene_name,
                    biologicalMaterial_geneReferences.ecogene_accession_number).filter(
                    biologicalMaterial_geneReferences.biologicalmaterial_id.like(biologicalmaterial_id_I),
                    biologicalMaterial_geneReferences.gene_name.like(gene_name_I)).all();
            data_O = [];
            for d in data: 
                data_dict = {};
                data_dict['ecogene_accession_number'] = d.ecogene_accession_number;
                data_O.append(data_dict);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_geneName_biologicalmaterialIDAndOrderedLocusName_biologicalMaterialGeneReferences(self,biologicalmaterial_id_I,ordered_locus_name_I):
        '''Query gene name from ordered locus name'''
        try:
            data = self.session.query(biologicalMaterial_geneReferences.biologicalmaterial_id,
                    biologicalMaterial_geneReferences.gene_name,
                    biologicalMaterial_geneReferences.ordered_locus_name).filter(
                    biologicalMaterial_geneReferences.biologicalmaterial_id.like(biologicalmaterial_id_I),
                    biologicalMaterial_geneReferences.ordered_locus_name.like(ordered_locus_name_I)).all();
            data_O = [];
            for d in data: 
                data_dict = {};
                data_dict['ordered_locus_name'] = d.ordered_locus_name;
                data_O.append(data_dict);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_ecogeneAccessionNumber_biologicalmaterialIDAndOrderedLocusName_biologicalMaterialGeneReferences(self,biologicalmaterial_id_I,ordered_locus_name_I):
        '''Query ecogene accession number from ordered locus name name'''
        try:
            data = self.session.query(biologicalMaterial_geneReferences.biologicalmaterial_id,
                    biologicalMaterial_geneReferences.ordered_locus_name,
                    biologicalMaterial_geneReferences.ecogene_accession_number).filter(
                    biologicalMaterial_geneReferences.biologicalmaterial_id.like(biologicalmaterial_id_I),
                    biologicalMaterial_geneReferences.ordered_locus_name.like(ordered_locus_name_I)).all();
            data_O = [];
            for d in data: 
                data_dict = {};
                data_dict['ecogene_accession_number'] = d.ecogene_accession_number;
                data_O.append(data_dict);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
        #table initializations:
    def drop_lims_biologicalMaterial(self):
        try:
            biologicalMaterial_storage.__table__.drop(self.engine,True);
            biologicalMaterial_description.__table__.drop(self.engine,True);
            biologicalMaterial_geneReferences.__table__.drop(self.engine,True);
            biologicalMaterial_massVolumeConversion.__table__.drop(self.engine,True);
        except SQLAlchemyError as e:
            print(e);
    def reset_lims_biologicalMaterial(self):
        try:
            reset = self.session.query(biologicalMaterial_storage).delete(synchronize_session=False);
            reset = self.session.query(biologicalMaterial_description).delete(synchronize_session=False);
            reset = self.session.query(biologicalMaterial_geneReferences).delete(synchronize_session=False);
            reset = self.session.query(biologicalMaterial_massVolumeConversion).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def initialize_lims_biologicalMaterial(self):
        try:
            biologicalMaterial_storage.__table__.create(self.engine,True);
            biologicalMaterial_description.__table__.create(self.engine,True);
            biologicalMaterial_geneReferences.__table__.create(self.engine,True);
            biologicalMaterial_massVolumeConversion.__table__.create(self.engine,True);

        except SQLAlchemyError as e:
            print(e);
            
    def add_biologicalMaterialDescription(self, data_I):
        '''add rows of biologicalMaterial_description'''
        if data_I:
            for d in data_I:
                try:
                    data_add = biologicalMaterial_description(d
                        #d['biologicalmaterial_id'],
                        #d['biologicalmaterial_strain'],
                        #d['biologicalmaterial_description'],
                        #d['biologicalmaterial_notes']
                        );
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def add_biologicalMaterialGeneReferences(self, data_I):
        '''add rows of biologicalMaterial_geneReferences'''
        if data_I:
            for d in data_I:
                try:
                    data_add = biologicalMaterial_geneReferences(d
                        #d['biologicalmaterial_id'],
                        #d['ordered_locus_name'],
                        #d['ordered_locus_name2'],
                        #d['swissprot_entry_name'],
                        #d['ac'],
                        #d['ecogene_accession_number'],
                        #d['gene_name']
                        );
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def update_biologicalMaterialGeneReferences(self,data_I):
        '''update rows of biologicalMaterial_geneReferences'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(biologicalMaterial_geneReferences).filter(
                           biologicalMaterial_geneReferences.id==d['id']).update(
                            {'biologicalmaterial_id':d['biologicalmaterial_id'],
                                'ordered_locus_name':d['ordered_locus_name'],
                                'ordered_locus_name2':d['ordered_locus_name2'],
                                'swissprot_entry_name':d['swissprot_entry_name'],
                                'ac':d['ac'],
                                'ecogene_accession_number':d['ecogene_accession_number'],
                                'gene_name':d['gene_name']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def add_biologicalMaterialMassVolumeConversion(self, data_I):
        '''add rows of biologicalMaterial_massVolumeConversion'''
        if data_I:
            for d in data_I:
                try:
                    data_add = biologicalMaterial_massVolumeConversion(d
                        #d['biological_material'],
                        #        d['conversion_name'],
                        #        d['conversion_factor'],
                        #        d['conversion_units'],
                        #        d['conversion_reference']
                                );
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    def update_biologicalMaterialMassVolumeConversion(self,data_I):
        '''update rows of biologicalMaterial_sampleVolumeConversion'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(biologicalMaterial_massVolumeConversion).filter(
                           biologicalMaterial_massVolumeConversion.id==d['id']).update(
                            {'biological_material':d['biological_material'],
                            'conversion_name':d['conversion_name'],
                            'conversion_factor':d['conversion_factor'],
                            'conversion_units':d['conversion_units'],
                            'conversion_reference':d['conversion_reference']},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    # query biologicalMaterial_massVolumeConversion
    def get_conversionAndConversionUnits_biologicalMaterialAndConversionName(self,biological_material_I,conversion_name_I):
        '''Querry conversion and conversion units from
        biological material and conversion name
        NOTE: intended to be used within a for loop'''
        try:
            physiologicalParameters = self.session.query(biologicalMaterial_massVolumeConversion.conversion_factor,
                    biologicalMaterial_massVolumeConversion.conversion_units).filter(
                    biologicalMaterial_massVolumeConversion.biological_material.like(biological_material_I),
                    biologicalMaterial_massVolumeConversion.conversion_name.like(conversion_name_I)).all();
            conversion_O, conversion_units_O = None,None;
            if physiologicalParameters:
                conversion_O = physiologicalParameters[0][0];
                conversion_units_O = physiologicalParameters[0][1];
            return conversion_O, conversion_units_O;
        except SQLAlchemyError as e:
            print(e);