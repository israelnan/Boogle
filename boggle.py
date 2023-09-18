import tkinter as tk
from typing import Tuple
import boggle_board_randomizer as bbr
import boggle_utils


LARGE_TEXT = ("Courier", 30)
SMALL_TEXT = ("Courier", 15)
DEFAULT_COLOR = "lightgrey"
DICTIONARY = []
for word in open("boggle_dict.txt"):
    DICTIONARY.append(word.strip())




class Board:
    """
    this class runs every aspect of the game. GUI-ing is very hard. :(
    """
    def __init__(self):
        # basic build blocks:
        root = tk.Tk()
        self.__main_window = root
        self.__found_words_frame = tk.Frame(self.__main_window)
        self.__board = bbr.randomize_board()
        self.__found_word_list = []
        self.__found_coordinates = []
        self.points = 0
        self.board_buttons = {}
        self.menu_buttons = {}
        self.__characters = ""
        self.__pressed_coordinates = []
        # frames:
        #   hud frames:
        self.__HUD = tk.Frame(self.__main_window)
        self.__HUD.pack(side=tk.TOP, fill=tk.Y, expand=True)
        self.__current_word = tk.Frame(self.__HUD)
        self.__found_words_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.__time = tk.Frame(self.__HUD)
        self.__time.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        #   menu:
        self.__menu = tk.Frame(self.__main_window)
        self.__menu.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.__instructions_frame = tk.Frame(self.__main_window)
        self.__instructions_frame.pack(side=tk.RIGHT)
        self.__instructions_label = self.instructions()
        # hint:
        self.__max_path = boggle_utils.max_score_paths(self.__board, DICTIONARY)
        self.__hint_frame = tk.Frame(self.__menu)
        self.__hint_frame.pack(side=tk.TOP)
        self.__hint_button = self.hint_button()
        self.__hint_flag = False
        #   board:
        self.__board_frame = ""
        # frames widgets:
        self.__found_words_label = tk.Label(self.__found_words_frame, text=", ".join(self.__found_word_list),
                                            font=SMALL_TEXT)
        self.__found_words_show = self.found_words_framing(self.__found_words_label)
        self.__found_words_show.pack()
        self.__current_word_label = tk.Label(self.__HUD, text=self.__characters, font=SMALL_TEXT)
        self.__current_word_show = self.current_word(self.__current_word_label)
        self.__score_label = tk.Label(self.__HUD, text="", font=LARGE_TEXT)
        self.__score_frame = self.score(self.__score_label)
        self.__score_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.__main_menu = self.main_menu()
        self.__time_show = ""


# board functions:
    def playing_board(self) -> tk.Frame:
        """
        builds the board and assign a button to each of the cells in the board.
        :return: a frame which contains a grid of buttons
        """
        frame = tk.Frame(self.__main_window)
        for row_ind in range(len(self.__board)):
            for cell_ind in range(len(self.__board[row_ind])):
                if len(self.__board[row_ind][cell_ind]) >= 2:
                    cube = self._make_board_buttons(self.__board[row_ind][cell_ind], row_ind, cell_ind, frame,
                                                    LARGE_TEXT, 0)
                else:
                    cube = self._make_board_buttons(self.__board[row_ind][cell_ind], row_ind, cell_ind, frame,
                                                    LARGE_TEXT)
                self.board_buttons[cube] = (row_ind, cell_ind)
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        return frame

    def add_letter(self, string: str, button: tk.Button) -> None:
        """
        _make_board_buttons() sub-function. adds letter to the letters that the player already choose when a
        board button is clicked
        :param string: the letter the player choose
        :param button: the button the player choose
        :return: None
        """
        if self.board_buttons[button] not in self.__pressed_coordinates:
            self.__characters += string
            self.__pressed_coordinates.append(self.board_buttons[button])
            self.__current_word_label.config(text=self.__characters)

    def _make_board_buttons(self, button_str: str, row: int, column: int, frame: tk.Frame,
                            text_style: Tuple[str, int], pad=12) -> tk.Button:
        """
        playing_board sub-function. creates the buttons of the board.
        :param button_str: the letter of the button
        :param row: the y index of the board
        :param column: the x index of the board
        :param frame: the frame which the buttons will be assigned to
        :param text_style: the style and the size of the text on the buttons
        :param pad: how much padding the buttons will have
        :return: a button
        """
        button = tk.Button(frame, padx=pad, text=button_str, font=text_style)
        button["bg"] = DEFAULT_COLOR
        button.grid(row=row, column=column)
        self.board_buttons[button] = (row, column)
        button.config(command=lambda: self.add_letter(button_str, button))

        def __hover(event) -> None:
            """
            changes the color of the button when the mouse cursor hoovers over it
            :param event: a user action
            :return: None
            """
            if button["background"] != "blue":
                button['background'] = "purple"

        def __alone(event) -> None:
            """
            changes the button color when the mouse cursor leaves it
            :param event: a user action
            :return: None
            """
            if button["background"] != "blue":
                button["background"] = DEFAULT_COLOR

        def __left_click(event):
            """
            changes the button color when the mouse cursor clicks it with left button
            :param event: a user action
            :return: None
            """
            button["background"] = "blue"

        button.bind("<Enter>", __hover)
        button.bind("<Leave>", __alone)
        button.bind("<Button-1>", __left_click)
        return button

