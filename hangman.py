# Zach Rubin, Reka Kovacs
# Project 3
# This program creates multiple Graphics windows which allows the user to click circles to make guesses
# in order to try to guess the randomly selected word chosen from the words.txt file. They also have the
# option to use the hint button to rule out 3 incorrect characters for 3 guesses. If the user is
# incorrect for 10 guesses the player loses and enters their score to the file. If the player wins they click
# to continue to play a new game with their score transferred from the previous result. They also have
# the option to view the highscores.txt file.

# Import the graphics and random libraries in order to use the graphics functions and select a random word
import random as rand
from graphics import *

# Defines the main function
def main():
    # Creates a list of background colors to cycle through
    background_colors = ['gold', 'yellow', 'green yellow', 'spring green', 'turquoise', 'light blue',
                         'light slate blue', 'dark violet', 'maroon', 'firebrick3']
    # Calls the control_panel() function and return the window object
    window = control_panel()
    # Total and score are set to zero and games is set to 1 so it is true
    total, games, score, rounds = 0, 1, 0, 0
    # While loop runs until games equals one
    while games:
        wind = 0
        # Sets games to the result of the clicked() function
        try:
            games = clicked(window.checkMouse(), window)
        except:
            break
        if games == 2:
            # Try and except block closes the window if possible, otherwise passes
            try:
                wind.close()
            except:
                pass
            # Calls the game panel function and sets count equal to the length
            wind, circles, letters, squares, polygons, status, prompt, selected_word, length = game_panel()
            count = length
        elif games == 4:
            high_scores()
        elif games == 5:
            manual()
        # While the number of games is set to 2 the while loop plays the game
        while games == 2:
            # The score is increased by 10 and rounds by 1
            score += 10
            rounds += 1
            # and i and wrong_guesses are set to 0
            x, i, wrong_guesses, hint_check, hint_letters = 0, 0, 0, 0, []
            # The score object is created using the current score
            score_text = Text(Point(230, 15), "SCORE:   " + str(score))
            # Try and except block attempts to draw in the window, otherwise passes
            try:
                score_text.draw(wind)
            except:
                pass
            # For loop iterates through for each of the 10 guesses a user is given
            while i < 10:
                # Checks to see if the guess was only a single character
                click = window.checkMouse()
                click_check = clicked(click, wind)
                # If 0 is return from the click function quit was clicked so the program ends
                if not click_check:
                    return
                # If games = 2 then new game was clicked so the current window is closed
                elif 2 == click_check:
                    wind.close()
                    # New game panel is created resetting all of the graphics objects
                    wind, circles, letters, squares, polygons, status, prompt, selected_word, length = game_panel()
                    # wrong_guesses is reset to zero, games is set to 2 so the function continues, and score is reset
                    wrong_guesses, games, count, score = 0, 2, length, 0
                    # breaks the while loop
                    break
                # If games = 3 then hint was clicked so
                elif 3 == click_check:
                    # Checks if score is not equal to one so the can't have a negative score
                    if score != 1:
                        # Checks to see the hint hasn't already been clicked this round
                        if not hint_check:
                            q = 0
                            # While loop runs until 3 incorrect letters have been ruled out
                            while q < 3:
                                # Sets actual letter to zero to check if the random circle was in fact correct
                                actual_letter = 0
                                # Sets x to a random number that would be within the list of circles
                                x = rand.randint(0, 25)
                                # If the circle is set to False, the while loop continues
                                if not circles[x]:
                                    continue
                                # For loop iterates through the selected word and if it matches a character then actual
                                #  letter is set to one so it will be avoided
                                for z in range(length):
                                    if chr(x + 65) == selected_word[z]:
                                        actual_letter += 1
                                # Checks that it isn't a correct letter
                                if not actual_letter:
                                    # Sets the fill of the incorrect letter to gold and black
                                    circles[x].setFill('gold')
                                    letters[x].setFill('black')
                                    # The corresponding circle object is set to False and q is incremented by one
                                    circles[x] = False
                                    q += 1
                            # Upon completing the while loop wrong_guesses and the score is updated
                            wrong_guesses += 2
                            # Two polygons are dropped
                            drop(polygons, i)
                            drop(polygons, i+1)
                            # Hint check becomes set to one and the i counter is incremented by 2
                            hint_check = 1
                            i += 2
                            continue
                # If games = 4 then scores was clicked so
                elif 4 == click_check:
                    high_scores()
                elif 5 == click_check:
                    manual()
                else:
                    # Draws the score object in the window
                    score_text.setText("SCORE :   " + str(score - wrong_guesses))
                    # Sets the background based on the number of incorrect guesses
                    wind.setBackground(background_colors[wrong_guesses])
                    # Try and except block attempts to check for a mouse click
                    try:
                        click = wind.checkMouse()
                    except:
                        pass
                    if click:
                        # For loop iterates through the range of all possible circles
                        for j in range(len(circles)):
                            # If the circle is set to False, the for loop continues
                            if not circles[j]:
                                continue
                            # define the x and y coordinates of the clicked point
                            x = click.getX()
                            y = click.getY()
                            # define the radius and center of the specific circle being used
                            radius = circles[j].getRadius()
                            center = circles[j].getCenter()
                            # define the x and y values of the specific circle being used
                            x_val = center.getX()
                            y_val = center.getY()
                            # calculate the distance between the center of the circle and the clicked point
                            distance = (x - x_val) ** 2 + (y - y_val) ** 2
                            # if the click is within the circle, the letter and circles are filled
                            if distance < radius ** 2:
                                circles[j].setFill('gold')
                                letters[j].setFill('black')
                                # The corresponding circle object is set to False as well as the guessed_char variable
                                circles[j], guessed_char = False, False
                                # The for loop iterates through the selected word
                                for z in range(length):
                                    # The if block checks if a character in the word matches the guessed character
                                    if chr(j + 65) == selected_word[z]:
                                        # point is set to the center of the square
                                        point = squares[z].getCenter()
                                        # Creates a letter object, sets it to bold, and draws it
                                        letter = Text(point, selected_word[z])
                                        letter.setStyle('bold')
                                        letter.draw(wind)
                                        # Subtracts one from the count and set guessed_char to False
                                        count -= 1
                                        guessed_char = True
                                # Checks to see if all of the characters of the word have been correctly guessed
                                if count == 0:
                                    # Sets the text and prompt to the winning condition
                                    status.setText("YOU WIN - BOILER UP!")
                                    prompt.setText("Click to continue")
                                    wind.getMouse()
                                    wind.close()
                                    # Resets all the variables and also calls the game_panel()
                                    score = score - wrong_guesses + 10
                                    wind, circles, letters, squares, polygons, status, prompt, selected_word, length = game_panel()
                                    count = length
                                    i, wrong_guesses, games = 0, 0, 2
                                    # Sets the new score_text to the updated score and then draws it in the window
                                    score_text = Text(Point(230, 15), "SCORE:   " + str(score))
                                    score_text.draw(wind)
                                    break
                                if not guessed_char:
                                    # Increments wrong_guesses and i by 1
                                    wrong_guesses += 1
                                    i += 1
                                    # Updates the score text and drops the corresponding polygon
                                    score_text.setText("SCORE :   " + str(score - wrong_guesses))
                                    drop(polygons, i-1)
                                    continue
            # If i equals 10 then that means the user used all ten of their guesses
            if i == 10:
                wind.setBackground('firebrick4')
                # Sets the fill of the status and prompt texts to red and changes the test to Click to Exit and Game Over
                status.setFill('red')
                prompt.setFill('red')
                # Sets the prompt and text to the losing conditions
                prompt.setText("Click to exit")
                status.setText('GAME OVER')
                myEntry = Entry(Point(280, 350), 16)
                myEntry.setFill('white')
                myEntry.draw(wind)
                # Creates and draws a black rectangle
                prompt_box = Rectangle(Point(220, 320), Point(340, 350))
                prompt_box.setFill('black')
                prompt_box.draw(wind)
                # Creates and draws a black rectangle
                save_box = Rectangle(Point(340, 340), Point(400, 360))
                save_box.setFill('black')
                save_box.draw(wind)
                # Creates a text object stating save
                save = Text(Point(370, 350), "SAVE")
                save.setSize(12)
                save.setFill('white')
                save.draw(wind)
                # Text object instructs user to enter their name
                prompt = Text(Point(280, 330), "Enter your name")
                prompt.setSize(12)
                prompt.setFill('white')
                prompt.draw(wind)
                # While loop runs until a name is entered
                while True:
                    click = wind.checkMouse()
                    if click:
                        # define the x and y coordinates of the clicked point
                        x = click.getX()
                        y = click.getY()
                        # Checks if the y component of the click matches the new and quit objects
                        if 340 <= y <= 360:
                            # Checks if the new object was clicked
                            if 340 <= x <= 400:
                                # Collects the entry string
                                myString = myEntry.getText()
                                with open('scores.txt', 'a') as f:
                                    # If no name is entered their name becomes Anonymous
                                    if myString == '':
                                        myString = 'Anonymous'
                                    # The scores is subtracted by 10 to avoid it being added again due to loop sequence
                                    score -= 10
                                    # Writes the player's name, round, and score to the file and breaks the while loop
                                    f.write('\n'+myString+','+str(rounds)+','+str(score))
                                    break
                # CLoses the window and sets games to 2
                wind.close()
                games = 2


