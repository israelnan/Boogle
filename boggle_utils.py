import copy
from typing import*


def board_coordiantes():
    """
    this function returns a list with tuples of all board coordinates in form of (y,x)
    where y is the row index and accordingly x is the column index.
    :return: list of all board coordinates.
    """
    coordinate_list = []
    for y in range(4):
        for x in range(4):
            coordinate_list.append((y, x))
    return coordinate_list


SURROND_DICT = [(-1, -1), (0, -1), (1, -1), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
COORDINATE_TYPE = list[tuple[int, int]]
BOARD_TYPE = list[list[str]]
COORDINATES = board_coordiantes()


def is_valid_path(board: BOARD_TYPE, path: COORDINATE_TYPE, words: list[str]) -> Optional[str]:
    """
    this function checks whether a path it receives is for word contained in the words list, and
     whether the path to it is legal
    :param board: 2D list of all 16 characters of the board.
    :param path: list of tuples of possible path to a word.
    :param words: list of all legal words.
    :return: the word if all conditions met, None otherwise.
    """
    if not(is_path_legal(board, path)):
        return None
    word = ""
    for coordinate in path:
        word += board[coordinate[0]][coordinate[1]]
    if word in words:
        return word
    return None


def is_path_legal(board, path: COORDINATE_TYPE) -> bool:
    """
    this is sub function for helping is_valid_path to determine whether the path is legal by the number
     of steps allowed.
    :param board: 2D list of all 16 characters of the board.
    :param path: list of tuples of possible path to a word.
    :return: True if all the steps in the path are legal, False otherwise.
    """
    for index in range(len(path)):
        if path[index][0] >= len(board) or path[index][0] < 0 or path[index][1] >= len(board[0]) or path[index][1] < 0:
            return False
        if index != len(path) - 1:
            if abs(path[index][0] - path[index+1][0]) >= 2 or abs(path[index][1] - path[index+1][1]) >= 2:
                return False
    return True


def find_max_possible_length(n: int, board: BOARD_TYPE) -> int:
    """
    this function helps to set the upper limit for word length, to reduce the running time of find_length_n_paths.
    :param n: lower limit of word length.
    :param board: 2D list of all 16 characters of the board.
    :return: an integer of upper limit for path length to be found.
    """
    m = n
    for x in board:
        for cell in x:
            if len(cell) > 1:
                m += (len(cell) - 1)
    return m


def find_length_n_paths(n: int, board: BOARD_TYPE, words: list[str]) -> list[COORDINATE_TYPE]:
    """
    this function finds all the paths of legal words in the board, in length of n.
    :param n: lower limit of word length.
    :param board: 2D list of all 16 characters of the board.
    :param words: list of all legal words allowed in the board.
    :return: list of all possible paths in length n of all words in the list.
    """
    coordinate_list = []
    words = filter_impossible_words(n, find_max_possible_length(n, board), words)
    for word in words:
        for y, x in COORDINATES:
            if is_cell_in_word(board[y][x], word):
                path_lst = find_word(word, word, board, (y, x), [(y, x)], [])
                for path in path_lst:
                    if len(path) == n and path not in coordinate_list and\
                            is_word_legally_in_board(word, board, path):
                        coordinate_list.append(path)
    return coordinate_list


def filter_impossible_words(n: int, m: int, words) -> dict[str]:
    """
    this function alternate a dictionary with all words up for find_length_n_paths, to reduce its running time.
    :param n: a lower limit of words length.
    :param m: an upper limit of words length.
    :param words: list of all legal words to be found in the board.
    :return: a dictionary with all the relevant words to be found.
    """
    filtered_words = {}
    for word in words:
        if m >= len(word) >= n:
            filtered_words[word.strip().upper()] = ""
    return filtered_words


def find_word(word: str, complete_word: str, board: BOARD_TYPE, coordinate: tuple[int, int],
              path_list: Optional[COORDINATE_TYPE], all_path_list) -> Optional[list[COORDINATE_TYPE]]:
    """
    this function used for finding all possible paths in the board for given word. uses a backtracking methods.
    :param word: word to be found on the board.
    :param complete_word: string that writen with the function running to compare the word, whether the process ended.
    :param board: 2D list of all 16 characters of the board.
    :param coordinate: tuple with the first appearance of the word on the board.
    :param path_list: list of current path coordinates.
    :param all_path_list: list of all possible paths to the word.
    :return: list of all possible paths to the word.
    """
    if len(word) == 0:
        return path_list
    length_cell = len(board[coordinate[0]][coordinate[1]])
    new_word = word[length_cell::]
    next_list = next_move(coordinate, new_word, board)
    if not next_list:
        all_path_list.append(copy.deepcopy(path_list))
        return all_path_list
    for cell in next_list:
        if cell in path_list:
            continue
        path_list.append(cell)
        find_word(new_word, complete_word, board, cell, path_list, all_path_list)
        path_list.pop()
    if word == complete_word:
        return all_path_list
    return []


def next_move(coordinate: tuple[int, int], word: str, board: BOARD_TYPE) -> Optional[COORDINATE_TYPE]:
    """
    this function helps find_word function to find the next move given a single path list.
    :param coordinate: tuple with the last coordinate in the current path.
    :param word: the next part of the word to be found.
    :param board: 2D list of all 16 characters of the board.
    :return: path list with added next coordinate.
    """
    if len(word) == 0:
        return []
    path_list = []
    for variable in SURROND_DICT:
        new_coordinate = (coordinate[0] + variable[0], coordinate[1] + variable[1])
        if is_coordinate_in_board(new_coordinate) and\
                is_cell_in_word(board[new_coordinate[0]][new_coordinate[1]], word):
            path_list.append(new_coordinate)
    return path_list


def is_coordinate_in_board(coordinate: tuple[int, int]) -> bool:
    """
    this function helps next_move to determine whether it's in the board or not.
    :param coordinate: tuple with coordinate to be checked.
    :return: True if it's the board, False if not.
    """
    return 0 <= coordinate[0] < 4 and 0 <= coordinate[1] < 4


def is_cell_in_word(cell: str, word: str) -> bool:
    if len(word) < len(cell):
        return False
    for idx in range(len(cell)):
        if cell[idx] != word[idx]:
            return False
    return True


def find_length_n_words(n: int, board: BOARD_TYPE, words: list[str]) -> list[COORDINATE_TYPE]:
    words = filter_words(n, words)
    coordinate_list = []
    for word in words:
        # if len(word) == n:
        for y,x in COORDINATES:
            if is_cell_in_word(board[y][x], word):
                path_lisy = find_word(word, word, board, (y, x), [(y,x)], [])
                for path in path_lisy:
                    if is_word_legally_in_board(word, board, path) and path not in coordinate_list:
                            coordinate_list.append(path)
    return coordinate_list


def filter_words(n: int, words: list[str]) -> dict:
    filtered_words = {}
    for word in words:
        if len(word) == n:
            filtered_words[word.strip().upper()] = ""
    return filtered_words


def is_word_legally_in_board(word: str, board: BOARD_TYPE, path_list: COORDINATE_TYPE) -> bool:
    compared_word = ""
    for coordinate in path_list:
        compared_word += board[coordinate[0]][coordinate[1]]
    return word == compared_word


def max_score_paths(board: BOARD_TYPE, words: list[str]) -> list[COORDINATE_TYPE]:
    max_lst = []
    for word in words:
        paths = find_length_n_words(len(word), board, [word])
        if paths:
            max_lst.append(find_max_path(paths, word))
    return max_lst


def find_max_path(path_list, word):
    max_path = []
    for path in path_list:
        if len(path) == len(word):
            return path
        if len(path) > len(max_path):
            max_path = path
    return max_path