# score functions:
    def score(self, score: tk.Label) -> tk.Frame:
        """
        creates the frame which displays the score
        :param score: a label
        :return: a frame which contains the score label
        """
        frame = tk.Frame(self.__HUD)
        show_score = score
        show_score.pack(side=tk.LEFT, padx= 80, fill=tk.BOTH, expand=True)
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        return frame

    def calculate_score(self, dic=None) -> None:
        """
        this function calculates the score and assign to the proper label so it will be display in the HUD
        :param dic: a list of the words from the game dictionary
        :return: None
        """
        if dic is None:
            dic = DICTIONARY
        if boggle_utils.is_path_legal(self.__board, self.__pressed_coordinates) and self.__characters in dic and\
                self.__pressed_coordinates not in self.__found_coordinates:
            self.points += len(self.__pressed_coordinates)**2
            self.__score_label.config(text=str(self.points))
            self.distribute_words()
            self.__found_words_label.config(text=", ".join(self.__found_word_list))
            self.__found_coordinates.append(self.__pressed_coordinates)

    def distribute_words(self) -> None:
        """
        calculate_score sub_function. make sure every 4 words the found_words label drops
         a line, so it will look nice.
        :return: None
        """
        if len(self.__found_word_list) % 4 == 3:
            self.__characters += "\n"
        self.__found_word_list.append(self.__characters)

# time functions:
    def time(self) -> None:
        """
        this function displays the time remained for the game
        :return: None
        """
        frame = tk.Frame(self.__HUD)
        minutes, seconds = 3, 00
        time_remain = tk.Label(frame, pady=10, text="3:00", font=SMALL_TEXT)
        time_remain.after(1000, lambda: self.time_update(seconds, minutes, time_remain))
        time_remain.pack()
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def time_update(self, seconds: int, minutes: int, label: tk.Label) -> None:
        """
        time() sub-function, updates the clock each second. stops the game when the time runs out.
        :param seconds: shows how many seconds left on the clock
        :param minutes: shows how many minutes left on the clock
        :param label: the label which is assigned to the frame
        :return:
        """
        seconds -= 1
        if seconds < 0:
            minutes -= 1
            seconds = 59
        if minutes < 0:
            self.time_out()
            return
        if seconds < 10:
            label.config(text=str(minutes) + ":0" + str(seconds))
        elif seconds < 20 and minutes == 0:
            label.config(text=str(minutes) + ":" + str(seconds), fg="red")
        else:
            label.config(text=str(minutes)+":"+str(seconds))
        label.after(1000, lambda: self.time_update(seconds, minutes, label))

    def time_out(self) -> None:
        """
        time_update() sub-function, stops the game and asks the player if he wants to quit or play another round.
        :return: None
        """
        self.__menu.destroy()
        self.__board_frame.destroy()
        self.__HUD.destroy()
        self.__found_words_frame.destroy()
        question = tk.Label(self.__main_window, text="TIME'S UP!\n Do you wanna play again?", font=LARGE_TEXT,
                            fg="red")
        question.pack()
        play_again = tk.Button(self.__main_window, text="Play Again", bg="green", command=self.new_game,
                               font=LARGE_TEXT, fg="white")
        play_again.pack()
        stop = tk.Button(self.__main_window, text="Exit", bg="red", command=self.__main_window.destroy,
                         font=LARGE_TEXT, padx=73)
        stop.pack()

    def new_game(self) -> None:
        """
        time_out() sub-function, runs a new round if the player chooses to play another round.
        :return: None
        """
        self.__main_window.destroy()
        board = Board()
        board.run()

# words functions:
    def current_word(self, current: tk.Label) -> tk.Frame:
        """
        creates the frame that displays the current characters that the player choose out of the board.
        :param current: a label that displays the characters the player choose from the board.
        :return: frame
        """
        frame = tk.Frame(self.__HUD)
        current.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        return frame

    def found_words_framing(self, word_label: tk.Label) -> tk.Frame:
        """
        creates the farme that displays al the words the player found in the board
        :param word_label: a label that shows the word the player already found in the board
        :return: frame
        """
        frame = tk.Frame(self.__found_words_frame)
        finding = word_label
        finding.pack()
        frame.pack()
        return frame

    def clear(self) -> None:
        """
        main_menu() sub-function. clears the lists of characters and coordinates which
        the player choose from the board and reset the board buttons colors.
        :return: None
        """
        self.__characters = ""
        self.__pressed_coordinates = []
        self.__current_word_label.config(text="")
        for button in self.board_buttons:
            button["bg"] = DEFAULT_COLOR

