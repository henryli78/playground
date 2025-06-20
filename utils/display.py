import pygame


def render_centered_text_lines(screen: pygame.Surface, lines: list[str], font: pygame.font.Font, color="black"):
    """Render multiple lines of text centered on the screen."""
    rendered_lines = [font.render(line, True, color) for line in lines]
    total_height = sum(line.get_height() for line in rendered_lines)

    # Start Y so that the whole block is vertically centered
    start_y = screen.get_height() / 2 - total_height / 2

    for line in rendered_lines:
        x = screen.get_width() / 2 - line.get_width() / 2
        screen.blit(line, (x, start_y))
        start_y += line.get_height()