# Defines control_panel function
def control_panel():
    # Creates a 300x280 window titled Welcome to:
    window = GraphWin('Welcome to:', 300, 280)
    window.setBackground('light grey')
    # Creates a header box and sets its background to black
    header_box = Rectangle(Point(0, 0), Point(300, 20))
    header_box.setFill('black')
    header_box.draw(window)
    # Creates a bold, gold text object for the header block with
    title = Text(Point(150, 10), "GUESS MASTER 2.0")
    title.setFill('gold')
    title.setStyle("bold")
    title.draw(window)
    # Creates a new box and sets its background to gold
    new_box = Rectangle(Point(15, 40), Point(75, 70))
    new_box.setFill('gold')
    new_box.draw(window)
    # Creates a black, bold text object for the header block
    new_text = Text(Point(45, 55), "NEW")
    new_text.setFill('black')
    new_text.setStyle("bold")
    new_text.draw(window)
    # Creates a new box and sets its background to gold
    hint_box = Rectangle(Point(85, 40), Point(145, 70))
    hint_box.setFill('black')
    hint_box.draw(window)
    # Creates a black, bold text object for the header block
    hint_text = Text(Point(115, 55), "HINT")
    hint_text.setFill('gold')
    hint_text.setStyle("bold")
    hint_text.draw(window)
    # Creates a quit box and sets its background to black
    scores_box = Rectangle(Point(155, 40), Point(215, 70))
    scores_box.setFill('gold')
    scores_box.draw(window)
    # Creates a bold, gold text object for the header block
    scores_text = Text(Point(185, 55), "HIGH\nSCORES")
    scores_text.setSize(8)
    scores_text.setFill('black')
    scores_text.setStyle("bold")
    scores_text.draw(window)
    # Creates a quit box and sets its background to black
    quit_box = Rectangle(Point(225, 40), Point(285, 70))
    quit_box.setFill('black')
    quit_box.draw(window)
    # Creates a bold, gold text object for the header block
    quit_text = Text(Point(255, 55), "QUIT")
    quit_text.setFill('gold')
    quit_text.setStyle("bold")
    quit_text.draw(window)
    # Create a box for the game instructions
    manual = Rectangle(Point(15,240),Point(75,270))
    manual.setFill("white")
    manual.draw(window)
    # Create a title for the game instructions
    info = Text(Point(45,255),"How to\nplay")
    info.setSize(9)
    info.setFill("black")
    info.draw(window)

    # Creates a bold text object prompting instructions
    instructions = Text(Point(150, 230), "Click NEW to start a game...")
    instructions.setStyle("bold")
    instructions.draw(window)
    # Creates a white filled rectangle
    prompt_box = Rectangle(Point(21, 100), Point(279, 200))
    prompt_box.setFill('white')
    prompt_box.draw(window)
    # Creates a text object describing the game play
    prompt = Text(Point(150, 150), " This is a game where your score is\n  based on the number of 4-6 letter\n"
                                   "words you can guess within 10 tries.")
    prompt.draw(window)
    return window


