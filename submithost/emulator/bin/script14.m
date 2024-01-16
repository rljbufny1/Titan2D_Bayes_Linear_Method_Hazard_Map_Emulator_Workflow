%**********************************************************************
% matlab script: script14.m
%
% argument(s): datadir_
%
% input(s): AZ_vol_dir_bed_int.phm, phm_from_eval* files
%
% output(s): AZ_vol_dir_bed_int_final.phm
%**********************************************************************

function script14(datadir_)

    datadir = strcat(datadir_, '/');
    
    hazmapfilename = strcat(datadir, 'AZ_vol_dir_bed_int.phm');
    hazmapfilefinalname = strcat(datadir, 'AZ_vol_dir_bed_int_final.phm');
    hazmapfilename
    hazmapfilefinalname

    copyfile(hazmapfilename, hazmapfilefinalname);

    listing = dir(strcat(datadir,'phm_from_eval*'));
    [m,n] = size(listing)
    fprintf('Total phm_from_eval files to merge: %d\n', m);
    for i = 1:m
       phm_from_eval = strcat(datadir, listing(i,1).name);
       fprintf('\nMerging %d: %s ...\n',i,phm_from_eval);
       merge_probability_of_hazard_maps(datadir_,hazmapfilefinalname,phm_from_eval);
    end
   
end




