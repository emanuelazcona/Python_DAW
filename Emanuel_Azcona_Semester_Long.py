"""
	Emanuel Azcona, Spring 2016 

	Assignment: Semester Long Project (Music Mixer & MIDI-Drum Pad)

	Course: EE-UY 373 Guided Studies in Electrical Engineering (Spring 2016)

	Several libraries were downloaded and imported from the PyGame website (ex: EasyGame module, 
	for obtaining path's via directory search. The objective of this project was to use already 
	obtained knowledge from this course and prior courses to create an application that does some
	sort of signal processing. My project resides in the topic of MIDI interfaces and audio processing.

	I created a MIDI Channel class and created two instances of that class to emulate two 
	different channels of a standard audio mixer used by producers and audio engineers. A third
	instance of the MIDI Channel class was created but this Channel was modified to work as a MIDI
	input Channel that processed a sound based on which one of four keys were pressed (my defaults
	were: i, o, k, l).
"""

##############################################################################################
# Module Imports

import pygame
import wave
import pyaudio
import time
from math import atan2
import numpy as np
from MIDI_Channel import MIDI_Channel
from pygame.locals import *
from matplotlib import pyplot as plt
from music21 import *

from sys import path
import os.path
thisrep = os.path.dirname(os.path.abspath(__file__))
path.append(os.path.dirname(thisrep))

from EasyGame import pathgetter

##############################################################################################
# Initialization of sources and intial values

source1 = str(pathgetter())
source2 = str(pathgetter())

note1 = note.Note("F#4")
freq1 = note1.pitch.frequency
note2 = note.Note("A#")
freq2 = note2.pitch.frequency
note3 = note.Note("G")
freq3 = note3.pitch.frequency
note4 = note.Note("D")
freq4 = note4.pitch.frequency

Channel_1 = MIDI_Channel(1)
Channel_1.MIDI_wav(source1)
p1 = pyaudio.PyAudio()
Channel_1.open_stream(p1, False)

Channel_2 = MIDI_Channel(2)
Channel_2.MIDI_wav(source2)
p2 = pyaudio.PyAudio()
Channel_2.open_stream(p2, False)

Channel_3 = MIDI_Channel(3)
Channel_3.MIDI_pad(3, freq1, "i", freq2, "o", freq3, "k", freq4, "l")
p3 = pyaudio.PyAudio()
Channel_3.open_stream(p3, False)
Channel_3.gain = 0.25

pygame.init()
screen = pygame.display.set_mode((900, 900))
pygame.display.set_caption('Emanuel Azcona Music Mixer & MIDI-Drum Pad')

done = False

red = (235, 8, 23)
green = (28,239, 70)
blue = (11, 80, 242)

mute1 = False
mute2 = False
mute3 = False

mod1 = [False, False, False]
mod2 = [False, False, False]

mod1param = [0, 0, 0]
mod2param = [0, 0, 0]

num_keys = 4

while not done:
# Program OFF Button	

	for event in pygame.event.get():
		
		if event.type == pygame.KEYDOWN and event.key == pygame.K_0:
			done = True

##############################################################################################
# Channel 1 Controls

		elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
			Channel_1.on = not Channel_1.on
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
			if Channel_1.gain + 0.05 > 1.50:
				Channel_1.gain = 1.50
			else:
				Channel_1.gain += 0.05
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_x:
			if Channel_1.gain - 0.05 < 0.0:
				Channel_1.gain = 0.0
			else:
				Channel_1.gain -= 0.05
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
			if Channel_1.left_gain + 0.1 > 2.0 and Channel_1.right_gain - 0.1 < 0.0:
				Channel_1.left_gain = 2.0
				Channel_1.right_gain = 0.0
			else:
				Channel_1.left_gain += 0.1
				Channel_1.right_gain -= 0.1
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
			if Channel_1.right_gain + 0.1 > 2.0 and Channel_1.left_gain - 0.1 < 0.0:
				Channel_1.right_gain = 2.0
				Channel_1.left_gain = 0.0
			else:
				Channel_1.right_gain += 0.1
				Channel_1.left_gain -= 0.1
