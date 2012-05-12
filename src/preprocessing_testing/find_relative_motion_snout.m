

angle=30
imshow(imrotate(imfilter(double(edge(image2,'prewitt')),fspecial('gaussian',5*3,5)),angle,'crop'));

foreach <angle,pos> calculate correlation, pick the one with the highest and put
in the list of deltas

generate => list [<dangle,dpos>]

to later decode just cumsum([<dangle,dpos>]) to get [<angle,pos>]


this gives how much the head has rotated/moved

