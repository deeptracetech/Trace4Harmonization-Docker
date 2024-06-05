import time
from shutil import copyfile, unpack_archive
from datetime import datetime
import os
import subprocess

#python3

def run_calibrate(whole_data_csv_fpath: str):
    start = time.time()
    script_path = f'/app/scripts/run_Trace4Harmonization.sh '
    mat_runtime_path = '/opt/mcr/R2023a '
    script_arg = '-phase calibrate '
    #print("Running", script_path)
    command = script_path + mat_runtime_path + script_arg + whole_data_csv_fpath
    print("command", command)
    #subprocess.run([script_path, mat_runtime_path, script_arg + whole_data_csv_fpath], shell=True)
    os.system(command)
    end = time.time()
    print("elapsed:", (end - start))
    
def run_apply(csv_fpath, parameters_t4r_fpath):
    start = time.time()
    command = f'/app/scripts/run_Trace4Harmonization.sh /opt/mcr/R2023a -phase apply {csv_fpath} {parameters_t4r_fpath}'
    print("command",  command)
    os.system(command)
    end = time.time()
    print("elapsed:",(end-start))



operation = os.environ['OPERATION']
local_files_folderpath = os.environ['WORKDIR'] if 'WORKDIR' in os.environ else '/app/files'



if operation == 'calibrate':
    
    source_calibration_fname = os.environ['TRAINING_CALIBRATION_FILENAME']
    local_calibration_fpath = os.path.join(local_files_folderpath, source_calibration_fname)
    run_calibrate(local_calibration_fpath)
    harmonized_calibration_results_fname = f'harmonized_{source_calibration_fname}'
    parameters_fname = 'params.t4r'


elif operation == 'apply':

    source_application_fname = os.environ['CLASSIFICATION_APPLY_FILENAME']

    local_application_fpath = os.path.join(local_files_folderpath, source_application_fname)

    remote_params_fname = 'params.t4r'
    local_params_fpath = os.path.join(local_files_folderpath, remote_params_fname)

    run_apply(local_application_fpath, local_params_fpath)


else:
    print("Unrecognized operation. Allowed operations are: 'calibrate', 'apply'. Terminating.")