##############################################################################################
# Channel 2 Controls

		elif event.type == pygame.KEYDOWN and event.key == pygame.K_g:
			Channel_2.on = not Channel_2.on
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_t:
			if Channel_2.gain + 0.05 > 1.50:
				Channel_2.gain = 1.50
			else:
				Channel_2.gain += 0.05
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_b:
			if Channel_2.gain - 0.05 < 0.0:
				Channel_2.gain = 0.0
			else:
				Channel_2.gain -= 0.05
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
			if Channel_2.left_gain + 0.1 > 2.0 and Channel_2.right_gain - 0.1 < 0.0:
				Channel_2.left_gain = 2.0
				Channel_2.right_gain = 0.0
			else:
				Channel_2.left_gain += 0.1
				Channel_2.right_gain -= 0.1
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_h:
			if Channel_2.right_gain + 0.1 > 2.0 and Channel_2.left_gain - 0.1 < 0.0:
				Channel_2.right_gain = 2.0
				Channel_2.left_gain = 0.0
			else:
				Channel_2.right_gain += 0.1
				Channel_2.left_gain -= 0.1
##############################################################################################
# Channel 3 Controls (MIDI Keypads)

		elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
			Channel_3.on = not Channel_3.on
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_EQUALS:
			if Channel_3.gain + 0.05 > 1.50:
				Channel_3.gain = 1.50
			else:
				Channel_3.gain += 0.05
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_MINUS:
			if Channel_3.gain - 0.05 < 0.0:
				Channel_3.gain = 0.0
			else:
				Channel_3.gain -= 0.05

