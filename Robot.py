class Robot:
	def __init__(self, nix, niv, nl):
		self.l = nl
		self.e = [0 for _ in range(self.l)] # Error
		self.x = [0 for _ in range(self.l)] # Position
		self.v = [0 for _ in range(self.l)] # Velocity
		self.a = [0 for _ in range(self.l)] # Acceleration
		self.f = [0 for _ in range(self.l)] # Force
		self.m = 1000.0 # Mass
		self.k = 1.0 # Spring Constant
		self.mu = 0.0 # Friction
		self.mf = 1.0 # Max force
		self.c = "Red" # Color
		
		self.ix = nix
		self.iv = niv

	def s(self):
		s1 = -self.mu / (2.0 * self.m)
		s2 = (self.mu ** 2 - 4 * self.m * self.k) ** 0.5 / (2.0 * self.m)
		return [s1+s2, s1-s2]

	def acc(self, d):
		pass

	def mag(l):
		return sum([i**2 for i in l])**0.5

	def energy():
		return None

	def goal(self, t):
		return 0

	def feq_spring(self, t):
		return -self.k * self.x[t-1] - self.mu * self.v[t-1]

	def feq(self, t):
		pass

	def pid(self):
		self.x[0] = self.ix
		self.v[0] = self.iv
		for t in range(1, self.l):
			self.e[t] = self.goal(t) - self.x[t-1]
			self.f[t] = self.feq(t)
			self.a[t] = self.f[t] / self.m
			self.v[t] += self.a[t]
			self.x[t] += self.v[t]
		return None
  
	def info(self):
		return f"ix = {self.ix}, iv = {self.iv}, k = {self.k}, mu = {self.mu}"