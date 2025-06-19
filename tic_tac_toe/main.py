import pygame
import numpy as np
from dataclasses import dataclass
from enum import Enum
from utils.logging import Log


class Player(Enum):
    X = 1
    O = -1


@dataclass
class Point:
    x: int
    y: int


class TicTacToe:
    def __init__(self):
        # pixels on screen
        self.px: int = 720
        self.px_unit: int = self.px // 6
        self.line_width: int = 5
        self.screen = pygame.display.set_mode((self.px, self.px))
        self.screen.fill("gray")
        self._render_gridlines()

        self.grid: np.ndarray[int] = np.array([[0 for _ in range(3)] for _ in range(3)])
        self.active_player: Player = Player.X

        self.running: bool = True
        self._finished: bool = False  # checks if a winner has been found or not

    def __enter__(self):
        pygame.init()
        self.font = pygame.font.Font(pygame.font.get_default_font(), 36)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pygame.quit()

    def _render_gridlines(self):
        for i in range(1, 3):
            px = self.px_unit * 2 * i

            pygame.draw.line(
                self.screen,
                "black",
                start_pos=(px, 0),
                end_pos=(px, self.px),
                width=self.line_width,
            )
            pygame.draw.line(
                self.screen,
                "black",
                start_pos=(0, px),
                end_pos=(self.px, px),
                width=self.line_width,
            )

    def main(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_click()
            if self._finished and (event.type == pygame.KEYDOWN) and (event.key == pygame.K_r):
                Log.info("Triggered restart callback")
                self.restart()

        # flip() the display to put your work on screen
        pygame.display.flip()

    def handle_click(self):
        if self._finished:
            return
        pos: Point = Point(*pygame.mouse.get_pos())
        grid_x, grid_y = self.coords_to_grid_idx(pos)
        Log.info("Found (%s,%s)", grid_x, grid_y)
        if self.grid[grid_y][grid_x]:
            Log.info("Cell already occupied, nothing done")
            return

        # clicked, see whose turn it is
        self.grid[grid_y][grid_x] = self.active_player.value
        if self.active_player == Player.O:
            self.render_O(grid_x, grid_y)
        else:
            self.render_X(grid_x, grid_y)

        if winner := self.check_any_win():
            self.render_centered_text_lines([f"{winner.name} wins!", "Press R to restart"])
            self._finished = True
            return
        elif not np.any(self.grid == 0):
            self.render_centered_text_lines(["It's a tie!", "Press R to restart"])
            self._finished = True
            return
        self.swap_players()

    def render_centered_text_lines(self, lines: list[str], color="black"):
        """Render multiple lines of text centered on the screen."""
        rendered_lines = [self.font.render(line, True, color) for line in lines]
        total_height = sum(line.get_height() for line in rendered_lines)

        # Start Y so that the whole block is vertically centered
        start_y = self.px / 2 - total_height / 2

        for line in rendered_lines:
            x = self.px / 2 - line.get_width() / 2
            self.screen.blit(line, (x, start_y))
            start_y += line.get_height()

    def render_O(self, x: int, y: int):
        pygame.draw.circle(
            self.screen,
            "white",
            self.grid_idx_to_center(x, y),
            int(self.px_unit * 0.9),
            self.line_width,
        )

    def render_X(self, x: int, y: int):
        center_x, center_y = self.grid_idx_to_center(x, y)
        offset: int = int(self.px_unit * 0.9)

        pygame.draw.line(
            self.screen,
            "white",
            start_pos=(center_x - offset, center_y - offset),
            end_pos=(center_x + offset, center_y + offset),
            width=self.line_width,
        )

        pygame.draw.line(
            self.screen,
            "white",
            start_pos=(center_x - offset, center_y + offset),
            end_pos=(center_x + offset, center_y - offset),
            width=self.line_width,
        )

    def grid_idx_to_center(self, x: int, y: int) -> tuple[int, int]:
        x_center: int = self.px_unit * (2 * x + 1)
        y_center: int = self.px_unit * (2 * y + 1)
        return (x_center, y_center)

    def coords_to_grid_idx(self, p: Point) -> tuple[int, int]:
        return (int(p.x // (self.px / 3)), int(p.y // (self.px / 3)))

    def restart(self):
        self.__init__()

    def swap_players(self):
        self.active_player = Player(-self.active_player.value)

    def check_win(self, player: Player) -> bool:
        win_con = player.value * 3
        win_con_row: bool = np.any(np.sum(self.grid, axis=0) == win_con)
        win_con_col: bool = np.any(np.sum(self.grid, axis=1) == win_con)
        win_con_diag: bool = np.any((np.trace(self.grid) == win_con) | (np.trace(np.fliplr(self.grid)) == win_con))
        return win_con_row or win_con_col or win_con_diag

    def check_any_win(self) -> Player | None:
        if self.check_win(Player.X):
            Log.info("X wins")
            return Player.X
        elif self.check_win(Player.O):
            Log.info("O wins")
            return Player.O
        return None


def main():
    with TicTacToe() as game:
        while game.running:
            game.main()


if __name__ == "__main__":
    main()
