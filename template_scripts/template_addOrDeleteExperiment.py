import sys
sys.path.append('C:/Users/dmccloskey-sbrg/Google Drive/SBaaS_base')
from SBaaS_base.postgresql_settings import postgresql_settings
from SBaaS_base.postgresql_orm import postgresql_orm

# read in the settings file
filename = 'C:/Users/dmccloskey-sbrg/Google Drive/SBaaS_base/settings.ini';
pg_settings = postgresql_settings(filename);

# connect to the database from the settings file
pg_orm = postgresql_orm();
pg_orm.set_sessionFromSettings(pg_settings.database_settings);
session = pg_orm.get_session();
engine = pg_orm.get_engine();

# your app...
sys.path.append('C:/Users/dmccloskey-sbrg/Google Drive/SBaaS_LIMS')
sys.path.append('C:/Users/dmccloskey-sbrg/Documents/GitHub/io_utilities')
sys.path.append('C:/Users/dmccloskey-sbrg/Documents/GitHub/calculate_utilities')

# initialize the experiment
from SBaaS_LIMS.lims_experiment_execute import lims_experiment_execute
limsexperiment = lims_experiment_execute(session,engine,pg_settings.datadir_settings);
limsexperiment.drop_lims_experimentTypes();
limsexperiment.initialize_lims_experimentTypes();
limsexperiment.reset_lims_experimentTypes();
limsexperiment.drop_lims_experiment();
limsexperiment.initialize_lims_experiment();
limsexperiment.reset_lims_experiment('chemoCLim01');
limsexperiment.execute_deleteExperiments(['chemoCLim01']);
limsexperiment.execute_makeExperimentFromSampleFile('data/tests/analysis_quantification/150727_Quantification_chemoCLim01_sampleFile01.csv',1,[10.0]);
limsexperiment.execute_makeExperimentFromCalibrationFile('data/tests/analysis_quantification/150805_Quantification_chemoCLim01_calibrationFile01.csv');
# export the analyst acquisition batch files
limsexperiment.execute_makeBatchFile('chemoCLim01', '150805','data/tests/analysis_quantification/150727_Quantification_chemoCLim01.txt',experiment_type_I=4);