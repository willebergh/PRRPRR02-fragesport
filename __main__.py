import os
import json
import time
import random

class Game:
    def __init__(self):
        if self.ask_to_start():
            self.start()
            
    # Method for clearing console on 
    # both windwos and unix based machines
    def clear(self):
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

    # Method for asking the user if they want to start the game or not
    def ask_to_start(self):
        self.clear()
        print("Vill du starta frågesporten? (J|n)")
        answer = input().lower()
        if answer == "j" or answer == "y" or answer == "ja" or answer == "yes":
            print("Förbereder start av frågesport!")
            return True
        else: 
            return False

    # Method for starting the game
    def start(self):
        self.clear()
      
        difficulty = self.ask_for_difficulty()
        questions = self.get_questions(difficulty)
      
        right_answers = 0
        wrong_answers = 0
      
        for i in questions:
            self.clear()
            if self.ask_question(i):
                right_answers += 1
            else:
                wrong_answers += 1
      
        self.clear()
        print(f"\nGrattis!")    
        print(f"Du har nu svarat på alla frågor!")
        print(f"\nResultat: {right_answers}/{right_answers + wrong_answers} rätt")

    # Method for asking the user what difficulty they want to use
    def ask_for_difficulty(self):
        print("\nVälj svårighetsgrad:\n")
        difficulties = os.listdir("./questions")
        for i in range(len(difficulties)):
            with open(f"./questions/{difficulties[i]}", encoding="utf-8") as file:
                parsed_file = json.load(file)
                print(f"{i + 1}. {parsed_file['difficulty']}")

        user_input = input(f"\nSvar (1-{len(difficulties)}): ")
        if user_input.isdigit() and len(user_input) == 1:
            
            index = int(user_input) - 1
            if index > -1 and index < len(difficulties):
                return difficulties[index]
            else:
                self.clear()
                print(f"Du kan endast välja en siffra mellan 1-{len(difficulties)}!")
                return self.ask_for_difficulty()
            
        else:
            self.clear()
            print(f"Du kan endast välja en siffra mellan 1-{len(difficulties)}!")
            return self.ask_for_difficulty()

    # Method for getting the questions from the choosen difficulty
    def get_questions(self, difficulty):
        file_name = f"./questions/{difficulty}"
        with open(file_name, encoding="utf-8") as file:
            return json.load(file)["questions"]

    # Mehtod for asking the user a question
    def ask_question(self, obj):
        question = obj["question"]
        right_answer = obj["right_answer"]
        wrong_answers = obj["wrong_answers"]

        answer_options = [right_answer]

        randomIndex = random.randint(0, len(wrong_answers) - 1)
        answer_options.append(wrong_answers[randomIndex])
        wrong_answers.pop(randomIndex)

        randomIndex = random.randint(0, len(wrong_answers) - 1)
        answer_options.append(wrong_answers[randomIndex])

        random.shuffle(answer_options)

        def convert_index_1x2(a):
            return {
                0: "1",
                1: "x",
                2: "2",
                "1": 0,
                "x": 1,
                "2": 2
            }.get(a)

        def handle_user_input():
            print(f"\n{question}\n")
            for i in range(len(answer_options)):
                print(f"{convert_index_1x2(i)}: {answer_options[i]}")

            user_input = input("\nSvar (1|x|2): ").lower()
            if user_input == "1" or user_input == "x" or user_input == "2":
                index = convert_index_1x2(user_input)
                if answer_options[index] == right_answer:
                    return True
                else:
                    return False
            else:
                self.clear()
                print("Ditt kan endast vara 1, X eller 2!")
                return handle_user_input()

        return handle_user_input()