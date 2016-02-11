import sys
sys.path.append('C:/Users/dmccloskey-sbrg/Google Drive/SBaaS_base')
#sys.path.append('C:/Users/dmccloskey/Google Drive/SBaaS_base')
from SBaaS_base.postgresql_settings import postgresql_settings
from SBaaS_base.postgresql_orm import postgresql_orm

# read in the settings file
filename = 'C:/Users/dmccloskey-sbrg/Google Drive/SBaaS_base/settings_1.ini';
#filename = 'C:/Users/dmccloskey/Google Drive/SBaaS_base/settings_2.ini';
#filename = 'C:/Users/dmccloskey-sbrg/Google Drive/SBaaS_base/settings_metabolomics.ini';
pg_settings = postgresql_settings(filename);

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

#initialize the lims msMethod for quantitative and isotopomer experiments
from SBaaS_LIMS.lims_msMethod_execute import lims_msMethod_execute
limsmsmeth = lims_msMethod_execute(session,engine,pg_settings.datadir_settings);
limsmsmeth.drop_lims_msMethod();
limsmsmeth.initialize_lims_msMethod();
limsmsmeth.reset_lims_msMethod();
limsmsmeth.import_MSComponents_add('data/tests/lims/150902_ms_components.csv');
limsmsmeth.import_MSComponentList_add('data/tests/lims/150902_ms_component_list.csv');
limsmsmeth.import_MSMethod_add('data/tests/lims/150902_ms_method.csv');
#TODO: make import and add methods
limsmsmeth.import_MSSourceParameters_add('data/tests/lims/150902_ms_sourceparameters.csv');
limsmsmeth.import_MSInformation_add('data/tests/lims/150902_ms_information.csv');