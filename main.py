import pygame
import random
import math
import sys


class Pong:
    """main game class"""

    def __init__(self):
        """initialize pygame, game screen and other game attribute"""

        # initialize pygame resources
        pygame.init()
        # set screen, window size
        self.screen = pygame.display.set_mode((640, 360))
        # set window title bar text
        pygame.display.set_caption("Pong")

        # background color
        self.br_color = "#050103"
        # clock object to handle time sensitive data and operations
        self.clock = pygame.time.Clock()

        # instantiate players #
        self.player1 = Paddle(self, 1)
        self.player2 = Paddle(self, 2)

        # instantiate center line #
        self.center_line = CenterLine(self)

        # instantiate score labels #
        self.score1 = ScoreLabel(self, 0, 1)
        self.score2 = ScoreLabel(self, 0, 2)

        # instantiate ball #
        self.ball = Ball(self)

        # instantiate sound effects #
        self.hit_sound = SFX("hit.mp3")
        self.score_sound = SFX("score.mp3")

    def run(self):
        """game loop"""

        while True:
            self.check_input()
            self.update()
            self.render()

            # make sure loop is called 60 times per second
            self.clock.tick(60)

    def check_input(self):
        """input event loop: handles users input"""
        for event in pygame.event.get():
            # stop program if the window close button is pressed
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.key_pressed(event.key)
            elif event.type == pygame.KEYUP:
                self.key_released(event.key)

    def key_pressed(self, key):
        """handle keydown events"""
        if key == pygame.K_w:
            # start moving player one up #
            self.player1.moving_up = True
        elif key == pygame.K_UP:
            # start moving player two up #
            self.player2.moving_up = True
        elif key == pygame.K_s:
            # start moving player one down #
            self.player1.moving_down = True
        elif key == pygame.K_DOWN:
            # start moving player two down #
            self.player2.moving_down = True
        elif key == pygame.K_SPACE:
            # start game when the space button is pressed
            self.new_game()

    def key_released(self, key):
        """handle keyup events"""
        if key == pygame.K_w:
            # stop moving player one up #
            self.player1.moving_up = False
        elif key == pygame.K_UP:
            # stop moving player two up #
            self.player2.moving_up = False
        elif key == pygame.K_s:
            # stop moving player one down #
            self.player1.moving_down = False
        elif key == pygame.K_DOWN:
            # stop moving player two down #
            self.player2.moving_down = False

    def new_game(self):
        """start a new game"""
        # center player one #
        self.player1.set_position()
        # center player two #
        self.player2.set_position()
        # reset player one score #
        self.score1.reset()
        # reset player two score #
        self.score2.reset()
        # position ball to center of screen #
        self.ball.start()

    def point(self, player):
        """add point when a player scores"""
        if player == 1:
            # add point to player one #
            self.score1.add()
        elif player == 2:
            # add point to player two #
            self.score2.add()
        # position ball to center of screen #
        self.ball.start()
        # play score sound effect #
        self.score_sound.play()

    def play_hit_sound(self):
        """hit sound effect"""
        # play sound effect when ball hits wall or paddle #
        self.hit_sound.play()

    def update(self):
        """updates game elements"""
        # update ball #
        self.ball.update()

        # update players #
        self.player1.update()
        self.player2.update()

    def render(self):
        """draws game elements to the screen"""

        # fill window with background color
        self.screen.fill(self.br_color)

        # draw score labels #
        self.score1.render()
        self.score2.render()

        # draw center line #
        self.center_line.render()

        # draw players #
        self.player1.render()
        self.player2.render()

        # draw ball #
        self.ball.render()

        # show latest frame
        pygame.display.flip()


class Paddle:
    """paddle class"""

    def __init__(self, pong, player, width=8, height=96, margin=10):
        # get game screen surface
        self.parent_surf = pong.screen
        # get game screen rectangle/size
        self.parent_rect = pong.screen.get_rect()

        # paddle rectangle
        self.rect = pygame.Rect(0, 0, width, height)
        self.player = player

        # paddle color
        self.color = None
        # space between paddle and wall
        self.margin = margin

        # movement speed
        self.speed = 2

        # movement flags
        self.moving_up = False
        self.moving_down = False

        self.set_position()

    def set_position(self):
        """set paddle position according to it's side"""
        if self.player == 1:
            self.color = "#c92631"
            self.rect.midleft = self.parent_rect.midleft
            # add margin
            self.rect.x += self.margin
        elif self.player == 2:
            self.color = "#1a7827"
            self.rect.midright = self.parent_rect.midright
            # add margin
            self.rect.x -= self.margin

    def update(self):
        """handle paddle movement and collisions"""
        if self.moving_up and self.rect.top > 0:
            self.rect.y -= self.speed
        if self.moving_down and self.rect.bottom < self.parent_rect.bottom:
            self.rect.y += self.speed

    def render(self):
        """draw paddle to screen"""
        pygame.draw.rect(self.parent_surf, self.color, self.rect)


