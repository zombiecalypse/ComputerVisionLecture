function A=create_a(lpoints, rpoints)
	if size(lpoints) != size(rpoints)
		error("No matching coordinates");
  end
	n = size(lpoints)(1);
	A = zeros(n, 9);
	for i=1:n
    x1 = lpoints(i,1);
    y1 = lpoints(i,2);
    x2 = rpoints(i,1);
    y2 = rpoints(i,2);
    A(i,:) = [x1*x2 y1*x2 x2 x1*y2 y1*y2 y2 x1 y1 1];
	end
end
