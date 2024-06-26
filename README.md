# Trace4Harmonization-Docker

## Description

Harmonize numerical values extracted from medical images (e.g. acquired with different models of image-acquisition system)

## Usage

### In production
If the image is production-ready (i.e. it has been built and loaded on the chaimeleon platform), you can run the following commands, for the **training stage**:

```
jobman submit -i trace4harmonization -- -- OPERATION=calibrate WORKDIR=~/persistent-home TRAINING_CALIBRATION_FILENAME=<file_to_be_used_for_harmonization_training>.csv
```
and for the **application stage**:

```
jobman submit -i trace4harmonization -- -- OPERATION=apply WORKDIR=~/persistent-home CLASSIFICATION_APPLY_FILENAME=<file_to_be_harmonized>.csv
```

### During development
For the calibration stage run:

```
jobman submit -- "udocker load -i ~/persistent-home/trace4harmonization-docker.tar.gz trace4harmonization && udcoker run --user=root -t --rm -v /home/chaimeleon/persistent-home:/app/files --env OPERATION=calibrate --env TRAINING_CALIBRATION_FILENAME=<csv_filename_for_calibration_inside_persistend_mount.csv>  trace4harmonization:latest python3 /app/startup.py"
```

For the application stage run:

```
jobman submit -- "udocker load -i ~/persistent-home/trace4harmonization-docker.tar.gz trace4harmonization && udcoker run --user=root -t --rm -v /home/chaimeleon/persistent-home:/app/files --env OPERATION=apply --env TRAINING_CALIBRATION_FILENAME=<csv_filename_for_application_inside_persistend_mount.csv>  trace4harmonization:latest python3 /app/startup.py"
```

### Additional commands

To see the list of the job launched and their status:

```
jobman list
```
 To see the logs of a particular job listed:

```
jobman logs -j <job_id>
```

## Dev info

For building the image put the content of the folder 'for_redistribution_files_only' (you can find it in release attched files) generated by MATLAB inside the app/scripts folder. Then:

```
docker build -t trace4harmonization .
```

To save it:
```
docker run -ti --rm -v </local/path/to/repo/Docker/app/files>:/app/files --env-file ./envfile  --env-file <path/to/aws/credentials>  trace4harmonization python3 /app/startup.py
```

Then upload to the chAImeleon platform as follows:

- After Log-in select "app dashboard" from the menu in the top-right corner
- In the new dashboard opened launch a desktop environment
- Load the compressed docker image by drag and drop pr through the guacamole interface
- Test the application as described in Usage


## LICENSE

The code in the repository is distributed under the AGPL-v3.0 license attached. PLEASE NOTICE that the license refers ONLY TO THE CODE publicly visible here in the repository AND NOT IN ANY WAY to the attached asset files in the release section, that are not generated from code packaging. In particular, the software `Trace4Harmonization.exe`, for which you can find more details here: https://openebench.bsc.es/tool/trace4harmonization, is distributed only with a commercial license and YOU SHOULD CONTACT DeepTrace Technologies s.r.l. for its usage and redistribution.
