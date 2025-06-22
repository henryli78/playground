import pygame
import numpy as np
from enum import Enum
from utils.logging import Log
from dataclasses import dataclass
from typing import Optional
from utils.display import FadingText, create_fading_text


class Orientation(Enum):
    LEFT = 1
    RIGHT = 2


@dataclass
class Velocity:
    x: float
    y: float


class Paddle:
    def __init__(self, orientation: Orientation, screen_width: int, screen_height: int, screen: pygame.Surface):
        self.width: int = 10
        self.height: int = 100
        self.screen: pygame.Surface = screen
        self.screen_height: int = screen_height

        self.orientation: Orientation = orientation
        if orientation == Orientation.LEFT:
            self.x = 0
            self.CONTROL_UP = pygame.K_w
            self.CONTROL_DOWN = pygame.K_s
        else:
            self.x = screen_width - self.width
            self.CONTROL_UP = pygame.K_UP
            self.CONTROL_DOWN = pygame.K_DOWN

        self.rect = pygame.Rect(self.x, screen_height / 2 - self.height / 2, self.width, self.height)

    def draw(self):
        self.render = pygame.draw.rect(self.screen, "black", self.rect)

    def move(self, movement: int):
        new_y = self.rect.y + movement
        # paddles can't move out of the screen
        new_y = max(0, min(new_y, self.screen_height - self.height))

        self.rect.y = new_y


class Ball:
    def __init__(self, screen_width: int, screen_height: int, screen: pygame.Surface):
        self.x: int = screen_width / 2
        self.y: int = screen_height / 2
        self.screen: pygame.Surface = screen
        self.radius: int = 10
        self.velocity: Velocity = Velocity(x=0, y=0)
        self.hit_box: pygame.Rect = pygame.Rect(
            self.x - self.radius, self.y - self.radius, 2 * self.radius, 2 * self.radius
        )

    def draw(self):
        self.circle = pygame.draw.circle(self.screen, "red", (self.x, self.y), self.radius)

    def start(self, speed: float, direction: Orientation):
        self.velocity.x = speed if direction == Orientation.RIGHT else -speed
        self.velocity.y = speed * np.random.uniform(-0.5, 0.5)

    def move(self, dt: float):
        self.x += self.velocity.x * dt
        self.y += self.velocity.y * dt
        self.hit_box.centerx = self.x
        self.hit_box.centery = self.y

    def bounce_x(self):
        self.velocity.x = -self.velocity.x

    def bounce_y(self):
        self.velocity.y = -self.velocity.y


class Score:
    def __init__(self, screen_width: int, screen: pygame.Surface):
        self.screen: pygame.Surface = screen
        self.font_size: int = 36
        self.x: int = screen_width / 2
        self.y: int = self.font_size
        self.font = pygame.font.Font(pygame.font.get_default_font(), self.font_size)
        self.left_score: int = 0
        self.right_score: int = 0

    def draw(self):
        self.text = self.font.render(f"{self.left_score} - {self.right_score}", True, "black")
        text_rect = self.text.get_rect()
        text_rect.center = (self.x, self.y)
        self.screen.blit(self.text, text_rect)

    def increment_left(self):
        self.left_score += 1

    def increment_right(self):
        self.right_score += 1


class Pong:
    def __init__(self, speed: int = 300, latest_winner: Orientation = Orientation.LEFT):
        self.px_width: int = 720
        self.px_height: int = 480
        self.screen = pygame.display.set_mode((self.px_width, self.px_height))
        self.screen.fill("gray")
        self.dt: int = 0
        self.speed: int = speed

        # Speed indicator properties
        self.speed_indicator: Optional[FadingText] = None
        self.speed_font = pygame.font.Font(pygame.font.get_default_font(), 36)

        self.init_objects()

        self.game_start_state: bool = True
        self.latest_winner: Orientation = latest_winner
        self.running: bool = True
        self.paused: bool = False

    def __enter__(self):
        self.clock = pygame.time.Clock()
        self.score = Score(self.px_width, self.screen)
        pygame.display.set_caption("Pong")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pygame.quit()

    def init_objects(self):
        self.left = Paddle(Orientation.LEFT, self.px_width, self.px_height, self.screen)
        self.right = Paddle(Orientation.RIGHT, self.px_width, self.px_height, self.screen)

        self.left.draw()
        self.right.draw()

        self.ball = Ball(self.px_width, self.px_height, self.screen)
        self.ball.draw()

    def update_game_state(self):
        if self.paused or self.game_start_state:
            return

        keys = pygame.key.get_pressed()
        movement = self.speed * self.dt
        if keys[self.left.CONTROL_UP]:
            self.left.move(-movement)
        if keys[self.left.CONTROL_DOWN]:
            self.left.move(movement)
        if keys[self.right.CONTROL_UP]:
            self.right.move(-movement)
        if keys[self.right.CONTROL_DOWN]:
            self.right.move(movement)

        self.ball.move(self.dt)
        self.check_collision()

    def show_speed_indicator(self):
        self.speed_indicator = create_fading_text(text=f"Speed: {self.speed}", color="black", font=self.speed_font)

    def render_speed_indicator(self):
        if self.speed_indicator:
            current_time = pygame.time.get_ticks() / 1000
            self.speed_indicator.render(self.screen, (self.px_width / 2, self.px_height / 2), current_time)
            if not self.speed_indicator.should_render(current_time):
                self.speed_indicator = None

    def event_handler(self):
        self.screen.fill("gray")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.game_start_state:
                    self.game_start_state = False
                    self.ball.start(self.speed, self.latest_winner)
                elif event.key == pygame.K_p:
                    self.paused = not self.paused
                elif event.unicode == "+":
                    old_speed = self.speed
                    self.speed += 30
                    self.ball.velocity.x *= self.speed / old_speed
                    self.show_speed_indicator()
                elif event.unicode == "-":
                    old_speed = self.speed
                    self.speed -= 30
                    self.ball.velocity.x *= self.speed / old_speed
                    self.show_speed_indicator()

        self.update_game_state()
        self.display_objects()

        # Show pause indicator if paused
        if self.paused:
            pause_font = pygame.font.Font(pygame.font.get_default_font(), 48)
            pause_text = pause_font.render("PAUSED", True, "red")
            text_rect = pause_text.get_rect(center=(self.px_width / 2, self.px_height / 2))
            self.screen.blit(pause_text, text_rect)

        # Render speed indicator with fade effect
        self.render_speed_indicator()

        self.dt = self.clock.tick(60) / 1000
        pygame.display.flip()

    def display_objects(self):
        self.left.draw()
        self.right.draw()
        self.ball.draw()
        self.score.draw()

    def check_collision(self):
        if self.ball.hit_box.colliderect(self.left.rect) or self.ball.hit_box.colliderect(self.right.rect):
            self.ball.bounce_x()

        if self.ball.y - self.ball.radius <= 0 or self.ball.y + self.ball.radius >= self.px_height:
            self.ball.bounce_y()

        if self.ball.x < 0:
            self.score.increment_right()
            self.latest_winner = Orientation.RIGHT
            self.restart()
        elif self.ball.x > self.px_width:
            self.score.increment_left()
            self.latest_winner = Orientation.LEFT
            self.restart()

    def restart(self):
        self.__init__(self.speed, self.latest_winner)


def main():
    pygame.init()
    with Pong() as game:
        while game.running:
            game.event_handler()


if __name__ == "__main__":
    main()