class CenterLine:
    """draws a line at the center of the screen"""

    def __init__(self, pong):
        # get game screen
        self.parent_surf = pong.screen
        # get game screen rect
        self.parent_rect = pong.screen.get_rect()

        # line's color
        self.color = "#91896e"
        # set line position
        self.line_start_pos = (self.parent_rect.centerx, 0)
        self.line_end_pos = (self.parent_rect.centerx, self.parent_rect.height)

    def render(self):
        """draw line on screen"""
        pygame.draw.line(self.parent_surf, self.color, self.line_start_pos, self.line_end_pos)


class ScoreLabel:
    """displays player score on screen"""

    def __init__(self, pong, text, player, margin=32):
        # get game screen
        self.parent_surf = pong.screen
        # get game screen rect
        self.parent_rect = pong.screen.get_rect()

        self.player = player
        self.margin = margin

        self.font = pygame.font.Font(None, 32)
        self.color = "#403830"

        self.surf = None
        self.rect = None

        self.score = int(text)
        self.set_text()

    def set_text(self):
        """set text"""
        self.surf = self.font.render(str(self.score), True, self.color)
        self.rect = self.surf.get_rect()
        self.rect.y += self.margin

        if self.player == 1:
            self.rect.right = self.parent_rect.centerx - self.margin
        elif self.player == 2:
            self.rect.left = self.parent_rect.centerx + self.margin

    def add(self):
        """add point to score"""
        self.score += 1
        self.set_text()

    def reset(self):
        """reset point to zero"""
        self.score = 0
        self.set_text()

    def render(self):
        """draw score label to screen"""
        self.parent_surf.blit(self.surf, self.rect)


class Ball:
    """ball class"""

    def __init__(self, pong, size=8):
        # reference to game instance
        self.pong = pong
        # reference to players
        self.player1 = pong.player1
        self.player2 = pong.player2

        # get game screen
        self.parent_surf = pong.screen
        # get game screen rect
        self.parent_rect = pong.screen.get_rect()

        # ball's color
        self.color = "#f5d776"

        # ball's rectangle
        self.rect = pygame.Rect(0, 0, size, size)
        self.center_ball()

        # ball's speed and direction
        self.speed = 3
        self.direction = [0.5, 0.5]

    def center_ball(self):
        """position ball at the center of the screen"""
        self.rect.center = self.parent_rect.center

    def start(self):
        """start game"""
        self.center_ball()
        dir_x, dir_y = self.normalize_vector(random.randint(-5, 5), random.randint(-5, 5))
        self.direction = [dir_x, dir_y]

    @staticmethod
    def normalize_vector(x, y):
        """returns a normalized vector"""
        mag = math.sqrt(x*x + y*y)
        if mag == 0:
            return x, y
        return (x/mag), (y/mag)

    def update(self):
        """handle ball movement and collision"""
        self.player_collision()
        self.wall_collision()
        self.move()

    def player_collision(self):
        """check for collision with players"""
        # player one
        if self.rect.colliderect(self.player1.rect):
            self.direction[0] = abs(self.direction[0])
            self.pong.play_hit_sound()
        elif self.rect.colliderect(self.player2.rect):
            self.direction[0] = -abs(self.direction[0])
            self.pong.play_hit_sound()

    def wall_collision(self):
        """handle wall collision"""
        # top wall
        if self.rect.top < 0:
            self.direction[1] = abs(self.direction[1])
            self.pong.play_hit_sound()
        # bottom wall
        if self.rect.bottom > self.parent_rect.bottom:
            self.direction[1] = -abs(self.direction[1])
            self.pong.play_hit_sound()
        # left wall
        if self.rect.right < 0:
            self.pong.point(2)
        # right wall
        if self.rect.left > self.parent_rect.right:
            self.pong.point(1)

    def move(self):
        """move ball"""
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed

    def render(self):
        """draw ball to the screen"""
        pygame.draw.rect(self.parent_surf, self.color, self.rect)


class SFX:
    """sound effect player"""
    def __init__(self, sound):
        self.sound = pygame.mixer.Sound(sound)

    def play(self):
        """play sound effect"""
        pygame.mixer.Sound.play(self.sound)


# create and run an instance of pong
Pong().run()
