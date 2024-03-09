import pygame
import random
import math
import sys


class Main:
    """main game class"""

    def __init__(self):
        # initialize pygame
        pygame.init()

        # set window size, and title
        self.screen = pygame.display.set_mode((640, 360))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Pong")

        # background color
        self.br_color = "#050103"
        # clock object to handle time related data and operations
        self.clock = pygame.time.Clock()

        # initialize players #
        self.left_player = Player("left", self.screen, self.screen_rect)
        self.right_player = Player("right", self.screen, self.screen_rect)

        # initialize center line #
        self.center_line = CenterLine(self.screen, self.screen_rect)

        # initialize score labels #
        self.left_score_label = ScoreLabel(0, "left", self.screen, self.screen_rect)
        self.right_score_label = ScoreLabel(0, "right", self.screen, self.screen_rect)

        # initialize ball #
        self.ball = Ball(self.screen, self.screen_rect)

        # initialize manager #
        self.manager = Manager(self)

    def run(self):
        """game loop"""
        while True:
            self.check_input()
            self.update()
            self.render()

            # make sure game loop is called 60 times per second
            self.clock.tick(60)

    def check_input(self):
        """check for user inputs using an event loop"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # key pressed method #
                self.manager.key_pressed(event.key)
            elif event.type == pygame.KEYUP:
                # key released method #
                self.manager.key_released(event.key)

    def update(self):
        """update game elements"""
        # update players #
        self.left_player.update()
        self.right_player.update()

        # update manager #
        self.manager.update()

        # update ball #
        self.ball.update()

    def render(self):
        """render game elements to the screen"""
        # set background color
        self.screen.fill(self.br_color)

        # render players #
        self.left_player.render()
        self.right_player.render()

        # render center line #
        self.center_line.render()

        # render score labels #
        self.left_score_label.render()
        self.right_score_label.render()

        # render ball #
        self.ball.render()

        # show most recent frame
        pygame.display.flip()


class Player:
    """player/paddle class"""

    def __init__(self, side, screen, screen_rect, width=8, height=96, margin=10):
        # which player? either left or right
        self.side = side

        # screen attributes
        self.screen = screen
        self.screen_rect = screen_rect

        # players rect and margin
        self.color = ""
        self.margin = margin
        self.rect = pygame.Rect(0, 0, width, height)

        # movement_flags
        self.moving_up = False
        self.moving_down = False

        self.speed = 2

        self.set_position()

    def set_position(self):
        """set player position and color according the player's side"""
        if self.side == "left":
            self.color = "#c92631"
            self.rect.midleft = self.screen_rect.midleft
            # add margin
            self.rect.x += self.margin
        elif self.side == "right":
            self.color = "#1a7827"
            self.rect.midright = self.screen_rect.midright
            # add margin
            self.rect.x -= self.margin

    def update(self):
        """move player accordingly"""
        if self.moving_up and self.rect.top > 0:
            self.rect.y -= self.speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.rect.y += self.speed

    def render(self):
        """draw player on screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)


class CenterLine:
    """line at the center of the screen"""

    def __init__(self, screen, screen_rect):
        # screen properties
        self.screen = screen
        self.screen_rect = screen_rect

        # line color, start position and end position
        self.color = "#91896e"
        self.start_pos = self.screen_rect.midtop
        self.end_pos = self.screen_rect.midbottom

    def render(self):
        """draw line on screen"""
        pygame.draw.line(self.screen, self.color, self.start_pos, self.end_pos)


class ScoreLabel:
    """render score text on screen"""

    def __init__(self, text, side, screen, screen_rect, margin=32):
        # set which side of the screen and margin
        self.side = side
        self.margin = margin

        # screen attributes
        self.screen = screen
        self.screen_rect = screen_rect

        # font color and object
        self.color = "#403830"
        self.font = pygame.font.Font(None, 32)

        # label surface, and rect
        self.surf = None
        self.rect = None
        self.set_text(text)

    def set_text(self, text):
        """set score label text and position it on screen accordingly"""
        self.surf = self.font.render(str(text), True, self.color)
        self.rect = self.surf.get_rect()
        self.rect.centery = self.margin

        if self.side == "left":
            self.rect.centerx = self.screen_rect.centerx - self.margin
        elif self.side == "right":
            self.rect.centerx = self.screen_rect.centerx + self.margin

    def render(self):
        """draw score label on screen"""
        self.screen.blit(self.surf, self.rect)


class Ball:
    """ball class"""

    def __init__(self, screen, screen_rect, radius=5):
        # screen attributes
        self.screen = screen
        self.screen_rect = screen_rect

        # ball position, radius, and color
        self.x = self.screen_rect.centerx
        self.y = self.screen_rect.centery
        self.radius = radius
        self.color = "#f5d776"

        # ball speed and direction
        self.speed = 3
        self.direction = [0, 0]

    def center_ball(self):
        """position ball at the center of the screen"""
        self.x = self.screen_rect.centerx
        self.y = self.screen_rect.centery

    def update(self):
        """move ball according to its direction and speed"""
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed

    def render(self):
        """draw ball on screen"""
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)


class Manager:
    """manages game data and operations like player scores, and user input"""

    def __init__(self, main):
        # reference to main game object
        self.main = main

        # player scores
        self.left_score = 0
        self.right_score = 0

    def key_pressed(self, key):
        """manages key down events"""
        if key == pygame.K_w:
            # start moving left player up
            self.main.left_player.moving_up = True
        elif key == pygame.K_UP:
            # start moving right player up
            self.main.right_player.moving_up = True
        elif key == pygame.K_s:
            # start moving left player down
            self.main.left_player.moving_down = True
        elif key == pygame.K_DOWN:
            # start moving right player down
            self.main.right_player.moving_down = True
        elif key == pygame.K_SPACE:
            self.new_game()

    def key_released(self, key):
        """manages key up events"""
        if key == pygame.K_w:
            # stop moving left player up
            self.main.left_player.moving_up = False
        elif key == pygame.K_UP:
            # stop moving right player up
            self.main.right_player.moving_up = False
        elif key == pygame.K_s:
            # stop moving left player down
            self.main.left_player.moving_down = False
        elif key == pygame.K_DOWN:
            # stop moving right player down
            self.main.right_player.moving_down = False

    def new_game(self):
        """start a new game"""
        self.left_score = 0
        self.right_score = 0
        self.main.left_score_label.set_text(self.left_score)
        self.main.right_score_label.set_text(self.right_score)
        self.main.left_player.set_position()
        self.main.right_player.set_position()
        self.shoot_ball()

    def shoot_ball(self):
        """shoot ball at a random angle"""
        self.main.ball.center_ball()

        angle = random.randint(0, 360)
        x = math.cos(angle)
        y = math.sin(angle)

        self.main.ball.direction = [x, y]

    def update(self):
        self.ball_wall_collision()
        self.ball_player_collision()

    def ball_wall_collision(self):
        """handle ball collisions"""
        ball = self.main.ball
        if (ball.y - ball.radius) < 0:
            # top wall
            ball.direction[1] = abs(ball.direction[1])
        elif (ball.y + ball.radius) > ball.screen_rect.bottom:
            # bottom wall
            ball.direction[1] = -abs(ball.direction[1])
        elif ball.x < 0:
            # left side
            self.score_player("right")
        elif ball.x > self.main.screen_rect.right:
            # right side
            self.score_player("left")

    def score_player(self, side):
        """add point to player score"""
        if side == "left":
            self.left_score += 1
            self.main.left_score_label.set_text(self.left_score)
        elif side == "right":
            self.right_score += 1
            self.main.right_score_label.set_text(self.right_score)
        self.shoot_ball()

    def ball_player_collision(self):
        ball = self.main.ball
        if self.circle_rect(ball, self.main.left_player.rect):
            ball.direction[0] = abs(ball.direction[0])
        elif self.circle_rect(ball, self.main.right_player.rect):
            ball.direction[0] = -abs(ball.direction[0])

    @staticmethod
    def circle_rect(circle, rect):
        """detect collision between circle and rectangle"""
        x = circle.x
        y = circle.y

        if circle.x < rect.x:
            x = rect.x
        elif circle.x > rect.x+rect.width:
            x = rect.x+rect.width
        if circle.y < rect.y:
            y = rect.y
        elif circle.y > rect.y+rect.height:
            y = rect.y+rect.height

        a = circle.x-x
        b = circle.y-y
        distance = math.sqrt(a*a + b*b)

        if distance < circle.radius:
            return True
        return False


Main().run()
