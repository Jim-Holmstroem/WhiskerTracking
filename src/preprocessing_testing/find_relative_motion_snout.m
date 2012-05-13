

%angle=30
%imshow(imrotate(imfilter(double(edge(image2,'prewitt')),fspecial('gaussian',5*3,5)),angle,'crop'));

%foreach <angle,pos> calculate correlation, pick the one with the highest and put
%in the list of deltas

%generate => list [<dangle,dpos>]

%to later decode just cumsum([<dangle,dpos>]) to get [<angle,pos>]

%this gives how much the head has rotated/moved


%NOTE dangle is given according to the center of the image, this must be taken into
%account later when one tries to transform the whiskersbase

%to fix the issue with image edges when, no support for even-filterse, sry 
gaussian=gpuArray(fspecial('gaussian',5*3,5));
prewitt =gpuArray(fspecial('prewitt'));

conv2replicate = @(img,filter) padarray(conv2(img,filter,'valid'),(size(filter)-1)/2,'replicate','both');

edge_response = @(img) sqrt( ...
                            conv2replicate(img,prewitt ).^2+ ...
                            conv2replicate(img,prewitt').^2  ...
                           );

search_angle=0;%-pi/8:pi/16:(pi/8+pi/16);
search_translation=-25:1:(25+1);
A=size(search_angle,2);
T=size(search_translation,2);

%search_size=A*T^2;

start=gpuArray(double(imread('frames/m8_multi-frames/preprocessed_snout/frame-0535.png')));
image1=gpuArray(double(imread('frames/m8_multi-frames/preprocessed_snout/frame-0539.png')));

start_edge=conv2replicate(edge_response(start),gaussian);
start_edge=start_edge/sum(sum(start_edge));

image1_edge=conv2replicate(edge_response(image1),gaussian);
image1_edge=image1_edge/sum(sum(image1_edge));

largest_response=gpuArray([0,0,0,0]); %<dangle,dx,dy,response>

for at=search_angle
    for xt=search_translation
        for yt=search_translation
            %image_rot_trans=imtranslate(imrotate(image1_edge,(180/pi)*at,'bilinear','crop'),xt,yt); %rotate then translate
            image_rot_trans=imtranslate(image1_edge,xt,yt); %rotate then translate
            image_rot_trans=image_rot_trans/sum(sum(image_rot_trans));
            response=(sum(sum(image_rot_trans.*start_edge))); %correlate the edges
            
            if(largest_response(4)<response)
                largest_response=[at,-xt,-yt,response];
            end
 %           search_size=search_size-1;
 %           if(mod(search_size,100)==0)
 %               disp(search_size)
 %           end
        end
    end
end

gather(largest_response)

%THE RESULT
%start_rot_trans=imtranslate(imrotate(start_edge,(180/pi)*largest_response(1),'bilinear','crop'),largest_response(2),largest_response(3)); %rotate then translate
%imagesc(start_rot_trans-image1_edge)

