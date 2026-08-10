BLOCKED = set()

with open('hosts') as f:
	for line in f:
		if line.startswith('0.0.0.0'):
			domain = line.split()[1]
			BLOCKED.add(domain)

	
