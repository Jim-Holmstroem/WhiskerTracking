
test_range=370:500;
ref=(double(imread(strcat('frames/m8_multi-frames/preprocessed_snout/frame-0',int2str(test_range(1)),'.png'))));

imgs=zeros([size(ref) size(test_range,1)]);

for idx=1:size(test_range,2)
    imgs(:,:,idx)=(double(imread(strcat('frames/m8_multi-frames/preprocessed_snout/frame-0',int2str(test_range(idx)),'.png'))));
end

size(imgs)

disp('loading done');
positions = snout_position_in_sequence(ref,imgs);
disp('preprocessing done');

while (1)
for idx=1:size(test_range,2)
    hold off;
    imshow(imgs(:,:,idx));
    hold on;
    warning('ref_centroid hardcoded')
    plot(260+positions(idx,2),85+positions(idx,3),'rx');
    title(strcat('response=',int2str(positions(idx,4))));
    drawnow;
    pause;
end
end
