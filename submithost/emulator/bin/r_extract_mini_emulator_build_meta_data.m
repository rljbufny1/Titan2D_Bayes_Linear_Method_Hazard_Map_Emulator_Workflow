%**********************************************************************
% matlab script: r_extract_mini_emulator_build_meta_data.m
%
% wrapper for extract_mini_emulator_build_meta_data.m
%
% argument(s): datadir_,samplenumber
%
%**********************************************************************

% Get the arguments from the argument list

arg_list = argv();

arg1 = arg_list{1};            % datadir_
arg2 = str2num(arg_list{2});   % samplenumber

printf ("%s arg1: %s arg2: %d\n", program_name(), arg1, arg2);

extract_mini_emulator_build_meta_data(arg1, arg2)
