
test_range=370:500;
ref=(double(imread(strcat('frames/m8_multi-frames/preprocessed_snout/frame-0',int2str(test_range(1)),'.png'))));

imgs=zeros([size(ref) size(test_range,1)]);
real_imgs=zeros(size(imgs));

for idx=1:size(test_range,2)
    imgs(:,:,idx)=(double(imread(strcat('frames/m8_multi-frames/preprocessed_snout/frame-0',int2str(test_range(idx)),'.png'))));
    real_imgs(:,:,idx)=(double(imread(strcat('frames/m8_multi-frames/frame-0',int2str(test_range(idx)),'.png'))));
    real_imgs(:,:,idx)=real_imgs(:,:,idx)/255;
    whisker_imgs(:,:,idx)=(double(imread(strcat('frames/m8_multi-frames/preprocessed_whiskers/frame-0',int2str(test_range(idx)),'.png'))));
    whisker_imgs(:,:,idx)=whisker_imgs(:,:,idx)/255;
end

size(imgs)

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

    hold off;
    h=imshow(imtranslate(whisker_imgs(:,:,idx),-position_data(idx,2),-position_data(idx,3)));
    hold on;
    warning('ref_centroid hardcoded')
%    plot(260+position_data(idx,2),85+position_data(idx,3),'rx');
    h=plot(230,53,'rx');
    h=plot(295,57,'rx');
    h=plot(291,64,'rx');
    h=plot(288,73,'rx');
    h=plot(240,77,'rx');
    size(whisker_imgs(:,:,idx))
    disp('test')
    title(strcat('response=',int2str(position_data(idx,4))));
    drawnow;
    pause;
end
end
