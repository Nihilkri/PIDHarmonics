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
		self.atgoal = [0 for _ in range(self.l)] # At Goal
		self.overshooting = [0 for _ in range(self.l)] # Overshooting
		self.c = nc # Color
		self.info = ""
		self.stats = ""
		
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
		if self._m != n and n > 0:
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
		if self._mf != n and n > 0:
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
		return -1

	def feq_spring(self, t):
		return -self._p * self.x[t - 1]

	def feq_pid(self, t):
		p = self._p * self.e[t]
		i = 0 if t < 10 else self._i * (sum(self.e[t-10:t]) / 10)
		d = self._d * (self.e[t] - self.e[t - 1])
		return p + i + d


	def feq(self, t):
		pass

	def sim(self):
		# Take notes
		se = 0.0
		tforce = 0.0
		nerror = 0.0
		terror = 0.0
		tlosses = 0.0
		tatgoal = 0.0
		overshot = 0.0
		tovershot = 0.0

		# Initialize
		self.x[0] = self._ix
		self.v[0] = self._iv
		self.g[0] = self.goal(0)
		self.e[0] = self.g[0] - self.x[0]
		se = self.e[0] / abs(self.e[0])

		# Simulate
		for t in range(1, self.l):
			# Define goal
			self.g[t] = self.goal(t)
			# Error
			self.e[t] = self.g[t] - self.x[t - 1]
			nerror += abs(self.e[t])
			terror += self.e[t]
			# Generate required thrust
			f = self._feq(t)
			# Generate actual available thrust
			f = min(self.mf, f) if f > 0 else max(-self.mf, f)
			# Accumulate total forces
			tforce += abs(f)
			# Generate force due to friction
			loss = self._mu * self.v[t - 1]
			# Accumulate total losses
			tlosses += loss
			# Sum total force
			self.f[t] = f - loss
			# Physics
			self.a[t] = self.f[t] / self.m
			self.v[t] = self.v[t - 1] + self.a[t]
			self.x[t] = self.x[t - 1] + self.v[t]

			if abs(self.g[t] - self.x[t]) < abs(self._mf):
				self.atgoal[t] = True
				tatgoal += 1
			else:
				self.atgoal[t] = False
			if abs(self.x[t] - self.x[0]) > abs(self.g[t] - self.x[0]):
				self.overshooting[t] = True
				overshot += self.v[t]
			else:
				self.overshooting[t] = False

		# Update information
		s1, s2 = self.s()
		self.info = f"ix = {self._ix:.3f}, iv = {self._iv:.3f}, p = {self._p:.3f}, i = {self._i:.3f}, d = {self._d:.3f}, "
		self.info += f"m = {self._m:.3f}, mu = {self._mu:.3f}, mf = {self._mf:.3f}, s = [{s1:.3f}, {s2:.3f}]        "

		# Calculate post-sim stats
		self.info += f"Total force = {tforce:.3f}, net error = {nerror:.3f}, total error = {terror:.3f}, "
		self.info += f"total losses = {tlosses:.3f}, "
		self.info += f"total at goal = {tatgoal/self.l:05.2%}, total overshoot = {overshot:.3f}"

		return None
