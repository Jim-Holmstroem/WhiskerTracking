


test_range=370:500;

assert(min(test_range)>99 & max(test_range)<1000) %no support for this range

dirname='m8_multi-frames';

ref=(double(imread(strcat('frames/',dirname,'/preprocessed_snout/frame-0',int2str(test_range(1)),'.png'))));

imgs=zeros([size(ref) size(test_range,1)]);
real_imgs=zeros(size(imgs));

for idx=1:size(test_range,2)
    imgs(:,:,idx)=(double(imread(strcat('frames/',dirname,'/preprocessed_snout/frame-0',int2str(test_range(idx)),'.png'))));
    real_imgs(:,:,idx)=(double(imread(strcat('frames/',dirname,'/frame-0',int2str(test_range(idx)),'.png'))));
    real_imgs(:,:,idx)=real_imgs(:,:,idx)/255;
    whisker_imgs(:,:,idx)=(double(imread(strcat('frames/',dirname,'/preprocessed_whiskers/frame-0',int2str(test_range(idx)),'.png'))));
    whisker_imgs(:,:,idx)=whisker_imgs(:,:,idx)/255;
end

disp('loading done');
if(~exist('position_data'))
    position_data = snout_position_in_sequence(ref,imgs);
    save('position_data','position_data');
else
    warning('Using precalced data')
    load('position_data');
end

disp('preprocessing done');

while(1)
for idx=1:size(test_range,2)

    %hold off;
    
    img=imtranslate(whisker_imgs(:,:,idx),-position_data(idx,2),-position_data(idx,3)); %assumes pitch black pixels are only those generate by the algorithm, almost completly true got some salt and paper noise in the background but since we will use this to set to the mean color we will not feel the effect.
    %img(find(img==0))=mean(mean(img(find(img~=0))));
%    hold off;
    imshow(img);
    %imwrite(img,strcat('frames/',dirname,'/preprocessed_solid/seq',int2str(min(test_range)),'-',int2str(max(test_range)),'/frame-0',int2str(test_range(idx)),'.png'),'PNG');    

    hold on;
    warning('ref_centroid hardcoded')
%    plot(260+position_data(idx,2),85+position_data(idx,3),'rx');
    plot(230,53,'rx');
    plot(295,57,'rx');
    plot(291,64,'rx');
    plot(288,73,'rx');
    plot(240,77,'rx');
    size(whisker_imgs(:,:,idx))
    disp('test')
    title(strcat('response=',int2str(position_data(idx,4))));
    drawnow;
%    pause;
end
end
