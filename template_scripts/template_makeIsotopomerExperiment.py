import sys
sys.path.append('C:/Users/dmccloskey-sbrg/Google Drive/SBaaS_base')
from SBaaS_base.postgresql_settings import postgresql_settings
from SBaaS_base.postgresql_orm import postgresql_orm

# read in the settings file
filename = 'C:/Users/dmccloskey-sbrg/Google Drive/SBaaS_base/settings_1.ini';
pg_settings = postgresql_settings(filename);

## make a new database and user from the settings file
#pg_orm = postgresql_orm();
#pg_orm.create_newDatabaseAndUserFromSettings(
#            # default login made when installing postgresql
#            database_I='postgres',user_I='postgres',password_I='18dglass',host_I="localhost:5432",
#            # new settings
#            settings_I=pg_settings.database_settings,
#            # privileges for the new user
#            privileges_O=['ALL PRIVILEGES'],tables_O=['ALL TABLES'],schema_O='public');

# connect to the database from the settings file
pg_orm = postgresql_orm();
pg_orm.set_sessionFromSettings(pg_settings.database_settings);
session = pg_orm.get_session();
engine = pg_orm.get_engine();

# your app...
sys.path.append(pg_settings.datadir_settings['drive']+'/SBaaS_LIMS')
sys.path.append(pg_settings.datadir_settings['github']+'/molmass')
sys.path.append(pg_settings.datadir_settings['github']+'/chemioinformatics_utilities')
sys.path.append(pg_settings.datadir_settings['github']+'/io_utilities')
sys.path.append(pg_settings.datadir_settings['github']+'/calculate_utilities')

# initialize the sample information
from SBaaS_LIMS.lims_sample_execute import lims_sample_execute
limssample = lims_sample_execute(session,engine,pg_settings.datadir_settings);
limssample.export_sampleStorage_csv(sample_ids_I=['%'],filename_O = 'sample_storage.csv');

# initialize the experiment
from SBaaS_LIMS.lims_experiment_execute import lims_experiment_execute
limsexperiment = lims_experiment_execute(session,engine,pg_settings.datadir_settings);
limsexperiment.execute_deleteExperiments(['EcoliOptTracer01']);
limsexperiment.execute_makeExperimentFromSampleFile(pg_settings.datadir_settings['workspace_data']+'/_input/150928_Isotopomer_EcoliOptTracer01_sampleFile01.csv',1,[10.0,100.0,1000.0]);
limsexperiment.execute_makeExperimentFromSampleFile(pg_settings.datadir_settings['workspace_data']+'/_input/150928_Isotopomer_EcoliOptTracer01_sampleBiomass01.csv',0,[]);
##correct the acquisition method for 1000.0x samples (glucose only)
#cmd = '''UPDATE experiment
#SET acquisition_method_id='140719_McCloskey2013_13CFlux'
#WHERE id LIKE 'EcoliOptTracer01'
#AND sample_name LIKE '%1000.0x';'''
# export the analyst acquisition batch files
limsexperiment.execute_makeBatchFile('EcoliOptTracer01', '150928',pg_settings.datadir_settings['workspace_data']+ '/_output/150928_Isotopomer_EcoliOptTracer01.txt',experiment_type_I=5);