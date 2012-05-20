function preprocess_whisker( directory, filename ) 
    % preprocess the images trying to pickout the whiskers (making them white)
    %
    %

    
    bnames=dir(strcat(directory,'/background/*.png'));
    B=size(bnames,1);

    background=zeros([size(imread(strcat(directory,'/background/',bnames(1).name))),B]);

    for it = 1:B
        background(:,:,it)=double(imread(strcat(directory,'/background/',bnames(it).name)))/255;
    end
    
    img=double(imread(strcat(directory,'/',filename,'.png')))/255;
    blur=blurry(img,background);
    bg=BG(img,background);
    sub=subtracted(img,background);

    imwrite(uint8(255*blur),strcat(filename,'_blur.png'),'png');
    imwrite(uint8(255*bg),strcat(filename,'_bg.png'),'png');
    imwrite(uint8(255*sub),strcat(filename,'_sub.png'),'png');

function [blured] = blurry(img,background)
    result = img-mean(background,3);%remove static background
    result = (result-min(min(result)))/max(max(result)-min(min(result))); %stretch linearly
    sigma = 9;
    blured = imfilter(result,fspecial('gaussian',sigma*3,sigma),'symmetric');

function [bg] = BG(img,background)
    bg = mean(background,3);%remove static background

function [sub] = subtracted(img,background)
    sub = img-mean(background,3);%remove static background
    sub = (sub-min(min(sub)))/max(max(sub)-min(min(sub))); %stretch linearly


