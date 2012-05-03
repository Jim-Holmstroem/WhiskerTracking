points = [
245 84;
285 90;
332 88;
366 80;
387 71];

x = points(:,1);
y = points(:,2);

A = [[1;1;1;1;1] x x.^2 x.^3 x.^4];
a = A\y;

X = 0:640;
Y = a(1) + a(2)*X + a(3)*X.^2 + a(4)*X.^3 + a(5)*X.^4;

I = plot_spline_load_image();
figure(1);
clf;
imshow(I);
hold on;
plot(X,Y, 'g--');
