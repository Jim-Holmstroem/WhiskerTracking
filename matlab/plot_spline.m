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

degree = 3

for n = 1:size(points, 3)
    x = points(:,1,n);
    y = points(:,2,n);
    
    A = zeros(length(x),degree+1);
    for m=0:degree
        A(:,m+1) = x.^m;
    end
    %x.^2 x.^3 x.^4];
    a = A\y;
    
    plotX = min(x):max(x);

    X = zeros(length(plotX), degree+1);
    for n=0:degree
        X(:,n+1) = plotX.^(n);
    end

    Y = X * a;
    %Y = a(1) + a(2)*X + a(3)*X.^2 + a(4)*X.^3;% + a(5)*X.^4;
    
    plot(plotX,Y, 'g--');
end

print(figure(1), 'rat-vanilla.png', '-dpng');
print(figure(2), 'rat-splines.png', '-dpng');
