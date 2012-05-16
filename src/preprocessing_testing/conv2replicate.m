function res = conv2replicate(img,filter)
%
% Avoids nasty imageedges when differentiating
%
    res = padarray(conv2(img,filter,'valid'),(size(filter)-1)/2,'replicate','both');
