import numpy as np


class Robot:
	def __init__(self, nid, i, nl, nc):
		self.id   = nid		# Serial Identification Number
		self._skl = i[0]	# Time scaling
		self._ix  = i[1]	# Initial Position
		self._iv  = i[2]	# Initial Velocity
		self._p   = i[3]	# Proportional Coefficient
		self._i   = i[4]	# Integral Coefficient
		self._d   = i[5]	# Derivative Coefficient
		self._k   = i[6]	# Spring Constant
		self._m   = i[7]	# Mass
		self._mu  = i[8]	# Friction
		self._mf  = i[9]	# Max force
		self.l = nl				# Simulation Length
		self.g = np.zeros(self.l) # Goal
		self.e = np.zeros(self.l) # Error
		self.x = np.zeros(self.l) # Position
		self.v = np.zeros(self.l) # Velocity
		self.a = np.zeros(self.l) # Acceleration
		self.f = np.zeros(self.l) # Total Force
		self.fp = np.zeros(self.l) # Force due to proportion
		self.fi = np.zeros(self.l) # Force due to integration
		self.fd = np.zeros(self.l) # Force due to derivation
		self.fk = np.zeros(self.l) # Force due to spring
		self.fftr = np.zeros(self.l) # Real FFT of Pos
		self.ffti = np.zeros(self.l) # Im FFT of Pos
		self.atgoal = np.zeros(self.l) # At Goal
		self.overshooting = np.zeros(self.l) # Overshooting
		self.c = nc # Color
		self.info = ""
		self.stats = ""
		self.linevis = [False for _ in range(12)]

		self.goal()
		self.sim()

	def s(self):
		s1 = -self._mu / (2.0 * self.m)
		s2 = (self._mu ** 2 - 4 * self.m * self._p) ** 0.5 / (2.0 * self.m)
		return [s1+s2, s1-s2]

	def mag(l):
		return sum([i**2 for i in l])**0.5

	def energy():
		return None

	def goal(self):
		for s in range(1, self.l):
			t = s * self._skl
			#self.g[s] = np.sin(t * (2.0 * np.pi))
			#self.g[s] = self.x[s - 1]
			#self.g[s] = np.floor(t) % 10.0
			self.g[s] = self.id + 1
		return None

	def feq(self, t, s):
		self.fp[s] = self._p * self.e[s]
		self.fi[s] = self._i * (sum(self.e[s - min(100, s):s]) * self._skl)
		self.fd[s] = self._d * (self.e[s] - self.e[s - 1]) / self._skl
		self.fk[s] = -self._k * self.x[s - 1]
		self.f[s] = self.fp[s] + self.fi[s] + self.fd[s] + self.fk[s]
		return self.f[s]

	def sim(self):
		twopi = 2.0 * np.pi
		# Take notes
		signerror = 0.0
		tforce = 0.0
		nerror = 0.0
		terror = 0.0
		tlosses = 0.0
		tatgoal = 0.0
		overshot = 0.0
		tovershot = 0.0
		wavelength = 0.0

		# Initialize
		self.x[0] = self._ix
		peak = self.x[0]
		oldpeak = self.x[0]
		self.v[0] = self._iv
		self.e[0] = self.g[0] - self.x[0]
		#signerror = self.e[0] / abs(self.e[0])

		# Simulate
		for s in range(1, self.l):
			t = s * self._skl
			# Error
			self.e[s] = self.g[s] - self.x[s - 1]
			nerror += abs(self.e[s])
			terror += self.e[s]
			# Generate required thrust
			f = self.feq(t, s)
			# Generate actual available thrust
			f = min(self.mf, f) if f > 0 else max(-self.mf, f)
			# Accumulate total forces
			tforce += abs(f)
			# Generate force due to friction
			loss = self._mu * self.v[s - 1] * self._skl
			# Accumulate total losses
			tlosses += loss
			# Sum total force
			self.f[s] = f - loss
			# Physics
			self.a[s] = self.f[s] / self.m
			self.v[s] = self.v[s - 1] + self.a[s] * self._skl
			self.x[s] = self.x[s - 1] + self.v[s] * self._skl

			if self.x[s] >= self.x[s - 1]:
				peak = s
			else:
				if peak == s - 1:
					wavelength = (peak - oldpeak) * self._skl
					oldpeak = peak

			if abs(self.g[s] - self.x[s]) < abs(self._skl):
				self.atgoal[s] = True
				tatgoal += 1
			else:
				self.atgoal[s] = False
			if abs(self.x[s] - self.x[0]) > abs(self.g[s] - self.x[0]):
				self.overshooting[s] = True
				overshot += self.v[s]
			else:
				self.overshooting[s] = False

		# Update information
		s1, s2 = self.s()
		c = 2 * (self._k * self._m) ** 0.5
		f = (self._k / self._m) ** 0.5
		freq = 0.0 if wavelength == 0.0 else 1.0 / wavelength * twopi
		self.info = f"ix = {self._ix:.3f}m, iv = {self._iv:.3f}m/s, p = {self._p:.3f}, i = {self._i:.3f}, d = {self._d:.3f}, "
		self.info += f"k = {self._k:.3f}, m = {self._m:.3f}kg, mu = {self._mu:.3f}, mf = {self._mf:.3f}N, "
		self.info += f"s = [{s1:.3f}, {s2:.3f}], c = {c:.3f}, f = {f:.3f}, freq = {freq:.3f}/2pi        "

		# Calculate post-sim stats
		avg = sum(self.x) / self.l
		f = np.fft.fft(self.x + avg)
		self.fftr, self.ffti = f.real, f.imag
		#for i in range(len(self.fft)):
		#	print(f, " = ", self.fft[f])

		self.stats = f"Total force = {tforce:.3f}, net error = {nerror:.3f}, total error = {terror:.3f}, "
		self.stats += f"total losses = {tlosses:.3f}, avg = {avg:.3f}, "
		self.stats += f"freqr = {max(self.fftr):.3f}, freqr = {max(self.ffti):.3f}, "
		self.stats += f"total at goal = {tatgoal/self.l:05.2%}, total overshoot = {overshot:.3f}"

		return None

	@property
	def skl(self):
		return self._skl
	@skl.setter
	def skl(self, n):
		if self._skl != n:
			self._skl = n
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
	def k(self):
		return self._k
	@k.setter
	def k(self, n):
		if self._k != n:
			self._k = n
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
