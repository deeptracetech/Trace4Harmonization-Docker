import time
from shutil import copyfile, unpack_archive
from datetime import datetime
import os, boto3
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



remote_source_folderpath = os.environ['STORAGE_SOURCE_FOLDERPATH']
remote_dest_folderpath = os.environ['STORAGE_RESULTS_FOLDERPATH']
operation = os.environ['OPERATION']

local_storage_folderpath = '/app/files'

if operation == 'calibration':
    
    source_calibration_fname = os.environ['TRAINING_CALIBRATION_FILENAME']
    local_calibration_fpath = os.path.join(local_storage_folderpath, source_calibration_fname)
    s3 = boto3.client('s3')
    with open(local_calibration_fpath, 'wb') as f:
        s3.download_fileobj(remote_source_folderpath, source_calibration_fname, f)
    run_calibrate(local_calibration_fpath)
    
    # TO DO: aggiungere _calibration a var names e.g. harmonized_calibration_results vd. stessa parte in apply elif
    harmonized_results_fname = f'harmonized_{source_calibration_fname}'
    harmonized_results_fpath = os.path.join(local_storage_folderpath, harmonized_results_fname)
    parameters_fname = 'params.t4r'
    parameters_fpath = os.path.join(local_storage_folderpath, parameters_fname)
 
    remote_results_foldername = f'harmonization_{datetime.now().strftime("%m%d%Y_%H%M%S")}'
    
    remote_results_fname = os.path.join(remote_results_foldername, harmonized_results_fname)
    with open(harmonized_results_fpath, "rb") as f:
        s3.upload_fileobj(f, remote_dest_folderpath, remote_results_fname)

    remote_params_fname = os.path.join(remote_results_foldername, parameters_fname)
    with open(parameters_fpath, "rb") as f:
        s3.upload_fileobj(f, remote_dest_folderpath, remote_params_fname)


elif operation == 'apply':

    source_application_fname = os.environ['CLASSIFICATION_APPLY_FILENAME']
    remote_results_foldername = os.environ['REMOTE_RESULTS_FOLDERNAME'] 

    local_application_fpath = os.path.join(local_storage_folderpath, source_application_fname)
    s3 = boto3.client('s3')
    with open(local_application_fpath, 'wb') as f:
        s3.download_fileobj(remote_source_folderpath, source_application_fname, f)

    remote_params_fname = 'params.t4r'
    remote_params_fpath = os.path.join(remote_results_foldername, remote_params_fname)
    local_params_fpath = os.path.join(local_storage_folderpath, remote_params_fname)
    s3 = boto3.client('s3')
    with open(local_params_fpath, 'wb') as f:
        s3.download_fileobj(remote_dest_folderpath, remote_params_fpath, f)

    run_apply(local_application_fpath, local_params_fpath)

    local_harmonized_apply_results_fname = f'harmonized_{source_application_fname}'
    local_harmonized_apply_results_fpath = os.path.join(local_storage_folderpath, local_harmonized_apply_results_fname)
    remote_harmonized_results_fname = os.path.join(remote_results_foldername, local_harmonized_apply_results_fname)
    with open(local_harmonized_apply_results_fpath, "rb") as f:
        s3.upload_fileobj(f, remote_dest_folderpath, remote_harmonized_results_fname)


else:
    print("Unrecognized operation. Allowed operations are: 'calibration', 'apply'. Terminating.")