# Defines the game_panel() function which takes the score, window, and games as parameters
def game_panel():
    # Creates the graphics window and sets the background to gold
    wind = GraphWin('Save the Block P', 460, 500)
    wind.setBackground('gold')
    # Sets height to 427 and creates four empty lists
    height = 427
    circles, letters, squares, polygons = [], [], [], []
    # Iterates through a range of 26
    for i in range(26):
        # If block checks to see if its one of the first 13 circles
        if i <= 12:
            # z is the multiple of the current range index
            z = i * 33
            # Circles with radius 16.5 is created with a radius of 16.5 with a black fill
            c = Circle(Point(32 + z, height), 16.5)
            c.setFill('black')
        else:
            # height is changed since it's now the lower half
            height = 460
            # z is the multiple of the current range index
            z = (i - 13) * 33
            # Circles with radius 16.5 is created with a radius of 16.5 with a black fill
            c = Circle(Point(32 + z, height), 16.5)
            c.setFill('black')
        # The created circles are drawn and appended to the circles list
        c.draw(wind)
        circles.append(c)

        # Text objects are created using the same points as the circles
        a = Text(Point(32 + z, height), chr(i + 65))
        # The fill is set to white, style to bold, and the letters are drawn and appended
        a.setFill('white')
        a.setStyle("bold")
        a.draw(wind)
        letters.append(a)
    # Creates polygon object and fills it white
    p1 = Polygon(Point(160, 160), Point(170, 100), Point(235, 100), Point(225, 160))
    p1.setFill('white')
    p1.draw(wind)
    # Creates polygon object and fills it white
    p2 = Polygon(Point(225, 160), Point(235, 100), Point(300, 100), Point(290, 160))
    p2.setFill('white')
    p2.draw(wind)
    # Creates polygon object and fills it white
    p3 = Polygon(Point(290, 160), Point(300, 100), Point(365, 100), Point(355, 160))
    p3.setFill('white')
    p3.draw(wind)
    # Creates polygon object and fills it white
    p4 = Polygon(Point(150, 220), Point(160, 160), Point(225, 160), Point(215, 220))
    p4.setFill('white')
    p4.draw(wind)
    # Creates polygon object and fills it white
    p5 = Polygon(Point(280, 220), Point(290, 160), Point(355, 160), Point(345, 220))
    p5.setFill('white')
    p5.draw(wind)
    # Creates polygon object and fills it white
    p6 = Polygon(Point(140, 280), Point(150, 220), Point(215, 220), Point(205, 280))
    p6.setFill('white')
    p6.draw(wind)
    # Creates polygon object and fills it white
    p7 = Polygon(Point(205, 280), Point(215, 220), Point(280, 220), Point(270, 280))
    p7.setFill('white')
    p7.draw(wind)
    # Creates polygon object and fills it white
    p8 = Polygon(Point(270, 280), Point(280, 220), Point(345, 220), Point(335, 280))
    p8.setFill('white')
    p8.draw(wind)
    # Creates polygon object and fills it white
    p9 = Polygon(Point(130, 340), Point(140, 280), Point(205, 280), Point(195, 340))
    p9.setFill('white')
    p9.draw(wind)
    # Creates polygon object and fills it white
    p10 = Polygon(Point(110, 390), Point(120, 340), Point(205, 340), Point(195, 390))
    p10.setFill('white')
    p10.draw(wind)
    # Creates polygon object, fills it black, and appends it to the list of polygons
    p10 = Polygon(Point(110, 390), Point(120, 340), Point(205, 340), Point(195, 390))
    p10.setFill('black')
    p10.draw(wind)
    polygons.append(p10)
    # Creates polygon object, fills it black, and appends it to the list of polygons
    p9 = Polygon(Point(130, 340), Point(140, 280), Point(205, 280), Point(195, 340))
    p9.setFill('black')
    p9.draw(wind)
    polygons.append(p9)
    # Creates polygon object, fills it black, and appends it to the list of polygons
    p6 = Polygon(Point(140, 280), Point(150, 220), Point(215, 220), Point(205, 280))
    p6.setFill('black')
    p6.draw(wind)
    polygons.append(p6)
    # Creates polygon object, fills it black, and appends it to the list of polygons
    p4 = Polygon(Point(150, 220), Point(160, 160), Point(225, 160), Point(215, 220))
    p4.setFill('black')
    p4.draw(wind)
    polygons.append(p4)
    # Creates polygon object, fills it black, and appends it to the list of polygons
    p1 = Polygon(Point(160, 160), Point(170, 100), Point(235, 100), Point(225, 160))
    p1.setFill('black')
    p1.draw(wind)
    polygons.append(p1)
    # Creates polygon object, fills it black, and appends it to the list of polygons
    p2 = Polygon(Point(225, 160), Point(235, 100), Point(300, 100), Point(290, 160))
    p2.setFill('black')
    p2.draw(wind)
    polygons.append(p2)
    # Creates polygon object, fills it black, and appends it to the list of polygons
    p3 = Polygon(Point(290, 160), Point(300, 100), Point(365, 100), Point(355, 160))
    p3.setFill('black')
    p3.draw(wind)
    polygons.append(p3)
    # Creates polygon object, fills it black, and appends it to the list of polygons
    p5 = Polygon(Point(280, 220), Point(290, 160), Point(355, 160), Point(345, 220))
    p5.setFill('black')
    p5.draw(wind)
    polygons.append(p5)
    # Creates polygon object, fills it black, and appends it to the list of polygons
    p8 = Polygon(Point(270, 280), Point(280, 220), Point(345, 220), Point(335, 280))
    p8.setFill('black')
    p8.draw(wind)
    polygons.append(p8)
    # Creates polygon object, fills it black, and appends it to the list of polygons
    p7 = Polygon(Point(205, 280), Point(215, 220), Point(280, 220), Point(270, 280))
    p7.setFill('black')
    p7.draw(wind)
    polygons.append(p7)

    # Opens the words.txt file using a with block
    with open('words.txt') as words:
        # The readlines() method creates a list named words_list of all the words in the file
        words_list = words.readlines()
    # Randomly selects a word from the list of words from the file
    selected_word = words_list[rand.randint(0, len(words_list))]
    # Chops off the last two elements of the string to remove \n
    selected_word = selected_word[:len(selected_word) - 1].upper()
    length = len(selected_word)
    # If else statements set the initial x value of the squares to be centered given the length of the word
    if length == 4:
        initial_x = 110
    elif length == 5:
        initial_x = 80
    else:
        initial_x = 50
    # For loop iterates through the length of the word
    for i in range(length):
        # j is set to the multiple of the range index of the squares
        j = i*60
        # The squares are created as rectangles, filled gold, drawn, and appended
        square = Rectangle(Point(initial_x+j, 30), Point(initial_x+60+j, 90))
        square.setFill('gold')
        square.draw(wind)
        squares.append(square)
    # Status object is created filled grey and drawn
    status = Text(Point(230, 240), "")
    status.setFill('grey')
    status.draw(wind)
    # Prompt object is created filled grey and drawn
    prompt = Text(Point(230, 270), "")
    prompt.setSize(12)
    prompt.setFill('grey')
    prompt.draw(wind)
    return wind, circles, letters, squares, polygons, status, prompt, selected_word, length


