
% G = [[0,1,0,0];
%     [1,0,0,0];
%     [0,0,0,1];
%     [0,0,1,0];];
% 
% A = [[1,1,0,0,0];
%     [1,1,0,0,0];
%     [0,0,0,1,1];
%     [0,0,0,1,1];];

%G=user_network;
%A=user_tags;

load('user_network_100.mat')

A=UT;
G=(G+G')/2;
[n,m] = size(A);

%S = sum(A,2);
%S = repmat(S,1,m);
%P = A ./ S; % probability of tags


count = sum(sum(A>0));

T_p = zeros(1,count);
T_r = zeros(1,count);

cc = 1
counter = 1;
for i = 1:n
    cc = cc + 1 
    for j = 1:n
        if (G(i,j)>0 & i ~= j) 
            % find a user u_k
            k = randi([1 n],1,1);
            while (G(i,k)==0 & i == k & j == k)
                k = randi([1 n],1,1);
            end
            %disp(sprintf('%d,%d,%d', i,j,k))
            % select a tag used by u_i based on the frequency
            %t = find(rand<cumsum(P(i,:)),1,'first')
            
            for t= 1:m
                
                if A(i,t) > 0
                    %d_ij = abs(A(i,t)-A(j,t));
                    %d_ik = abs(A(i,t)-A(k,t));
                    
                    T_p(counter) = 0;
                    if A(j,t) > 0
                       T_p(counter) = 1;
                    end
                    
                    T_r(counter) = 0;
                    if A(k,t) > 0
                       T_r(counter) = 1;
                    end
                    
                    counter = counter+1;
                end
                
            end
            
        end
    end
end

T_p;
T_r;

S = sqrt(((counter-1)*(std(T_p))^2 + (counter-1)*(std(T_r))^2) / (counter+counter-2));

effect_size= (mean(T_p)-mean(T_r))/S


[h,p,ci,stats] =ttest2(T_p,T_r,'Alpha',0.01,'Tail','right');
h
p
