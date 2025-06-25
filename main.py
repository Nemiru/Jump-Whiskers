import pygame
import os
import random

# Asset directory
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")

def load_image(filename, scale=None):
    path = os.path.join(ASSETS_DIR, filename)
    image = pygame.image.load(path).convert_alpha()
    if scale:
        image = pygame.transform.scale(image, scale)
    return image


# PrinceCat Class
class PrinceCat(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_image("cat.png", (50, 50))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity_y = 0
        self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.velocity_y = -15
            self.is_jumping = True

    def update(self):
        self.velocity_y += 1
        self.rect.y += self.velocity_y

        if self.rect.y >= 300:
            self.rect.y = 300
            self.is_jumping = False


# Obstacle Class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = load_image("obstacle.png", (30, 60))
        self.rect = self.image.get_rect(topleft=(x, 300))

    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.kill()

# GameState Class
class GameState:
    def __init__(self):
        self.score = 0
        self.is_running = True

    def update_score(self):
        self.score += 1

# Game Class
class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 400
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Prince Cat Runner")
        self.clock = pygame.time.Clock()

        self.background_image = load_image("background.jpg", (self.screen_width, self.screen_height))
        self.cat = PrinceCat(365, 350)
        self.cat_group = pygame.sprite.GroupSingle(self.cat)
        self.obstacles = pygame.sprite.Group()

        self.state = GameState()
        self.spawn_timer = 0

    def run(self):
        while self.state.is_running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        self.end_game_screen()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state.is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.cat.jump()

    def update(self):
        self.cat_group.update()
        self.obstacles.update()
        self.spawn_timer += 1

        if self.spawn_timer > 90:
            self.obstacles.add(Obstacle(800))
            self.spawn_timer = 0

        if pygame.sprite.spritecollide(self.cat, self.obstacles, False):
            self.state.is_running = False

        self.state.update_score()

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))  # Use image background
        self.cat_group.draw(self.screen)
        self.obstacles.draw(self.screen)

        font = pygame.font.SysFont(None, 36)
        score_surf = font.render(f"Score: {self.state.score}", True, (0, 0, 0))
        self.screen.blit(score_surf, (10, 10))

        pygame.display.flip()

    def end_game_screen(self):
        font = pygame.font.SysFont(None, 60)
        small_font = pygame.font.SysFont(None, 36)

        game_over_text = font.render("GAME OVER", True, (176, 96, 205))
        score_text = small_font.render(f"Final Score: {self.state.score}", True, (0, 0, 0))
        continue_text = small_font.render("Press ESC to Quit", True, (100, 100, 100))

        self.screen.fill((255, 255, 255))  # white background for clarity
        self.screen.blit(game_over_text, (self.screen_width // 2 - 150, self.screen_height // 2 - 80))
        self.screen.blit(score_text, (self.screen_width // 2 - 100, self.screen_height // 2))
        self.screen.blit(continue_text, (self.screen_width // 2 - 130, self.screen_height // 2 + 40))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        waiting = False
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
