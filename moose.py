import random
WIDTH = 512
HEIGHT = 512
FPS = 30
TITLE = "Mash The Moose!"
moose = Actor("moose", center=(WIDTH/2, HEIGHT/2))
moose2 = Actor("moose", center=(WIDTH/2, HEIGHT/2 + 70))
forest = Actor("forest") 
text = Actor("preview", center=(WIDTH/2, HEIGHT/2 + 100)) 
count = 0
sound_control = True
moose_control = None
total_time = 60
move = 5
movement = "diagonal_left_up"
mode = 'info'

# The draw() function
def draw():
    if mode == 'game':
        forest.draw()
        moose.draw()
        screen.draw.text("MASH THAT MOOSE!!!", fontname='bauhaus93', center=(WIDTH/2, HEIGHT/2 - 150), color='white', fontsize=35, owidth=2, ocolor="black")
    if mode == 'info':
        forest.draw()
        screen.draw.text("Welcome to Mash The Moose!.\nIn this game, the moose will move around. Every 15 seconds, \nit will get faster. You'll have to click the moose for 60 seconds,\nafterwards, you'll see a results screen\ngiving you a grade on how much you've clicked the moose.\nThe higher the clicks, the higher the grade.\nCan you get the A grade?", center=(WIDTH/2, HEIGHT/2), fontsize=24, color="black", lineheight=1.1) 
        text.draw()
    if mode == 'results':
        forest.draw()
        result_value = calculate_results(count)
        screen.draw.text("Your score is: " + str(count), fontname='bauhaus93', fontsize=30, center=(WIDTH/2, HEIGHT/2 - 200), color='white', ocolor='black', owidth=2)
        screen.draw.text("Your grade is: " + result_value, fontname='bauhaus93', fontsize=30, center=(WIDTH/2, HEIGHT/2 - 100), color='white', ocolor='black', owidth=2)
        screen.draw.text("Bored? Press Space to try again", fontname='bauhaus93', fontsize=30, center=(WIDTH/2, 490), color='white', ocolor='black', owidth=2)
        moose2.draw()

# The calculate_results() function
def calculate_results(final_score):
    global sound_control
    global moose_control
    if final_score / total_time <= 1:
        if sound_control:
            sounds.lose.play()
        sound_control = False
        moose_control = 'F'
        return "F"
    elif final_score / total_time <= 2:
        if sound_control:
            sounds.ouch.play()
        sound_control = False
        moose_control = 'B'
        return "B"
    elif final_score / total_time <= 3:
        if sound_control:
            sounds.victory.play()
        sound_control = False
        moose_control = 'A'
        return "A"
    elif final_score / total_time <= 4:
        if sound_control:
            sounds.collide.play()
        sound_control = False
        moose_control = 'S'
        moose.image = "moose_1"
        moose2.image = "moose_1"
        return "S\n:O You unlocked the secret moose!"
    else:
        if sound_control:
            sounds.glass.play()
        sound_control = False
        moose_control = 'O'
        moose.image = "moose_2"
        moose2.image = "moose_2"
        return "O\nAre you a machine or something?\nBecause you unlocked the\nugly moose."

direction = ["left", "right", "down", "diagonal_right_up", "up", "diagonal_left_up", "diagonal_right_down", "diagonal_left_down"]

# Get valid directions based on moose's current position
def get_valid_directions():
    valid_directions = direction[:]  # Copy all directions

    # Check for boundaries and remove invalid directions
    if moose.top <= 20:  # Moose is at the top
        valid_directions = [d for d in valid_directions if "up" not in d]
    
    if moose.bottom >= HEIGHT - 20:  # Moose is at the bottom
        valid_directions = [d for d in valid_directions if "down" not in d]

    if moose.left <= 20:  # Moose is at the left edge
        valid_directions = [d for d in valid_directions if "left" not in d]
    
    if moose.right >= WIDTH - 20:  # Moose is at the right edge
        valid_directions = [d for d in valid_directions if "right" not in d]

    return valid_directions

# Update random_direction to pick a valid direction based on position
def random_direction():
    global movement
    valid_directions = get_valid_directions()  # Get valid directions
    movement = random.choice(valid_directions)  # Choose a new valid direction
    
# The mode_change() function
def mode_change():
    global mode
    mode = 'results'
    clock.unschedule(move_change)

# The move_change() function
def move_change():
    global move
    move += 5

# The on_mouse_down() function
def on_mouse_down(button, pos):
    global count
    global mode
    if button == mouse.LEFT:
        if mode == 'game':
            if moose.collidepoint(pos):
                count += 1
        if mode == 'info':
            if text.collidepoint(pos):
                mode = 'game'
                clock.schedule_interval(move_change, 15.0)
                clock.schedule_unique(mode_change, 60.0)
        if mode == 'results':
            if moose_control == 'F':
                if moose2.collidepoint(pos):
                    sounds.lose.play()
            if moose_control == 'B':
                if moose2.collidepoint(pos):
                    sounds.ouch.play()
            if moose_control == 'A':
                if moose2.collidepoint(pos):
                    sounds.victory.play()
            if moose_control == 'S':
                if moose2.collidepoint(pos):
                    sounds.collide.play()
            if moose_control == 'O':
                if moose2.collidepoint(pos):
                    sounds.glass.play()

# Updated move_moose function to ensure movement is within bounds
def move_moose(direction):
    if direction == "diagonal_right_up":
        moose.x = min(WIDTH, moose.x + move)
        moose.y = max(0, moose.y - move)
    elif direction == "diagonal_left_up":
        moose.x = max(0, moose.x - move)
        moose.y = max(0, moose.y - move)
    elif direction == "diagonal_right_down":
        moose.x = min(WIDTH, moose.x + move)
        moose.y = min(HEIGHT, moose.y + move)
    elif direction == "diagonal_left_down":
        moose.x = max(0, moose.x - move)
        moose.y = min(HEIGHT, moose.y + move)
    elif direction == "down":
        moose.y = min(HEIGHT, moose.y + move)
    elif direction == "up":
        moose.y = max(0, moose.y - move)
    elif direction == "left":
        moose.x = max(0, moose.x - move)
    elif direction == "right":
        moose.x = min(WIDTH, moose.x + move)

# Check if moose is touching screen edges
def is_touching_corner():
    if moose.left <= 20 or moose.right >= WIDTH - 20 or moose.top <= 20 or moose.bottom >= HEIGHT - 20:
        return True
    return False

def on_key_down(key):
    global mode
    global move
    global sound_control
    global count
    if mode == 'results':
        if keyboard.space:
            mode = 'info'
            move = 5
            count = 0
            sound_control = True
            moose.pos = (WIDTH/2, HEIGHT/2)
    if mode == 'info':
        if keyboard.space:
            mode = 'trophies'
    if mode == 'trophies':
        if keyboard.space:
            mode = 'info'

# The update() function
def update():
    global movement
    if mode == 'game':
        if is_touching_corner():
            random_direction()

        move_moose(movement)