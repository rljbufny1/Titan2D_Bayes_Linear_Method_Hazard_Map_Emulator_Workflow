%**********************************************************************
% matlab script: r_script11_12_13.m
%
% wrapper for script11_12_13.m
%
% argument(s): datadir_, start simplex number, stop simplex number
%
%**********************************************************************

% Get the arguments from the argument list

arg_list = argv();

arg1 = arg_list{1};            % datadir_
arg2 = str2num(arg_list{2});   % start simplex number
arg3 = str2num(arg_list{3});   % stop simplex number

printf ("%s arg1: %s arg2: %d arg3: %d\n", program_name(), arg1, arg2, arg3);

script11_12_13(arg1, arg2, arg3)
