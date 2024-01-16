%**********************************************************************
% matlab script: script5_8_9_10.m
%
% argument(s): datadir_
%
% input(s): runParams.mat
%
% output(s):  macro_emulator.pwem, macro_resamples.tmp, 
%   macro_resample_assemble.inputs, AZ_vol_dir_bed_int.phm,
%   step11_12_13_staged_input.txt,
%
%**********************************************************************

function script5_8_9_10(datadir_)

    datadir = strcat(datadir_, '/');
        
    % Step 5
    % matlab script: build_macro_emulator.m
    % argument(s): datadir_
    % input(s): uncertain_input_list.txt
    % output(s): macro_emulator.pwem

    build_macro_emulator(datadir_);

    % Step 8
    % matlab script: gen_random_macro_emulator_resample_inputs.m
    % argument(s): datadir_
    % input(s): runParams.mat
    % output(s): macro_resamples.tmp

    gen_random_macro_emulator_resample_inputs(datadir_);

    % Step 9
    % matlab script: identify_mini_emulators_to_evaluate.m
    % argument(s): datadir_
    % input(s): macro_emulator.pwem, macro_resamples.tmp
    % output(s): macro_resample_assemble.inputs

    identify_mini_emulators_to_evaluate(datadir_);

    % Step 10
    % matlab script: make_initial_hazard_map.m
    % argument(s): datadir_
    % input(s): runParams.mat
    % output(s): AZ_vol_dir_bed_int.phm

    make_initial_hazard_map(datadir_);

    % Stage for steps 11 to 13

    % matlab script: script11_12_13_stage.m
    % argument(s): datadir_
    % input(s): macro_emulator.pwem, macro_resample_assemble.inputs, 
    %   AZ_vol_dir_bed_int.phm
    % output(s): step11_12_13_staged_input.txt

    script11_12_13_stage(datadir_);

return;
