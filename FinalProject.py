import pygame
import sys
import random
import time
import os

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 900
GRID_SIZE = 5
TILE_SIZE = WIDTH // GRID_SIZE
FONT = pygame.font.SysFont("comicsans", 40)
WHITE = (255, 255, 255)
BG_COLOR = (187, 173, 160)

# Load dead tile image
dead_tile_image = pygame.image.load(os.path.join("SJW.png"))
dead_tile_image = pygame.transform.scale(dead_tile_image, (TILE_SIZE, TILE_SIZE))

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
    512: (100, 170, 255),
    1024: (160, 100, 255),
    2048: (255, 80, 150),
    -1: (100, 100, 100),  
}

DEAD_TILE_THRESHOLDS = [16, 32, 64, 128, 256, 512, 1024, 2048]

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048 with Dead Tiles")

class Game:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.score = 0
        self.dead_tile_flags = set()
        self.start_time = time.time()
        self.time_limit = 120
        self.spawn_tile()
        self.spawn_tile()
        self.game_over = False

    def time_remaining(self):
        return max(0, int(self.time_limit - (time.time() - self.start_time)))

    def spawn_tile(self):
        empty = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if self.grid[r][c] == 0]
        if empty:
            r, c = random.choice(empty)
            self.grid[r][c] = 4 if random.random() < 0.1 else 2

    def spawn_dead_tile(self):
        empty = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if self.grid[r][c] == 0]
        if empty:
            r, c = random.choice(empty)
            self.grid[r][c] = -1

    def can_move(self):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                val = self.grid[r][c]
                if val == 0:
                    return True
                if val == -1:
                    continue
                if c < GRID_SIZE - 1 and self.grid[r][c + 1] == val:
                    return True
                if r < GRID_SIZE - 1 and self.grid[r + 1][c] == val:
                    return True
        return False

    def merge_line(self, line):
        merged = []
        skip = False
        for i in range(len(line)):
            if line[i] == -1:
                merged.append(-1)
            elif line[i] == 0:
                merged.append(0)
            elif not skip and i + 1 < len(line) and line[i] == line[i + 1] and line[i + 1] != -1:
                merged_val = line[i] * 2
                self.score += merged_val
                self.check_dead_tile_trigger(merged_val)
                merged.append(merged_val)
                skip = True
            elif skip:
                skip = False
            else:
                merged.append(line[i])
        while len(merged) < GRID_SIZE:
            merged.append(0)
        return merged[:GRID_SIZE]

    def check_dead_tile_trigger(self, val):
        if val in DEAD_TILE_THRESHOLDS and val not in self.dead_tile_flags:
            self.spawn_dead_tile()
            self.dead_tile_flags.add(val)

    def move_left(self):
        moved = False
        for r in range(GRID_SIZE):
            new_row = []
            for c in range(GRID_SIZE):
                if self.grid[r][c] != 0:
                    new_row.append(self.grid[r][c])
            merged = self.merge_line(new_row)
            new_row = []
            merge_index = 0
            for c in range(GRID_SIZE):
                if merge_index < len(merged):
                    new_row.append(merged[merge_index])
                    merge_index += 1
                else:
                    new_row.append(0)
            if new_row != self.grid[r]:
                self.grid[r] = new_row
                moved = True
        if moved:
            self.spawn_tile()

    def move_right(self):
        self.reverse()
        self.move_left()
        self.reverse()

    def move_up(self):
        self.transpose()
        self.move_left()
        self.transpose()

    def move_down(self):
        self.transpose()
        self.reverse()
        self.move_left()
        self.reverse()
        self.transpose()

    def reverse(self):
        for r in range(GRID_SIZE):
            self.grid[r].reverse()

    def transpose(self):
        self.grid = [list(row) for row in zip(*self.grid)]

    def draw(self, window):
        window.fill(BG_COLOR)
        pygame.draw.rect(window, (119, 110, 101), (0, 0, WIDTH, 100))
        score_text = FONT.render(f"Score: {self.score}", True, WHITE)
        timer_color = (255, 0, 0) if self.time_remaining() <= 10 else WHITE
        timer_text = FONT.render(f"Time: {self.time_remaining()}s", True, timer_color)
        window.blit(score_text, (10, 30))
        window.blit(timer_text, (WIDTH - 200, 30))

        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                val = self.grid[r][c]
                color = TILE_COLORS.get(val, (255, 255, 255))
                rect = pygame.Rect(c * TILE_SIZE, r * TILE_SIZE + 100, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(window, color, rect)
                pygame.draw.rect(window, (119, 110, 101), rect, 4)

                if val > 0:
                    text = FONT.render(str(val), True, (0, 0, 0))
                    text_rect = text.get_rect(center=rect.center)
                    window.blit(text, text_rect)
                elif val == -1:
                    window.blit(dead_tile_image, rect)

        if self.time_remaining() == 0 or not self.can_move():
            self.game_over = True
            over_text = FONT.render("Game Over! Press R to Restart", True, (0, 255, 0))
            window.blit(over_text, over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

    def restart(self):
        self.__init__()

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
                if game.game_over and event.key == pygame.K_r:
                    game.restart()
                elif not game.game_over:
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