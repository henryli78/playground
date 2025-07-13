import pygame
from dataclasses import dataclass
from typing import Optional


@dataclass
class FadingText:
    text: str
    color: str | tuple[int, int, int]
    font: pygame.font.Font
    fade_start: float
    fade_duration: float = 1.0

    def should_render(self, current_time: float) -> bool:
        return current_time - self.fade_start < self.fade_duration

    def render(self, screen: pygame.Surface, center_pos: tuple[int, int], current_time: float):
        if not self.should_render(current_time):
            return

        elapsed = current_time - self.fade_start
        # Calculate alpha based on time elapsed (fade from 255 to 0)
        alpha = int(255 * (1 - elapsed / self.fade_duration))

        # Create text surface
        text_surface = self.font.render(self.text, True, self.color)

        # Create a surface with alpha channel
        alpha_surface = pygame.Surface(text_surface.get_size(), pygame.SRCALPHA)
        alpha_surface.fill((0, 0, 0, alpha))
        text_surface.blit(alpha_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        # Center and render the text
        text_rect = text_surface.get_rect(center=center_pos)
        screen.blit(text_surface, text_rect)


def render_centered_text_lines(
    screen: pygame.Surface, lines: list[str], font: pygame.font.Font, color: str | tuple[int, int, int]
):
    """Renders multiple lines of text centered on the screen."""
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    line_height = font.get_linesize()
    total_height = line_height * len(lines)
    start_y = (screen_height - total_height) / 2

    for i, line in enumerate(lines):
        text = font.render(line, True, color)
        text_rect = text.get_rect(center=(screen_width / 2, start_y + i * line_height))
        screen.blit(text, text_rect)


def create_fading_text(
    text: str, color: str | tuple[int, int, int], font: pygame.font.Font, fade_duration: float = 1.0
) -> FadingText:
    """Creates a FadingText object with the current time as fade start."""
    return FadingText(
        text=text, color=color, font=font, fade_start=pygame.time.get_ticks() / 1000, fade_duration=fade_duration
    )
