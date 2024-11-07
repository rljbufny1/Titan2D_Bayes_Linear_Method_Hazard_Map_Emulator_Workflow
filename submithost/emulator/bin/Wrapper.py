#----------------------------------------------------------------------------------------------------------------------
# Class: Wrapper
# Component of: Titan2D Bayes Linear Method Hazard Map Emulator Workflow
# Purpose: Run a Pegasus workflow
# Author: Renette Jones-Ivey
# Date: Sep 2024
#
# See ./doc/Phm_tut.pdf for function decriptions.
#
# Steps 1, 2, 5, 6, 8, 9, 10 and 15 (Local)
# Steps 3, 4, 7, 11, 12, 13 and 14 (Pegasus)
#
#---------------------------------------------------------------------------------------------------------------------

# References:
# https://github.com/pegasus-isi/pegasus/tree/master/share/pegasus/examples/awsbatch-black-nonsharedfs/blackdiamond.py
# https://pegasus.isi.edu/documentation/python/Pegasus.api.html#module-Pegasus.api.workflow
# https://pegasus.isi.edu/documentation/reference-guide/data-management.html

#########################################################
#########################################################

import datetime
import os
from pathlib import Path
import shutil
import subprocess
import sys
import re
import uuid

from Pegasus.api import *

# Wrapper class
# Called from ipynb
class Wrapper():
    
    def __init__(self, logger, workingdir, bindir, scriptsdir, datadir, examplesdir, workflow_results_directory, num_simulations, maxwalltime):

        self.logger = logger
        self.workingdir = workingdir
        self.bindir = bindir
        self.scriptsdir = scriptsdir
        self.datadir = datadir
        self.examplesdir = examplesdir
        self.workflow_results_directory = workflow_results_directory
        self.num_simulations = num_simulations
        self.maxwalltime = maxwalltime
        
        '''
        print('self.workingdir: ', self.workingdir)
        print('self.bindir: ', self.bindir)
        print('self.scriptsdir: ', self.scriptsdir)
        print('self.datadir: ', self.datadir)
        print('self.examplesdir: ', self.examplesdir)
        print('self.workflow_results_directory: ', self.workflow_results_directory)
        print('self.num_simulations: ', self.num_simulations)
        print('self.maxwalltime: ', self.maxwalltime)
        print('\n')
        '''
        
    def display_output (self, message):
        print (message)
        self.logger.info (message)
                
    def subprocess_popen (self, subprocess_args):
    
        #https://stackoverflow.com/questions/21953835/run-subprocess-and-print-output-to-logging
        #https://stackoverflow.com/questions/5631624/how-to-get-exit-code-when-using-python-subprocess-communicate-method
        subprocess_result = subprocess.Popen(subprocess_args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        #print ('type(subprocess_result): ', type(subprocess_result)) #<class 'subprocess.Popen'>
        subprocess_output, _ =  subprocess_result.communicate() # Wait for and communicate output
        returncode = subprocess_result.returncode
        #print ('type(subprocess_output): ', type(subprocess_output)) #<class 'bytes'>
        #print ("type(returncode): ", type (returncode)) #<class 'int'>
        decoded_string = subprocess_output.decode('utf-8')  # Or the appropriate encoding
        lines = decoded_string.splitlines()
        for line in lines:
            self.logger.info(line)
        return returncode
        
    def initialize_workflow(self, grassgis_database, \
        volcano_lat_utmn, volcano_lon_utme, lat_south, lat_north, lon_west, lon_east, \
        material_model, int_frict_angle, \
        pile_type, orientation_angle, initial_speed, initial_direction, \
        minvol, maxvol, minbed, maxbed, radius,
        memory, subnet, security_group):
        
        self.grassgis_database = grassgis_database

        '''
        print('volcano_lat_utmn: ', volcano_lat_utmn)
        print('volcano_lon_utme: ', volcano_lon_utme)
        print('lat_south: ', lat_south)
        print('lat_north: ', lat_north)
        print('lon_west: ', lon_west)
        print('lon_east: ', lon_east)
        print('self.grassgis_database: ', self.grassgis_database)
        print('material_model: ', material_model)
        print('int_frict_angle: ', int_frict_angle)
        print('pile_type: ', pile_type)
        print('orientation_angle: ', orientation_angle)
        print('initial_speed: ', initial_speed)
        print('initial_direction: ', initial_direction)
        print('minvol: ', minvol)
        print('maxvol: ', maxvol)
        print('minbed: ', minbed)
        print('maxbed: ', maxbed)
        print('memory: ', memory)
        print('subnet: ', subnet)
        print('security_group: ', security_group)
        print ('\n')
        '''
        
        try:

            self.display_output('Initializing the workflow...')
            
            # get input value for input.string(titan2dInputFile).
            # Full pathname of the Titan2D input file
            
            #titan2dInputFile = io.get("input.string(titan2d_inputfile).current")
            #print ('titan2dInputFile: ', titan2dInputFile)

            #Verify that the file exists
            #if os.path.exists(titan2dInputFile) == False:
                #sys.stderr.write("Titan2D input file %s not found.\n" % titan2dInputFile)
                #message = "Emulation error: Titan2D input file %s not found" % titan2dInputFile
                #io.put("output.string(runstate).about.label", value=message)
                #Rappture.result(io)
                #sys.exit(0)
                
            self.display_output("Creating the Titan2D input files...");

            titan2d_simulation_input_file = os.path.join(self.examplesdir, "simulation.py")
            #print ('titan2d_simulation_input_file: ', titan2d_simulation_input_file)
            
            if (os.path.exists(titan2d_simulation_input_file)):
                FH2 = open(titan2d_simulation_input_file, 'r')
                output = FH2.read()
                FH2.close()
                #print (output)
            else:
                self.logger.error ('Wrapper.py initialize_workflow: %s does not exist.' %titan2d_simulation_input_file)
                return False
                    

            # Extract paths.
            # Reference:
            # http://stackoverflow.com/questions/2860153/how-do-i-get-the-parent-directory-in-python
            #titan2dInputFile = titan2d_simulation_input_file
            #titan2dInputFiled = os.path.abspath(os.path.join(titan2dInputFile, os.pardir))
            #titan2dInputFiledd = os.path.abspath(os.path.join(titan2dInputFiled, os.pardir))
            #print("titan2dInputFile: %s " % titan2dInputFile)
            #print("titan2dInputFiled: %s " % titan2dInputFiled)
            #print("titan2dInputFiledd: %s " % titan2dInputFiledd)
            
            titan2dInputFile = titan2d_simulation_input_file
            titan2dInputFiled = self.examplesdir #os.path.abspath(os.path.join(titan2dInputFile, os.pardir))
            titan2dInputFiledd = self.workingdir #os.path.abspath(os.path.join(titan2dInputFiled, os.pardir))
            #log_info("titan2dInputFile: %s " % titan2dInputFile)
            #log_info("titan2dInputFiled: %s " % titan2dInputFiled)
            #log_info("titan2dInputFiledd: %s " % titan2dInputFiledd)

            #########################################################
            #########################################################

            #########################################################
            # Setup the grass directory.
            # Create the runParams.mat input file required for
            # steps 1, 8 and 10
            #########################################################

            # Call runParams.m
            #
            # Input(s): Values from Rappture and simulation.py
            # Output(s): runParams.mat

            run_params_mat_filename = "runParams.mat"
            run_params_mat_filepath = os.path.join(self.workingdir,run_params_mat_filename)
            if (os.path.exists(run_params_mat_filepath) == True):
                os.remove(run_params_mat_filepath)

            script_path = os.path.join(self.bindir, "setup.sh")
            self.logger.info ('Calling %s...' %script_path)
            resamplePointsStr = '1024'
            subprocess_args = [script_path,self.workingdir,self.bindir,self.datadir,\
                             titan2dInputFile,titan2dInputFiled,titan2dInputFiledd,\
                             str(material_model), str(int_frict_angle), \
                             str(pile_type), str(orientation_angle), str(initial_speed), str(initial_direction), \
                             str(minvol),str(maxvol),str(minbed),str(maxbed),
                             str(volcano_lon_utme),str(volcano_lat_utmn),str(radius),\
                             resamplePointsStr,str(self.num_simulations)]
            returncode = self.subprocess_popen(subprocess_args)

            # Verify

            if (os.path.exists(run_params_mat_filepath) == False):
                #sys.stderr.write("%s not generated by setup processing\n" % run_params_mat_filename)
                #sys.stderr.write("The gis_main path in the Titan2d input file is invalid or not resolved\n")
                self.logger.error("Wrapper.py initialize_workflow: %s not generated by setup processing\n" % run_params_mat_filename)
                self.logger.error("Wrapper.py initialize_workflow: the gis_main path in the Titan2d input file is invalid or not resolved\n")
                #io.put("output.string(runstate).about.label", value="Emulation error")
                #Rappture.result(io)
                #sys.exit(1)
                return False
            #else:
                #self.display_output("%s successfully created" % run_params_mat_filename)
            
            # Step 1 - Call Gen_Titan_Input_Samples.m
            #
            # Input(s): runParams.mat
            # Output(s): uncertain_input_list.txt and uncertain_input_list_h.txt

            uncertain_input_list_filename = "uncertain_input_list.txt"
            uncertain_input_list_filepath = os.path.join(self.workingdir,uncertain_input_list_filename)
            if (os.path.exists(uncertain_input_list_filepath) == True):
                os.remove(uncertain_input_list_filepath)

            uncertain_input_list_h_filename = "uncertain_input_list_h.txt"
            uncertain_input_list_h_filepath = os.path.join(self.workingdir,uncertain_input_list_h_filename)
            if (os.path.exists(uncertain_input_list_h_filepath) == True):
                os.remove(uncertain_input_list_h_filepath)

            script_path = os.path.join(self.bindir, "step_1.sh")
            self.logger.info ('Calling %s...' %script_path)
            subprocess_args = [script_path,self.bindir,self.workingdir,str(self.num_simulations)]
            returncode = self.subprocess_popen(subprocess_args)

            # Verify

            if (os.path.exists(uncertain_input_list_filepath) == False):
                #sys.stderr.write("%s not generated by step 1\n" % uncertain_input_list_filename)
                logger.error ("Wrapper.py initialize_workflow: %s not generated by step 1\n" % uncertain_input_list_filename)
                #io.put("output.string(runstate).about.label", value="Emulation error")
                #Rappture.result(io)
                #sys.exit(1)
                return False

            if (os.path.exists(uncertain_input_list_h_filepath) == False):
                #sys.stderr.write("%s not generated by step 1\n" % uncertain_input_list_h_filename)
                logger.error("Wrapper.py initialize_workflow: %s not generated by step 1\n" % uncertain_input_list_h_filename)
                #io.put("output.string(runstate).about.label", value="Emulation error")
                #Rappture.result(io)
                #sys.exit(1)
                return False

            # Run step 2 - Create Titan2D input file for each of the samples
            #
            # Input(s): uncertain_input_list_h.txt
            # Output(s): simulation_<%06d sample number>.py

            script_path = os.path.join(self.bindir, "step_2.sh")
            self.logger.info ('Calling %s...' %script_path)
            
            for i in range (1, self.num_simulations + 1):
                filename = "simulation_%06d.py" %i
                filepath = os.path.join(self.workingdir,filename)
                if (os.path.exists(filepath) == True):
                    os.remove(filepath)

            checkPercent = 10;
            if (self.num_simulations > checkPercent):
                done = 0;
                nextDoneIncrement = self.num_simulations/checkPercent;
                nextDoneCheck = done + nextDoneIncrement;
                nextDonePercent = 0;

            for i in range (1, self.num_simulations + 1):

                if (self.num_simulations > checkPercent):
                    done = done + 1;
                    if (done > nextDoneCheck):
                        nextDoneCheck = done + nextDoneIncrement;
                        nextDonePercent = nextDonePercent + checkPercent;
                        print ("%d percent complete..." % nextDonePercent)
                subprocess_args = [script_path,self.workingdir,titan2dInputFile,str(i)]
                returncode = self.subprocess_popen(subprocess_args)

            # Verify

            filecheck = 0
            for i in range (1, self.num_simulations + 1):
                filename = "simulation_%06d.py" %i
                filepath = os.path.join(self.workingdir,filename)
                if (os.path.exists(filepath) == True):
                    filecheck=filecheck+1
                else:
                    self.logger.error ("file %s not found" % filepath)

            #print ("filecheck: %d" %filecheck)
            if (filecheck != self.num_simulations):
                self.logger.error ("Wrapper.py initialize_workflow: one or more Titan2D input files were not created by step 2\n")
                #sys.exit(1)
                return False
            else:
                self.display_output("Titan2D input files successfully created")
                
                self.display_output("Creating the emulator input files...");
                
                # Steps 5, 8, 9 and 10
                # Create macro_emulator.pwem, macro_resamples.tmp, macro_resample_assemble.inputs,
                # AZ_vol_dir_bed_int.phm and step11_12_13_staged_input.txt

                script_path = os.path.join(self.bindir,"step_5_8_9_10.sh")
                self.logger.info ('Calling %s...' %script_path)
                subprocess_args = [script_path,self.bindir,self.workingdir]
                returncode = self.subprocess_popen(subprocess_args)

                # Step 6 - Call extract_mini_emulator_build_meta_data.m
                #
                # Input(s): macro_emulator.pwem
                # Output(s): build_mini_pwem_meta.<%06d sample number>
                
                script_path = os.path.join(self.bindir,"step_6.sh")
                self.logger.info ('Calling %s...' %script_path)

                # Create build_mini_pwem_meta.<samplenumber - formatted as %06g> for each sample
                for i in range (1, self.num_simulations + 1):
                    subprocess_args = [script_path,self.bindir,self.workingdir,str(i)]
                    returncode = self.subprocess_popen(subprocess_args)

                # Create the list of phm files for Pegasus
                
                # Per legacy code, set the start simplex number to 90.
                # Used by steps 11-13 and 14
                self.simplexStart = 90
                
                step11_12_13_staged_input_filename = "step11_12_13_staged_input.txt"
                step11_12_13_staged_input_filepath = os.path.join(self.workingdir,step11_12_13_staged_input_filename)

                f = open(step11_12_13_staged_input_filepath, "r")

                # Get the filenames into array
                
                # phm* file names
                self.phm_filenames = []

                self.numSimplices = 0
                for line in f:
                    self.numSimplices+=1
                    if (line == "0\n"):
                        filename = "0"
                    else:
                        simplexNumber, simplexKey = line.split(".",1)
                        filename = "phm_from_eval_%d.%08d.%d" % (int(simplexNumber), int(simplexKey), 1)
                    self.phm_filenames.append(filename)
                    
                f.close

                # Use numSamples number of processors for this

                numSimplicesTruncated = self.numSimplices-(self.simplexStart-1)
                self.logger.info ("numSimplicesTruncated: %d " % numSimplicesTruncated)
                
                if (numSimplicesTruncated <= 0):
                    self.logger.error("Wrapper.py initialize_workflow: steps 11-13: Not enough simplices to continue. Verify the number of erupt simulations.\n")
                    return False


                # //: divide with integral results (discard remainder)
                # %: modulus
                self.numSimplicesPerProcessor = numSimplicesTruncated//self.num_simulations
                self.numSimplicesRemaining = numSimplicesTruncated%self.num_simulations

                self.logger.info ("self.simplexStart: %d " % self.simplexStart)
                self.logger.info ("self.numSimplices: %d " % self.numSimplices)
                #print ("self.numSimplicesPerProcessor: %d " % self.numSimplicesPerProcessor)
                #print ("self.numSimplicesRemaining: %d " % self.numSimplicesRemaining)
                #print ("len(self.phm_filenames): " + str(len(self.phm_filenames)))
                #print ("self.phm_filenames: " + str(self.phm_filenames))
                count = 0
                for i in range (len(self.phm_filenames)):
                    if (self.phm_filenames[i] != "0"):
                        count = count + 1
                self.logger.info ("self.phm_filenames count of nonzero files: %d" % count)
                
                self.display_output("Emulator input files successfully created")

                # Update pegasus aws batch configuration files based on user selected parameters.
                script_path = os.path.join(self.scriptsdir,"pegasus-aws-batch-configure.sh")
                self.logger.info ('Calling %s...' %script_path)
                subprocess_args = [script_path,str(memory),subnet,security_group]
                returncode = self.subprocess_popen(subprocess_args)

                sys.stdout.flush()
                return True
            
        except Exception as e:
            
            self.logger.error ('Wrapper.py initialize_workflow: Exception: %s\n' %str(e))
            return False

    def run_workflow(self, aws_region, aws_iam_username):

        try:

            self.display_output('Configuring the workflow...')
            self.logger.info('aws_region: %s' %aws_region)
            self.logger.info('iam_username: %s' %aws_iam_username)
            
            #########################################################
            # Create environment variables
            #########################################################

            # Create the TOPDIR, PEGASUS_LOCAL_BIN_DIR, S3_URL_PREFIX, S3_BUCKET, and S3_BUCKET_KEY
            # environment variables for ./conf/sites.xml.
            
            TOPDIR = os.getcwd()
            os.environ['TOPDIR'] = TOPDIR
            self.logger.info("os.environ['TOPDIR']: %s" %str(os.environ['TOPDIR']))
            
            #BIN_DIR=`pegasus-config --bin`
            #echo "BIN_DIR: "$BIN_DIR
            #PEGASUS_LOCAL_BIN_DIR=${BIN_DIR}
            #export PEGASUS_LOCAL_BIN_DIR
            PEGASUS_LOCAL_BIN_DIR = '/usr/bin'
            os.environ['PEGASUS_LOCAL_BIN_DIR'] = PEGASUS_LOCAL_BIN_DIR
            self.logger.info("os.environ['PEGASUS_LOCAL_BIN_DIR']: %s" %str(os.environ['PEGASUS_LOCAL_BIN_DIR']))
            
            S3_URL_PREFIX = 's3://user@amazon'
            os.environ['S3_URL_PREFIX'] = S3_URL_PREFIX
            self.logger.info("os.environ['S3_URL_PREFIX']: %s" %str(os.environ['S3_URL_PREFIX']))
            
            # ./pegasusrc sets pegasus.catalog.site.file=./conf/sites.xml.
            # ./conf/sites.xml aws-batch site's file server definition sets url to "${S3_URL_PREFIX}/${S3_BUCKET}/${S3_BUCKET_KEY}"
            # The globally unique S3_BUCKET is created by Pegasus (if it does not already exist), for the current Amazon AWS Partition and IAM user.
            # See https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html for more information on bucket naming rules.
            bucket_name_suffix = re.sub(r'[^a-zA-Z0-9]+', '', str(aws_region + aws_iam_username)).lower()[:63]
            S3_BUCKET = 'titan2d-blm-emulator-%s' %bucket_name_suffix
            #print ('S3_BUCKET: ', S3_BUCKET)
            os.environ['S3_BUCKET'] = S3_BUCKET
            self.logger.info("os.environ['S3_BUCKET']: %s" %str(os.environ['S3_BUCKET']))
            # The S3_BUCKET_KEY (i.e. directory) is created for each workflow run and deleted after each workflow run.
            S3_BUCKET_KEY = 'pegasus-workflow'
            #print ('S3_BUCKET_KEY: ', S3_BUCKET_KEY)
            os.environ['S3_BUCKET_KEY'] = S3_BUCKET_KEY
            self.logger.info("os.environ['S3_BUCKET_KEY']: %s" %str(os.environ['S3_BUCKET_KEY']))
    
            #########################################################
            # Path to the titan and octave launch scripts
            #########################################################

            # Create the Pegasus workflow
            wf = Workflow('emulatorworkflow')
            tc = TransformationCatalog()
            wf.add_transformation_catalog(tc)
            rc = ReplicaCatalog()
            wf.add_replica_catalog(rc)
            
            # Add titan launch script and input files to the DAX-level transformation catalog
                
            titanlaunch = Transformation(
                'titanlaunch',
                site='local',
                pfn=os.path.join(self.workingdir,'remotebin','titanLaunch.sh'),
                is_stageable = True, #Stageable or installed
                arch=Arch.X86_64,
                os_type=OS.LINUX)\
            .add_profiles(Namespace.PEGASUS, key="clusters_size", value=self.num_simulations) \
            .add_profiles(Namespace.PEGASUS, key="clusters_num", value=self.num_simulations)
            tc.add_transformations(titanlaunch)
            
            octavelaunch = Transformation(
                'octavelaunch',
                site='local',
                pfn=os.path.join(self.workingdir,'remotebin','octaveLaunch.sh'),
                is_stageable = True, #Stageable or installed
                arch=Arch.X86_64,
                os_type=OS.LINUX)\
            .add_profiles(Namespace.PEGASUS, key="clusters_size", value=self.num_simulations) \
            .add_profiles(Namespace.PEGASUS, key="clusters_num", value=self.num_simulations)
            tc.add_transformations(octavelaunch)

            #########################################################
            #########################################################

            # PFNs:

            # All files in a Pegasus workflow are referred to in the DAX using their Logical File Name (LFN).
            # These LFNs are mapped to Physical File Names (PFNs) when Pegasus plans the workflow.
            # Add input files to the DAX-level replica catalog

            # Grass database
            grassgis_database_zipped = self.grassgis_database+'.tar.gz'
            self.logger.info ('grassgis_database_zipped: %s' %grassgis_database_zipped)
            # titanlaunch script unzips before titan is invoked
            rc.add_replica("local", File(grassgis_database_zipped), os.path.join(self.workingdir, grassgis_database_zipped))
            
            # Octave scripts
            rc.add_replica("local", File('down_sample_pileheightrecord.m'), os.path.join(self.bindir, 'down_sample_pileheightrecord.m'))
            rc.add_replica("local", File('r_down_sample_pileheightrecord.m'), os.path.join(self.bindir, 'r_down_sample_pileheightrecord.m'))
            rc.add_replica("local", File('r_build_mini_emulator.m'), os.path.join(self.bindir, 'r_build_mini_emulator.m'))
            rc.add_replica("local", File('build_mini_emulator.m'), os.path.join(self.bindir, 'build_mini_emulator.m'))
            rc.add_replica("local", File('r_script11_12_13.m'), os.path.join(self.bindir, 'r_script11_12_13.m'))
            rc.add_replica("local", File('script11_12_13.m'), os.path.join(self.bindir, 'script11_12_13.m'))
            rc.add_replica("local", File('extract_macrosimplex_resample_inputs_P.m'), os.path.join(self.bindir, 'extract_macrosimplex_resample_inputs_P.m'))
            rc.add_replica("local", File('evaluate_mini_emulator_mean.m'), os.path.join(self.bindir, 'evaluate_mini_emulator_mean.m'))
            rc.add_replica("local", File('assemble_minis_to_macro_to_phm_P.m'), os.path.join(self.bindir, 'assemble_minis_to_macro_to_phm_P.m'))
            rc.add_replica("local", File('r_script14.m'), os.path.join(self.bindir, 'r_script14.m'))
            rc.add_replica("local", File('script14.m'), os.path.join(self.bindir, 'script14.m'))
            rc.add_replica("local", File('merge_probability_of_hazard_maps.m'), os.path.join(self.bindir, 'merge_probability_of_hazard_maps.m'))
            
            # Files generated by emulator.ipynb
            rc.add_replica("local", File('uncertain_input_list.txt'), os.path.join(self.workingdir, 'uncertain_input_list.txt'))
            rc.add_replica("local", File('macro_emulator.pwem'), os.path.join(self.workingdir, 'macro_emulator.pwem'))
            rc.add_replica("local", File('macro_resample_assemble.inputs'), os.path.join(self.workingdir, 'macro_resample_assemble.inputs'))
            rc.add_replica("local", File('AZ_vol_dir_bed_int.phm'), os.path.join(self.workingdir, 'AZ_vol_dir_bed_int.phm'))
            rc.add_replica("local", File('step11_12_13_staged_input.txt'), os.path.join(self.workingdir, 'step11_12_13_staged_input.txt'))
            
            for i in range (1, self.num_simulations + 1):
            
                rc.add_replica("local", File('simulation_%06d.py' % i), os.path.join(self.workingdir, 'simulation_%06d.py' % i))
                rc.add_replica("local", File('build_mini_pwem_meta.%06d' % i), os.path.join(self.workingdir, 'build_mini_pwem_meta.%06d' % i))
                
            # Add jobs
            
            step_4_jobs = []
            
            for i in range (1, self.num_simulations + 1):
                
                # Step 3 - Call titan
                #
                # Input(s): simulation.py for the sample
                # Output(s): pileheightrecord.<%06d sample number>
            
                titanjob  = Job(titanlaunch)\
                    .add_args("""-nt 1 simulation_%06d.py""" % i)\
                    .add_inputs(File(grassgis_database_zipped))\
                    .add_inputs(File('simulation_%06d.py' % i))\
                    .add_outputs(File('pileheightrecord.%06d' % i), stage_out=False)\
                    .set_stdout(File('titan2d_%06d.stdout' % i), stage_out=True)\
                    .set_stderr(File('titan2d_%06d.stderr' % i), stage_out=True)\
                    .add_metadata(time="%d" %self.maxwalltime)
                if i==1:
                    titanjob.add_outputs(File('elevation.grid'), stage_out=True)
                
                wf.add_jobs(titanjob)
                
                # Step 4 - Call down_sample_pileheightrecord.m
                #
                # Input(s): uncertain_input_list.txt, pileheightrecord.<%06d sample number>
                # Output(s): down_sampled_data.<%06d sample number>
                #

                octavejob = Job(octavelaunch)\
                    .add_args("""r_down_sample_pileheightrecord.m %s %d""" % (".", i))\
                    .add_inputs(File('r_down_sample_pileheightrecord.m'))\
                    .add_inputs(File('down_sample_pileheightrecord.m'))\
                    .add_inputs(File('uncertain_input_list.txt'))\
                    .add_inputs(File('pileheightrecord.%06d' % i))\
                    .add_outputs(File('down_sampled_data.%06d' % i), stage_out=False)\
                    .add_metadata(time="%d" %self.maxwalltime)
                    
                wf.add_jobs(octavejob)
                
                wf.add_dependency(octavejob, parents=[titanjob])
                
                step_4_jobs.append(octavejob)
                
            # Step 7 - Call build_mini_emulator.m
            #
            # Inputs(s): down_sampled_data.<%06d sample number> files, build_mini_pwem_meta.<%06d sample number>
            # Output(s):  mini_emulator.<%06d sample number>

            step_7_jobs = []
            
            for i in range (1, self.num_simulations + 1):
            
                octavejob = Job(octavelaunch)\
                    .add_args("""r_build_mini_emulator.m %s %d""" % (".", i))\
                    .add_inputs(File('r_build_mini_emulator.m'))\
                    .add_inputs(File('build_mini_emulator.m'))\
                    .add_inputs(File('build_mini_pwem_meta.%06d' % i))\
                    .add_outputs(File('mini_emulator.%06d' % i), stage_out=False)\
                    .add_metadata(time="%d" %self.maxwalltime)
                    
                for j in range (1, self.num_simulations + 1):
                    octavejob.add_inputs(File('down_sampled_data.%06d' % j))\
                    
                wf.add_jobs(octavejob)
                
                # Needs all step 4 jobs to be complete
                wf.add_dependency(octavejob, parents=step_4_jobs)
                
                step_7_jobs.append(octavejob)

            i=self.simplexStart
            remaining = self.numSimplicesRemaining

            # Steps 11-13 - Call script11_12_13.m
            #
            # Input(s): step11_12_13_staged_input.txt, macro_emulator.pwem,
            #   macro_resample_assemble.inputs, AZ_vol_dir_bed_int.phm,
            #   mini_emulator.<%06d sample number> files
            # Output(s): phm_from_eval* files
            
            step_11_12_13_jobs = []
            
            count = 0
            while (i < self.numSimplices):

                begin=i
                if (remaining > 0):
                    end = begin + self.numSimplicesPerProcessor
                    remaining = remaining - 1
                else:
                    end = begin + self.numSimplicesPerProcessor - 1

                octavejob = Job(octavelaunch)\
                    .add_args("""r_script11_12_13.m %s %d %d""" % (".", begin, end))\
                    .add_inputs(File('r_script11_12_13.m'))\
                    .add_inputs(File('script11_12_13.m'))\
                    .add_inputs(File('extract_macrosimplex_resample_inputs_P.m'))\
                    .add_inputs(File('evaluate_mini_emulator_mean.m'))\
                    .add_inputs(File('assemble_minis_to_macro_to_phm_P.m'))\
                    .add_inputs(File('macro_emulator.pwem'))\
                    .add_inputs(File('macro_resample_assemble.inputs'))\
                    .add_inputs(File('AZ_vol_dir_bed_int.phm'))\
                    .add_inputs(File('step11_12_13_staged_input.txt'))\
                    .add_metadata(time="%d" %self.maxwalltime)
                    
                for j in range (1, self.num_simulations + 1):
                    octavejob.add_inputs(File('mini_emulator.%06d' % j))\

                for j in range (begin, end + 1):
                    # phm filenames are 0 or phm_*
                    if (self.phm_filenames[j-1] != "0"):
                        phm_filename = self.phm_filenames[j-1]
                        octavejob.add_outputs(File(phm_filename), stage_out=False)

                count = count + 1
                wf.add_jobs(octavejob)
                
                # Needs all step 7 jobs to be complete
                wf.add_dependency(octavejob, parents=step_7_jobs)
                
                step_11_12_13_jobs.append(octavejob)
                
                i=end+1
             
            self.logger.info ("Number of r_script11_12_13.m jobs added: %d" % count)
            
            # Step 14 - Call script14.m
            #
            # Input(s): AZ_vol_dir_bed_int.phm, phm_from_eval* files
            # Output(s): AZ_vol_dir_bed_int_final.phm
    
            octavejob = Job(octavelaunch)\
                .add_args("""r_script14.m %s""" % ("."))\
                .add_inputs(File('r_script14.m'))\
                .add_inputs(File('script14.m'))\
                .add_inputs(File('merge_probability_of_hazard_maps.m'))\
                .add_inputs(File('AZ_vol_dir_bed_int.phm'))\
                .add_metadata(time="%d" %self.maxwalltime)
                
            for i in range (self.simplexStart, len(self.phm_filenames)):
                # Filenames are 0 or phm_*
                if (self.phm_filenames[i] != "0"):
                    #print ('phm_filenames[%d]: %s'  %(i, self.phm_filenames[i]))
                    phm_filename = self.phm_filenames[i]
                    octavejob.add_inputs(File(phm_filename))
            octavejob.add_outputs(File('AZ_vol_dir_bed_int_final.phm'), stage_out=True)
            
            wf.add_jobs(octavejob)
                
            #Needs all step_11_12_13 jobs to be complete
            wf.add_dependency(octavejob, parents=step_11_12_13_jobs)
            
            # Create the DAX file
            try:
                wf.write()
                wf.graph(include_files=True, label='xform-id', output=os.path.join(self.workflow_results_directory, 'graph.png'))
            except PegasusClientError as e:
                self.logger.error('Wrapper.py run_workflow: PegasusClientError Exception: %s\n' %str(e))
                return False

            utcnow = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
            prefix = 'remotehost-' + utcnow
            self.logger.info ('prefix: %s' %prefix)
                
            try:

                script_path = os.path.join(self.scriptsdir,"pegasus-aws-batch-create.sh")
                self.logger.info ('Calling %s...' %script_path)
                subprocess_args = [script_path,self.workingdir,prefix]
                returncode = self.subprocess_popen(subprocess_args)

                if returncode == 0:
                
                    self.display_output ('Planning the workflow...')
                    wf.plan(conf='./pegasusrc',\
                            cluster = ['horizontal'],\
                            sites = ['aws-batch'],\
                            output_sites = ['local'],\
                            dir = './dags',\
                            force = True,\
                            submit = False)

                    submit_dir = wf.braindump.submit_dir
                    self.logger.info ('submit_dir: %s' %str(submit_dir))

                    if os.path.exists(submit_dir):
                    
                        #'''
                        self.display_output ('Running for the workflow...')
                        wf.run()
                        self.logger.info ('wf.run_output: %s\n' %str(wf.run_output))
                    
                        self.display_output ('Waiting for the workflow to complete...')
                        wf.wait()
                        #'''
                        
                        script_path = os.path.join(self.scriptsdir,"pegasus-analyzer.sh")
                        self.logger.info ('Calling %s...' %script_path)
                        subprocess_args = [script_path,self.workflow_results_directory,submit_dir]
                        returncode = self.subprocess_popen(subprocess_args)
                        if returncode != 0:
                            self.logger.warning ('pegasus-analyzer.sh returned nonzero returncode: %s' %str(returncode))

                        script_path = os.path.join(self.scriptsdir,"pegasus-statistics.sh")
                        self.logger.info ('Calling %s...' %script_path)
                        subprocess_args = [script_path,self.workflow_results_directory,submit_dir]
                        returncode = self.subprocess_popen(subprocess_args)
                        if returncode != 0:
                            self.logger.warning ('pegasus-statistics.sh returned nonzero returncode: %s' %str(returncode))

                        # Clean up
                        
                        self.display_output("Cleanup...")

                        for i in range (1, 5):
                            filename = "elevation%d.tif" %i
                            filepath = os.path.join(self.workingdir,filename)
                            if (os.path.exists(filepath) == True):
                                os.remove(filepath)
                                
                        for i in range (1, self.num_simulations + 1):
                            filename = "build_mini_pwem_meta.%06d" %i
                            filepath = os.path.join(self.workingdir,filename)
                            if (os.path.exists(filepath) == True):
                                os.remove(filepath)
                                
                            filename = "simulation_%06d.py" %i
                            filepath = os.path.join(self.workingdir,filename)
                            if (os.path.exists(filepath) == True):
                                os.remove(filepath)
                        
                        script_path = os.path.join(self.scriptsdir,"pegasus-s3-rm.sh")
                        self.logger.info ('Calling %s...' %script_path)
                        subprocess_args = [script_path,S3_URL_PREFIX,S3_BUCKET,S3_BUCKET_KEY]
                        returncode = self.subprocess_popen(subprocess_args)
                        if returncode != 0:
                            self.logger.warning ('pegasus-s3-rm.sh returned nonzero returncode: %s' %str(returncode))
        
                        script_path = os.path.join(self.scriptsdir,"pegasus-aws-batch-delete.sh")
                        self.logger.info ('Calling %s...' %script_path)
                        subprocess_args = [script_path,self.workingdir,prefix]
                        returncode = self.subprocess_popen(subprocess_args)
                        if returncode != 0:
                            self.logger.warning ('pegasus-aws-batch-delete.sh returned nonzero exitCode: %s' %str(exitCode))

                        shutil.rmtree(submit_dir)
                        return True
                        
                    else:
                        self.logger.error ('Wrapper.py run_workflow: Pegasus submit directory %s not created' %submit_dir)
                        return False
                
                else:
                    self.logger.error ('Wrapper.py run_workflow: pegasus-aws-batch-create.sh returned nonzero returncode: %s' %str(returncode))
                    return False
                
            except PegasusClientError as e:
            
                self.logger.error ('Wrapper.py run_workflow: PegasusClientError Exception: %s\n' %str(e))
                return False
                
        except Exception as e:
            
            self.logger.error ('Wrapper.py run_workflow: Exception: %s\n' %str(e))
            return False
 
