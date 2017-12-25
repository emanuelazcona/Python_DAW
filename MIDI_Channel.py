import wave
import struct
import numpy as np
import pygame
import math
from math import cos, sin, atan2, tan
from scipy import signal
import cmath

CHUNK = 1024 * 3
MAXVALUE = (2.0**15) - 1
MINVALUE = -(2.0**15)

class MIDI_Channel:

	def __init__(self, channel):
		self.channel_num = channel
		self.gain = 0.5
		self.left_gain = 1.0
		self.right_gain = 1.0
		self.on = False

	def MIDI_wav(self, filename):
		self.wf = wave.open(filename, 'rb')
		self.channels = self.wf.getnchannels()
		self.rate = self.wf.getframerate()
		self.length = self.wf.getnframes()
		self.width = self.wf.getsampwidth()
		self.input = False
		self.output = True
		self.data = self.wf.readframes(CHUNK)

	def MIDI_pad(self, decay_time, freq1, key1, freq2, key2, freq3, key3, freq4, key4):
		self.channels = 2
		self.rate = 16000
		self.width = 2
		self.input = False
		self.output = True
		self.decay = decay_time

		if (key1 == "i" or key1 == "I"):
			key1 = pygame.K_i
		elif (key1 == "o" or key1 == "O"):
			key1 = pygame.K_o
		elif (key1 == "k" or key1 == "K"):
			key1 = pygame.K_k
		elif (key1 == "l" or key1 == "L"):
			key1 = pygame.K_l

		if (key2 == "i" or key2 == "I"):
			key2 = pygame.K_i
		elif (key2 == "o" or key2 == "O"):
			key2 = pygame.K_o
		elif (key2 == "k" or key2 == "K"):
			key2 = pygame.K_k
		elif (key2 == "l" or key2 == "L"):
			key2 = pygame.K_l

		if (key3 == "i" or key3 == "I"):
			key3 = pygame.K_i
		elif (key3 == "o" or key3 == "O"):
			key3 = pygame.K_o
		elif (key3 == "k" or key3 == "K"):
			key3 = pygame.K_k
		elif (key3 == "l" or key3 == "L"):
			key3 = pygame.K_l
		if (key4 == "i" or key4 == "I"):
			key4 = pygame.K_i
		elif (key4 == "o" or key4 == "O"):
			key4 = pygame.K_o
		elif (key4 == "k" or key4 == "K"):
			key4 = pygame.K_k
		elif (key4 == "l" or key4 == "L"):
			key4 = pygame.K_l
		
		self.freq1 = freq1
		self.pole1 = 0.01**(1.0/(self.decay*self.rate))
		self.omega1 = 2.0 * np.pi * float(self.freq1)/self.rate
		self.a11 = -2 * self.pole1 * cos(self.omega1)
		self.a12 = self.pole1**2
		self.b10 = sin(self.omega1)
		self.key1 = key1

		self.freq2 = freq2
		self.pole2 = 0.01**(0.0/(self.decay*self.rate))
		self.omega2 = 2.0 * np.pi * float(self.freq2)/self.rate
		self.a21 = -2 * self.pole2 * cos(self.omega2)
		self.a22 = self.pole2**2
		self.b20 = sin(self.omega2)
		self.key2 = key2

		self.freq3 = freq3
		self.pole3 = 0.01**(1.0/(self.decay*self.rate))
		self.omega3 = 2.0 * np.pi * float(self.freq3)/self.rate
		self.a31 = -2 * self.pole3 * cos(self.omega3)
		self.a32 = self.pole3**2
		self.b30 = sin(self.omega3)
		self.key3 = key3

		self.freq4 = freq4
		self.pole4 = 0.01**(1.0/(self.decay*self.rate))
		self.omega4 = 2.0 * np.pi * float(self.freq4)/self.rate
		self.a41 = -2 * self.pole4 * cos(self.omega4)
		self.a42 = self.pole4**2
		self.b40 = sin(self.omega4)
		self.key4 = key4

		self.key1_pressed = False
		self.key2_pressed = False
		self.key3_pressed = False
		self.key4_pressed = False


	def open_stream(self, p, sign):
		self.p = p
		self.stream = self.p.open(
								  format = self.p.get_format_from_width(self.width, unsigned = sign),
								  channels = self.channels,
								  rate = self.rate,
								  input = self.input,
								  output = self.output,
								  )

	def close_stream(self):
		self.stream.stop_stream()
		self.stream.close()
		if hasattr(self, "wf"):
			self.wf.close()
		self.p.terminate()

	def play(self, mute, mod, modparam):
		mute = int(not mute)
			
		self.data_tuple = list(struct.unpack('h'*self.channels*CHUNK, self.data))

		if mod[0]:
			b = [tan(modparam[0] * np.pi / self.rate), tan(modparam[0] * np.pi / self.rate)]
			a = [tan(modparam[0] * np.pi / self.rate) + 1, tan(modparam[0] * np.pi / self.rate) - 1]

			out = signal.lfilter(b, a, self.data_tuple)
			self.data_tuple = out
			self.data_tuple = np.clip(self.data_tuple, MINVALUE, MAXVALUE)

		if mod[1]:
			b = [1, -1]
			a = [tan(modparam[1] * np.pi / self.rate) + 1, tan(modparam[1] * np.pi / self.rate) - 1]

			out = signal.lfilter(b,a,self.data_tuple)
			self.data_tuple = out
			self.data_tuple = np.clip(self.data_tuple, MINVALUE, MAXVALUE)

		if mod[2]:

			b_lpf, a_lpf = signal.ellip(7, 0.2, 50, 0.48)
			I = cmath.sqrt(-1)
			K_array = np.linspace(0, 7, 8)
			s = []
			for i in range(len(K_array)):
				s.append( np.exp(I * 0.5 * np.pi * K_array[i]))

			b = []
			a = []
			for i in range(len(s)):
				b.append(b_lpf[i] * s[i])
				a.append(a_lpf[i] * s[i])

			r = signal.lfilter(b, a, self.data_tuple)

			c = [np.exp(2 * I * np.pi * modparam[2] * j / self.rate) for j in range(CHUNK* self.channels)]

			out = np.multiply(r, c)
			out = out.real
			self.data_tuple = out
			self.data_tuple = np.clip(self.data_tuple, MINVALUE, MAXVALUE)

		for i in range(len(self.data_tuple)):
			if (i % 2) == 0:
				self.data_tuple[i] *= ((self.left_gain * self.gain) * mute)

			elif (i % 2) != 0:
				self.data_tuple[i] *= ((self.right_gain * self.gain) * mute)

		self.data_tuple = np.clip(self.data_tuple, MINVALUE, MAXVALUE)
		self.data = struct.pack('h'*self.channels*CHUNK, *self.data_tuple)
		self.stream.write(self.data)
		self.data = self.wf.readframes(CHUNK)

	def play_key(self, mute, key):
		if self.key1 == key:
			a1 = self.a11
			a2 = self.a12
			b0 = self.b10
		elif self.key2 == key:
			a1 = self.a21
			a2 = self.a22
			b0 = self.b20
		elif self.key3 == key:
			a1 = self.a31
			a2 = self.a32
			b0 = self.b30
		elif self.key4 == key:
			a1 = self.a41
			a2 = self.a42
			b0 = self.b40

		y = np.zeros(self.channels*CHUNK)
		x = np.zeros(self.channels*CHUNK)
		x[0] = self.gain*15000

		for n in range(self.channels*CHUNK):
			y[n] = b0 * x[n] - a1 * y[n-1] - a2 * y[n-2]

		y = np.clip(y, MINVALUE, MAXVALUE)
		self.data = struct.pack('h' * len(y), *y)
		self.stream.write(self.data)