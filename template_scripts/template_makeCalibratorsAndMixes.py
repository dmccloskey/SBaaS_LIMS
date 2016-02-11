import sys
sys.path.append('C:/Users/dmccloskey-sbrg/Google Drive/SBaaS_base')
from SBaaS_base.postgresql_settings import postgresql_settings
from SBaaS_base.postgresql_orm import postgresql_orm

# read in the settings file
filename = 'C:/Users/dmccloskey-sbrg/Google Drive/SBaaS_base/settings.ini';
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

#initialize the lims calibrators for quantitative experiments
from SBaaS_LIMS.lims_calibratorsAndMixes_execute import lims_calibratorsAndMixes_execute
limscalandmix = lims_calibratorsAndMixes_execute(session,engine,pg_settings.datadir_settings);
limscalandmix.drop_lims_calibratorsAndMixes();
limscalandmix.initialize_lims_calibratorsAndMixes();
limscalandmix.reset_lims_calibratorsAndMixes();
limscalandmix.import_calibratorConcentrations_add('data/tests/analysis_quantification/140827_calibratorConcentrations.csv');
#limscalandmix.export_calibratorConcentrations_csv('data/tests/analysis_quantification/140827_calibratorConcentrations_check.csv');