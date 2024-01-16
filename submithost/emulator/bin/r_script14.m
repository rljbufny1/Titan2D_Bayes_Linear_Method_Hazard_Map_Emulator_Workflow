%**********************************************************************
% matlab script: r_script14.m
%
% wrapper for script14.m
%
% argument(s): datadir_,samplenumber
%
%**********************************************************************

% Get the arguments from the argument list

arg_list = argv();

arg1 = arg_list{1};            % datadir_

printf ("%s arg1: %s\n", program_name(), arg1);

script14(arg1)
