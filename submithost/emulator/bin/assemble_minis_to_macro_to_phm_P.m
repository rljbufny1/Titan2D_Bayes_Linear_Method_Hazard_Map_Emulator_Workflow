%**********************************************************************
% matlab script: assemble_minis_to_macro_to_phm_P.m
%
% argument(s): datadir_,aminievalfilename,crith,NdiminmacroX,Nxmap,xmap
%
% input(s): mini_emulator_eval_<simplex id string>,
%    macro_resample_assemble.inputs, AZ_vol_dir_bed_int.phm
%
% returns: newhazmapfilename
%
% output(s): phm_from_eval_<simplex number,key,moment>
%**********************************************************************

function newhazmapfilename=assemble_minis_to_macro_to_phm_P ...
    (datadir_,aminievalfilename,crith,NdiminmacroX,Nxmap,xmap)
    
    datadir = strcat(datadir_, '/');
    
    iftoc=1;
    if(iftoc)
        tic;
    end
    
    scanstr = strcat(datadir, 'mini_emulator_eval_%d.%d.%d.%d');
    yada=sscanf(aminievalfilename,scanstr,4);
    if(numel(yada)~=4)
        disp(sprintf('ERROR: You entered "%s" as one of the mini emulator evaluations. The format of the filename needs to be "mini_emulator_eval_%%d.%%08d.%%d.%%06d"',aminievalfilename));
        bob; %cause the code to crash
    end
    MacroSimplexNumber=yada(1);
    RandomKey=yada(2);
    MomentToAssemble=yada(3);
    aNodeInMacroSimplex=yada(4);   

    if(MomentToAssemble<0)
        Nmoments=-MomentToAssemble;
    else
        Nmoments=1;
    end
     
    if(~((MomentToAssemble==1)||(MomentToAssemble==-2)))
        disp(sprintf('ERROR: you need the first statistical moment (mean) to create a phm file, the file you entered only contains moment %g',MomentToAssemble));
        bob;
    end

    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %read in input file #1
    
    filename = strcat(datadir, 'macro_resample_assemble.inputs');
    fid=fopen(filename,'r');
    Nskip=sscanf(fgets(fid),'additional file format lines=%g',1);
    for i=1:Nskip
        fgets(fid);
    end
    %fprintf(fid,'%%Ndiminmacro=4: of macro-emulator input dimensions (log10(volume [m^3]),Direction [deg CC from east],BedFrictAng [deg],IntFrictAng [deg]): [1] integer\n');
    %fprintf(fid,'%%Nxmacroinside: the number of macro emulator (log10(volume [m^3]),Direction [deg CC from east],BedFrictAng [deg],IntFrictAng [deg]) input points to evaluate: [1] integer\n');    
    %fprintf(fid,'%%{{(log10(volume [m^3]),Direction [deg CC from east],BedFrictAng [deg],IntFrictAng [deg]): [Ndiminmacro] doubles},{isimp: index of  macro-emulator simplex: [1] integer},{simulation/mini-emulator indices/ids: [Ndiminmacro+1] integers},{barycentric coordinates: [Ndiminmacro+1] doubles},{w: relative weight for hazmap assembly, sum(w)~=1 is ok: [1] double}}\n');
    %fprintf(fid,'%%Nxmacrooutside: the number of randomly generated input points that can''t evaluate because they lie outside the convex hull of simulations\n');
    %fprintf(fid,'%%{{(log10(volume [m^3]),Direction [deg CC from east],BedFrictAng [deg],IntFrictAng [deg]): [Ndiminmacro] doubles},{w: relative weight for hazmap assembly: [1] double}}\n');
    
    Ndiminmacro  =sscanf(fgets(fid),'%g',1);
    Nxmacroinside=sscanf(fgets(fid),'%g',1);
    yada=sprintf('%s%%g\n',repmat('%g ',1,Ndiminmacro+1+(Ndiminmacro+1)*2));
    assemblethesemacro=fscanf(fid,yada,[(Ndiminmacro+1)*3+1 Nxmacroinside])';
    fclose(fid);
    iassemblethesemacro=find(assemblethesemacro(:,Ndiminmacro+1)==MacroSimplexNumber);
    Nmacroseachx=numel(iassemblethesemacro);
    assemblethesemacro=assemblethesemacro(iassemblethesemacro,:);
    NodesOfMacroSimplex=unique(assemblethesemacro(:,Ndiminmacro+1+(1:Ndiminmacro+1)),'rows');
    assemblethesemacro=sortrows(assemblethesemacro,Ndiminmacro:-1:1);
    ifsaidminianode=sum(NodesOfMacroSimplex==aNodeInMacroSimplex);
    if(size(NodesOfMacroSimplex,1)~=1)
        save DEBUG_ASSEMBLE_MINIS_TO_MACRO_TO_PHM1;
        disp(sprintf('ERROR: there are %g SETS of nodes for simplex %g!!!! Workspace saved to DEBUG_ASSEMBLE_MINIS_TO_MACRO_TO_PHM1.mat\n',size(NodesOfMacroSimplex,1),MacroSimplexNumber));
        bob; %cause the code to crash
    elseif(ifsaidminianode~=1)
        save DEBUG_ASSEMBLE_MINIS_TO_MACRO_TO_PHM2;
        disp(sprintf('ERROR: in file "macro_resample_assemble.inputs" the nodes of simplex %d are {%s}, and you said "%s" was 1 of them!!!! Workspace saved to DEBUG_ASSEMBLE_MINIS_TO_MACRO_TO_PHM2.mat\n',...
            MacroSimplexNumber,aminievalfilename));
        bob; %cause the code to crash
    end

    if(iftoc)
        disp(sprintf('Done reading "macro_resample_assemble.inputs" at time t=%g [sec]',toc));
    end


    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %read in an old hazard map to learn the map points etc. but will not 
    %update this file or use the probability data in it.  Start a new phm
    %file
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    
    newhazmapfilename=strcat(datadir,sprintf('phm_from_eval_%d.%08d.%d',MacroSimplexNumber,RandomKey,MomentToAssemble));
    fidnewphm=fopen(newhazmapfilename,'w');
    
    yada = 'additional file format lines=0';
    fprintf(fidnewphm,'%s\n',yada); %copy the line to the new file

    %{
    fid=fopen(ahazmapfilename,'r');
    yada=fgets(fid);
    Nskip=sscanf(yada,'additional file format lines=%g',1);
     
    for i=1:Nskip
        fprintf(fidnewphm,'%s',fgets(fid)); %copy the line to the new file
    end
%     fprintf(fid,'%%This file contains data for a probability of hazard map generated by resampling a piecewise linear ensemble emulator constructed from titan simulations\n');
%     fprintf(fid,'%%crith [m]: the critical flow depth in meters, a .phm file contains the data needed to plot a map of P(h(east,north)>crith): [1] double\n');
%     fprintf(fid,'%%Ndiminmacro=4: number of uncertain dimensions (see what they are below) for each resample input: [1] integer\n');
%     fprintf(fid,'%%W: total so far weight of all resamples (macro emulator inputs) used to make this file:  [1] double\n');
%     fprintf(fid,'%%Nxmap: the number of (east,north) points on the map directly represented by this file: [1] integer\n');
%     fprintf(fid,'%%[Nxmap] lines containing {{x=(east,north):[2] doubles},{{WI WI^2}: these are the sum of all w*indicator_function and w*indicator_function^2, you compute the probability of exceeding the critical height as P(h(east,north)>crith)=WI/W: [2] doubles}}\n');
%     fprintf(fid,'%%Nresamp: number of resample inputs used so far to produce this .phm file: [1] integer\n');
%     fprintf(fid,'%%[Nresamp] lines containing the {{resample macro-inputs: (log10(volume [m^3]),Direction [deg CC from east],BedFrictAng [deg],IntFrictAng [deg]): [Ndiminmacro] doubles},{w: weight of this resample macro-input: [1] double}}\n');
         
    crith=sscanf(fgets(fid),'%g',1); 
    checkNdiminmacro=sscanf(fgets(fid),'%g',1);
    W=sscanf(fgets(fid),'%g',1); 
    Nxmap=sscanf(fgets(fid),'%g',1);

    if(Ndiminmacro~=checkNdiminmacro)
        save DEBUG_ASSEMBLE_MINIS_TO_MACRO_TO_PHM3;
        disp(sprintf('ERROR: Ndiminmacro from "macro_resample_assemble.inputs" ~= Nidminmacro from "%s"!!!! Workspace saved to DEBUG_ASSEMBLE_MINIS_TO_MACRO_TO_PHM3.mat\n',ahazmapfilename));
        bob; %cause the code to crash
    end

    XMAPWIWI2=fscanf(fid,'%g %g %g\n',[4 Nxmap])';
    fclose(fid);
    %}
    XMAPWIWI2 = xmap;
        
    XMAPWIWI2(:,3:4)=0; %this new temporary phm file only contains the contribution from this simplex evaluation
    Nresamp=0; W=0;   
    if(iftoc)
        %disp(sprintf('Done reading "%s" at time t=%g [sec]',ahazmapfilename,toc));
        disp(sprintf('Done processing hazard map file info at time t=%g [sec]',toc));
    end
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %Now to read the mini-emulator evaluations and assemble them into
    %macro-emulator evaluations
        
    MINIEVALFILENAMEFORMAT=sprintf('mini_emulator_eval_%d.%08d.%d.%%06d',MacroSimplexNumber,RandomKey,MomentToAssemble);
            
    for iMacroNode=1:Ndiminmacro+1
        openthisminievalfile=strcat(datadir, sprintf(MINIEVALFILENAMEFORMAT,NodesOfMacroSimplex(iMacroNode)));

        itothisbary=Ndiminmacro+1+Ndiminmacro+1+iMacroNode;
        
        fid=fopen(openthisminievalfile,'r');
        if(fid==-1)
            disp(sprintf('ERROR: can''t find file "%s"!!!!\n', openthisminievalfile));
            bob; %cause the code to crash
        end
        
        Nskip=sscanf(fgets(fid),'additional file format lines=%g',1);
        for i=1:Nskip
            fgets(fid);
        end

        %fprintf(fid,'%%a UniqueKey that contains simplex id, the randomly generated after seeded by time key passed in (allows for pairing), the degree of the statistical moment evaluated (1=mean, 2=variance, 3=skewness, 4=kurtosis,...,-2=first 2 moments, -3=first 3 moments), and the 6 digit (left padded by zeros) id of this mini-emulator\n');
        %fprintf(fid,'%%Nmoments: Nmoments=1 if the moment key is positive, otherwise it is absolute value of the moment key: [1] integer\n');
        %fprintf(fid,'%%Ndiminmacro=2: #of uncertain dimensions (log10(volume [m^3]),Direction [deg CC from east],BedFrictAng [deg],IntFrictAng [deg]), for each resample input: [1] integer\n');
        %fprintf(fid,'%%{{(simplex id): a sanity check: [1] integer},{id''s of simulation/mini-emulator in the simplex, another sanity check this mini-emulator should one of the ones listed here: [Ndiminmacro+1] integers}}\n');
        %fprintf(fid,'%%Ndimin=4: #of mini-emulator input dimensions (east,north,log10(volume [m^3]),Direction [deg CC from east],BedFrictAng [deg],IntFrictAng [deg]): [1] integer\n');
        %fprintf(fid,'%%file format option indicator: [1] integer\n');
        %fprintf(fid,'%%one of the following two options\n');
        %fprintf(fid,'%%option 1: for when all map points need to be evaluated at the same set(s) of macro coordinates\n');
        %fprintf(fid,'%%     Nmacroseachx: #of macro input points associated with each map point: [1] integer\n');
        %fprintf(fid,'%%     one line containing: [Nmacroseachx] sets of {(log10(volume [m^3]),Direction [deg CC from east],BedFrictAng [deg],IntFrictAng [deg]): macro input coordinates: [Ndiminmacro] doubles}\n');
        %fprintf(fid,'%%     Nxmap: #of unique map-points: [1]\n');
        %fprintf(fid,'%%     [Nxmap] lines containing {(east,north): [2] doubles}\n');
        %fprintf(fid,'%%     [(Nxmap)*Nmoments] lines containing: {adjusted moment for Nmacroseachx macro inputs: [Nmacroseachx] doubles}, if Nmoments >1, all mean values come before all variance values, etc\n'); 
        %fprintf(fid,'%%option 2: for when each map point can be paired with different macro input(s), in this case there can also be duplicates of listed (east,north) coordinates that have different macro coordinates\n');
        %fprintf(fid,'%%     Nx: #of (Ndimin-tuple) input points the mini-emulator was evalutated at: [1] integer\n');
        %fprintf(fid,'%%     [Nx] lines, each of which contains {{x=(east,north,log10(volume [m^3]),Direction [deg CC from east],BedFrictAng [deg],IntFrictAng [deg]): [Ndimin] doubles},{the adjusted statistical moment(s): [Nmoment] double(s)}}\n');
    
    
        UniqueMiniEmulatorKeyStr=fgetl(fid);
        UniqueMiniEmulatorKey=sscanf(UniqueMiniEmulatorKeyStr,'%d.%d.%d.%d',4);
        if(~(...
                (MacroSimplexNumber==UniqueMiniEmulatorKey(1))&&...
                (RandomKey==UniqueMiniEmulatorKey(2))&&...
                (MomentToAssemble==UniqueMiniEmulatorKey(3))&&...
                (NodesOfMacroSimplex(iMacroNode)==UniqueMiniEmulatorKey(4))...
            ))
            save DEBUG_ASSEMBLE_MINIS_TO_MACRO_TO_PHM4;
            disp(sprintf('ERROR: file "%s" says its key is %s!!!! Workspace saved to DEBUG_ASSEMBLE_MINIS_TO_MACRO_TO_PHM4.mat\n',...
                openthisminievalfile,UniqueMiniEmulatorKeyStr));
            bob; %cause the code to crash
        end

        checkNmoments=sscanf(fgets(fid),'%g',1);
        if(~((numel(checkNmoments)==1)&&(Nmoments==checkNmoments)))
            save DEBUG_ASSEMBLE_MINIS_TO_MACRO_TO_PHM5;
            disp(sprintf('ERROR: file "%s" says it contains %d instead of %d different moments!!!! Workspace saved to DEBUG_ASSEMBLE_MINIS_TO_MACRO_TO_PHM5.mat\n',openthisminievalfile,checkNmoments,Nmoments));
            bob; %cause the code to crash
        end
        
        checkNdiminmacro=sscanf(fgets(fid),'%g',1);
        if(isempty(checkNdiminmacro)||(Ndiminmacro~=checkNdiminmacro))
            save DEBUG_ASSEMBLE_MINIS_TO_MACRO_TO_PHM6;
            disp(sprintf('ERROR: "macro_resample_assemble.inputs" says Ndiminmacro=%g but "%s" says Ndiminmacro=%g!!!! Workspace saved to DEBUG_ASSEMBLE_MINIS_TO_MACRO_TO_PHM6.mat\n',openthisminievalfile,checkNdiminmacro));
            bob; %cause the code to crash
        end
                
        yada=sscanf(fgets(fid),sprintf('(%%g)%s',repmat(' %g',1,Ndiminmacro+1)),Ndiminmacro+2);
        if(UniqueMiniEmulatorKey(1)~=yada(1))
            save DEBUG_ASSEMBLE_MINIS_TO_MACRO_TO_PHM7;
            disp(sprintf('ERROR: UniqueMiniEmulatorKey=%s but file says simplex id is %g!!!! Workspace saved to DEBUG_ASSEMBLE_MINIS_TO_MACRO_TO_PHM7.mat\n',...
                UniqueMiniEmulatorKeyStr,yada(1)));
            bob; %cause the code to crash
        end

        checkNodesOfMacroSimplex=yada(2:Ndiminmacro+2)';
        %NodesOfMacroSimplex
        %checkNodesOfMacroSimplex
        if(isempty(checkNodesOfMacroSimplex)||~all(checkNodesOfMacroSimplex==NodesOfMacroSimplex))
            %Note from Keith to future people using my code... When I wrote
            %this, I made sure that the nodes of all simplices were always 
            %sorted into ascending order.  Furthermore simplices in a
            %tesselation were rowsorted in ascending order.  Since I
            %know this is the case I do not need to sort them here, and
            %specifically did not sort them here so that users would be 
            %alerted to the fact that they have changed my file formats, 
            %which was probably accidental, and that they need to be 
            %careful
            save DEBUG_ASSEMBLE_MINIS_TO_MACRO_TO_PHM8;
            disp(sprintf('ERROR: in "macro_resample_assemble.inputs" macro simplex %d has nodes {%d%s} but in file "%s" it has nodes {%d%s}!!!! Workspace saved to DEBUG_ASSEMBLE_MINIS_TO_MACRO_TO_PHM8.mat\n',MacroSimplexNumber,...
                NodesOfMacroSimplex(     1),sprintf(repmat(',%d',1,Ndiminmacro),NodesOfMacroSimplex(     2:Ndiminmacro+1)),...
                checkNodesOfMacroSimplex(1),sprintf(repmat(',%d',1,Ndiminmacro),checkNodesOfMacroSimplex(2:Ndiminmacro+1))));
            bob; %cause the code to crash
        end 
 
        checkNdimin=sscanf(fgets(fid),'%g',1);
        if(iMacroNode==1)
            Ndimin=checkNdimin;
            Idimout=Ndimin+(1:Nmoments);
        end
        if((numel(checkNdimin)~=1)||(Ndimin~=checkNdimin))
            save DEBUG_ASSEMBLE_MINIS_TO_MACRO_TO_PHM9;
            disp(sprintf('ERROR: mini-emulator %d said that Ndimin=%d and mini-emulator %d said that Ndimin is %d!!!! Workspace saved to DEBUG_ASSEMBLE_MINIS_TO_MACRO_TO_PHM9.mat\n',...
                NodesOfMacroSimplex(1),Ndimin,NodesOfMacroSimplex(iMacroNode),checkNdimin));
            bob; %cause the code to crash
        end
            
        Ndiminspatial=Ndimin-Ndiminmacro;
   
        fileformatoption=sscanf(fgets(fid),'%g',1);
        switch(fileformatoption)
            case 1,
                checkNmacroseachx=sscanf(fgets(fid),'%g',1);
                newmacros=sscanf(fgets(fid),'%g',[Ndiminmacro checkNmacroseachx])';
                % rlj - update by Dr Keith Dalbey sent by Matt Williams
                %[blah,iA,iB]=intersect(assemblethesemacro(:,1:Ndiminmacro),newmacros,'rows');
                [~,iA,~]=intersect(assemblethesemacro(:,1:Ndiminmacro),newmacros,'rows');
                
                if(iMacroNode==1)
                    if((Nmacroseachx~=checkNmacroseachx))
                        if(numel(iA)==checkNmacroseachx)
                            assemblethesemacro=sortrows(assemblethesemacro(iA,:),Ndiminmacro:-1:1);
                            Nmacroseachx=checkNmacroseachx;
                        else
                            save DEBUG_ASSEMBLE_MINIS_TO_MACRO_TO_PHM10;
                            disp(sprintf('ERROR: "%s" should contain evaluations at %d different Macro coordinates but contains %d!!!! Workspace saved to DEBUG_ASSEMBLE_MINIS_TO_MACRO_TO_PHM10.mat\n',...
                                openthisminievalfile,Nmacroseachx,checkNmacroseachx));
                            bob; %cause the code to crash
                        end
                    end
                elseif(~((Nmacroseachx==checkNmacroseachx)&&(numel(iA)==Nmacroseachx)))
                    save DEBUG_ASSEMBLE_MINIS_TO_MACRO_TO_PHM11;
                    disp(sprintf('ERROR: "%s" contains a different set of Macro/uncertain inputs than previous mini-emulators in this macro simplex evaluation!!! Workspace saved to DEBUG_ASSEMBLE_MINIS_TO_MACRO_TO_PHM11.mat\n',...
                        openthisminievalfile));
                    bob; %cause the code to crash
                end
                
                checkNxmap=sscanf(fgets(fid),'%g',1);
                if(any(Nxmap~=checkNxmap))
                    save DEBUG_ASSEMBLE_MINIS_TO_MACRO_TO_PHM12;
                    disp(sprintf('ERROR: there are %d map-points in the phm file but "%s" has a {%s} of them!!! Workspace saved to DEBUG_ASSEMBLE_MINIS_TO_MACRO_TO_PHM12.mat\n',...
                        Nxmap,openthisminievalfile,sprintf(['%d' repmat(',%d',1,checkNmacroseachx-1)],checkNxmap)));
                    bob; %cause the code to crash
                end

                xmap=fscanf(fid,'%g %g\n',[2 Nxmap])';
                
                if(~all(all(XMAPWIWI2(:,1:2)==xmap)))
                    save DEBUG_ASSEMBLE_MINIS_TO_MACRO_TO_PHM13;
                    disp(sprintf('ERROR: "%s" contains a different set of map-points than the phm file!!! Workspace saved to DEBUG_ASSEMBLE_MINIS_TO_MACRO_TO_PHM13.mat\n',...
                        openthisminievalfile));
                    bob; %cause the code to crash                                 
                end

                yada=sprintf('%%g%s\n',repmat(' %g',1,Nmacroseachx-1));
                %save DEBUGMEWTFmini2macro2phm;
                newxsx=permute(reshape(fscanf(fid,yada,Nmacroseachx*Nxmap*Nmoments),[Nmacroseachx Nxmap Nmoments]),[2 1 3]);

                fclose(fid);
                if(iftoc)
                    disp(sprintf('Done reading %g/%g mini emulator evaluations at time t=%g [sec]',iMacroNode,Ndiminmacro+1,toc));
                end
                
            case 2,
                checkNx=sscanf(fgets(fid),'%g',1);
                if(iMacroNode==1)
                    Nx=checkNx;
                end
                if((numel(checkNx)~=1)||(Nx~=checkNx))
                    save DEBUG_ASSEMBLE_MINIS_TO_MACRO_TO_PHM14;
                    disp(sprintf('ERROR: mini-emulator %d was evaluated at Nx=%d data points and mini-emulator %d was evaluated at Nx=%d data points!!!! Workspace saved to DEBUG_ASSEMBLE_MINIS_TO_MACRO_TO_PHM14.mat\n',...
                        NodesOfMacroSimplex(1),Nx,NodesOfMacroSimplex(iMacroNode),checkNx));
                    bob; %cause the code to crash
                end

                yada=sprintf('%%g%s\n',repmat(' %g',1,Ndimin+Nmoments-1));
                newxsx=sortrows(fscanf(fid,yada,[Ndimin+Nmoments Nx])',[Ndimin:-1:1 Idimout]);
                fclose(fid);
                if(iftoc)
                    disp(sprintf('Done reading %g/%g mini emulator evaluations at time t=%g [sec]',iMacroNode,Ndiminmacro+1,toc));
                end

                idiffmacro=[find(any(diff(newxsx(:,Ndiminspatial+1:Ndimin),1,1),2)); Nx];
                checkNmacroseachx=numel(idiffmacro);
                checkNxmap=unique([idiffmacro(1); diff(idiffmacro)]);
                
                newmacros=newxsx(idiffmacro,3:Ndimin);
                % rlj - update by Dr Keith Dalbey sent by Matt Williams                
                %[blah,iA,iB]=intersect(assemblethesemacro(:,1:2),newmacros,'rows');
                [~,iA,~]=intersect(assemblethesemacro(:,1:Ndiminmacro),newmacros,'rows');
                 
                if(iMacroNode==1)
                    if((Nmacroseachx~=checkNmacroseachx))
                        if(numel(iA)==checkNmacroseachx)
                            assemblethesemacro=sortrows(assemblethesemacro(iA,:),Ndiminmacro:-1:1);
                            Nmacroseachx=checkNmacroseachx;
                        else
                            save DEBUG_ASSEMBLE_MINIS_TO_MACRO_TO_PHM15;
                            disp(sprintf('ERROR: "%s" should contain evaluations at %d different Macro coordinates but contains %d!!!! Workspace saved to DEBUG_ASSEMBLE_MINIS_TO_MACRO_TO_PHM15.mat\n',...
                                openthisminievalfile,Nmacroseachx,checkNmacroseachx));
                            bob; %cause the code to crash
                        end
                    end
                elseif(~((Nmacroseachx==checkNmacroseachx)&&(numel(iA)==Nmacroseachx)))
                    save DEBUG_ASSEMBLE_MINIS_TO_MACRO_TO_PHM16;
                    disp(sprintf('ERROR: "%s" contains a different set of Macro/uncertain inputs than previous mini-emulators in this macro simplex evaluation!!! Workspace saved to DEBUG_ASSEMBLE_MINIS_TO_MACRO_TO_PHM16.mat\n',...
                        openthisminievalfile));
                    bob; %cause the code to crash
                end

                if(any(Nxmap~=checkNxmap))
                    save DEBUG_ASSEMBLE_MINIS_TO_MACRO_TO_PHM17;
                    disp(sprintf('ERROR: there are %d map-points in the phm file but "%s" has a {%s} of them!!! Workspace saved to DEBUG_ASSEMBLE_MINIS_TO_MACRO_TO_PHM17.mat\n',...
                        Nxmap,openthisminievalfile,sprintf(['%d' repmat(',%d',1,checkNmacroseachx-1)],checkNxmap)));
                    bob; %cause the code to crash
                end

                i=1:Nxmap;
                if(~all(all(XMAPWIWI2(:,1:2)==newxsx(i,1:2))))
                    save DEBUG_ASSEMBLE_MINIS_TO_MACRO_TO_PHM18;
                    disp(sprintf('ERROR: "%s" contains a different set of map-points than the phm file!!! Workspace saved to DEBUG_ASSEMBLE_MINIS_TO_MACRO_TO_PHM18.mat\n',...
                        openthisminievalfile));
                    bob; %cause the code to crash
                end

                newxsx=reshape(newxsx(:,Idimout),[Nxmap Nmacroseachx Nmoments]);
                
            otherwise,
                save DEBUG_ASSEMBLE_MINIS_TO_MACRO_TO_PHM19;
                disp(sprintf('ERROR: I don''t know how to handle file format %d!!! Workspace saved to DEBUG_ASSEMBLE_MINIS_TO_MACRO_TO_PHM19.mat\n',fileformatoption));
                bob; %cause the code to crash   
        end


        %now actually combine the minis into the macro
        if(iMacroNode==1)
            XSX=newxsx;
            for imacroeachx=1:Nmacroseachx
                p=assemblethesemacro(imacroeachx,itothisbary);
                XSX(:,imacroeachx,:)=XSX(:,imacroeachx,:)*p;
            end
        else
            for imacroeachx=1:Nmacroseachx
                p=assemblethesemacro(imacroeachx,itothisbary);
                XSX(:,imacroeachx,:)=XSX(:,imacroeachx,:)+newxsx(:,imacroeachx,:)*p;                
            end
        end
    end        

    if(iftoc)
        disp(sprintf('Done assembling mini-emulator evaluations into macro emulator evaluations at time t=%g [sec]',toc));
    end
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %now compute the first and second moment columns in the phm file

    IdimoutMAP=Ndiminspatial+(1:2);
    itow=(Ndiminmacro+1)*3+1;

    for imacroeachx=1:Nmacroseachx
        w=assemblethesemacro(imacroeachx,itow);
        W=W+w;
                
        %%these are for if you want to account for the emulator's
        %%uncertainty about the simulator output, it can only be used if
        %%you evaluated the mini-emulators' adjusted mean AND variance
        %%uses probability in place of the indicator function
        %if(any(XSX(:,imacroeachx,2)<0))
        %    bob;
        %end
        %temp=0.5*(1+erf((-crith+XSX(:,imacroeachx,1))./sqrt(2*XSX(:,imacroeachx,2))));
        %temp=w*max(temp,isnan(temp));
             %%previous 1 line replaces the next 2
             %%temp(find(isnan(temp)))=1; %triggers iff h=crith and sigma=0 
             %%temp=temp*w;
        
        %%this is for if you want to take the emulator's mean as the
        %%simulator output
        temp=w*(XSX(:,imacroeachx,1)>=crith);
        
        XMAPWIWI2(:,IdimoutMAP)=XMAPWIWI2(:,IdimoutMAP)+[temp temp.^2];
    end

    XMACROw=assemblethesemacro(:,[1:Ndiminmacro itow]);
    Nresamp=Nresamp+Nmacroseachx;

    if(iftoc)
        disp(sprintf('Done transforming macro-emulator evalutaion into a phm at time t=%g [sec]',toc));
    end

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%    
    %write the real data to the new .phm file
     
    fprintf(fidnewphm,'%.14g\n',crith,Ndiminmacro,W,Nxmap);
    fprintf(fidnewphm,'%.2f %.2f %.14g %.14g\n',XMAPWIWI2');
    fprintf(fidnewphm,'%g\n',Nresamp);
    fprintf(fidnewphm,sprintf('%%.10g%s\n',repmat(' %.10g',1,Ndiminmacro)),XMACROw');
    fclose(fidnewphm);
 
    if(iftoc)
        disp(sprintf('Done writing the phm to file "%s" at time t=%g [sec]',newhazmapfilename,toc));
    end

return
