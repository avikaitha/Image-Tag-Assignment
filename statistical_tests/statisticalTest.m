

G=user_network;
A=user_tags;

[n,m] = size(A);

%S = sum(A,2);
%S = repmat(S,1,m);
%P = A ./ S; % probability of tags


count = sum(sum(A));

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
                    d_ij = abs(A(i,t)-A(j,t));
                    d_ik = abs(A(i,t)-A(k,t));
                    
                    if d_ij < d_ik
                       T_p(counter) = 1;
                    end
                    
                    if d_ik < d_ij
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

[h,p,ci,stats] =ttest2(T_p,T_r,'Alpha',0.01,'Tail','right');
h
p
