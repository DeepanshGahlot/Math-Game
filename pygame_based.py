import pygame
import random
import math
import time
import os
import json 
# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
DARK_BLUE = (0, 0, 139)
SILVER = (192, 192, 192)
GOLD = (255, 215, 0)
DARK_RED = (139, 0, 0)
DARK_GREEN = (0, 100, 0)

class Particle:
    def __init__(self, x, y, color, speed_x, speed_y, life=30):
        self.x = x
        self.y = y
        self.color = color
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.life = life
        self.max_life = life
        self.size = random.randint(2, 5)
        
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.life -= 1
        self.speed_y += 0.2  # Gravity
        
    def draw(self, screen):
        if self.life > 0:
            alpha = int(255 * (self.life / self.max_life))
            color = (*self.color, alpha)
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

class NinjaNumberSlashGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🥷 Ninja Number Slash 🥷")
        self.clock = pygame.time.Clock()
        
        # Load assets
        self.load_assets()
        
        # Game state
        self.game_state = "menu"  # menu, instructions, game, game_over
        self.score = 0
        
        with open("high_score.json", "r") as f:
            self.high_score = json.load(f)
            print(self.high_score,'---------------')

        self.level = 1
        self.time_limit = 30
        self.correct_answers = 0
        self.total_questions = 0
        self.current_property = ""
        self.current_number = 0
        
        # Timing
        self.level_start_time = 0
        self.question_start_time = 0
        self.time_per_question = 5
        
        # Visual effects
        self.particles = []
        self.slash_animation = 0
        self.number_scale = 1.0
        self.background_color = DARK_BLUE
        self.flash_color = None
        self.flash_timer = 0
        self.bg_alpha = 180  # For background transparency overlay
        
        # Button positions
        self.slash_button = pygame.Rect(200, 500, 200, 80)
        self.dodge_button = pygame.Rect(600, 500, 200, 80)
        
        # Menu buttons
        self.start_button = pygame.Rect(350, 300, 300, 60)
        self.instructions_button = pygame.Rect(350, 380, 300, 60)
        self.quit_button = pygame.Rect(350, 460, 300, 60)
        
    def load_assets(self):
        """Load background image and fonts with error handling"""
        # Load background image
        try:
            self.bg_image = pygame.image.load("assets/ninja bg.jpg")
            self.bg_image = pygame.transform.scale(self.bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            print("✓ Background image loaded successfully")
        except pygame.error:
            print("⚠ Background image not found, using gradient background")
            self.bg_image = None
            
        # Load custom font
        try:
            font_path = "assets/Tanji-Wp9rn.otf"
            self.ninja_font_big = pygame.font.Font(font_path, 72)
            self.ninja_font_medium = pygame.font.Font(font_path, 48)
            self.ninja_font_small = pygame.font.Font(font_path, 32)
            self.ninja_font_tiny = pygame.font.Font(font_path, 24)
            print("✓ Custom ninja font loaded successfully")
        except pygame.error:
            print("⚠ Custom font not found, using default fonts")
            self.ninja_font_big = pygame.font.Font(None, 72)
            self.ninja_font_medium = pygame.font.Font(None, 48)
            self.ninja_font_small = pygame.font.Font(None, 32)
            self.ninja_font_tiny = pygame.font.Font(None, 24)
            
        # Set up font hierarchy
        self.big_font = self.ninja_font_big
        self.medium_font = self.ninja_font_medium
        self.small_font = self.ninja_font_small
        self.tiny_font = self.ninja_font_tiny
        
    def draw_background(self, overlay_alpha=100):
        """Draw background with optional overlay for better text readability"""
        if self.bg_image:
            self.screen.blit(self.bg_image, (0, 0))
            
            # Add semi-transparent overlay for better text visibility
            if overlay_alpha > 0:
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                overlay.set_alpha(overlay_alpha)
                overlay.fill(BLACK)
                self.screen.blit(overlay, (0, 0))
        else:
            # Fallback gradient background
            for i in range(SCREEN_HEIGHT):
                color_value = int(50 + (i / SCREEN_HEIGHT) * 100)
                color = (0, 0, color_value)
                pygame.draw.line(self.screen, color, (0, i), (SCREEN_WIDTH, i))
        
    def is_prime(self, n):
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        return True
        
    def is_perfect_square(self, n):
        if n < 0:
            return False
        sqrt_n = int(math.sqrt(n))
        return sqrt_n * sqrt_n == n
        
    def is_multiple_of_3(self, n):
        return n % 3 == 0
        
    def is_fibonacci(self, n):
        fib_numbers = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987]
        return n in fib_numbers
        
    def is_even(self, n):
        return n % 2 == 0
        
    def check_property(self, number, property_type):
        if property_type == "prime":
            return self.is_prime(number)
        elif property_type == "perfect_square":
            return self.is_perfect_square(number)
        elif property_type == "multiple_of_3":
            return self.is_multiple_of_3(number)
        elif property_type == "fibonacci":
            return self.is_fibonacci(number)
        elif property_type == "even":
            return self.is_even(number)
        return False
        
    def get_level_config(self):
        if self.level == 1:
            return {
                "properties": ["prime", "even", "multiple_of_3"],
                "number_range": (1, 50),
                "time_per_question": 5
            }
        else:
            return {
                "properties": ["prime", "perfect_square", "fibonacci", "multiple_of_3"],
                "number_range": (1, 100),
                "time_per_question": 4
            }
            
    def get_property_description(self, property_type):
        descriptions = {
            "prime": "Prime Number",
            "even": "Even Number",
            "multiple_of_3": "Multiple of 3",
            "perfect_square": "Perfect Square",
            "fibonacci": "Fibonacci Number"
        }
        return descriptions.get(property_type, "Unknown")
        
    def create_particles(self, x, y, color, count=10):
        for _ in range(count):
            speed_x = random.uniform(-5, 5)
            speed_y = random.uniform(-8, -2)
            self.particles.append(Particle(x, y, color, speed_x, speed_y))
            
    def draw_ninja(self, x, y, size=50):
        # Ninja body with glow effect
        pygame.draw.circle(self.screen, (30, 30, 30), (x, y), size + 3)
        pygame.draw.circle(self.screen, BLACK, (x, y), size)
        
        # Ninja eyes with glow
        pygame.draw.circle(self.screen, (200, 200, 255), (x-15, y-10), 10)
        pygame.draw.circle(self.screen, WHITE, (x-15, y-10), 8)
        pygame.draw.circle(self.screen, (200, 200, 255), (x+15, y-10), 10)
        pygame.draw.circle(self.screen, WHITE, (x+15, y-10), 8)
        pygame.draw.circle(self.screen, BLACK, (x-15, y-10), 4)
        pygame.draw.circle(self.screen, BLACK, (x+15, y-10), 4)
        
        # Ninja sword with enhanced effects
        if self.slash_animation > 0:
            sword_length = 40 + self.slash_animation * 2
            sword_end_x = x + sword_length
            sword_end_y = y - 20
            
            # Sword trail effect
            for i in range(5):
                trail_alpha = 255 - (i * 50)
                trail_x = x + 20 + (i * 5)
                trail_y = y - 10 + (i * 2)
                pygame.draw.line(self.screen, (192, 192, 192, trail_alpha), 
                               (trail_x, trail_y), (sword_end_x - i*3, sword_end_y + i*2), 2)
                
            # Main sword
            pygame.draw.line(self.screen, SILVER, (x+20, y-10), (sword_end_x, sword_end_y), 4)
            pygame.draw.line(self.screen, WHITE, (x+20, y-10), (sword_end_x, sword_end_y), 2)
            pygame.draw.circle(self.screen, GOLD, (x+20, y-10), 6)
            pygame.draw.circle(self.screen, YELLOW, (x+20, y-10), 4)
            
    def draw_button(self, rect, text, color, text_color=WHITE, glow=False):
        # Enhanced button with glow effect
        if glow:
            glow_rect = pygame.Rect(rect.x - 3, rect.y - 3, rect.width + 6, rect.height + 6)
            pygame.draw.rect(self.screen, (min(255, color[0] + 50), min(255, color[1] + 50), min(255, color[2] + 50)), glow_rect)
            
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, WHITE, rect, 3)
        
        text_surface = self.medium_font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)
        
    def draw_text_with_shadow(self, text, font, color, x, y, shadow_color=(0, 0, 0), shadow_offset=2):
        """Draw text with shadow effect"""
        # Draw shadow
        shadow_surface = font.render(text, True, shadow_color)
        shadow_rect = shadow_surface.get_rect(center=(x + shadow_offset, y + shadow_offset))
        self.screen.blit(shadow_surface, shadow_rect)
        
        # Draw main text
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)
        
    def draw_menu(self):
        # Draw background
        self.draw_background(overlay_alpha=80)
        
        # Title with enhanced effects
        self.draw_text_with_shadow("🥷 NINJA NUMBER SLASH 🥷", self.big_font, GOLD, 
                                  SCREEN_WIDTH//2, 150, shadow_offset=3)
        
        # Subtitle
        self.draw_text_with_shadow("Master the Art of Mathematical Combat", self.medium_font, WHITE, 
                                  SCREEN_WIDTH//2, 200)
        # High score with glow effect
        self.draw_text_with_shadow(f"High Score: {self.high_score}", self.small_font, YELLOW, 
                                  SCREEN_WIDTH//2, 250)
        
        # Draw ninja
        self.draw_ninja(SCREEN_WIDTH//2, 600, 60)
        
        # Buttons with hover effects
        mouse_pos = pygame.mouse.get_pos()
        
        start_glow = self.start_button.collidepoint(mouse_pos)
        instructions_glow = self.instructions_button.collidepoint(mouse_pos)
        quit_glow = self.quit_button.collidepoint(mouse_pos)
        
        self.draw_button(self.start_button, "START GAME", DARK_GREEN, glow=start_glow)
        self.draw_button(self.instructions_button, "INSTRUCTIONS", BLUE, glow=instructions_glow)
        self.draw_button(self.quit_button, "QUIT", DARK_RED, glow=quit_glow)
        
    def draw_instructions(self):
        self.draw_background(overlay_alpha=120)
        
        self.draw_text_with_shadow("NINJA TRAINING SCROLL", self.big_font, GOLD, 
                                  SCREEN_WIDTH//2, 50, shadow_offset=3)
        
        instructions = [
            "MISSION: Slash correct numbers, dodge wrong ones!",
            "",
            "LEVEL 1 TARGETS:",
            "• Prime numbers (2, 3, 5, 7, 11...)",
            "• Even numbers (2, 4, 6, 8...)",
            "• Multiples of 3 (3, 6, 9, 12...)",
            "",
            "LEVEL 2 TARGETS:",
            "• All Level 1 targets PLUS:",
            "• Perfect squares (1, 4, 9, 16, 25...)",
            "• Fibonacci numbers (0, 1, 1, 2, 3, 5, 8...)",
            "",
            "CONTROLS:",
            "• Click SLASH button or press SPACE for YES",
            "• Click DODGE button or press D for NO",
            "",
            "SCORING:",
            "• Level 1: +10 points correct, -5 wrong",
            "• Level 2: +15 points correct, -5 wrong",
            "",
            "Press ESC to return to menu"
        ]
        
        y_offset = 120
        for line in instructions:
            if line.startswith("•"):
                color = YELLOW
            elif line.isupper() and line.endswith(":"):
                color = ORANGE
            else:
                color = WHITE
                
            text_surface = self.small_font.render(line, True, color)
            # Add shadow for better readability
            shadow_surface = self.small_font.render(line, True, BLACK)
            self.screen.blit(shadow_surface, (52, y_offset + 2))
            self.screen.blit(text_surface, (50, y_offset))
            y_offset += 25
            
    def draw_game(self):
        # Background with flash effect
        if self.flash_color and self.flash_timer > 0:
            self.draw_background(overlay_alpha=50)
            flash_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            flash_surface.set_alpha(100)
            flash_surface.fill(self.flash_color)
            self.screen.blit(flash_surface, (0, 0))
        else:
            self.draw_background(overlay_alpha=100)
        
        # Draw particles
        for particle in self.particles[:]:
            particle.update()
            particle.draw(self.screen)
            if particle.life <= 0:
                self.particles.remove(particle)
                
        # HUD with shadows
        self.draw_text_with_shadow(f"Score: {self.score}", self.medium_font, WHITE, 120, 35)
        self.draw_text_with_shadow(f"Level: {self.level}", self.medium_font, WHITE, 120, 75)
        
        accuracy = (self.correct_answers / max(1, self.total_questions)) * 100
        self.draw_text_with_shadow(f"Accuracy: {accuracy:.1f}%", self.small_font, WHITE, 120, 115)
        
        # Time remaining
        time_left = self.time_limit - (time.time() - self.level_start_time)
        time_color = RED if time_left < 5 else WHITE
        self.draw_text_with_shadow(f"Time: {max(0, time_left):.1f}s", self.medium_font, time_color, 
                                  SCREEN_WIDTH-120, 35)
        
        # Current target
        self.draw_text_with_shadow(f"TARGET: {self.get_property_description(self.current_property)}", 
                                  self.medium_font, YELLOW, SCREEN_WIDTH//2, 150, shadow_offset=3)
        
        # Current number (with scale animation and glow)
        number_size = int(120 * self.number_scale)
        number_font = pygame.font.Font(None, number_size)
        
        # Number glow effect
        for offset in range(5, 0, -1):
            glow_alpha = 50 - (offset * 10)
            glow_color = (255, 255, 255, glow_alpha)
            glow_text = number_font.render(str(self.current_number), True, (200, 200, 255))
            glow_rect = glow_text.get_rect(center=(SCREEN_WIDTH//2 + offset, 300 + offset))
            self.screen.blit(glow_text, glow_rect)
            
        # Main number
        self.draw_text_with_shadow(str(self.current_number), number_font, WHITE, 
                                  SCREEN_WIDTH//2, 300, shadow_offset=4)
        
        # Question
        self.draw_text_with_shadow(f"Is {self.current_number} a {self.current_property.replace('_', ' ')}?", 
                                  self.medium_font, WHITE, SCREEN_WIDTH//2, 400)
        
        # Enhanced buttons
        mouse_pos = pygame.mouse.get_pos()
        slash_glow = self.slash_button.collidepoint(mouse_pos)
        dodge_glow = self.dodge_button.collidepoint(mouse_pos)
        
        self.draw_button(self.slash_button, "SLASH", GREEN, glow=slash_glow)
        self.draw_button(self.dodge_button, "DODGE", RED, glow=dodge_glow)
        
        # Draw ninja
        ninja_x = 100 if self.slash_animation == 0 else 150
        self.draw_ninja(ninja_x, 550)
        
        # Instructions
        self.draw_text_with_shadow("SPACE = Slash | D = Dodge", self.small_font, SILVER, 
                                  SCREEN_WIDTH//2, 620)
        
        # Update animations
        if self.slash_animation > 0:
            self.slash_animation -= 1
            
        if self.number_scale > 1.0:
            self.number_scale -= 0.02
        elif self.number_scale < 1.0:
            self.number_scale = 1.0
            
        if self.flash_timer > 0:
            self.flash_timer -= 1
            if self.flash_timer <= 0:
                self.flash_color = None
                
    def draw_game_over(self):
        self.draw_background(overlay_alpha=120)
        
        # Game over title
        self.draw_text_with_shadow("MISSION COMPLETE!", self.big_font, GOLD, 
                                  SCREEN_WIDTH//2, 150, shadow_offset=4)
        
        # Final stats
        stats = [
            f"Final Score: {self.score}",
            f"Questions Answered: {self.total_questions}",
            f"Correct Answers: {self.correct_answers}",
            f"Accuracy: {(self.correct_answers/max(1, self.total_questions))*100:.1f}%"
        ]
        
        # Ninja rank
        if self.score >= 300:
            rank = "🥇 MASTER NINJA"
            rank_color = GOLD
        elif self.score >= 200:
            rank = "🥈 SKILLED NINJA"
            rank_color = SILVER
        elif self.score >= 100:
            rank = "🥉 APPRENTICE NINJA"
            rank_color = ORANGE
        else:
            rank = "🥷 NINJA IN TRAINING"
            rank_color = WHITE
            
        y_offset = 250
        for stat in stats:
            self.draw_text_with_shadow(stat, self.medium_font, WHITE, SCREEN_WIDTH//2, y_offset)
            y_offset += 50
            
        # Rank
        self.draw_text_with_shadow(rank, self.big_font, rank_color, SCREEN_WIDTH//2, y_offset + 50, 
                                  shadow_offset=3)
        
        # New high score
        if self.score > self.high_score:
            
            self.draw_text_with_shadow("🎉 NEW HIGH SCORE! 🎉", self.medium_font, YELLOW, 
                                      SCREEN_WIDTH//2, y_offset + 120, shadow_offset=2)
            
        # Return instruction
        self.draw_text_with_shadow("Press SPACE to return to menu", self.small_font, WHITE, 
                                  SCREEN_WIDTH//2, SCREEN_HEIGHT - 50)
        
    def generate_question(self):
        config = self.get_level_config()
        self.current_number = random.randint(*config["number_range"])
        self.current_property = random.choice(config["properties"])
        self.question_start_time = time.time()
        self.number_scale = 1.3  # Start with bigger scale for animation
        
    def handle_answer(self, user_answer):
        correct_answer = self.check_property(self.current_number, self.current_property)
        self.total_questions += 1
        
        if user_answer == correct_answer:
            self.correct_answers += 1
            points = 10 if self.level == 1 else 15
            self.score += points
            self.create_particles(SCREEN_WIDTH//2, 300, GREEN, 15)
            self.flash_color = (0, 100, 0)
            self.flash_timer = 15
        else:
            self.score = max(0, self.score - 5)
            self.create_particles(SCREEN_WIDTH//2, 300, RED, 15)
            self.flash_color = (100, 0, 0)
            self.flash_timer = 15
            
        self.slash_animation = 15
        
    def start_new_game(self):
        self.score = 0
        self.correct_answers = 0
        self.total_questions = 0
        self.level = 1
        self.level_start_time = time.time()
        self.game_state = "game"
        self.generate_question()
        
    def run(self):
        running = True
        print("🥷 Starting Ninja Number Slash Game...")
        print("📁 Make sure 'assets' folder contains:")
        print("   - ninja bg.jpg (background image)")
        print("   - Karasha-z8mYw.otf (ninja font)")
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                elif event.type == pygame.KEYDOWN:
                    if self.game_state == "menu":
                        if event.key == pygame.K_SPACE:
                            self.start_new_game()
                        elif event.key == pygame.K_i:
                            self.game_state = "instructions"
                        elif event.key == pygame.K_q:
                            running = False
                            
                    elif self.game_state == "instructions":
                        if event.key == pygame.K_ESCAPE:
                            self.game_state = "menu"
                            
                    elif self.game_state == "game":
                        if event.key == pygame.K_SPACE:
                            self.handle_answer(True)
                            self.generate_question()
                        elif event.key == pygame.K_d:
                            self.handle_answer(False)
                            self.generate_question()
                            
                    elif self.game_state == "game_over":
                        if event.key == pygame.K_SPACE:
                            self.game_state = "menu"
                            
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    if self.game_state == "menu":
                        if self.start_button.collidepoint(mouse_pos):
                            self.start_new_game()
                        elif self.instructions_button.collidepoint(mouse_pos):
                            self.game_state = "instructions"
                        elif self.quit_button.collidepoint(mouse_pos):
                            running = False
                            
                    elif self.game_state == "game":
                        if self.slash_button.collidepoint(mouse_pos):
                            self.handle_answer(True)
                            self.generate_question()
                        elif self.dodge_button.collidepoint(mouse_pos):
                            self.handle_answer(False)
                            self.generate_question()
                            
            # Game logic
            if self.game_state == "game":
                time_left = self.time_limit - (time.time() - self.level_start_time)
                if time_left <= 0:
                    if self.level == 1:
                        self.level = 2
                        self.level_start_time = time.time()
                        self.generate_question()
                    else:
                        if self.score > self.high_score:
                            self.high_score = self.score

                            with open("high_score.json", "w") as f:
                                json.dump(self.high_score, f)
                            
                        self.game_state = "game_over"
                        
            # Draw everything
            if self.game_state == "menu":
                self.draw_menu()
            elif self.game_state == "instructions":
                self.draw_instructions()
            elif self.game_state == "game":
                self.draw_game()
            elif self.game_state == "game_over":
                self.draw_game_over()
                
            pygame.display.flip()
            self.clock.tick(FPS)
            
        pygame.quit()

if __name__ == "__main__":
    game = NinjaNumberSlashGame()
    game.run()