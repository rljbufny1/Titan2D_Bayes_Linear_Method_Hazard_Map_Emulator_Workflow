%**********************************************************************
% octave script: r_down_sample_pileheightrecord.m
%
% wrapper for down_sample_pileheightrecord.m
%
% argument(s): datadir_,samplenumber
%
%**********************************************************************

% Get the arguments from the argument list

arg_list = argv();

arg1 = arg_list{1};            % datadir_
arg2 = str2num(arg_list{2});   % samplenumber

printf ("%s arg1: %s arg2: %d\n", program_name(), arg1, arg2);

down_sample_pileheightrecord(arg1, arg2)
