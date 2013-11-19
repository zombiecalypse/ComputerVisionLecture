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

A = create_a(lpoints, rpoints);

FM = fundamental(A)

% Plotting epipolar lines


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
%
% Epipole corresponds to smallest singular value (ideally 0)
right_epipole = null(FM);
right_epipole = right_epipole/right_epipole(3)

left_epipole = null(FM');
left_epipole = left_epipole/left_epipole(3)

puts('3 points from left image');
for i=1:3
		
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
		
		left_epipolar_x = 1:2*rows;
		left_epipolar_y = left_y + (left_epipolar_x-left_x)*(left_epipole(2)-left_y)/(left_epipole(1)-left_x);
		subplot(1,2,1);
		hold on;
		plot(left_epipolar_x,left_epipolar_y,list(mod(i,8)+1));
end

puts('3 points from right image');

for i=1:3
		
		subplot(1,2,2);
		[right_x right_y, b] = ginput(1);
		hold on;
		plot(right_x,right_y,'r*');

		% Finding the epipolar line on the right image:
		right_P = [right_x; right_y; 1];

		left_P = FM'*right_P;  % FM translates the two

		left_epipolar_x=1:2*rows;
		% ax+by+c=0
		% => y = (-c-ax)/b
		left_epipolar_y=(-left_P(3)-left_P(1)*left_epipolar_x)/left_P(2);
		subplot(1,2,1);
		hold on;
		plot(left_epipolar_x,left_epipolar_y,list(mod(i,8)+1));
		
		right_epipolar_x = 1:2*rows;
		right_epipolar_y = right_y + (right_epipolar_x-right_x)*(right_epipole(2)-right_y)/(right_epipole(1)-right_x);
		subplot(1,2,2);
		hold on;
		plot(right_epipolar_x,right_epipolar_y,list(mod(i,8)+1));
end
