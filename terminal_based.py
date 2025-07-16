import random
import time
import math
import os

class NinjaNumberSlash:
    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.level = 1
        self.time_limit = 30  # seconds per level
        self.correct_answers = 0
        self.total_questions = 0
        self.current_property = ""
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def display_ninja_art(self):
        ninja_art = """
        ⚔️  NINJA NUMBER SLASH ⚔️
        
           /|   /|   
          ( :v:  )
           |(_)|
          /     \\
         /       \\
        🥷 Speed • Accuracy • Math 🥷
        """
        print(ninja_art)
        
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
        # Check if n is a Fibonacci number
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
        else:  # Level 2
            return {
                "properties": ["prime", "perfect_square", "fibonacci", "multiple_of_3"],
                "number_range": (1, 100),
                "time_per_question": 4
            }
            
    def get_property_description(self, property_type):
        descriptions = {
            "prime": "Prime numbers (only divisible by 1 and itself)",
            "even": "Even numbers (divisible by 2)",
            "multiple_of_3": "Multiples of 3",
            "perfect_square": "Perfect squares (1, 4, 9, 16, 25...)",
            "fibonacci": "Fibonacci numbers (0, 1, 1, 2, 3, 5, 8, 13...)"
        }
        return descriptions.get(property_type, "Unknown property")
        
    def display_game_state(self, number, time_left):
        self.clear_screen()
        print("⚔️" * 50)
        print(f"🥷 NINJA NUMBER SLASH - LEVEL {self.level} 🥷")
        print("⚔️" * 50)
        print(f"Score: {self.score} | High Score: {self.high_score}")
        print(f"Accuracy: {self.correct_answers}/{self.total_questions}")
        print(f"Time Left: {time_left:.1f}s")
        print("-" * 50)
        print(f"TARGET: {self.get_property_description(self.current_property)}")
        print("-" * 50)
        print(f"\n🎯 NUMBER TO SLASH: {number}")
        print(f"\nIs {number} a {self.current_property.replace('_', ' ')}?")
        print("\n[Y] - SLASH (Yes) | [N] - DODGE (No) | [Q] - Quit")
        
    def play_level(self):
        config = self.get_level_config()
        level_start_time = time.time()
        questions_this_level = 0
        level_score = 0
        
        print(f"\n🥷 STARTING LEVEL {self.level}! 🥷")
        print(f"Time Limit: {self.time_limit} seconds")
        print("Get ready ninja...")
        time.sleep(2)
        
        while time.time() - level_start_time < self.time_limit:
            # Generate random number and property
            number = random.randint(*config["number_range"])
            self.current_property = random.choice(config["properties"])
            
            question_start_time = time.time()
            
            while time.time() - question_start_time < config["time_per_question"]:
                time_left = self.time_limit - (time.time() - level_start_time)
                if time_left <= 0:
                    break
                    
                self.display_game_state(number, time_left)
                
                # Get user input with timeout simulation
                print("\nQuick! Make your choice:")
                try:
                    user_input = input().lower().strip()
                    
                    if user_input == 'q':
                        return False
                        
                    if user_input in ['y', 'yes', 'slash']:
                        user_answer = True
                    elif user_input in ['n', 'no', 'dodge']:
                        user_answer = False
                    else:
                        print("❌ Invalid input! Use Y/N")
                        time.sleep(1)
                        continue
                        
                    # Check answer
                    correct_answer = self.check_property(number, self.current_property)
                    self.total_questions += 1
                    questions_this_level += 1
                    
                    if user_answer == correct_answer:
                        self.correct_answers += 1
                        points = 10 if self.level == 1 else 15
                        self.score += points
                        level_score += points
                        print(f"⚔️ CORRECT SLASH! +{points} points!")
                        if correct_answer:
                            print(f"✅ {number} IS a {self.current_property.replace('_', ' ')}!")
                        else:
                            print(f"✅ {number} is NOT a {self.current_property.replace('_', ' ')}!")
                    else:
                        self.score = max(0, self.score - 5)
                        print(f"❌ WRONG MOVE! -5 points!")
                        if correct_answer:
                            print(f"💡 {number} IS a {self.current_property.replace('_', ' ')}!")
                        else:
                            print(f"💡 {number} is NOT a {self.current_property.replace('_', ' ')}!")
                    
                    time.sleep(1.5)
                    break
                    
                except KeyboardInterrupt:
                    return False
                    
        # Level complete
        self.clear_screen()
        print("⚔️" * 50)
        print(f"🎉 LEVEL {self.level} COMPLETE! 🎉")
        print("⚔️" * 50)
        print(f"Level Score: {level_score}")
        print(f"Questions Answered: {questions_this_level}")
        print(f"Total Score: {self.score}")
        
        if self.level == 1:
            print(f"Accuracy: {(self.correct_answers/self.total_questions)*100:.1f}%")
            print("\nPreparing for Level 2...")
            time.sleep(3)
            return True
        else:
            return True
            
    def show_final_stats(self):
        self.clear_screen()
        print("⚔️" * 50)
        print("🏆 FINAL NINJA STATS 🏆")
        print("⚔️" * 50)
        print(f"Final Score: {self.score}")
        print(f"Questions Answered: {self.total_questions}")
        print(f"Correct Answers: {self.correct_answers}")
        print(f"Accuracy: {(self.correct_answers/self.total_questions)*100:.1f}%")
        
        if self.score > self.high_score:
            self.high_score = self.score
            print("🎉 NEW HIGH SCORE! 🎉")
        
        # Ninja ranking
        if self.score >= 300:
            rank = "🥇 MASTER NINJA"
        elif self.score >= 200:
            rank = "🥈 SKILLED NINJA"
        elif self.score >= 100:
            rank = "🥉 APPRENTICE NINJA"
        else:
            rank = "🥷 NINJA IN TRAINING"
            
        print(f"Ninja Rank: {rank}")
        
    def show_instructions(self):
        self.clear_screen()
        print("📜 NINJA TRAINING SCROLL 📜")
        print("=" * 50)
        print("🎯 MISSION: Slash correct numbers, dodge wrong ones!")
        print("\n🔢 LEVEL 1 TARGETS:")
        print("• Prime numbers (2, 3, 5, 7, 11...)")
        print("• Even numbers (2, 4, 6, 8...)")
        print("• Multiples of 3 (3, 6, 9, 12...)")
        print("\n🔢 LEVEL 2 TARGETS:")
        print("• All Level 1 targets PLUS:")
        print("• Perfect squares (1, 4, 9, 16, 25...)")
        print("• Fibonacci numbers (0, 1, 1, 2, 3, 5, 8...)")
        print("\n⚔️ SCORING:")
        print("• Level 1: +10 points for correct, -5 for wrong")
        print("• Level 2: +15 points for correct, -5 for wrong")
        print("\n⏱️ TIME LIMITS:")
        print("• Level 1: 30 seconds total, 5 seconds per question")
        print("• Level 2: 30 seconds total, 4 seconds per question")
        print("\nPress Enter to continue...")
        input()
        
    def main_menu(self):
        while True:
            self.clear_screen()
            self.display_ninja_art()
            print(f"High Score: {self.high_score}")
            print("\n🗡️  NINJA MENU 🗡️")
            print("1. Start New Game")
            print("2. View Instructions")
            print("3. Quit")
            
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == '1':
                self.start_new_game()
            elif choice == '2':
                self.show_instructions()
            elif choice == '3':
                print("🥷 Farewell, ninja! Train hard and return stronger!")
                break
            else:
                print("❌ Invalid choice! Try again.")
                time.sleep(1)
                
    def start_new_game(self):
        self.score = 0
        self.correct_answers = 0
        self.total_questions = 0
        self.level = 1
        
        # Play Level 1
        if self.play_level():
            self.level = 2
            # Play Level 2
            self.play_level()
            
        self.show_final_stats()
        print("\nPress Enter to return to menu...")
        input()

if __name__ == "__main__":
    game = NinjaNumberSlash()
    game.main_menu()