# Defines drop function taking in polygons and the increment j
def drop(polygons, j):
    polygons[j].setFill('red')
    # For loop of range 200 moves the polygon object a small amount for that many times
    for movement in range(400):
        polygons[j].move(0, 20)


# Defines the clicked function taking click and window as arguments
def clicked(click, window):
    # Checks to see if a click was registered
    if click is not None:
        # define the x and y coordinates of the clicked point
        x = click.getX()
        y = click.getY()
        # Checks if the y component of the click matches the new and quit objects
        if 40 <= y <= 70:
            # Checks if the new object was clicked
            if 15 <= x <= 75:
                return 2
            # Checks if the hint object was clicked
            elif 85 <= x <= 145:
                return 3
            # Checks if the scores object was clicked
            elif 155 <= x <= 215:
                return 4
            # Checks if the quit object was clicked
            elif 225 <= x <= 285:
                window.close()
                return 0
        elif 240 <= y <= 270 and 15 <= x <= 75:
            return 5
    # Returns 1 if neither object was clicked
    return 1

# Defines manual function
def manual():
    # Creates manual window
    manualpanel = GraphWin("Guess Master 3.0 Instruction Manual", 200, 200)
    # Creates and draws instructions text
    instructions = Text(Point(100, 20), "How to play:")
    instructions.draw(manualpanel)
    # Text object details gameplay, is set to size 14, and drawn in the window
    gameplay = Text(Point(100, 100), "Players must click on\nletters in order to guess\nthe word. "
                                     "A hint may used \nonce per round, elimating 3\nincorrect letters, "
                                     "but using up\n2 guesses. Player wins if they\ncorrectly "
                                     "enter the word\nwithin 10 guesses.")
    gameplay.setSize(14)
    gameplay.draw(manualpanel)
    # Click to close text prompt is displayed
    closemanual = Text(Point(100, 180), "Click to close")
    closemanual.draw(manualpanel)
    # Pauses for mouse click and closes window
    manualpanel.getMouse()
    manualpanel.close()

