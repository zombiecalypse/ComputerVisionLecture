function FM=fundamental(A)
% SVD of A:
[U D V] = svd(A);

% Fundamental matrix is "vanishing" part (smallest singular value):
f = V(:,9);
F = [f(1) f(2) f(3); f(4) f(5) f(6); f(7) f(8) f(9)];

[FU FD FV]= svd (F);
FDnew = FD;
% ensure rank 2:
FDnew(3,3) = 0;

FM = FU*FDnew*FV';

end