# menu functions:
    def main_menu(self) -> tk.Frame:
        """
        creates the main menu frame of the game and it's buttons: exit button exists the game, start button starts the game,
        lock button locks the word and clear button clears the word and the board.
        :return: frame
        """
        frame = tk.Frame(self.__menu)
        exit = self._make_menu_buttons("Exit", frame)
        start = self._make_menu_buttons("Start", frame, 0)
        lock = self._make_menu_buttons("Lock", frame)
        clear = self._make_menu_buttons("Clear", frame, 0)
        exit.config(command=self.__main_window.destroy)
        clear.config(command=self.clear)
        start.config(command=lambda: self.start(start))
        lock.config(command=self.lock)
        frame.pack(fill=tk.BOTH, expand=True)
        return frame

    def _make_menu_buttons(self, button_str: str, frame: tk.Frame, pad=12) -> tk.Button:
        """
        main_menu() sub-function. creates the graphic of the menu buttons.
        :param button_str: the string which will be displayed on the button.
        :param frame: the frame which the button will be display on.
        :param pad: how much padding the button will have
        :return: None
        """
        button = tk.Button(frame, padx=pad, text=button_str, font=LARGE_TEXT, fg="lightblue")
        button["bg"] = "green"
        button.pack()
        self.menu_buttons[button] = button_str

        def __left_click(event) -> None:
            """
            decides what the left button of the mouse will do to the button
            :param event: an action of the user
            :return: None
            """
            button["background"] = DEFAULT_COLOR

        def __alone(event) -> None:
            """
            decides what will happen when the mouse cursor leaves the button
            :param event: an action of the user
            :return: None
            """
            button["background"] = "green"

        button.bind("<Button-1>", __left_click)
        button.bind("<ButtonRelease-1>", __alone)
        return button

    def start(self, start: tk.Button) -> None:
        """
        main_menu() sub-function. starts the game and the clock.
        :param start: button
        :return: None
        """
        # changes the command to something benign so if the player accidentally presses it again nothing
        # would happen. v
        start.config(command="")
        self.__score_label["text"] = "0"
        self.__instructions_frame.destroy()
        self.time()
        self.__board_frame = self.playing_board()

    def lock(self) -> None:
        """
        locks the word the player choose and checks if it's a legal word. if it is, adds to the score.
        if it's not, does nothing.
        in any case it clears the HUD and the board using the clear() function (see above).
        :return: None
        """
        self.__hint_flag = False
        self.calculate_score()
        self.clear()

    def instructions(self):
        """
        puts the game instructions on the main window before we start the game.
        :return: a label
        """
        f = "GAME INSTRUCTIONS\n" \
            "to start the game press START.\n" \
            "to choose a character press one of the board buttons.\n" \
            "to check if the word is legal and get points on it press LOCK.\n" \
            "to clear your chosen characters without checking them press CLEAR.\n" \
            "to get a hint press HINT, every hint cost 5 points."
        h = tk.Label(self.__instructions_frame, text=f, font=SMALL_TEXT)
        h.pack()
        return h

# hint:
    def hinted_path(self):
        """
        the path that the Hint... hints the player.
        :return: a list of coordinates
        """
        for path in self.__max_path:
            if path not in self.__found_coordinates:
                 return path

    def hint_button(self) -> tk.Button:
        """
        creates the Hint button
        :return: a button
        """
        button = tk.Button(self.__hint_frame, padx=12, text="HINT", fg="white", bg="black",
                           font=LARGE_TEXT, command=self.da_hint)
        button.pack()
        return button

    def da_hint(self) -> None:
        """
        hint_button sub-function, chooses for the player the first coordinate of the random word,
        exactly like the player himself clicked the button. it means lighting the button blue
        up to puts the coordinate and the letter in their proper variables.
        :return: None
        """
        if self.__hint_flag:
            return
        self.__hint_flag = True
        self.clear()
        path = self.hinted_path()
        for button, coordinate in self.board_buttons.items():
            if path[0] == coordinate:
                button["bg"] = "blue"
                self.add_letter(button["text"], button)
                self.points -= 5


# the RUN function:
    def run(self) -> None:
        """
        runs the game.
        :return: None
        """
        self.__main_window.mainloop()


if __name__=="__main__":
    board = Board()
    board.run()