# Defines high_scores function
def high_scores():
    # Creates a 250x200 window titled High Scores
    high_scores_win = GraphWin('High Scores', 250, 200)
    # Opens the scores.txt file in a with block
    with open('scores.txt', 'r') as file:
        # Readlines method creates a list of every line in the file
        lines = file.readlines()
    # Defines two empty lists and puts the header in the other
    line, text_objects, output, = [], [], ['Player\tRounds\tScore', '=-=-=-=-=-=-=-=-=-=-=']
    # For loop iterates through every line from the file
    for i in lines:
        # splits the data and appends it to the line list
        data = i.split(',')
        line.append(data)
    # For loop iterates through each line and reorganizes it
    for j in range(len(line)):
        # Makes the third element the first as an integer and the first element the third
        first = line[j][2]
        last = line[j][0]
        line[j][0] = int(first)
        line[j][2] = last
    # Sorts the scores since the first element is the score integer
    scores = sorted(line, reverse=True)
    # For loop iterates through the sorted scores list
    for e in range(len(scores)):
        # Formats the output as name, round, and score as a list
        out = ['{0:<10}{1:<6}{2:>5}'.format(scores[e][2], scores[e][1], scores[e][0])]
        # Adds the row as an element to the prior list including the header
        output = output + out
    # For loop takes the two header elements and the seven top scores
    for s in range(9):
        # Creates and draws centered text objects progressively farther down, appending each object to a list
        text = Text(Point(125, 10 + 20 * s), output[s])
        text.setSize(14)
        text.draw(high_scores_win)
        text_objects.append(text)
    # While loop runs while the window is open
    while high_scores_win:
        # For loop iterates through 9 for the 9 elements in the list
        for w in range(9):
            # Checks if w == 0 since there is a gap between final score and the header
            if w == 0:
                first = 20
            else:
                first = 0
            # For loop goes through twenty unless it's the first in which it's doubled
            for o in range(20 + first):
                # For loop goes in range 9 for each element in the list and moves it up by 1
                for r in range(9):
                    text_objects[r].move(0, -1)
            # Upon moving everything a full sequence, creates a new text object at the bottom and undraws
            #  the one that is at the top and updates the list accordingly
            text = Text(Point(125, 190), output[w])
            text.setSize(14)
            text_objects[w].undraw()
            text_objects[w] = text
            # try and except block to ensure there window is not closed already
            try:
                text.draw(high_scores_win)
            # If the window is already closed it closes it to ensure it is and then returns from the function
            except:
                high_scores_win.close()
                return


# Calls the main function
main()