%% Investigation of some approximations assumed by the mechanical model
% 
% The \emph{action} of a mechanical process is defined as
%
% \int_{t_0}^{t_1} (T - U) dt, 
%
% where T is kinetic energy and U is potential energy.
% The Hamilton principle states that for a mechanical process, the action
% is minimized.
% 
% Consider a string of length l, with elasticity module E and whose
% cross-section has the moment of inertia I. Consider it as a chain of
% point masses joined by springs with spring constant S.
% For this string,
% 
% T = 0.5 * \int_0^l \rho (du/dt)^2 dx, and
% U = 0.5 * \int_0^l [S (du/dx)^2 + EI (d^2u/dx^2)^2] dx,
% where u(x, t) is the displacement of the string at time t.
%
% Physical interpretation:
% 1/2 * \rho (du/dt)^2 dx is the kinetic energy of a string element with
%     density \rho and length dx, travelling at speed du/dt
%
% (du/dx)^2 is the second order Taylor expansion of
%     (\sqrt(dx^2+du^2) - dx)/dx, the relative stretch of a spring whose
%     equillibrium is a distance dx along the x axis, and whose right end
%     is displaced a distance du in the u direction. The elastic energy
%     needed to stretch a string element of length dx in this fashion is
%     this S * \sin((du/dx)^2). This, in turn, can be Taylor expanded to
%     the first order as simply (du/dx)^2, if (du/dx)^2 is small.
%
% EI(d^2u/dx^2)^2 dx is the elastic energy needed to bend a string element
%     of length dx. It is zero where the string is locally straight and
%     high where the string bends a lot in a short x distance.
%

%% Comparisons between approximations and true values

max_relative_diff = 0.05;

%% String stretch
% True value: (sqrt(dx^2+du^2)-dx)/dx = sqrt(1 + (du/dx)^2) - 1
% Approximation: 1/2*(du/dx)^2

x = 0:0.001:1;
test_approximation(x, 0.5*x.^2, sqrt(1 + x.^2) - 1, max_relative_diff)
title('Comparison between 0.5x^2 and sqrt(1+x^2)-1')

%% Taylor expansion of sin
% True value: sin(x)
% Approximation: x

x = 0:0.001:1;
test_approximation(x, x, sin(x), max_relative_diff)
title('Comparison between x and sin(x)')
