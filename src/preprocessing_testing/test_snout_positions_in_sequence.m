
test_range=370:500;
ref=(double(imread(strcat('frames/m8_multi-frames/preprocessed_snout/frame-0',int2str(test_range(1)),'.png'))));

imgs=zeros([size(ref) size(test_range,1)]);

for frame=test_range
    imgs(:,:,frame)=(double(imread(strcat('frames/m8_multi-frames/preprocessed_snout/frame-0',int2str(test_range(frame)),'.png'))));
end

disp('loading done');
positions = snout_position_in_sequence(ref,imgs);