##############################################################################################
# Channel ON/OFF Button Controls & Muting Controls

	if not Channel_1.on: 
		color1 = red
	else:
		color1 = green
		if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
			mute1 = not mute1
		Channel_1.play(mute1, mod1, mod1param)

	if not Channel_2.on:
		color2 = red
	else:
		color2 = green
		if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
			mute2 = not mute2
		Channel_2.play(mute2, mod2, mod2param)

	if not Channel_3.on:
		color3 = red
	else:
		color3 = green

		if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
			mute3 = not mute3
	
		if event.type == pygame.KEYDOWN and event.key == Channel_3.key1 and not Channel_3.key1_pressed:
			Channel_3.play_key(mute3, Channel_3.key1)
			Channel_3.key1_pressed = True
		elif event.type == pygame.KEYUP and event.key == Channel_3.key1 and Channel_3.key1_pressed:
			Channel_3.key1_pressed = False
		
		if event.type == pygame.KEYDOWN and event.key == Channel_3.key2 and not Channel_3.key2_pressed:
			Channel_3.play_key(mute3, Channel_3.key2)
			Channel_3.key2_pressed = True
		elif event.type == pygame.KEYUP and event.key == Channel_3.key2 and Channel_3.key2_pressed:
			Channel_3.key2_pressed = False
		
		if event.type == pygame.KEYDOWN and event.key == Channel_3.key3 and not Channel_3.key3_pressed:
			Channel_3.play_key(mute3, Channel_3.key3)
			Channel_3.key3_pressed = True
		elif event.type == pygame.KEYUP and event.key == Channel_3.key3 and Channel_3.key3_pressed:
			Channel_3.key3_pressed = False
		
		if event.type == pygame.KEYDOWN and event.key == Channel_3.key4 and not Channel_3.key4_pressed:
			Channel_3.play_key(mute3, Channel_3.key4)
			Channel_3.key4_pressed = True
		elif event.type == pygame.KEYUP and event.key == Channel_3.key4 and Channel_3.key4_pressed:
			Channel_3.key4_pressed = False
	
	mx, my = pygame.mouse.get_pos()
	
	tri_1color = red
	TP1_left = 280
	TP1_right = 300
	TP1_base = 160
	if mx >= TP1_left and mx <= TP1_right and atan2((TP1_base - my), mx - TP1_left) >= 0 and atan2((TP1_base - my), mx - TP1_left) <= np.pi / 3 and atan2((TP1_base - my), TP1_right - mx) >= 0 and atan2((TP1_base - my), TP1_right - mx) <= np.pi / 3:
		if pygame.mouse.get_pressed()[0]:
			tri_1color = green
			if mod1param[0] + 40 > 14000:
				mod1param[0] = 14000
			else:
				mod1param[0] += 40

	tri_1bcolor = red
	TP1b_left = 480
	TP1b_right = 500
	TP1b_base = 160
	if mx >= TP1b_left and mx <= TP1b_right and atan2((TP1b_base - my), mx - TP1b_left) >= 0 and atan2((TP1b_base - my), mx - TP1b_left) <= np.pi / 3 and atan2((TP1b_base - my), TP1b_right - mx) >= 0 and atan2((TP1b_base - my), TP1b_right - mx) <= np.pi / 3:
		if pygame.mouse.get_pressed()[0]:
			tri_1bcolor = green
			if mod1param[1] + 30 > 14000:
				mod1param[1] = 14000
			else:
				mod1param[1] += 30

	tri_1ccolor = red
	TP1c_left = 680
	TP1c_right = 700
	TP1c_base = 160
	if mx >= TP1c_left and mx <= TP1c_right and atan2((TP1c_base - my), mx - TP1c_left) >= 0 and atan2((TP1c_base - my), mx - TP1c_left) <= np.pi / 3 and atan2((TP1c_base - my), TP1c_right - mx) >= 0 and atan2((TP1c_base - my), TP1c_right - mx) <= np.pi / 3:
		if pygame.mouse.get_pressed()[0]:
			tri_1ccolor = green
			if mod1param[2] + 10 > 1400:
				mod1param[2] = 1400
			else:
				mod1param[2] += 10	

	tri_2color = red
	TP2_left = 280
	TP2_right = 300
	TP2_base = 460
	if mx >= TP2_left and mx <= TP2_right and atan2((TP2_base - my), mx - TP2_left) >= 0 and atan2((TP2_base - my), mx - TP2_left) <= np.pi / 3 and atan2((TP2_base - my), TP2_right - mx) >= 0 and atan2((TP2_base - my), TP2_right - mx) <= np.pi / 3:
		if pygame.mouse.get_pressed()[0]:
			tri_2color = green
			if mod2param[0] + 30 > 14000:
				mod2param[0] = 14000
			else:
				mod2param[0] += 30

	tri_2bcolor = red
	TP2b_left = 480
	TP2b_right = 500
	TP2b_base = 460
	if mx >= TP2b_left and mx <= TP2b_right and atan2((TP2b_base - my), mx - TP2b_left) >= 0 and atan2((TP2b_base - my), mx - TP2b_left) <= np.pi / 3 and atan2((TP2b_base - my), TP2b_right - mx) >= 0 and atan2((TP2b_base - my), TP2b_right - mx) <= np.pi / 3:
		if pygame.mouse.get_pressed()[0]:
			tri_2bcolor = green
			if mod2param[1] + 30 > 14000:
				mod2param[1] = 14000
			else:
				mod2param[1] += 30

	tri_2ccolor = red
	TP2c_left = 680
	TP2c_right = 700
	TP2c_base = 460
	if mx >= TP2c_left and mx <= TP2c_right and atan2((TP2c_base - my), mx - TP2c_left) >= 0 and atan2((TP2c_base - my), mx - TP2c_left) <= np.pi / 3 and atan2((TP2c_base - my), TP2c_right - mx) >= 0 and atan2((TP2c_base - my), TP2c_right - mx) <= np.pi / 3:
		if pygame.mouse.get_pressed()[0]:
			tri_2ccolor = green
			if mod2param[2] + 10 > 1400:
				mod2param[2] = 1400
			else:
				mod2param[2] += 10

	tri_3color = red
	TP3_left = 280
	TP3_right = 300
	TP3_base = 210
	if mx >= TP3_left and mx <= TP3_right and atan2((TP3_base - my), mx - TP3_left) >= -np.pi/3 and atan2((TP3_base - my), mx - TP3_left) <= 0 and atan2((TP3_base - my), TP3_right - mx) >= -np.pi / 3 and atan2((TP3_base - my), TP3_right - mx) <= 0:
		if pygame.mouse.get_pressed()[0]:
			tri_3color = green
			if mod1param[0] - 30 < 0:
				mod1param[0] = 0
			else:
				mod1param[0] -= 30

	tri_3bcolor = red
	TP3b_left = 480
	TP3b_right = 500
	TP3b_base = 210
	if mx >= TP3b_left and mx <= TP3b_right and atan2((TP3b_base - my), mx - TP3b_left) >= -np.pi/3 and atan2((TP3b_base - my), mx - TP3b_left) <= 0 and atan2((TP3b_base - my), TP3b_right - mx) >= -np.pi / 3 and atan2((TP3b_base - my), TP3b_right - mx) <= 0:
		if pygame.mouse.get_pressed()[0]:
			tri_3bcolor = green
			if mod1param[1] - 30 < 0:
				mod1param[1] = 0
			else:
				mod1param[1] -= 30

	tri_3ccolor = red
	TP3c_left = 680
	TP3c_right = 700
	TP3c_base = 210
	if mx >= TP3c_left and mx <= TP3c_right and atan2((TP3c_base - my), mx - TP3c_left) >= -np.pi/3 and atan2((TP3c_base - my), mx - TP3c_left) <= 0 and atan2((TP3c_base - my), TP3c_right - mx) >= -np.pi / 3 and atan2((TP3c_base - my), TP3c_right - mx) <= 0:
		if pygame.mouse.get_pressed()[0]:
			tri_3ccolor = green
			if mod1param[2] - 10 < 0:
				mod1param[2] = 0
			else:
				mod1param[2] -= 10

	tri_4color = red
	TP4_left = 280
	TP4_right = 300
	TP4_base = 510
	if mx >= TP4_left and mx <= TP4_right and atan2((TP4_base - my), mx - TP4_left) >= -np.pi/3 and atan2((TP4_base - my), mx - TP4_left) <= 0 and atan2((TP4_base - my), TP4_right - mx) >= -np.pi / 3 and atan2((TP4_base - my), TP4_right - mx) <= 0:
		if pygame.mouse.get_pressed()[0]:
			tri_4color = green
			if mod2param[0] - 30 < 0:
				mod2param[0] = 0
			else:
				mod2param[0] -= 30

	tri_4bcolor = red
	TP4b_left = 480
	TP4b_right = 500
	TP4b_base = 510
	if mx >= TP4b_left and mx <= TP4b_right and atan2((TP4b_base - my), mx - TP4b_left) >= -np.pi/3 and atan2((TP4b_base - my), mx - TP4b_left) <= 0 and atan2((TP4b_base - my), TP4b_right - mx) >= -np.pi / 3 and atan2((TP4b_base - my), TP4b_right - mx) <= 0:
		if pygame.mouse.get_pressed()[0]:
			tri_4bcolor = green
			if mod2param[1] - 30 < 0:
				mod2param[1] = 0
			else:
				mod2param[1] -= 30

	tri_4ccolor = red
	TP4c_left = 680
	TP4c_right = 700
	TP4c_base = 510
	if mx >= TP4c_left and mx <= TP4c_right and atan2((TP4c_base - my), mx - TP4c_left) >= -np.pi/3 and atan2((TP4c_base - my), mx - TP4c_left) <= 0 and atan2((TP4c_base - my), TP4c_right - mx) >= -np.pi / 3 and atan2((TP4c_base - my), TP4c_right - mx) <= 0:
		if pygame.mouse.get_pressed()[0]:
			tri_4ccolor = green
			if mod2param[2] - 10 < 0:
				mod2param[2] = 0
			else:
				mod2param[2] -= 10

	if mx >= TP1_left and mx <= TP1_right and my >= TP1_base + 15 and my <= TP1_base + 35:
		if pygame.mouse.get_pressed()[0]:
			mod1[0] = not mod1[0]

	elif mx >= TP1_left + 200 and mx <= TP1_right + 200 and my >= TP1_base + 15 and my <= TP1_base + 35:
		if pygame.mouse.get_pressed()[0]:
			mod1[1] = not mod1[1]

	elif mx >= TP1_left + 400 and mx <= TP1_right + 400 and my >= TP1_base + 15 and my <= TP1_base + 35:
		if pygame.mouse.get_pressed()[0]:
			mod1[2] = not mod1[2]

	elif mx >= TP2_left and mx <= TP2_right and my >= TP2_base + 15 and my <= TP2_base + 35:
		if pygame.mouse.get_pressed()[0]:
			mod2[0] = not mod2[0]

	elif mx >= TP2_left + 200 and mx <= TP2_right + 200 and my >= TP2_base + 15 and my <= TP2_base + 35:
		if pygame.mouse.get_pressed()[0]:
			mod2[1] = not mod2[1]

	elif mx >= TP2_left + 400 and mx <= TP2_right + 400 and my >= TP2_base + 15 and my <= TP2_base + 35:
		if pygame.mouse.get_pressed()[0]:
			mod2[2] = not mod2[2]


	if not mod1[0]:
		color4 = red
	else:
		color4 = green

	if not mod1[1]:
		color6 = red
	else:
		color6 = green

	if not mod1[2]:
		color8 = red
	else:
		color8 = green


	if not mod2[0]:
		color5 = red
	else:
		color5 = green

	if not mod2[1]:
		color7 = red
	else:
		color7 = green

	if not mod2[2]:
		color9 = red
	else:
		color9 = green


	if not Channel_3.key1_pressed:
		padcolor1 = red
	else:
		padcolor1 = green

	if not Channel_3.key2_pressed:
		padcolor2 = red
	else:
		padcolor2 = green

	if not Channel_3.key3_pressed:
		padcolor3 = red
	else:
		padcolor3 = green

	if not Channel_3.key4_pressed:
		padcolor4 = red
	else:
		padcolor4 = green	

