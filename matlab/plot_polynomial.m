maxcoeffs = [0 1 0.001 0.00002]';

x = (0:150)';

X = zeros(length(x), length(maxcoeffs));
for n=1:length(maxcoeffs)
  X(:,n) = x.^(n-1);
end

y = X * maxcoeffs;

xoffset = 256-75;
yoffset = 256;

x = x + xoffset;

clf;
hold on;
plot(x, yoffset+y, 'r')
plot(x, yoffset-y, 'r')
plot([0 0 512 512], [0 512 512 0], 'black');
axis equal;

for n=1:1
  randcoeffs = random('uniform', -maxcoeffs, maxcoeffs);
  randy = X * randcoeffs;
  randy = randy + yoffset;
  plot(x, randy, 'g')
end

legend('Max', 'Min', '512x512 Window', 'Randoms')
