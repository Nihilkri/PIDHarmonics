class Robot:
	def __init__(self, nix, niv, nl, nfeq = None):
		self.l = nl
		self.e = [0 for _ in range(self.l)] # Error
		self.x = [0 for _ in range(self.l)] # Position
		self.v = [0 for _ in range(self.l)] # Velocity
		self.a = [0 for _ in range(self.l)] # Acceleration
		self.f = [0 for _ in range(self.l)] # Force
		self.m = 1000.0 # Mass
		self._k = 1.0 # Spring Constant
		self._mu = 0.0 # Friction
		self.mf = 1.0 # Max force
		self.c = "Red" # Color
		
		self._ix = nix
		self._iv = niv
		if nfeq == None:
			self._feq = self.feq_spring
		else:
			self._feq = nfeq
		self.pid()

	@property
	def k(self):
		return self._k
	@k.setter
	def k(self, n):
		self._k = n
		self.pid()

	@property
	def mu(self):
		return self._mu
	@mu.setter
	def mu(self, n):
		self._mu = n
		self.pid()	

	@property
	def ix(self):
		return self._ix
	@ix.setter
	def ix(self, n):
		self._ix = n
		self.pid()	

	@property
	def iv(self):
		return self._iv
	@iv.setter
	def iv(self, n):
		self._iv = n
		self.pid()

	@property
	def feq(self):
		return self._feq
	@feq.setter
	def feq(self, n):
		self._feq = n
		self.pid()

	def s(self):
		s1 = -self._mu / (2.0 * self.m)
		s2 = (self._mu ** 2 - 4 * self.m * self._k) ** 0.5 / (2.0 * self.m)
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
		self.e[t] = self.goal(t) - self.x[t - 1]
		return -self._k * self.x[t - 1] - self._mu * self.v[t - 1]

	def feq(self, t):
		pass

	def pid(self):
		self.x[0] = self._ix
		self.v[0] = self._iv
		for t in range(1, self.l):
			self.f[t] = self._feq(t)
			self.a[t] = self.f[t] / self.m
			self.v[t] = self.v[t - 1] + self.a[t]
			self.x[t] = self.x[t - 1] + self.v[t]
		return None
  
	def info(self):
		return f"ix = {self._ix:.2f}, iv = {self._iv:.2f}, k = {self._k:.2f}, mu = {self._mu:.2f}"