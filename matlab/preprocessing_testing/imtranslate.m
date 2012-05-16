function [res] = imtranslate(img,dx,dy)
% IMTRANSLATE Translate image
% B = IMTRANSLATE(A,DX,DY) translates the image and crops it accordingly, where
% dx and dy are integers. The background is zeros.
    res = img; %more consistant this way 
    assert(uint8(abs(dx))==abs(dx)&uint8(abs(dy))==abs(dy))
   
    %TEST OK: all cases checked with img=[magic(5);magic(5)];

    W=size(img,2);
    H=size(img,1);

    if(abs(dx)>=W | abs(dy)>=H)
        res = zeros([H W]); %translated outside frame 
        dx=0;
        dy=0; %abort further execution
    end

    if(dx~=0)
        if(dx>0)
            res = [zeros(H,abs(dx)),res(:,1:(end-dx))];
        else
            res = [res(:,(1+abs(dx)):end),zeros(H,abs(dx))];
        end
    end
    if(dy~=0)
        if(dy>0)
            res = [zeros(abs(dy),W);res(1:(end-dy),:)];
        else
            res = [res((1+abs(dy)):end,:);zeros(abs(dy),W)];
        end
    end
