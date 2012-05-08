points = cat(3, [
    245 84;
    285 90;
    332 88;
    366 80;
    387 71], [158 80;
              141 85;
              111 84;
              79 82;
              117 84], [239 98;
                    256 111;
                    281 129;
                    323 154;
                    385 178], [171 104;
                    161 124;
                    149 146;
                    136 166;
                    122 185]);

I = plot_spline_load_image();
figure(1);
imshow(I);

figure(2);
clf;
imshow(I);
hold on;

for n = 1:size(points, 3)
    x = points(:,1,n);
    y = points(:,2,n);
    
    A = [[1;1;1;1;1] x x.^2 x.^3 x.^4];
    a = A\y;
    
    X = min(x):max(x);
    Y = a(1) + a(2)*X + a(3)*X.^2 + a(4)*X.^3 + a(5)*X.^4;
    
    plot(X,Y, 'g--');
end
