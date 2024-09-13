##!/usr/bin/env python3

#----------------------------------------------------------------------------------------------------------------------
# Class: Wrapper
# Component of: Titan2D Bayes Linear Method Hazard Map Emulator Workflow
# Purpose: Run a Pegasus workflow
# Author: Renette Jones-Ivey
# Date: Dec 2023
#---------------------------------------------------------------------------------------------------------------------

# References:
# https://github.com/pegasus-isi/pegasus/tree/master/share/pegasus/examples/awsbatch-black-nonsharedfs/blackdiamond.py
# https://pegasus.isi.edu/documentation/python/Pegasus.api.html#module-Pegasus.api.workflow
# https://pegasus.isi.edu/documentation/reference-guide/data-management.html

# Note all output is directed to the dax file so cannot have any print statements except for if an exception occurs.

import datetime
import os
from pathlib import Path
import shutil
import subprocess
import sys

#print (sys.path)

#from Pegasus.DAX3 import *
#/usr/lib64/python3.6/site-packages/Pegasus/DAX3.py:165: DeprecationWarning: Pegasus.DAX3 API has been deprecated and will be removed in v5.1.0. Please use the new API released in v5.0.0.
  #DeprecationWarning,
  
from Pegasus.api import *

#import ND_Kriging_Sinkhorn_Probabilities
import DEM

import logging
logging.basicConfig(level=logging.WARNING)

