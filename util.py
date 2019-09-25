def checksum(x):
	n = len(x)
	if n%2 == 1:
		x += bytes([0])
		n +=1
	s = 0
	t = n // 2
	for i in range (t):
		y = 2*i
		s ^= (x[y]<<8 + x[y+1])
		print(s)
		#print(s)
	return s%65536


print (checksum(x))
