function positions = snout_position_in_sequence(ref,imgs)
%
% Translates the ref to match each imgs, the 
% searchcenter will be updated according to its last choosen position
%

N=size(imgs,3);%number of frames

positions=zeros(N,4);

sigma=5;
gaussian=(fspecial('gaussian',3*sigma,sigma));

search_angle=0;%-pi/8:pi/16:(pi/8+pi/16);NOTE currently no support for angles!
assert(search_angle==0);
search_translation=-5:1:5;
A=size(search_angle,2);
T=size(search_translation,2);

search_size=A*T^2;

ref_edge=conv2replicate(edge_response(ref),gaussian);
ref_edge=ref_edge/max(max(ref_edge));

last.a=0; %relative to ref
last.x=0;
last.y=0;

for frame=1:N
    img=imgs(:,:,frame);
    img_edge=conv2replicate(edge_response(img),gaussian);
    img_edge=img_edge/max(max(img_edge));
    largest_response=([0,0,0,0]); %<dangle,dx,dy,response>
    for at=search_angle
        for xt=search_translation
            for yt=search_translation
                ref_try=imtranslate(ref_edge,last.x+xt,last.y+yt);
                mask=img_edge.*ref_try;
                response=(sum(sum(mask))); %correlate the edges
                if(largest_response(4)<response)
                    largest_response=[last.a+at,last.x+xt,last.y+yt,response];
                end
            end
        end
    end

    %imshow(img_edge/2+imtranslate(ref_edge,largest_response(2),largest_response(3))/2);

    render = zeros([size(img_edge) 3]);
    render(:,:,1) = img_edge;
    render(:,:,2) = imtranslate(ref_edge,largest_response(2),largest_response(3));
    imshow(render);
    
    drawnow;

    pause;

    positions(frame,:)=gather(largest_response)';
    last.a=largest_response(1);
    last.x=largest_response(2);
    last.y=largest_response(3);
    disp(positions(frame,:));
end
