import random
import sys
from dataclasses import dataclass

import pygame

# Game config
CELL = 20
GRID_W = 30
GRID_H = 22
WIDTH = GRID_W * CELL
HEIGHT = GRID_H * CELL
FPS_START = 8
FPS_MAX = 18

BG = (18, 20, 24)
GRID = (30, 33, 40)
SNAKE = (93, 201, 159)
SNAKE_HEAD = (120, 220, 180)
FOOD = (235, 95, 95)
TEXT = (230, 232, 238)


@dataclass
class Vec:
    x: int
    y: int

    def __add__(self, other: "Vec") -> "Vec":
        return Vec(self.x + other.x, self.y + other.y)


DIRS = {
    pygame.K_UP: Vec(0, -1),
    pygame.K_DOWN: Vec(0, 1),
    pygame.K_LEFT: Vec(-1, 0),
    pygame.K_RIGHT: Vec(1, 0),
    pygame.K_w: Vec(0, -1),
    pygame.K_s: Vec(0, 1),
    pygame.K_a: Vec(-1, 0),
    pygame.K_d: Vec(1, 0),
}


class SnakeGame:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Snake")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 22)
        self.reset()

    def reset(self) -> None:
        mid = Vec(GRID_W // 2, GRID_H // 2)
        self.snake = [mid, Vec(mid.x - 1, mid.y), Vec(mid.x - 2, mid.y)]
        self.dir = Vec(1, 0)
        self.next_dir = Vec(1, 0)
        self.place_food()
        self.score = 0
        self.game_over = False

    def place_food(self) -> None:
        occupied = {(p.x, p.y) for p in self.snake}
        while True:
            x = random.randrange(GRID_W)
            y = random.randrange(GRID_H)
            if (x, y) not in occupied:
                self.food = Vec(x, y)
                return

    def handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)
                if self.game_over and event.key == pygame.K_SPACE:
                    self.reset()
                if event.key in DIRS:
                    new_dir = DIRS[event.key]
                    # Prevent reversing directly into itself
                    if not (new_dir.x == -self.dir.x and new_dir.y == -self.dir.y):
                        self.next_dir = new_dir

    def step(self) -> None:
        if self.game_over:
            return
        self.dir = self.next_dir
        head = self.snake[0] + self.dir

        # Wall collision
        if head.x < 0 or head.x >= GRID_W or head.y < 0 or head.y >= GRID_H:
            self.game_over = True
            return

        # Self collision
        if any(head.x == p.x and head.y == p.y for p in self.snake):
            self.game_over = True
            return

        self.snake.insert(0, head)

        # Food
        if head.x == self.food.x and head.y == self.food.y:
            self.score += 1
            self.place_food()
        else:
            self.snake.pop()

    def draw_grid(self) -> None:
        for x in range(0, WIDTH, CELL):
            pygame.draw.line(self.screen, GRID, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL):
            pygame.draw.line(self.screen, GRID, (0, y), (WIDTH, y))

    def draw(self) -> None:
        self.screen.fill(BG)
        self.draw_grid()

        # Food
        pygame.draw.rect(
            self.screen,
            FOOD,
            (self.food.x * CELL + 2, self.food.y * CELL + 2, CELL - 4, CELL - 4),
        )

        # Snake
        for i, p in enumerate(self.snake):
            color = SNAKE_HEAD if i == 0 else SNAKE
            pygame.draw.rect(
                self.screen,
                color,
                (p.x * CELL + 2, p.y * CELL + 2, CELL - 4, CELL - 4),
            )

        # HUD
        score_surf = self.font.render(f"Score: {self.score}", True, TEXT)
        self.screen.blit(score_surf, (8, 6))

        if self.game_over:
            msg = "Game Over — press Space to restart"
            msg_surf = self.font.render(msg, True, TEXT)
            rect = msg_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(msg_surf, rect)

        pygame.display.flip()

    def run(self) -> None:
        while True:
            self.handle_input()
            self.step()
            self.draw()
            # Speed scales with score
            fps = min(FPS_START + self.score // 2, FPS_MAX)
            self.clock.tick(fps)


if __name__ == "__main__":
    SnakeGame().run()
