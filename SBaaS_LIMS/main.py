import sys
#sys.path.append('C:/Users/dmccloskey-sbrg/Google Drive/SBaaS_base')
sys.path.append('C:/Users/dmccloskey/Google Drive/SBaaS_base')
from SBaaS_base.postgresql_settings import postgresql_settings
from SBaaS_base.postgresql_orm import postgresql_orm

# read in the settings file
#filename = 'C:/Users/dmccloskey-sbrg/Google Drive/SBaaS_base/settings_1.ini';
#filename = 'C:/Users/dmccloskey/Google Drive/SBaaS_base/settings_2.ini';
filename = 'C:/Users/dmccloskey/Google Drive/SBaaS_base/settings_metabolomics_labtop.ini';
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
sys.path.append(pg_settings.datadir_settings['github']+'/python_statistics')
sys.path.append(pg_settings.datadir_settings['github']+'/r_statistics')
sys.path.append(pg_settings.datadir_settings['github']+'/listDict')
sys.path.append(pg_settings.datadir_settings['github']+'/ddt_python')

##initialize the lims experiment
from SBaaS_LIMS.lims_experiment_execute import lims_experiment_execute
limsexperiment = lims_experiment_execute(session,engine,pg_settings.datadir_settings);
limsexperiment.initialize_supportedTables();

#delete a bad upload
limsexperiment.execute_deleteExperiments(['CfBcontrol01']);

# add in the samples for metabolomics
limsexperiment.execute_makeExperimentFromSampleFile(
    pg_settings.datadir_settings['workspace_data']+'/_input/160120_Quantification_CfBcontrol01_sampleFile01.csv',
    1,
    [10.0]
);

##TODO
##---------------------
##initialize the lims autosamplerMethod for quantitative and isotopomer experiments
#from SBaaS_LIMS.lims_autosamplerMethod_execute import lims_autosamplerMethod_execute
#limsautosampmeth = lims_autosamplerMethod_execute(session,engine,pg_settings.datadir_settings);
#limsautosampmeth.drop_lims_autosamplerMethod();
#limsautosampmeth.initialize_lims_autosamplerMethod();
#limsautosampmeth.reset_lims_autosamplerMethod();
#limsautosampmeth.import_-_add('data/tests/lims/.csv');

##initialize the lims lcMethod for quantitative and isotopomer experiments
#from SBaaS_LIMS.lims_lcMethod_execute import lims_lcMethod_execute
#limslcmeth = lims_lcMethod_execute(session,engine,pg_settings.datadir_settings);
#limslcmeth.drop_lims_lcMethod();
#limslcmeth.initialize_lims_lcMethod();
#limslcmeth.reset_lims_lcMethod();
#limslcmeth.import_calibratorConcentrations_add('data/tests/lims/.csv');

##initialize the lims acquisitionMethod for quantitative and isotopomer experiments
#from SBaaS_LIMS.lims_acquisitionMethod_execute import lims_acquisitionMethod_execute
#limsacquisitionmeth = lims_acquisitionMethod_execute(session,engine,pg_settings.datadir_settings);
#limsacquisitionmeth.drop_lims_acquisitionMethod();
#limsacquisitionmeth.initialize_lims_acquisitionMethod();
#limsacquisitionmeth.reset_lims_acquisitionMethod();
#limsacquisitionmeth.import_calibratorConcentrations_add('data/tests/lims/.csv');
#execute_exportAcqusitionMethod
##---------------------