# Wrapper class
# Called from ipynb
class Wrapper():
    
    #def __init__(self,\
           #parent, self_workingdir, self_bindir, self_scriptsdir, grassgis_database, grassgis_location, grassgis_mapset, grassgis_map, \
           #numsamples, simplexStart, numSimplices, numSimplicesPerProcessor, numSimplicesRemaining, phm_filenames, maxwalltime):
    def __init__(self, self_workingdir, self_bindir, self_scriptsdir, self_datadir, self_examplesdir, eruptsimulations, maxwalltime):

        self.workingdir = self_workingdir
        self.bindir = self_bindir
        self.scriptsdir = self_scriptsdir
        self.datadir = self_datadir
        self.examplesdir = self_examplesdir
        self.eruptsimulations = eruptsimulations
        '''
        self.simplexStart = simplexStart
        self.numSimplices = numSimplices
        self.numSimplicesPerProcessor = numSimplicesPerProcessor
        self.numSimplicesRemaining = numSimplicesRemaining
        self.phm_filenames = phm_filenames
        '''
        self.maxwalltime = maxwalltime
    
        print('self.workingdir: ', self.workingdir)
        print('self.bindir: ', self.bindir)
        print('self.scriptsdir: ', self.scriptsdir)
        print('self.datadir: ', self.datadir)
        print('self.examplesdir: ', self.examplesdir)
        print('self.eruptsimulations: ', self.eruptsimulations)
        '''
        print('self.simplexStart: ', self.simplexStart)
        print('self.numSimplices: ', self.numSimplices)
        print('self.numSimplicesPerProcessor: ', self.numSimplicesPerProcessor)
        print('self.numSimplicesRemaining: ', self.numSimplicesRemaining)
        print('len(self.phm_filenames): ', len(self.phm_filenames))
        #print('self.phm_filenames: ', str(self.phm_filenames))
        '''
        print('self.maxwalltime: ', self.maxwalltime)
        print('\n')
        
        #self.run()
        
    def initialize_workflow(self, volcano_lat_decimal_degrees, volcano_lon_decimal_degrees, \
        volcano_lat_utmn, volcano_lon_utme, \
        lat_south, lat_north, lon_west, lon_east, \
        grassgis_database, grassgis_location, grassgis_mapset, grassgis_map, \
        eruptminvol, eruptmaxvol, eruptminbed, eruptmaxbed, eruptradius):

        self.volcano_lat_decimal_degrees = volcano_lat_decimal_degrees
        self.volcano_lon_decimal_degrees = volcano_lon_decimal_degrees
        self.volcano_lat_utmn = volcano_lat_utmn
        self.volcano_lon_utme = volcano_lon_utme
        self.lat_south = lat_south
        self.lat_north = lat_north
        self.lon_west = lon_west
        self.lon_east = lon_east
        self.grassgis_database = grassgis_database
        self.grassgis_location = grassgis_location
        self.grassgis_mapset = grassgis_mapset
        self.grassgis_map = grassgis_map
        self.eruptminvol = eruptminvol
        self.eruptmaxvol = eruptmaxvol
        self.eruptminbed = eruptminbed
        self.eruptmaxbed = eruptmaxbed
        self.eruptradius = eruptradius
        
        print('self.volcano_lat_decimal_degrees: ', self.volcano_lat_decimal_degrees)
        print('self.volcano_lon_decimal_degrees: ', self.volcano_lon_decimal_degrees)
        print('self.volcano_lat_utmn: ', self.volcano_lat_utmn)
        print('self.volcano_lon_utme: ', self.volcano_lon_utme)
        print('self.lat_south: ', self.lat_south)
        print('self.lat_north: ', self.lat_north)
        print('self.lon_west: ', self.lon_west)
        print('self.lon_east: ', self.lon_east)
        print('self.grassgis_database: ', self.grassgis_database)
        print('self.grassgis_location ', self.grassgis_location)
        print('self.grassgis_mapset: ', self.grassgis_mapset)
        print('self.grassgis_map: ', self.grassgis_map)
        print('self.eruptminvol: ', self.eruptminvol)
        print('self.eruptmaxvol: ', self.eruptmaxvol)
        print('self.eruptminbed: ', self.eruptminbed)
        print('self.eruptmaxbed: ', self.eruptmaxbed)
        print('self.eruptradius: ', self.eruptradius)

        global simplexStart
        global numSimplices
        global numSimplicesPerProcessor
        global numSimplicesRemaining
        global phm_filenames
        
        try:
            # Create the GIS GRASS Database
            print("\nCreating GIS GRASS Database...");

            #'''
            DEM.get_DEM(self.workingdir, self.volcano_lat_decimal_degrees, self.volcano_lon_decimal_degrees, \
                        self.lat_south, self.lat_north, self.lon_west, self.lon_east, \
                        self.grassgis_database, self.grassgis_location, self.grassgis_mapset, self.grassgis_map)
            #'''

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
                
            titan2d_simulation_input_file = os.path.join(self.examplesdir, "simulation.py")
            print ('titan2d_simulation_input_file: ', titan2d_simulation_input_file)
            
            if (os.path.exists(titan2d_simulation_input_file)):
                FH2 = open(titan2d_simulation_input_file, 'r')
                output = FH2.read()
                FH2.close()
                #print (output)
            else:
                print ('%s does not exist.' %titan2d_simulation_input_file)
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

            #setup_path = os.path.join(srcdir,"setup.sh")
            #subprocess.call([setup_path,workingdir,srcdir,datadir,\
                             #titan2dInputFile,titan2dInputFiled,titan2dInputFiledd,\
                             #minvolStr,maxvolStr,BEDMINStr,BEDMAXStr,
                             #STARTUTMECENStr,STARTUTMNCENStr,STARTRADIUSMAXStr,\
                             #resamplePointsStr,numSamplesStr])
            setup_path = os.path.join(self.bindir,"setup.sh")
            resamplePointsStr = '1024'
            subprocess.call([setup_path,self.workingdir,self.bindir,self.datadir,\
                             titan2dInputFile,titan2dInputFiled,titan2dInputFiledd,\
                             str(self.eruptminvol),str(self.eruptmaxvol),str(self.eruptminbed),str(self.eruptmaxbed),
                             str(self.volcano_lon_utme),str(self.volcano_lat_utmn),str(self.eruptradius),\
                             resamplePointsStr,str(self.eruptsimulations)])
            
            # Verify

            if (os.path.exists(run_params_mat_filepath) == False):
                #sys.stderr.write("%s not generated by setup processing\n" % run_params_mat_filename)
                #sys.stderr.write("The gis_main path in the Titan2d input file is invalid or not resolved\n")
                print("%s not generated by setup processing\n" % run_params_mat_filename)
                print("The gis_main path in the Titan2d input file is invalid or not resolved\n")
                #io.put("output.string(runstate).about.label", value="Emulation error")
                #Rappture.result(io)
                #sys.exit(1)
                return False
            else:
                print("\n%s successfully created\n" % run_params_mat_filename)
            
            #########################################################
            # Steps 1 and 2
            #########################################################

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

            step_1_path = os.path.join(self.bindir,"step_1.sh")
            subprocess.call([step_1_path,self.bindir,self.workingdir,str(self.eruptsimulations)])

            # Verify

            if (os.path.exists(uncertain_input_list_filepath) == False):
                #sys.stderr.write("%s not generated by step 1\n" % uncertain_input_list_filename)
                print("%s not generated by step 1\n" % uncertain_input_list_filename)
                #io.put("output.string(runstate).about.label", value="Emulation error")
                #Rappture.result(io)
                #sys.exit(1)
                return False

            if (os.path.exists(uncertain_input_list_h_filepath) == False):
                #sys.stderr.write("%s not generated by step 1\n" % uncertain_input_list_h_filename)
                print("%s not generated by step 1\n" % uncertain_input_list_h_filename)
                #io.put("output.string(runstate).about.label", value="Emulation error")
                #Rappture.result(io)
                #sys.exit(1)
                return False

            # Step 2 - Create Titan2D input file for each of the samples
            #
            # Input(s): uncertain_input_list_h.txt
            # Output(s): simulation_<%06d sample number>.py

            print("\nCreating Titan2D input files...");

            for i in range (1, self.eruptsimulations + 1):
                filename = "simulation_%06d.py" %i
                filepath = os.path.join(self.workingdir,filename)
                if (os.path.exists(filepath) == True):
                    os.remove(filepath)

            step_2_path = os.path.join(self.bindir,"step_2.sh")
            checkPercent = 10;
            if (self.eruptsimulations > checkPercent):
                done = 0;
                nextDoneIncrement = self.eruptsimulations/checkPercent;
                nextDoneCheck = done + nextDoneIncrement;
                nextDonePercent = 0;

            for i in range (1, self.eruptsimulations + 1):

                if (self.eruptsimulations > checkPercent):
                    done = done + 1;
                    if (done > nextDoneCheck):
                        nextDoneCheck = done + nextDoneIncrement;
                        nextDonePercent = nextDonePercent + checkPercent;
                        print ("%d percent complete..." % nextDonePercent)
                subprocess.call([step_2_path,self.workingdir,titan2dInputFile,str(i)])

            # Verify

            filecheck = 0
            for i in range (1, self.eruptsimulations + 1):
                filename = "simulation_%06d.py" %i
                filepath = os.path.join(self.workingdir,filename)
                if (os.path.exists(filepath) == True):
                    filecheck=filecheck+1
                else:
                    print ("file %s not found" % filepath)

            #print ("filecheck: %d" %filecheck)
            if (filecheck != self.eruptsimulations):
                print("One or more Titan2D input files were not created by step 2\n")
                #sys.exit(1)
                return False
            else:
                print("Titan2D input files successfully created\n")
                
                print("\nCreating emulator input files...");
                
                # Create macro_emulator.pwem, macro_resamples.tmp, macro_resample_assemble.inputs,
                # AZ_vol_dir_bed_int.phm and step11_12_13_staged_input.txt
                

                step_5_8_9_10_path = os.path.join(self.bindir,"step_5_8_9_10.sh")
                subprocess.call([step_5_8_9_10_path,self.bindir,self.workingdir])
                
                step_6_path = os.path.join(self.bindir,"step_6.sh")

                # Create build_mini_pwem_meta.<samplenumber - formatted as %06g> for each sample
                for i in range (1, self.eruptsimulations + 1):
                    subprocess.call([step_6_path,self.bindir,self.workingdir,str(i)])

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
                #log_info ("numSimplicesTruncated: %d " % numSimplicesTruncated)
                
                # //: divide with integral results (discard remainder)
                # %: modulus
                self.numSimplicesPerProcessor = numSimplicesTruncated//self.eruptsimulations
                self.numSimplicesRemaining = numSimplicesTruncated%self.eruptsimulations


                if (numSimplicesTruncated <= 0):
                    sys.stderr.write("Steps 11-13: Not enough simplices to continue. Verify the number of erupt simulations.\n")
                    sys.stdout.flush()
                    return False

                #log_info ("self.numSimplicesPerProcessor: %d " % self.numSimplicesPerProcessor)
                #log_info ("self.numSimplicesRemaining: %d " % self.numSimplicesRemaining)
                #log_info ("len(self.phm_filenames): " + str(len(self.phm_filenames)))
                #log_info ("phm_filenames: " + str(phm_filenames))
                
                print("Emulator input files successfully created\n")

                sys.stdout.flush()
                return True
            
        except Exception as e:
            
            print ('Wrapper.py inititialize_workflow Exception: %s\n' %str(e))
            return False

    def run_workflow(self):

        try:

            #print ('Path(".").resolve(): ',  Path(".").resolve())

            #########################################################
            # Environment variables
            #########################################################

            print ('os.getcwd: ', os.getcwd())
            TOPDIR = os.getcwd()
            os.environ['TOPDIR'] = TOPDIR
            print("os.environ['TOPDIR']: ", os.environ['TOPDIR'])
            # pegasus bin directory is needed to find titan-simpletitan2d
            #BIN_DIR=`pegasus-config --bin`
            #echo "BIN_DIR: "$BIN_DIR
            #PEGASUS_LOCAL_BIN_DIR=${BIN_DIR}
            #export PEGASUS_LOCAL_BIN_DIR

            PEGASUS_LOCAL_BIN_DIR = '/usr/bin'
            os.environ['PEGASUS_LOCAL_BIN_DIR'] = PEGASUS_LOCAL_BIN_DIR
            print("os.environ['PEGASUS_LOCAL_BIN_DIR']: ", os.environ['PEGASUS_LOCAL_BIN_DIR'])
            
            S3_URL_PREFIX = 's3://user@amazon'
            os.environ['S3_URL_PREFIX'] = S3_URL_PREFIX
            print("os.environ['S3_URL_PREFIX']: ", os.environ['S3_URL_PREFIX'])
                  
            #s3_bucket = os.environ['S3_BUCKET']
            #print ('s3_bucket: ', s3_bucket)
            S3_BUCKET='titan2d-workdir-bucket/titan2d-workdir'
            os.environ['S3_BUCKET'] = S3_BUCKET
            print("os.environ['S3_BUCKET']: ", os.environ['S3_BUCKET'])

            # ./pegasusrc sets pegasus.catalog.site.file=./conf/sites.xml.
            # sites.xml aws-batch file server definition sets url to "${S3_URL_PREFIX}/${S3_BUCKET}"
            # url = os.environ['S3_URL_PREFIX'] + '/' +  os.environ['S3_BUCKET']
            # print ("url: %s" %url)
    
            #########################################################
            # Path to the titan and octave launch scripts
            #########################################################

            # Create the Pegasus workflow
            wf = Workflow('titanworkflow')
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
                os_type=OS.LINUX) \
            .add_profiles(Namespace.PEGASUS, key="clusters_size", value=self.eruptsimulations) \
            .add_profiles(Namespace.PEGASUS, key="clusters_num", value=self.eruptsimulations)
            tc.add_transformations(titanlaunch)
            
            octavelaunch = Transformation(
                'octavelaunch',
                site='local',
                pfn=os.path.join(self.workingdir,'remotebin','octaveLaunch.sh'),
                is_stageable = True, #Stageable or installed
                arch=Arch.X86_64,
                os_type=OS.LINUX) \
            .add_profiles(Namespace.PEGASUS, key="clusters_size", value=self.eruptsimulations) \
            .add_profiles(Namespace.PEGASUS, key="clusters_num", value=self.eruptsimulations)
            tc.add_transformations(octavelaunch)

            #########################################################
            #########################################################

            # PFNs:

            #filename = "grassdir"
            #filepath = os.path.join(self.workingdir,filename)
            #grass_dir = File(filename)
            #grass_dir.addPFN(PFN("file://" + filepath, "local"))
            #dax.addFile(grass_dir)

            # All files in a Pegasus workflow are referred to in the DAX using their Logical File Name (LFN).
            # These LFNs are mapped to Physical File Names (PFNs) when Pegasus plans the workflow.
            # Add input files to the DAX-level replica catalog

            # Grass database
            grassgis_database_zipped = self.grassgis_database+'.tar.gz'
            print ('grassgis_database_zipped: ', grassgis_database_zipped)
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
            
            for i in range (1, self.eruptsimulations + 1):
            
                rc.add_replica("local", File('simulation_%06d.py' % i), os.path.join(self.workingdir, 'simulation_%06d.py' % i))
                rc.add_replica("local", File('build_mini_pwem_meta.%06d' % i), os.path.join(self.workingdir, 'build_mini_pwem_meta.%06d' % i))
                
            # Add jobs
            
            step_4_jobs = []
            
            for i in range (1, self.eruptsimulations + 1):
                
                # Call titan
                #
                # Input(s): simulation.py for the sample
                # Output(s): pileheightrecord.<%06d sample number>
            
                # Pegasus returns for example, titan_ID0000001.stdout and  titan_ID0000001.stderr.
                # Cannot specify to use Stdout.txt and Stderr.txt as output or errors will occur.
                # Stdout and and Stdout info is contained in the titan_*.stdout files
             
                #.add_outputs(File('pileheightrecord.%06d' % i), stage_out=False)
                titanjob  = Job(titanlaunch)\
                    .add_args("""-nt 1 simulation_%06d.py""" %i)\
                    .add_inputs(File(grassgis_database_zipped))\
                    .add_inputs(File('simulation_%06d.py' % i))\
                    .add_checkpoint(File('pileheightrecord.%06d' % i), stage_out=True)\
                    .add_metadata(time="%d" %self.maxwalltime)
                if i==1:
                    titanjob.add_outputs(File('elevation.grid'), stage_out=True)
                
                wf.add_jobs(titanjob)
                
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
                
            step_7_jobs = []
            
            for i in range (1, self.eruptsimulations + 1):
            
                octavejob = Job(octavelaunch)\
                    .add_args("""r_build_mini_emulator.m %s %d""" % (".", i))\
                    .add_inputs(File('r_build_mini_emulator.m'))\
                    .add_inputs(File('build_mini_emulator.m'))\
                    .add_inputs(File('build_mini_pwem_meta.%06d' % i))\
                    .add_outputs(File('mini_emulator.%06d' % i), stage_out=False)\
                    .add_metadata(time="%d" %self.maxwalltime)
                    
                for j in range (1, self.eruptsimulations + 1):
                    octavejob.add_inputs(File('down_sampled_data.%06d' % j))\
                    
                wf.add_jobs(octavejob)
                
                # Needs all step 4 jobs to be complete
                wf.add_dependency(octavejob, parents=step_4_jobs)
                
                step_7_jobs.append(octavejob)

            i=self.simplexStart
            remaining = self.numSimplicesRemaining

            step_11_12_13_jobs = []
            
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
                    
                for j in range (1, self.eruptsimulations + 1):
                    octavejob.add_inputs(File('mini_emulator.%06d' % j))\

                for j in range (begin, end + 1):
                    # phm filenames are 0 or phm_*
                    if (self.phm_filenames[j-1] != "0"):
                        phm_filename = self.phm_filenames[j-1]
                        octavejob.add_outputs(File(phm_filename), stage_out=False)

                wf.add_jobs(octavejob)
                
                # Needs all step 7 jobs to be complete
                wf.add_dependency(octavejob, parents=step_7_jobs)
                
                step_11_12_13_jobs.append(octavejob)
                
                i=end+1
                
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
                wf.graph(include_files=True, label='xform-id', output='graph.png')
            except PegasusClientError as e:
                print(e)

            # view rendered workflow
            from IPython.display import Image
            Image(filename='graph.png')

            utcnow = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
            prefix = 'remotehost-' + utcnow
            print ('prefix: ' + prefix)

            try:
                
                script_path = os.path.join(self.scriptsdir,"pegasus-aws-batch.sh")
                subprocess.call([script_path,self.workingdir,prefix])

            except PegasusClientError as e:
                print ('pegasus-aws-batch PegasusClientError Exception: %s\n' %str(e))
                return False

            #'''
            try:
                
                wf.plan(conf='./pegasusrc',\
                        cluster = ['horizontal'],\
                        sites = ['aws-batch'],\
                        output_sites = ['local'],\
                        dir = './dags',\
                        force = True,\
                        submit = True)
                        
                submit_dir = wf.braindump.submit_dir
                print ('submit_dir: ' + str(submit_dir))

                print ('Waiting for the workflow to complete...')
                wf.wait()
                        
            except PegasusClientError as e:
                print ('workflow.plan PegasusClientError Exception: %s\n' %str(e))
                return False
            #'''
            
            try:
                
                script_path = os.path.join(self.scriptsdir,"pegasus-aws-batch-delete.sh")
                subprocess.call([script_path,self.workingdir,prefix])

            except PegasusClientError as e:
                print ('pegasus-aws-batch-delete PegasusClientError Exception: %s\n' %str(e))
            
            if os.path.exists(submit_dir):

                try:
                    
                    script_path = os.path.join(self.scriptsdir,"pegasus-analyzer.sh")
                    subprocess.call([script_path, self.workingdir, submit_dir])
                    
                except PegasusClientError as e:
                    print ('pegasus-analyzer PegasusClientError Exception: %s\n' %str(e))
                    
                try:
                    
                    script_path = os.path.join(self.scriptsdir,"pegasus-statistics.sh")
                    subprocess.call([script_path, self.workingdir, submit_dir])
                    
                except PegasusClientError as e:
                    print ('pegasus-statistics PegasusClientError Exception: %s\n' %str(e))
                    
                shutil.rmtree(submit_dir)
                return True
                
            else:
            
                print ('Wrapper.py error: submit directory %s not created' %submit_dir)
                return False
                
        except Exception as e:
            
            print ('Wrapper.py run_workflow Exception: %s\n' %str(e))
            return False
 
