#truth or lie the game!
from csv import reader
file_name = "truthOrLie.csv"

def add_ques():
    while True:
        print("")
        new_question = input("Enter new truth or lie to ask: ")
        new_answer = input("Is it a truth or a lie? (True / False): ")
        if new_question.lower() == "exit" or new_answer.lower() == "exit":
            break
        file = open(file_name, "at")
        file.write(f"{new_question},{new_answer}\n")
        file.close()

print("")
print("(1) Play Game")
print("(2) Add Questions")
print("")
options = input(">>> ")
if options == "1":
    pass
elif options == "2":
    add_ques()
else:
    print("Invalid option, starting game...")

# pygame main game
from engine import game_engine_50123 as game_engine
import os, pygame
pygame.font.init()
file_dir = os.getcwd()

#create window
w, h = 800, 600
window = game_engine.window.define("Truth Or Lie", w, h)

#variables
run = True
clock = pygame.time.Clock()
scale = 4
question_number = 0
question_data = []

#lists
display = []        #background display
background = game_engine.properties_object("bg", f"{file_dir}/textures/background.png", 0, 0, w, h, False)
title = game_engine.properties_object("title", f"{file_dir}/textures/title.png", w / 2 - (124 / 2 * scale), 30, 124 * scale, 15 * scale, False)
display += [background, title]

#sprites
display_sprite = []
#foreground
foreground = []
#text
text_foreground = []

#init programs
def init_buttons():         #initalises the buttons to be shown on screen
    global display_sprite
    truth_button = game_engine.properties_object("truth_button", f"{file_dir}/textures/truth_button.png", 100, h - 200, 60 * scale, 15 * scale, False)
    lie_button = game_engine.properties_object("lie_button", f"{file_dir}/textures/lie_button.png", w - (100 + 32 * scale), h - 200, 32 * scale, 15 * scale, False)
    display_sprite += [truth_button, lie_button]

def generate_list():            #when starting the program it will create a 2D array of all the questions in the csv file
    global question_data
    with open(file_name, "r") as read_obj:
        csv_reader = reader(read_obj)
        for row in csv_reader:
            if row == []:
                pass
            else:
                question_data += [[row[0], row[1]]]
# sub programs
def update(display, display_sprite, foreground, text_foregorund):               #update the screen to the game engine
    game_engine.window.update(window, display, display_sprite, foreground, text_foregorund, clock, 0)

def end_questions():                #prints to the screen that the questions have ran out and will now exit the program. Adds a slight delay for the user to read
    global text_foreground
    global run
    question = game_engine.properties_text("question", "End of questions. Exiting program.", "white", w, h - 250, 65, True)
    text_foreground += [question]
    run = False
    delay()
    
def delay():                #delays the code by 1000ms 
    update(display, display_sprite, foreground, text_foreground)
    pygame.time.delay(1000)
    
def generate_question():            #Displays to the screen the question
    global text_foreground
    question = game_engine.properties_text("question", f"{question_data[question_number][0]}", "white", w, h - 250, 65, True)
    text_foreground += [question]

def generate_answer(answer):            #creates an answer if the check is "correct" or "incorrect"
    global foreground, text_foreground
    global question_number
    if answer == "correct":         #displays to the screen to say if its correct or if its incorrect
        answer = game_engine.properties_object("answer", f"{file_dir}/textures/correct.png", w / 2 - (70 / 2 * scale), 250, 70 * scale, 15 * scale, False)
        foreground += [answer]
        delay()         #update and delays the code for the user to read the answer
    else:
        answer = game_engine.properties_object("answer", f"{file_dir}/textures/incorrect.png", w / 2 - (90 / 2 * scale), 250, 90 * scale, 15 * scale, False)
        foreground += [answer]
        delay()

    #increments the questions_number if the question number hasnt reached the end of the questions
    foreground = []
    text_foreground = []
    if len(question_data) - 1 == question_number:
        end_questions()
    else:
        question_number += 1
        generate_question()

def check_answer(user_input):           #checks the answer if the user_input equals the question answer
    if user_input == question_data[question_number][1]:
        generate_answer("correct")
    else:
        generate_answer("incorrect")

def main():             #main program that checks if the user has pressed a button. Once they have, it checks to see if thats the correct answer
    pygame.time.delay(100)
    if not pygame.mouse.get_pressed()[0]:
        pass
    elif game_engine.mouse.collision("truth_button", display_sprite):
        check_answer("True")
    elif game_engine.mouse.collision("lie_button", display_sprite):
        check_answer("False")

init_buttons()
generate_list()
generate_question()
while run:
    #keyboard and exit button
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        run = False

    main()
    update(display, display_sprite, foreground, text_foreground)
    clock.tick(60)
pygame.quit()