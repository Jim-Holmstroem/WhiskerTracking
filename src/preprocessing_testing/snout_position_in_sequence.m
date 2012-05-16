function positions = snout_position_in_sequence(ref,imgs)
%
% Translates the ref to match each imgs, the 
% searchcenter will be updated according to its last choosen position
%

N=size(imgs,3);%number of frames

positions=zeros(N,4);

gaussian=(fspecial('gaussian',5*3,5));

search_angle=0;%-pi/8:pi/16:(pi/8+pi/16);NOTE currently no support for angles!
assert(search_angle==0);
search_translation=-20:1:(20+1);
A=size(search_angle,2);
T=size(search_translation,2);

search_size=A*T^2;

ref_edge=conv2replicate(edge_response(ref),gaussian);
ref_edge=start_edge/sum(sum(ref_edge));

last.a=0;
last.x=0;
last.y=0;

for frame=N
    img=sequence_frames(:,:,frame);
    img_edge=conv2replicate(edge_response(img),gaussian);
    img_edge=img_edge/sum(sum(img_edge));
    largest_response=([0,0,0,0]); %<dangle,dx,dy,response>
    for at=search_angle
        for xt=search_translation
            for yt=search_translation
                ref_try=imtranslate(ref_edge,last.x+xt,last.y+yt);  
                response=(sum(sum(img.*ref_try))); %correlate the edges
                if(largest_response(4)<response)
                    largest_response=[last.a+at,last.x+xt,last.y+yt,response];
                end
            end
        end
    end
    positions(frame,:)=gather(largest_response)';
    last.a=largest_response(1);
    last.x=largest_response(2);
    last.y=largest_response(3);
    disp(positions(frame,:));
end
