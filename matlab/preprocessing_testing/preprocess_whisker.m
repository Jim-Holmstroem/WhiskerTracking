function preprocess_whisker( directory ) 
    % preprocess the images trying to pickout the whiskers (making them white)
    %
    %

    
    fnames=dir(strcat(directory,'/*.png'));
    bnames=dir(strcat(directory,'/background/*.png'));
    N=size(fnames,1);
    B=size(bnames,1);

    background=zeros([size(imread(strcat(directory,'/background/',bnames(1).name))),B]);
   

    dirname_prewhiskers=strcat(directory,'/preprocessed_whiskers');
    dirname_presnout   =strcat(directory,'/preprocessed_snout');

    if(~exist(dirname_prewhiskers))
        mkdir(dirname_prewhiskers)
    end
    if(~exist(dirname_presnout))
        mkdir(dirname_presnout)
    end

    matlabpool size;
    if(~ans)
        matlabpool open;
    end
    parfor it = 1:B
        background(:,:,it)=double(imread(strcat(directory,'/background/',bnames(it).name)))/255;
    end
    parfor it = 1:N
        img_name=strrep(fnames(it).name,'.png','');
        disp(img_name)
        img=double(imread(strcat(directory,'/',img_name,'.png')))/255;
        [whiskers,snout]=preprocess(img,background);
        imwrite(uint8(255*whiskers),strcat(dirname_prewhiskers,'/',img_name,'.png'),'png');
        imwrite(uint8(255*snout),strcat(dirname_presnout,'/',img_name,'.png'),'png');
   
     %   imshow([img;whiskers;snout]);
     %   drawnow; 
    end
    matlabpool size;
    if(ans)
        matlabpool close;
    end

function [whiskers,snout] = preprocess(img,background)
    result = img-mean(background,3);%remove static background
    result = (result-min(min(result)))/max(max(result)-min(min(result))); %stretch linearly
    sigma = 9;
    blured = imfilter(result,fspecial('gaussian',sigma*3,sigma),'symmetric');

    snout=blured<0.6;

    whiskers=(1-result).*~snout;