##############################################################################################
# Volume/Panning Bars Automatic Controls
	screen.fill((0,0,0))

	trackfont = pygame.font.SysFont("arial", 30)
	faderfont = pygame.font.SysFont("arial", 25)
	filterfont = pygame.font.SysFont("arial", 15)
	padfont = pygame.font.SysFont("arial", 40)
	titlefont = pygame.font.SysFont("arial", 25)

	track1 = trackfont.render("Track 1", True, color1)
	screen.blit(track1, (70 - track1.get_width() // 2, 60 - track1.get_height() // 2))
	pygame.draw.rect(screen, color1, pygame.Rect(30, 90, 60, 60))
	pygame.draw.rect(screen, red, pygame.Rect(160, 35, 20, 220))
	pygame.draw.rect(screen, green, pygame.Rect(160, 262.5, 20, -150*Channel_1.gain))

	track2 = trackfont.render("Track 2", True, color2)
	screen.blit(track2, (70 - track2.get_width() // 2, 360 - track2.get_height() // 2))
	pygame.draw.rect(screen, color2, pygame.Rect(30, 410, 60, 60))
	pygame.draw.rect(screen, red, pygame.Rect(160, 335, 20, 220))
	pygame.draw.rect(screen, green, pygame.Rect(160, 562.5, 20, -150*Channel_2.gain))

	track3 = trackfont.render("MIDI Pad", True, color3)
	screen.blit(track3, (70 - track3.get_width() // 2, 660 - track3.get_height() // 2))
	pygame.draw.rect(screen, color3, pygame.Rect(30, 690, 60, 60))
	pygame.draw.rect(screen, red, pygame.Rect(160, 635, 20, 220))
	pygame.draw.rect(screen, green, pygame.Rect(160, 862.5, 20, -150*Channel_3.gain))

	pygame.draw.rect(screen, blue, pygame.Rect(0, 590, 900, 3))
	pygame.draw.rect(screen, blue, pygame.Rect(0, 290, 900, 3))

	fader1 = faderfont.render("Fader 1 (L/R) = (" + str(Channel_1.left_gain / 2.0) + "/" + str(Channel_1.right_gain / 2.0) + ")", True, blue)
	screen.blit(fader1, (340 - fader1.get_width() // 2, 25 - fader1.get_height() // 2))
	pygame.draw.rect(screen, blue, pygame.Rect(220, 50, 240, 20))
	pygame.draw.rect(screen, red, pygame.Rect((440 - Channel_1.left_gain * 110), 50, 20, 20))

	fader2 = faderfont.render("Fader 2 (L/R) = (" + str(Channel_2.left_gain / 2.0) + "/" + str(Channel_2.right_gain / 2.0) + ")", True, blue)
	screen.blit(fader2, (340 - fader2.get_width() // 2, 325 - fader2.get_height() // 2))
	pygame.draw.rect(screen, blue, pygame.Rect(220, 350, 240, 20))
	pygame.draw.rect(screen, red, pygame.Rect((440 - Channel_2.left_gain * 110), 350, 20, 20))

	filter1 = filterfont.render("LPF: f_c = " + str(mod1param[0]) + " Hz", True, color4)
	screen.blit(filter1, (250 - filter1.get_width() // 2, 90 - filter1.get_height() // 2))
	pygame.draw.polygon(screen, tri_1color, [[TP1_left + 10, TP1_base - 20], [TP1_left, TP1_base], [TP1_right, TP1_base]], 0)
	pygame.draw.rect(screen, blue, pygame.Rect(240, 110, 20, 150))
	pygame.draw.rect(screen, red, pygame.Rect(240, 250 - mod1param[0]/100, 20, 10))

	filter2 = filterfont.render("HPF: f_c = " + str(mod1param[1]) + " Hz", True, color6)
	screen.blit(filter2, (450 - filter2.get_width() // 2, 90 - filter2.get_height() // 2))
	pygame.draw.polygon(screen, tri_1bcolor, [[TP1b_left + 10, TP1b_base - 20], [TP1b_left, TP1b_base], [TP1b_right, TP1b_base]], 0)
	pygame.draw.rect(screen, blue, pygame.Rect(440, 110, 20, 150))
	pygame.draw.rect(screen, red, pygame.Rect(440, 250 - mod1param[1]/100, 20, 10))

	filter3 = filterfont.render("Complex Modul.: f_shift = " + str(mod1param[2]) + " Hz", True, color8)
	screen.blit(filter3, (650 - filter3.get_width() // 2, 90 - filter3.get_height() // 2))
	pygame.draw.polygon(screen, tri_1ccolor, [[TP1c_left + 10, TP1c_base - 20], [TP1c_left, TP1c_base], [TP1c_right, TP1c_base]], 0)
	pygame.draw.rect(screen, blue, pygame.Rect(640, 110, 20, 150))
	pygame.draw.rect(screen, red, pygame.Rect(640, 250 - mod1param[2]/10, 20, 10))

	filter4 = filterfont.render("LPF: f_c = " + str(mod2param[0]) + " Hz", True, color5)
	screen.blit(filter4, (250 - filter4.get_width() // 2, 390 - filter4.get_height() // 2))
	pygame.draw.polygon(screen, tri_2color, [[TP2_left + 10, TP2_base - 20], [TP2_left, TP2_base], [TP2_right, TP2_base]], 0)
	pygame.draw.rect(screen, blue, pygame.Rect(240, 410, 20, 150))
	pygame.draw.rect(screen, red, pygame.Rect(240, 550 - mod2param[0]/100, 20, 10))

	filter5 = filterfont.render("HPF: f_c = " + str(mod2param[1]) + " Hz", True, color7)
	screen.blit(filter5, (450 - filter5.get_width() // 2, 390 - filter5.get_height() // 2))
	pygame.draw.polygon(screen, tri_2bcolor, [[TP2b_left + 10, TP2b_base - 20], [TP2b_left, TP2b_base], [TP2b_right, TP2b_base]], 0)
	pygame.draw.rect(screen, blue, pygame.Rect(440, 410, 20, 150))
	pygame.draw.rect(screen, red, pygame.Rect(440, 550 - mod2param[1]/100, 20, 10))

	filter6 = filterfont.render("Complex Modul.: f_shift = " + str(mod2param[2]) + " Hz", True, color9)
	screen.blit(filter6, (650 - filter6.get_width() // 2, 390 - filter6.get_height() // 2))
	pygame.draw.polygon(screen, tri_2ccolor, [[TP2c_left + 10, TP2c_base - 20], [TP2c_left, TP2c_base], [TP2c_right, TP2c_base]], 0)
	pygame.draw.rect(screen, blue, pygame.Rect(640, 410, 20, 150))
	pygame.draw.rect(screen, red, pygame.Rect(640, 550 - mod2param[2]/10, 20, 10))	
	
	pygame.draw.polygon(screen, tri_3color, [[TP3_left + 10, TP3_base + 20], [TP3_left, TP3_base], [TP3_right, TP3_base]], 0)
	pygame.draw.polygon(screen, tri_3bcolor, [[TP3b_left + 10, TP3b_base + 20], [TP3b_left, TP3b_base], [TP3b_right, TP3b_base]], 0)
	pygame.draw.polygon(screen, tri_3ccolor, [[TP3c_left + 10, TP3c_base + 20], [TP3c_left, TP3c_base], [TP3c_right, TP3c_base]], 0)

	pygame.draw.polygon(screen, tri_4color, [[TP4_left + 10, TP4_base + 20], [TP4_left, TP4_base], [TP4_right, TP4_base]], 0)
	pygame.draw.polygon(screen, tri_4bcolor, [[TP4b_left + 10, TP4b_base + 20], [TP4b_left, TP4b_base], [TP4b_right, TP4b_base]], 0)
	pygame.draw.polygon(screen, tri_4ccolor, [[TP4c_left + 10, TP4c_base + 20], [TP4c_left, TP4c_base], [TP4c_right, TP4c_base]], 0)

	pygame.draw.rect(screen, color4, pygame.Rect(TP1_left, TP1_base + 15, 20, 20))
	pygame.draw.rect(screen, color6, pygame.Rect(TP1_left + 200, TP1_base + 15, 20, 20))
	pygame.draw.rect(screen, color8, pygame.Rect(TP1_left + 400, TP1_base + 15, 20, 20))

	pygame.draw.rect(screen, color5, pygame.Rect(TP2_left, TP2_base + 15, 20, 20))
	pygame.draw.rect(screen, color7, pygame.Rect(TP2_left + 200, TP2_base + 15, 20, 20))
	pygame.draw.rect(screen, color9, pygame.Rect(TP2_left + 400, TP2_base + 15, 20, 20))

	pygame.draw.rect(screen, padcolor1, pygame.Rect(250, 650, 70, 70))
	pygame.draw.rect(screen, padcolor2, pygame.Rect(345, 650, 70, 70))
	pygame.draw.rect(screen, padcolor3, pygame.Rect(250, 745, 70, 70))
	pygame.draw.rect(screen, padcolor4, pygame.Rect(345, 745, 70, 70))
	
	pad1 = padfont.render("I", True, blue)
	screen.blit(pad1, (285 - pad1.get_width() // 2, 685 - pad1.get_height() // 2))
	pad2 = padfont.render("O", True, blue)
	screen.blit(pad2, (375 - pad2.get_width() // 2, 685 - pad2.get_height() // 2))
	pad3 = padfont.render("K", True, blue)
	screen.blit(pad3, (285 - pad3.get_width() // 2, 780 - pad3.get_height() // 2))
	pad4 = padfont.render("L", True, blue)
	screen.blit(pad4, (380 - pad4.get_width() // 2, 780 - pad4.get_height() // 2))

	title1 = titlefont.render("Music Mixer & MIDI Pad", True, red)
	screen.blit(title1, (575 - title1.get_width() // 2, 700 - title1.get_height() // 2))
	title2 = titlefont.render("Creator: Emanuel Azcona", True, red)
	screen.blit(title2, (580 - title2.get_width() // 2, 735 - title2.get_height() // 2))	
	title3 = titlefont.render("Guided Studies in Electrical Engineering", True, red)
	screen.blit(title3, (660 - title3.get_width() // 2, 770 - title3.get_height() // 2))	

	pygame.display.flip()

Channel_1.close_stream()
Channel_2.close_stream()
Channel_3.close_stream()

pygame.quit()
