import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 900
GRID_SIZE = 4
TILE_SIZE = WIDTH // GRID_SIZE
FONT = pygame.font.SysFont("comicsans", 40)
WHITE = (255, 255, 255)
BG_COLOR = (187, 173, 160)
TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048 Puzzle")

class Game:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.score = 0
        self.spawn_tile()
        self.spawn_tile()

    def spawn_tile(self):
        empty = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if self.grid[r][c] == 0]
        if empty:
            r, c = random.choice(empty)
            self.grid[r][c] = 4 if random.random() < 0.1 else 2

    def can_move(self):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.grid[r][c] == 0:
                    return True
                if c < GRID_SIZE - 1 and self.grid[r][c] == self.grid[r][c + 1]:
                    return True
                if r < GRID_SIZE - 1 and self.grid[r][c] == self.grid[r + 1][c]:
                    return True
        return False

    def merge_line(self, line):
        new_line = [val for val in line if val != 0]
        merged = []
        i = 0
        while i < len(new_line):
            if i + 1 < len(new_line) and new_line[i] == new_line[i + 1]:
                merged_val = new_line[i] * 2
                self.score += merged_val
                merged.append(merged_val)
                i += 2
            else:
                merged.append(new_line[i])
                i += 1
        merged += [0] * (GRID_SIZE - len(merged))
        return merged

    def move_left(self):
        moved = False
        for r in range(GRID_SIZE):
            original = self.grid[r]
            merged = self.merge_line(original)
            if merged != original:
                self.grid[r] = merged
                moved = True
        if moved:
            self.spawn_tile()

    def move_right(self):
        moved = False
        for r in range(GRID_SIZE):
            original = list(reversed(self.grid[r]))
            merged = self.merge_line(original)
            merged.reverse()
            if merged != self.grid[r]:
                self.grid[r] = merged
                moved = True
        if moved:
            self.spawn_tile()

    def move_up(self):
        moved = False
        for c in range(GRID_SIZE):
            col = [self.grid[r][c] for r in range(GRID_SIZE)]
            merged = self.merge_line(col)
            for r in range(GRID_SIZE):
                if self.grid[r][c] != merged[r]:
                    self.grid[r][c] = merged[r]
                    moved = True
        if moved:
            self.spawn_tile()

    def move_down(self):
        moved = False
        for c in range(GRID_SIZE):
            col = [self.grid[r][c] for r in range(GRID_SIZE - 1, -1, -1)]
            merged = self.merge_line(col)
            merged.reverse()
            for r in range(GRID_SIZE):
                if self.grid[r][c] != merged[r]:
                    self.grid[r][c] = merged[r]
                    moved = True
        if moved:
            self.spawn_tile()

    def draw(self, window):
        window.fill(BG_COLOR)
        pygame.draw.rect(window, (119, 110, 101), (0, 0, WIDTH, 100))
        score_text = FONT.render(f"Score: {self.score}", True, WHITE)
        window.blit(score_text, (10, 30))
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                val = self.grid[r][c]
                color = TILE_COLORS.get(val, (255, 255, 255))
                tile_rect = pygame.Rect(c * TILE_SIZE, r * TILE_SIZE + 100, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(window, color, tile_rect)
                pygame.draw.rect(window, (119, 110, 101), tile_rect, 4)
                if val != 0:
                    text = FONT.render(str(val), True, (0, 0, 0))
                    text_rect = text.get_rect(center=(tile_rect.centerx, tile_rect.centery))
                    window.blit(text, text_rect)

        if not self.can_move():
            over_text = FONT.render("Game Over!", True, (255, 0, 0))
            window.blit(over_text, over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

def main():
    game = Game()
    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    game.move_left()
                elif event.key == pygame.K_d:
                    game.move_right()
                elif event.key == pygame.K_w:
                    game.move_up()
                elif event.key == pygame.K_s:
                    game.move_down()

        game.draw(win)
        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
