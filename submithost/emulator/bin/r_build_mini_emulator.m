%**********************************************************************
% matlab script: r_build_mini_emulator.m
%
% wrapper for build_mini_emulator.m
%
% argument(s): datadir_,samplenumber
%
%**********************************************************************

% Get the arguments from the argument list

arg_list = argv();

arg1 = arg_list{1};            % datadir_
arg2 = str2num(arg_list{2});   % samplenumber

printf ("%s arg1: %s arg2: %d\n", program_name(), arg1, arg2);

build_mini_emulator(arg1, arg2)
