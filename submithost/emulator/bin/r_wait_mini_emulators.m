%**********************************************************************
% matlab script: r_wait_mini_emulators
%
% argument(s): datadir_, numSanples
%
%**********************************************************************

% Get the arguments from the argument list

arg_list = argv();

arg1 = arg_list{1};            % datadir_
arg2 = str2num(arg_list{2});   % numSamples

printf ("%s arg1: %s arg2: %d\n", program_name(), arg1, arg2);

datadir_ = arg1;
datadir = strcat(datadir_,'/');
numSamples = arg2;

for samplenumber = 1:numSamples
    
    filename = strcat(datadir,sprintf('mini_emulator.%06g',samplenumber));
    fid = fopen(filename, 'r');
    if fid == -1
       fprintf ("%s does not exist\n", filename);
    else
       fprintf ("%s exists\n", filename);
    end   
end
