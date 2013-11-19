graphics_toolkit fltk;
function im=as_gray(f)
	image = imread(f);
	s = size(image);
	if size(s) == 3
					im = double(rgb2gray(image));
	else
					im = double(image);
	endif
end
list =['r' 'b' 'g' 'y' 'm' 'k' 'w' 'c'];

left_image = as_gray('stereo/cor/bt.000.pgm');
right_image = as_gray('stereo/cor/bt.001.pgm');
figure(1);
axl = subplot(1,2,1);
imagesc(left_image); colormap(gray); title('Click a point and then'); axis image;
axr = subplot(1,2,2);
imagesc(right_image); colormap(gray); title('Click a corresponding point afterwards on the Right');axis image;

lpoints = zeros(8,2);
rpoints = zeros(8,2);

li = 1;
ri = 1;

while li <= 8 || ri <= 8
		figure(1);
    subplot(1,2,1);
    
    [p1,p2, b] = ginput(1), axis = gca()
		p = [p1,p2];
		puts("l");
		disp(p)
		lpoints(li, :) = p;
		hold on;
		plot(lpoints(li, 1),lpoints(li, 2),'r*');
		li += 1

		subplot(1,2,2);
    [p1,p2, b] = ginput(1), axis = gca()
		p = [p1,p2];
		puts("r");
		disp(p)
		rpoints(ri, :) = p;
		hold on;
		plot(rpoints(ri, 1),rpoints(ri, 2),'r*');
		ri += 1
end

close all;

% finding A matrix:

for i=1:8
  
    x1 = lpoints(i,1);
    y1 = lpoints(i,2);
    x2 = rpoints(i,1);
    y2 = rpoints(i,2);
    A(i,:) = [x1*x2 y1*x2 x2 x1*y2 y1*y2 y2 x1 y1 1];
    
end

% SVD of A:
[U D V] = svd(A);

% Fundamental matrix is "vanishing" part (smallest singular value):
f = V(:,9);
F = [f(1) f(2) f(3); f(4) f(5) f(6); f(7) f(8) f(9)];

[FU FD FV]= svd (F);
FDnew = FD;
% ensure rank 2:
FDnew(3,3) = 0;

FM = FU*FDnew*FV' ;

% Plotting epipolar line:


[rows cols] = size(left_image);

figure(1);
subplot(1,2,1);
imagesc(left_image);
colormap(gray);
title('Click here');

subplot(1,2,2);
imagesc(right_image);
colormap(gray);
title('Corresponding epipolar line');

for i=0:7
		
		subplot(1,2,1);
		[left_x left_y, b] = ginput(1);
		hold on;
		plot(left_x,left_y,'r*');

		% Finding the epipolar line on the right image:
		left_P = [left_x; left_y; 1];

		right_P = FM*left_P;  % FM translates the two

		right_epipolar_x=1:2*rows;
		% ax+by+c=0
		% => y = (-c-ax)/b
		right_epipolar_y=(-right_P(3)-right_P(1)*right_epipolar_x)/right_P(2);
		subplot(1,2,2);
		hold on;
		plot(right_epipolar_x,right_epipolar_y,list(mod(i,8)+1));

		% Epipole corresponds to smallest singular value (ideally 0)
		left_epipole = FV(:,3);
		left_epipole = left_epipole/left_epipole(3)
		
		left_epipolar_x = 1:2*rows;
		left_epipolar_y = left_y + (left_epipolar_x-left_x)*(left_epipole(2)-left_y)/(left_epipole(1)-left_x);
		subplot(1,2,1);
		hold on;
		plot(left_epipolar_x,left_epipolar_y,list(mod(i,8)+1));
end
