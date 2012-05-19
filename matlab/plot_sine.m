points = cat(3, [
    245 84;
    285 90;
    332 88;
    366 80;
    387 71], [158 80;
              141 85;
              %111 84;
              97 81;
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

order = 3;

for n = 1:size(points, 3)
    x = points(:,1,n);
    x0 = x(1);
    x = x - x0;
    L = x(5);
    
    y = points(:,2,n);
    y0 = y(1);
    y = y - y0;
    
    A = zeros(length(x),order);
    for m=1:order
        A(:,m) = sin(pi * x * m / 2 / L);
    end
    %x.^2 x.^3 x.^4];
    a = A\y;
    
    plotX = min(x):max(x);

    X = zeros(length(plotX), order);
    for m=1:order
        X(:,m) = sin(pi * plotX * m / 2 / L);
    end

    Y = X * a;
    %Y = a(1) + a(2)*X + a(3)*X.^2 + a(4)*X.^3;% + a(5)*X.^4;
    
    plot(plotX + x0, Y + y0, 'g--', points(:,1,n), points(:,2,n), 'rx');
end

print(figure(1), 'rat-vanilla.png', '-dpng');
print(figure(2), 'rat-sines.png', '-dpng');
