import pygame as pg
import sys
import random 

class Game:

    # Константы на класс
    RESOLUTION = WIDTH, HEIGHT = 800, 800
    SNAKE_BLOCK = 20
    BLACK = pg.color.Color(30, 30 ,30)
    LIGHT_BLACK = pg.color.Color(60, 60, 60)
    GREEN = pg.color.Color(0, 230, 0, 0)
    RED = pg.color.Color(230, 0, 0, 0)

    # Начальная инициализация
    def __init__(self):
        ''' Начальная инициализация экрана, фона, названия окна и объекта clock для поддержания фпс'''
        pg.init()
        self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        pg.display.set_caption('Snake')

        self._font = pg.font.Font(pg.font.get_default_font(), 30)
        self.clock = pg.time.Clock()
        self.new_game()

        self.game_over = False

    # Обновленеи состояния игры 
    def __update(self):
        self.snake._update()
        self.clock.tick(60)
        pg.display.flip()

    # Метод для запуска новой игры 
    def new_game(self):
        self.game_over = False
        self.snake = Snake(self)
        self.food = Food(self)
        self.menu = Menu(self)

    # Метод для отрисовки всей игры 
    def __draw(self):
        if (self.game_over):
            self.menu._draw()
        else:
            self.screen.fill(self.BLACK)
            self.draw_grid()
            self.food.draw()
            self.snake.draw()

    def draw_grid(self):
        [pg.draw.line(self.screen, self.LIGHT_BLACK, (x, 0), (x, self.WIDTH)) for x in range(0, self.WIDTH, self.SNAKE_BLOCK)]
        [pg.draw.line(self.screen, self.LIGHT_BLACK, (0, y), (self.HEIGHT, y)) for y in range(0, self.HEIGHT, self.SNAKE_BLOCK)]

    # Метод для проверки входящих данных от пользователя
    def __check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or event.type == pg.K_ESCAPE:
                sys.exit()
            
            if (self.snake.delta_time()):
                self.snake._control(event)

    # Главный цикл игры
    def run(self):
        while True:
            self.__check_events()
            self.__update()
            self.__draw()

class Snake:

    def __init__(self, game):
        self.game = game
        self.size = game.SNAKE_BLOCK
        self.area = self.game.screen.get_rect()
        self.snake = pg.surface.Surface((game.SNAKE_BLOCK, game.SNAKE_BLOCK)).convert()
        self.rect = self.snake.get_rect()
        self.rect.topleft = (random.randrange(0, game.WIDTH, 20), random.randrange(0, game.HEIGHT, 20))
        self.step_delay = 100
        self.time = 0
        self.length = 3
        self.segments = []
        self.direction = [self.size, 0]

    def _update(self):
        self.check_self_eating()
        self.check_borders()
        self.check_food()
        self._move()
    
    def _control(self, event):
        if event.type == pg.KEYDOWN:
            if (event.key == pg.K_UP and self.direction != [0, self.size]):
                self.direction = [0, -self.size]
            elif (event.key == pg.K_DOWN and self.direction != [0, -self.size]):
                self.direction = [0, self.size]
            elif (event.key == pg.K_RIGHT and self.direction != [-self.size, 0]):
                self.direction = [self.size, 0]
            elif (event.key == pg.K_LEFT and self.direction != [self.size, 0]):
                self.direction = [-self.size, 0]
            elif (event.key == pg.K_SPACE):
                self.game.new_game()
    
    def draw(self):
        [pg.draw.rect(self.game.screen, self.game.GREEN, segment) for segment in self.segments]

    def delta_time(self):
        time_now = pg.time.get_ticks()
        if time_now - self.time > self.step_delay:
            self.time = time_now
            return True
        return False 

    def check_borders(self):
        if (self.rect.right > self.area.right):
            self.rect.left = 0
        elif (self.rect.left < self.area.left):
            self.rect.right = self.area.right
        elif (self.rect.top < self.area.top):
            self.rect.bottom = self.area.bottom
        elif (self.rect.bottom > self.area.bottom):
            self.rect.top = 0
    
    def check_self_eating(self):
        if (self.rect in self.segments[-self.length:-1]):
            self.game.game_over = True
            

    def check_food(self):
        if(self.rect == self.game.food.rect):
            self.game.food.rect.topleft = (random.randrange(0, self.game.WIDTH, 20), random.randrange(0, game.HEIGHT, 20))
            self.length += 1

    def _move(self):
        if (self.delta_time()):
            self.rect = self.rect.move(self.direction[0], self.direction[1])
            self.segments.append(self.rect.copy())
            self.segments = self.segments[-self.length:]

class Food:

    def __init__(self, game):
        self.game = game
        self.size = game.SNAKE_BLOCK
        self.food = pg.surface.Surface((game.SNAKE_BLOCK, game.SNAKE_BLOCK)).convert()
        self.rect = self.food.get_rect()
        self.rect.topleft = (random.randrange(0, game.WIDTH, 20), random.randrange(0, game.HEIGHT, 20))
    
    def draw(self):
        pg.draw.rect(self.game.screen, self.game.RED, self.rect)

class Menu:
 
    def __init__(self, game):
        self.game = game
        self.menu = pg.surface.Surface((self.game.screen.get_size())).convert()
        self.rect = self.menu.get_rect()
        self.menu.fill(self.game.BLACK)
        self.instructions = self.game._font.render('PRESS [SPACE] TO RESTART THE GAME', True, (200, 200, 200))
        self.instructions_pos = self.instructions.get_rect(centerx=self.game.WIDTH / 2 + 30, centery=self.game.HEIGHT / 2 + 50)
    
    def _draw(self):
        self.game.screen.blit(self.menu, (0, 0))
        self.draw_score()
        self.game.screen.blit(self.instructions, self.instructions_pos)
        self.game.screen.blit(self.text, self.text_pos)

    def draw_score(self):
        self.text = self.game._font.render('Game Over! Score: {}'.format(game.snake.length), True, (200, 200, 200))
        self.text_pos = self.text.get_rect(centerx=self.game.WIDTH / 2, centery=self.game.HEIGHT / 2)

if __name__ == '__main__':
    game = Game()
    game.run()