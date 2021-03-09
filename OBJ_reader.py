# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw
import os

class OBJ(object):
	def __init__(self, file, img_size=(1000, 1000)):
		# === Variables ===
		self.v = []
		self.vt = []
		self.ft = []
		self.img_size = img_size
		temp_f = []
		line = 0

		file = open(file, mode='r', encoding='utf-8')
		polygons = file.read().split('\n')
		file.close()

		while line < len(polygons) - 1:
			if polygons[line][0:2] == 'v ':
				self.v.append(polygons[line].replace('  ', ' ').split(' ')[1:])

			elif polygons[line][0:2] == 'vt':
				self.vt.append(polygons[line].replace('  ', ' ').split(' ')[1:])

			elif polygons[line][0:2] == 'f ':
				temp_f.append(polygons[line].replace('  ', ' ').split(' ')[1:])

			else:	pass

			line += 1

		self.f  = [list(map(lambda val: val.split('/')[0], item)) for item in temp_f]
		for item in temp_f:
			try:
				temp = [float(item[i].split('/')[1]) for i in range(3)]
				self.ft.append(temp)
			except:	pass

		# self.ft = [list(map(lambda val: val.split('/')[0], item)) for item in temp_f]
		del temp_f

	def drawing_2d(self):
		self.picture = Image.new('RGBA', self.img_size, (255, 255, 255, 0))
		draw = ImageDraw.Draw(self.picture)
		f = 0

		# Rotate
		# import math
		# g = math.degrees(180)

		# self.v = [[float(item[0]) * math.cos(g) - float(item[1]) * math.sin(g) + float(item[0]), item[1]] for item in self.v]
		# self.v = [[item[0], float(item[0]) * math.sin(g) + float(item[1]) * math.cos(g) + float(item[1])] for item in self.v]

		# Block for rewrite list "v" and delete value < 0
		min_v = min([float(min(i)) for i in self.v])
		if min_v < 0:
			self.v = [list(map(lambda val: float(val) + abs(min_v), i[0:2])) for i in self.v]
		else:
			self.v = [list(map(lambda val: float(val) + min_v, i[0:2])) for i in self.v]

		# Block for rewrite list "v" in size picture
		max_x = max([i[0] for i in self.v])
		max_y = max([i[1] for i in self.v])
		x = max_x * 100 / self.img_size[0]
		y = max_y * 100 / self.img_size[1]

		self.v = [[i[0] / x * 100, self.img_size[1] - (i[1] / y * 100)] for i in self.v]

		# Draw picture
		while f < len(self.f) - 1:
			print('\rProgress: %s' % (int((f / len(self.f)) * 100) + 1), end='%')

			coord = [tuple(self.v[int(self.f[f][i]) - 1]) for i in range(3)]
			draw.polygon(coord, fill='#fff', outline='#000')
			f += 1
		print('')

		del draw

	def fill(self):
		pass

	def show(self):
		self.picture.show()

if __name__ == '__main__':
	obj = OBJ('%s\\models\\helmet.obj' % os.getcwd())
	obj.drawing_2d()

	obj.picture.save('%s\\output.png' % os.getcwd())
	os.system('%s\\output.png' % os.getcwd())

	# obj.show()
