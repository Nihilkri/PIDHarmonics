import numpy as np


class Robot:
	def __init__(self, nid, i, nl, nc, nfeq = "PID"):
		self.id = nid	  # Serial Identification Number
		self._ix = i[0]	# Initial Position
		self._iv = i[1]	# Initial Velocity
		self._p = i[2]  # Proportional Coefficient / Spring Constant
		self._i = i[3]  # Integral Coefficient
		self._d = i[4]  # Derivative Coefficient
		self._m = i[5]  # Mass
		self._mu = i[6] # Friction
		self._mf = i[7] # Max force
		self.l = nl			# Simulation Length
		self.e = [0 for _ in range(self.l)] # Error
		self.x = [0 for _ in range(self.l)] # Position
		self.v = [0 for _ in range(self.l)] # Velocity
		self.a = [0 for _ in range(self.l)] # Acceleration
		self.f = [0 for _ in range(self.l)] # Force
		self.g = [0 for _ in range(self.l)] # Goal
		self.c = nc # Color
		
		if nfeq == "Spring":
			self._feq = self.feq_spring
		elif nfeq == "PID":
			self._feq = self.feq_pid
		else:
			self._feq = nfeq
		self.sim()

	@property
	def ix(self):
		return self._ix
	@ix.setter
	def ix(self, n):
		if self._ix != n:
			self._ix = n
			self.sim()	

	@property
	def iv(self):
		return self._iv
	@iv.setter
	def iv(self, n):
		if self._iv != n:
			self._iv = n
			self.sim()

	@property
	def p(self):
		return self._p
	@p.setter
	def p(self, n):
		if self._p != n:
			self._p = n
			self.sim()

	@property
	def i(self):
		return self._i
	@i.setter
	def i(self, n):
		if self._i != n:
			self._i = n
			self.sim()

	@property
	def d(self):
		return self._d
	@d.setter
	def d(self, n):
		if self._d != n:
			self._d = n
			self.sim()

	@property
	def m(self):
		return self._m
	@m.setter
	def m(self, n):
		if self._m != n:
			self._m = n
			self.sim()

	@property
	def mu(self):
		return self._mu
	@mu.setter
	def mu(self, n):
		if self._mu != n:
			self._mu = n
			self.sim()	

	@property
	def mf(self):
		return self._mf
	@mf.setter
	def mf(self, n):
		if self._mf != n:
			self._mf = n
			self.sim()	

	@property
	def feq(self):
		return self._feq
	@feq.setter
	def feq(self, n):
		if self._feq != n:
			self._feq = n
			self.sim()

	def s(self):
		s1 = -self._mu / (2.0 * self.m)
		s2 = (self._mu ** 2 - 4 * self.m * self._p) ** 0.5 / (2.0 * self.m)
		return [s1+s2, s1-s2]

	def mag(l):
		return sum([i**2 for i in l])**0.5

	def energy():
		return None

	def goal(self, t):
		#return np.sin(t / 100.0)
		return 0

	def feq_spring(self, t):
		return -self._p * self.x[t - 1]

	def feq_pid(self, t):
		p = self._p * self.e[t]
		i = 0
		d = 0
		return p + i + d


	def feq(self, t):
		pass

	def sim(self):
		self.x[0] = self._ix
		self.v[0] = self._iv
		for t in range(1, self.l):
			self.g[t] = self.goal(t)
			self.e[t] = self.g[t] - self.x[t - 1]
			self.f[t] = self._feq(t) - self._mu * self.v[t - 1]
			self.a[t] = self.f[t] / self.m
			self.v[t] = self.v[t - 1] + self.a[t]
			self.x[t] = self.x[t - 1] + self.v[t]
		return None
  
	def info(self):
		s1, s2 = self.s()
		txt = f"ix = {self._ix:.2f}, iv = {self._iv:.2f}, p = {self._p:.2f}, i = {self._i:.2f}, d = {self._d:.2f}, "
		txt += f"m = {self._m:.2f}, mu = {self._mu:.2f}, mf = {self._mf:.2f}, s = [{s1:.2f}, {s2:.2f}]"
		return txt