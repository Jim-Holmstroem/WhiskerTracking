function [] = test_approximation(x, approx, true, max_relative_diff)
%TEST_APPROXIMATION Plots true, approx and rel_diff=(approx-true)./true
% against x and finds the greatest n such that rel_diff(n) <=
% max_relative_diff
%   Detailed explanation goes here

rel_diff = (approx - true)./true;
figure;
plot(x, approx, x, true, x, rel_diff)
title('Approximation test')
xlabel('x');
legend('Approximation', 'True value', 'Relative Difference');

for n=1:length(x)-1
    if(rel_diff(n+1) > max_relative_diff)
        break
    end
end
disp(strcat('Maximum x: ', num2str(x(n))))

end
