import copy

# Màn chơi mẫu
# 1: Vị trí hợp lệ
# 0: Vị trí không hợp lệ
# G: Vị trí block không thể đứng thẳng
# X: Đích
# LA: Cần gạt nhẹ cho vị trí A
# HA: Cần gạt nặng cho vị trí A
# 1A, 0A: Vị trí thay đổi khi chạm vào cần gạt
# level1 = [['1', '1', '1', '0', '0', '0', '0', '0', '0', '0'],
#           ['1', '1', '1', 'LA', '1', '0A', '0', '0', '0', '0'],
#           ['1', '1', '1', '1', '1', '1', '1', '1', '1', '0'],
#           ['1', '1', '1', '1', 'G', '1', '1', '1', '1', '1'],
#           ['0', '0', '0', '0', 'G', 'G', '1', 'X', '1', '1'],
#           ['0', '0', '0', '0', '0', '0', '1', '1', '1', '0']]
level1 = [['0','1','1','1','0','0','0','0','0','0'],
          ['0','1','1','1','1','0','0','0','0','0'],
          ['LK','1','1','1','1','0K','1','X','1','0'],
          ['0','1','1','1','1','1','1','1','1','1'],
          ['0','0','0','0','G','G','1','0','1','1'],
          ['0','0','0','0','0','0','1','1','1','0']]

# Order: [row col][row, col]
b_input = ((2, 1), (2, 2))

# Các bước có thể di chuyển được:
# 1: Lên
# 2: Phải
# -1: Xuống
# -2: Trái
list_direction = [1, 2, -1, -2]
listMove = []


def init_input(x1, y1, x2, y2):
    return (x1, y1), (x2, y2)


# 0: đứng, 1: dọc, -1: ngang
def block_direction(i_input=((0, 0), (0, 0))):
    if i_input[0][0] == i_input[1][0] and i_input[0][1] == i_input[1][1]:
        return 0
    elif i_input[0][0] == i_input[1][0] and abs(i_input[0][1] - i_input[1][1]) == 1:
        return 1
    elif abs(i_input[0][0] - i_input[1][0]) == 1 and i_input[0][1] == i_input[1][1]:
        return -1
    else:
        return 2


# Xử lý input với hướng nhận được
def move(direction, i_input=((0, 0), (0, 0))):
    row = 0
    col = 0
    is_horizontal = 1
    if direction == 1:
        row = row - 1
    elif direction == -1:
        row = row + 1
    elif direction == -2:
        col = col - 1
        is_horizontal = -1
    elif direction == 2:
        col = col + 1
        is_horizontal = -1
    else:
        return i_input

    orientation = block_direction(i_input) * is_horizontal
    if orientation == 0:
        if row == -1 or col == -1:
            return (i_input[0][0] + row * 2, i_input[0][1] + col * 2), (i_input[1][0] + row, i_input[1][1] + col)
        elif row == 1 or col == 1:
            return (i_input[0][0] + row, i_input[0][1] + col), (i_input[1][0] + row * 2, i_input[1][1] + col * 2)
    elif orientation == 1:
        return (i_input[0][0] + row, i_input[0][1] + col), (i_input[1][0] + row, i_input[1][1] + col)
    elif orientation == -1:
        if row == 1 or col == 1:
            return (i_input[0][0] + row * 2, i_input[0][1] + col * 2), (i_input[1][0] + row, i_input[1][1] + col)
        elif row == -1 or col == -1:
            return (i_input[0][0] + row, i_input[0][1] + col), (i_input[1][0] + row * 2, i_input[1][1] + col * 2)


