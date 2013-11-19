K = [
	-83-1/3, 0, 250; 
	0, -83-1/3, 250;
 	0, 0, 1];
fr = 4;
fl = 4;

limg = double(imread('matched/left.jpg'));
rimg = double(imread('matched/right.jpg'));
[h,w] = size(limg);

p = csvread('matched/matched.list');
n = size(p)(1);
sample = p(randsample(n, n/10), :);
X1 = sample(:, 1);
Y1 = h - sample(:, 2);
X2 = sample(:, 3);
Y2 = h - sample(:, 4);

A = create_a([X1, Y1], [X2, Y2]);

FM = fundamental(A)

rank = rank(FM)

E = K' * FM * K;

[U, S, V] = svd(E);
% assert that S(1,1) approx S(2,2) and
%             S(3,3) approx 0

W = [0, -1, 0; 1, 0, 0; 0, 0, 1];

% see report to reduce WTF

T = V * W * S * V';
R = U * W' * V'

t = [T(3,2), T(1, 3), T(2, 1)]
