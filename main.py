import random
import time
import pygame


class Game(object):

    def __init__(self, text_length=30):
        self.pool_of_words = ['Master', 'Jane', 'for', 'help', 'quire', 'hear', 'remote',
                              'sister', 'dark', 'remote', 'they', 'was', 'saw', 'shall',
                              'Paris', 'dear', 'ramen', 'pizza', 'when', 'literature',
                              'pineapple', 'good', 'rose', 'tomorrow', 'shield', 'wizard',
                              'people', 'dog', 'cat', 'shepherd', 'kiss', 'dear', 'cally',
                              'animals', 'a', 'if', 'yes', 'no', 'keys', 'mouse', 'beard',
                              'lily', 'the', 'rise', 'python', 'coding', 'beautiful', 'mercy',
                              'gold', 'red']
        self.accuracy = 0
        self.displayed = []
        self.speed = 0
        self.text_length = text_length

    def display_words(self):
        # displaying and then storing random words
        for i in range(0, self.text_length):
            self.displayed.append(self.pool_of_words[random.randint(0, 49)])
            print(self.displayed[i], end=" ")

    def typing_speed(self, total_time, user_input):
        typed = user_input.split()
        length = len(typed)

        # if the player takes this much time to type these many word then how many words in 60 seconds
        self.speed = int(length*(60/total_time))

        return self.speed

    def typing_accuracy(self, user_input):
        count = 0
        typed = user_input.split()

        # converting list to string to calculate total number of characters in the displayed sentence
        str = " "
        string = str.join(self.displayed)

        length_displayed = len(self.displayed)
        length = len(typed)

        if length > length_displayed:
            length = length_displayed

        temp = 0 # temporary variable

        # checking every word and if there is an error then finding how many characters did the player get write
        for i in range(0, length):
            if typed[i] == self.displayed[i]:
                count += len(typed[i]) + 1 # counting the blank
            else:
                if len(typed[i]) <= len(self.displayed[i]):
                    temp = len(typed[i])
                else:
                    temp = len(self.displayed[i])

                for j in range(0, temp):
                    if typed[i][j] == self.displayed[i][j]:
                        count += 1

                count += 1 # counting the blank

        # depending on the ratio between number of correct characters and total characters
        self.accuracy = int((count/(len(string)+1)) * 100)

        return self.accuracy

    def reset(self):
        self.accuracy = 0
        self.speed = 0
        self.displayed = []


def start_game():
    player = Game()
    print("Type the following sentence and then hit enter\n")
    start_time = time.time()
    player.display_words()
    user_input = input("\n")
    end_time = time.time()
    total_time = int(end_time - start_time)
    player_speed = player.typing_speed(total_time, user_input)
    player_accuracy = player.typing_accuracy(user_input)
    print("\nTyping Speed:", player_speed, "WPM")
    print("Accuracy:", player_accuracy, "%")
    data = [player_speed, player_accuracy]
    return data


def adding_score(file, f, name, speed, accuracy):
    data = []
    flag = 0
    for i in range(0, len(f)):
        data = f[i].split()
        # saving text in form of "name speed accuracy"
        if data[0] == name:
            flag = 1
            if int(data[1]) < int(speed):
                data[1] = str(speed)
                f.remove(f[i])
                f.append(name + " " + str(speed) + " " + str(accuracy) + "\n")
            break

    if flag == 0:
        f.append(name+" "+str(speed)+" "+str(accuracy)+"\n")

    file.close()
    file = open('game data.txt', 'w')
    for line in f:
        file.write(line)


def print_score(f):
    length = len(f)
    data = []
    # printing score of only those whose accuracy is more than 100
    for i in range(0, length):
        data = f[i].split()
        if int(data[2]) >= 85:
            print(data[1]+"WPM -"+data[0])


if __name__ == '__main__':

    player = Game
    game_data = open('game data.txt', 'r+')
    f = game_data.readlines()
    print("Bryden's Typing Speed Game")
    print("==========================\n")

    # main loop
    running = True
    while running:
        player_data = start_game()

        choice = input("\nDo you want to save this score (y or n)?:")
        if choice == 'y':
            name = input("Enter your name:")
            adding_score(game_data, f, name, player_data[0], player_data[1])

        choice = input("\nDo you want to see the leaderboard?")
        if choice == 'y':
            print("\nTyping Scores:")
            print("===============")
            print_score(f)

        choice = input("\nDo you want to play again (y or n)?:")
        if choice != 'y':
            running = False
            print("Goodbye!")

    game_data.close()