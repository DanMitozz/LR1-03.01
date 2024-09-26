from grid import Grid  # Импорт класса для работы с сеткой
from blocks import *  # Импорт классов для различных блоков
import random  # Импорт для случайного выбора блоков
import pygame  # Импорт библиотеки pygame для графики и звуков

class Game:
	def __init__(self):
		# Создаем игровую сетку
		self.grid = Grid()
		# Создаем список доступных блоков
		self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
		# Выбираем текущий блок и следующий блок случайным образом
		self.current_block = self.get_random_block()
		self.next_block = self.get_random_block()
		# Статус игры (True если игра окончена)
		self.game_over = False
		# Начальное значение счета
		self.score = 0
		# Загружаем звуковые эффекты для вращения и очистки линий
		self.rotate_sound = pygame.mixer.Sound("Sounds/rotate.ogg")
		self.clear_sound = pygame.mixer.Sound("Sounds/clear.ogg")

		# Загружаем и проигрываем фоновую музыку
		pygame.mixer.music.load("Sounds/music.ogg")
		pygame.mixer.music.play(-1)  # Бесконечный цикл воспроизведения

	def update_score(self, lines_cleared, move_down_points):
		# Обновляем счет в зависимости от числа очищенных линий
		if lines_cleared == 1:
			self.score += 100
		elif lines_cleared == 2:
			self.score += 300
		elif lines_cleared == 3:
			self.score += 500
		# Добавляем очки за движение блока вниз
		self.score += move_down_points

	def get_random_block(self):
		# Если все блоки были использованы, создаем их заново
		if len(self.blocks) == 0:
			self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
		# Случайный выбор блока из доступных
		block = random.choice(self.blocks)
		# Убираем выбранный блок из списка
		self.blocks.remove(block)
		return block

	def move_left(self):
		# Двигаем блок влево
		self.current_block.move(0, -1)
		# Если блок вышел за границы или пересекается с другими, отменяем движение
		if self.block_inside() == False or self.block_fits() == False:
			self.current_block.move(0, 1)

	def move_right(self):
		# Двигаем блок вправо
		self.current_block.move(0, 1)
		# Если блок вышел за границы или пересекается с другими, отменяем движение
		if self.block_inside() == False or self.block_fits() == False:
			self.current_block.move(0, -1)

	def move_down(self):
		# Двигаем блок вниз
		self.current_block.move(1, 0)
		# Если блок не может двигаться вниз, фиксируем его на месте
		if self.block_inside() == False or self.block_fits() == False:
			self.current_block.move(-1, 0)
			self.lock_block()

	def lock_block(self):
		# Фиксируем блок на текущем месте
		tiles = self.current_block.get_cell_positions()
		for position in tiles:
			self.grid.grid[position.row][position.column] = self.current_block.id
		# Выбираем следующий блок
		self.current_block = self.next_block
		self.next_block = self.get_random_block()
		# Проверяем, очищены ли строки
		rows_cleared = self.grid.clear_full_rows()
		if rows_cleared > 0:
			self.clear_sound.play()  # Проигрываем звук очистки строк
			self.update_score(rows_cleared, 0)  # Обновляем счет
		# Проверяем, может ли новый блок поместиться на поле, если нет — игра окончена
		if self.block_fits() == False:
			self.game_over = True

	def reset(self):
		# Сброс игры: очищаем сетку и список блоков, обнуляем счет
		self.grid.reset()
		self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
		self.current_block = self.get_random_block()
		self.next_block = self.get_random_block()
		self.score = 0

	def block_fits(self):
		# Проверяем, помещается ли текущий блок в сетку
		tiles = self.current_block.get_cell_positions()
		for tile in tiles:
			if self.grid.is_empty(tile.row, tile.column) == False:
				return False
		return True

	def rotate(self):
		# Поворачиваем блок
		self.current_block.rotate()
		# Если блок вышел за границы или пересекается с другими, отменяем вращение
		if self.block_inside() == False or self.block_fits() == False:
			self.current_block.undo_rotation()
		else:
			self.rotate_sound.play()  # Проигрываем звук вращения

	def block_inside(self):
		# Проверяем, находится ли блок внутри игрового поля
		tiles = self.current_block.get_cell_positions()
		for tile in tiles:
			if self.grid.is_inside(tile.row, tile.column) == False:
				return False
		return True

	def draw(self, screen):
		# Отрисовываем сетку и текущий блок на экране
		self.grid.draw(screen)
		self.current_block.draw(screen, 11, 11)

		# Отрисовываем следующий блок в зависимости от его формы
		if self.next_block.id == 3:
			self.next_block.draw(screen, 255, 290)
		elif self.next_block.id == 4:
			self.next_block.draw(screen, 255, 280)
		else:
			self.next_block.draw(screen, 270, 270)
