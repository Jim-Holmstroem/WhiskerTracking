function [] = Lp_analytical(func,func_name,param_string,range)
%
% a matlab script that generates a python script
% calculates the Lp norm of the function analytically
%
% Example: Lp_analytical(sym('a*x^2+b*x'),'poly2','a,b',1:10)
%
% Note: L is added automatic
%
%

    file = fopen(strcat('output/Lp_',func_name,'_',int2str(min(range)),'-',int2str(max(range)),'.py'),'w')

    for it=range,
        Lp = int(func^it,sym('x'),sym('0'),sym('L'));
	anal_solution=strrep(char(Lp),'^','**');
	
        outputrow=sprintf('def L%s_%s(%s,L):\n    return %s\n',int2str(it),func_name,param_string,anal_solution)
	fprintf(file,'%s',outputrow);
    end