# Tính giá trị từ input
def execute_move(i_input=((0, 0), (0, 0)), i_board=None):
    if i_board is None:
        i_board = []
    # Khởi tạo giá trị cho bàn cờ hiện tại
    height = len(i_board)
    width = len(i_board[0])
    i_state = 'N'
    block_dir = block_direction(i_input)

    if is_not_out_of_range(i_input, height, width):
        # Trường hợp thắng
        if is_equal(i_input, i_board, 'X'):
            i_state = 'W'

        # Trường hợp không thay đổi trạng thái
        elif is_equal([i_input[0]], i_board, '0') or is_equal([i_input[1]], i_board, '0') or (block_dir == 0 and is_equal(i_input, i_board, 'G')):
            i_state = 'L'

        # Trường hợp thay đổi trạng thái gạt cần
        elif (is_equal(i_input, i_board, 'H') and block_dir == 0) or is_equal([i_input[0]], i_board, 'L'):
            i_board = toggle_switch(i_board, get_string(i_input[0], i_board, 1))
        elif is_equal([i_input[1]], i_board, 'L'):
            i_board = toggle_switch(i_board, get_string(i_input[1], i_board, 1))
        # Trường hợp teleport
        elif is_equal([i_input[0]], i_board, 'T') or is_equal([i_input[0]], i_board, 'T'):
            if block_dir != 2:
                if block_dir == 0 or is_equal([i_input[0]], i_board, 'T'):
                    i_input[0] = teleports(i_board, get_string(i_input[0], i_board, 1))
                else:
                    i_input[1] = teleports(i_board, get_string(i_input[0], i_board, 1))

    # Trường hợp không hợp lệ
    else:
        i_state = 'L'

    # Giá trị trả về bao gồm trạng thái bàn cờ, bàn cờ, giá trị input
    return i_state, i_board, i_input


def toggle_switch(i_board, word):
    if i_board is None:
        i_board = []
    for row in range(len(i_board)):
        for col in range(len(i_board[row])):
            if len(i_board[row][col]) == 2 and i_board[row][col][1] == word:
                if i_board[row][col][0] == '0':
                    i_board[row][col] = '1' + i_board[row][col][1]
                elif i_board[row][col][0] == '1':
                    i_board[row][col] = '0' + i_board[row][col][1]
    return i_board


def teleports(i_board, word):
    if i_board is None:
        i_board = []
    for row in range(len(i_board)):
        for col in range(len(i_board[row])):
            if i_board[row][col][0] == 't' and i_board[row][col][1] == word:
                return row, col


def is_not_out_of_range(i_input, height, width):
    rs = True
    for i in i_input:
        rs = rs and i[0] >= 0 and i[1] >= 0 and i[0] < height and i[1] < width
    return rs


def is_equal(i_input, i_board, word, pos=0):
    rs = True
    for i in i_input:
        rs = rs and get_string(i, i_board, pos) == word
    return rs


def get_string(i_block, i_board, pos=0):
    return i_board[i_block[0]][i_block[1]][pos]


# In bàn cờ
def print_board(i_board, i_pos=((0, 0), (0, 0))):
    n_board = copy.deepcopy(i_board)
    n_board[i_pos[0][0]][i_pos[0][1]] = 'B'
    n_board[i_pos[1][0]][i_pos[1][1]] = 'B'
    for board in n_board:
        print(board)


# So sách 2 bàn cờ
def compare_board(i_board1, i_board2):
    for row in range(len(i_board1)):
        for col in range(len(i_board2[row])):
            if i_board1[row][col] != i_board2[row][col]: return False
    return True


def exist(moves_w_board, i_input, i_board):
    for i in moves_w_board:
        if i[0] == i_input and compare_board(i[1], i_board):
            return True
    return False

def dfs(moves_w_board, i_board, state, i_input):

    if state == 'L':
        return None
    elif state == 'N':
        if exist(moves_w_board, i_input, i_board):
            return None
        else:
            n_moves_w_board = copy.deepcopy(moves_w_board)
            n_moves_w_board.append((i_input, i_board))
            for d in list_direction:
                n_state, n_board, n_input = execute_move(move(d, i_input), copy.deepcopy(i_board))

                result = dfs(n_moves_w_board, n_board, n_state, n_input)
                if result is not None:
                    return result
    else:
        moves_w_board.append((i_input, i_board))
        return moves_w_board


def bfs():
    return 0


def test():
    i_input = ((2, 1), (2, 2))
    global level1
    while True:
        direct = input('Insert your method: ')
        i_input = move(int(direct), i_input)
        state, level1, i_input = execute_move(i_input, level1)
        print_board(level1, i_input)
        print('Block position: ', i_input)


# Phương thức chạy giải thuật
def run(i_inputs):
    if i_inputs is not None:
        for i in i_inputs:
            print('-------------')
            # state, i_board, n_input = execute_move(i, i_board)
            print_board(i[1], i[0])
            print('Block position: ', i[0])
        print('The path has been found')
    else:
        print('Cannot find the path')


while True:
    method = input('Insert your method: ')
    if method == 'dfs':
        run(dfs([], level1, 'N', b_input))
    elif method == 'bfs':
        pass
