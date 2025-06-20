import pygame
from enum import Enum
from utils.logging import Log


class Orientation(Enum):
    LEFT = 1
    RIGHT = 2


class Paddle:
    def __init__(self, orientation: Orientation, screen_width: int, screen_height: int, screen: pygame.Surface):
        self.width: int = 10
        self.height: int = 100
        self.y: int = screen_height / 2 - self.height / 2
        self.screen: pygame.Surface = screen

        self.orientation: Orientation = orientation
        if orientation == Orientation.LEFT:
            self.x = 0
            self.CONTROL_UP = pygame.K_w
            self.CONTROL_DOWN = pygame.K_s
        else:
            self.x = screen_width - self.width
            self.CONTROL_UP = pygame.K_UP
            self.CONTROL_DOWN = pygame.K_DOWN

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        self.render = pygame.draw.rect(self.screen, "black", self.rect)

    def move(self, movement: int):
        self.rect.move_ip(0, movement)


class Ball:
    def __init__(self, screen_width: int, screen_height: int, screen: pygame.Surface):
        self.x: int = screen_width / 2
        self.y: int = screen_height / 2
        self.screen: pygame.Surface = screen
        self.radius: int = 10

    def draw(self):
        pygame.draw.circle(self.screen, "red", (self.x, self.y), self.radius)


class Pong:
    def __init__(self):
        self.px_width: int = 720
        self.px_height: int = 480
        self.screen = pygame.display.set_mode((self.px_width, self.px_height))
        self.screen.fill("gray")
        self.dt: int = 0
        self.speed: int = 300

        self.init_objects()

        self.running: bool = True

    def __enter__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
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

    def event_handler(self):
        self.screen.fill("gray")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        # Handle keyboard input outside the event loop
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

        self.display_objects()

        self.dt = self.clock.tick(60) / 1000

        pygame.display.flip()

    def display_objects(self):
        self.left.draw()
        self.right.draw()
        self.ball.draw()

    def restart(self):
        self.__init__()


def main():
    with Pong() as game:
        while game.running:
            game.event_handler()


if __name__ == "__main__":
    main()
