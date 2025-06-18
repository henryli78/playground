import pygame
import logging
import numpy as np
from enum import Enum

log = logging.getLogger("myapp")
log.warning("woot")
logging.basicConfig(level=logging.INFO)


class Player(Enum):
    X = 1
    O = -1


class TicTacToe:
    def __init__(self):
        # pixels on screen
        self.px: int = 720
        self.px_unit: int = self.px // 6
        self.screen = pygame.display.set_mode((self.px, self.px))
        self.screen.fill("gray")
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0

        self.grid: np.ndarray[int] = np.array([[0 for _ in range(3)] for _ in range(3)])
        self.active_player: Player = Player.X

    def __enter__(self):
        pygame.init()
        self.font = pygame.font.Font(pygame.font.get_default_font(), 36)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pygame.quit()

    def main(self):
        for event in pygame.event.get():
            # log.info("Found event: %s", event)
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                grid_x, grid_y = self.coords_to_grid_idx(x, y)
                log.info("Found (%s,%s)", grid_x, grid_y)
                if self.grid[grid_y][grid_x]:
                    log.info("Cell already occupied, nothing done")
                    continue

                # clicked, see whose turn it is
                self.grid[grid_y][grid_x] = self.active_player.value
                if self.active_player == Player.O:
                    self.render_O(grid_x, grid_y)
                else:
                    self.render_X(grid_x, grid_y)

                if winner := self.check_any_win():
                    text = self.font.render(f"{winner.name} wins!", True, "black")
                    self.screen.blit(
                        text,
                        (
                            self.px / 2 - text.get_width() / 2,
                            self.px / 2 - text.get_height() / 2,
                        ),
                    )
                self.swap_players()

        # flip() the display to put your work on screen
        pygame.display.flip()

    def render_O(self, x: int, y: int):
        pygame.draw.circle(
            self.screen,
            "white",
            self.grid_idx_to_center(x, y),
            self.px_unit,
            2,
        )

    def render_X(self, x: int, y: int):
        center_x, center_y = self.grid_idx_to_center(x, y)

        pygame.draw.line(
            self.screen,
            "white",
            start_pos=(center_x - self.px_unit, center_y - self.px_unit),
            end_pos=(center_x + self.px_unit, center_y + self.px_unit),
            width=2,
        )

        pygame.draw.line(
            self.screen,
            "white",
            start_pos=(center_x - self.px_unit, center_y + self.px_unit),
            end_pos=(center_x + self.px_unit, center_y - self.px_unit),
            width=2,
        )

    def grid_idx_to_center(self, x: int, y: int) -> tuple[int, int]:
        x_center: int = self.px_unit * (2 * x + 1)
        y_center: int = self.px_unit * (2 * y + 1)
        return (x_center, y_center)

    def coords_to_grid_idx(self, x: int, y: int) -> tuple[int, int]:
        return (int(x // (self.px / 3)), int(y // (self.px / 3)))

    def swap_players(self):
        self.active_player = Player(-self.active_player.value)

    def check_win(self, player: Player) -> bool:
        win_con = player.value * 3
        win_con_row: bool = np.any(np.sum(self.grid) == win_con)
        win_con_col: bool = np.any(np.sum(self.grid, axis=1) == win_con)
        win_con_diag: bool = np.any(
            (np.trace(self.grid) == win_con)
            | (np.trace(np.fliplr(self.grid)) == win_con)
        )
        return win_con_row or win_con_col or win_con_diag

    def check_any_win(self) -> Player | None:
        if self.check_win(Player.X):
            log.info("X wins")
            return Player.X
        elif self.check_win(Player.O):
            log.info("O wins")
            return Player.O
        return None


def main():
    with TicTacToe() as game:
        while game.running:
            game.main()


if __name__ == "__main__":
    main()
