%   ���� ����������� ������������ ������� 
%A = [ infsup(98,100) infsup(99,101); infsup(97,99) infsup(98,100); infsup(96,98) infsup(97,99) ]
A = [ infsup(50,51) infsup(51,52) infsup(52,53); infsup(52,53) infsup(53,54) infsup(54,55) ]
  
%   ���������� ������� ������ ������� 
m = size(A,1); 
n = size(A,2);   
 
%   ����� ���������� ��������� �������� � ����������� ��������� 
NN = 10; 

%   �������������� ������� ������� ��� A 
Matr1 = ones(m,n); 
Matr2 = ones(m,n);   
  
%   �������������� MinCond - ������� ����� ��������������� �������� 
%   ������, ������������ � �������� ������������ ������� A   
MinCond = Inf; 
  
  
for k = 1:NN 

  
    %   �������� ��������� ������������� ������� EPM �� ����� � 
    %   ������, ��� �� ��������,  ���  �  A  (�������� ��������� 
    %   ������������� �������� ����������� ������ ���������� randi) 
    EPM = randi([0,1],m,n); 
      
    %   ��������� ������� �������, ����������� ��������������� 
    %   ���� �����, � ������������ � ���������� "������������" 
    %   ������� �����������     
    for i = 1:m
        for j = 1:n
            if EPM(i,j) == 0 
                Matr1(i,j) = inf(A(i,j)); 
                Matr2(i,j) = sup(A(i,j)); 
            else 
                Matr1(i,j) = sup(A(i,j));
                Matr2(i,j) = inf(A(i,j));                 
            endif 
        end
    end 
    
    %   ������� ����� ��������������� ���������� 
    %   ������� ������, ������������ ������ ��������  
    c1 = cond(Matr1,2); 
    c2 = cond(Matr2,2); 
    if MinCond > c1 
        MinCond = c1; 
    endif 
    if MinCond > c2 
        MinCond = c2; 
    endif     
    
end 
  
%   ������� ��������� ������� ����� ��������������� 
disp(MinCond); 
  