import copy
# Màn chơi mẫu
# 1: Vị trí hợp lệ
# 0: Vị trí không hợp lệ
# G: Vị trí block không thể đứng thẳng
# X: Đích
# LA: Cần gạt nhẹ cho vị trí A
# LA: Cần gạt nặng cho vị trí A
# sA: Vị trí thay đổi khi chạm vào cần gạt
level1 = [['1','1','1','0','0','0','0','0','0','0'],
          ['1','1','1','1','1','1','0','0','0','0'],
          ['1','1','1','1','1','1','1','1','1','0'],
          ['0','1','1','1','G','1','1','1','1','1'],
          ['0','0','0','0','G','G','1','X','1','1'],
          ['0','0','0','0','0','0','LK','1','1','0']]

# Order: [row col][row, col]
b_input = ((2, 1), (2, 2))

# Các bước có thể di chuyển được:
# 1: Lên
# 2: Phải
# -1: Xuống
# -2: Trái
avalMove = [1, 2, -1, -2]
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
def valid_move(i_input=((0, 0), (0, 0)), i_board=None):
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
        elif is_equal(i_input, i_board, '1') or (block_dir != 0 and is_equal(i_input, i_board, 'G')):
            i_state = 'N'

        # Trường hợp thay đổi trạng thái gạt cần
        elif (is_equal(i_input, i_board, 'H') and block_dir == 0) or is_equal([i_input[0]], i_board, 'L') or is_equal([i_input[1]], i_board, 'L'):
            i_state = 'S'
            i_board = toggle_switch(i_board, get_string(i_input[0], i_board, 1))

        # Trường hợp teraport
        elif is_equal([i_input[0]], i_board, 'T') or is_equal([i_input[0]], i_board, 'T'):
            if block_dir != 2:
                i_state = 'T'
                if block_dir == 0 or is_equal([i_input[0]], i_board, 'T'):
                    i_input[0] = teraport(i_board, get_string(i_input[0], i_board, 1))
                else:
                    i_input[1] = teraport(i_board, get_string(i_input[0], i_board, 1))

        # Trường hợp không hợp lệ
        else: i_state = 'L'

    # Trường hợp không hợp lệ
    else: i_state =   'L'

    # Giá trị trả về bao gồm trạng thái bàn cờ, bàn cờ, giá trị input
    return i_state, i_board, i_input


def toggle_switch(i_board, str):
    if i_board is None:
        i_board = []
    for row in range(len(i_board)):
        for col in range(len(i_board[row])):
            if i_board[row][col][0] == 's' and i_board[row][col][1].upper() == str:
                if i_board[row][col][1].isupper():
                    i_board[row][col] =  's' + i_board[row][col][1].lower()
                else:
                    i_board[row][col] =  's' + i_board[row][col][1].upper()
    return i_board

def teraport(i_board, str):
    if i_board is None:
        i_board = []
    for row in range(len(i_board)):
        for col in range(len(i_board[row])):
            if i_board[row][col][0] == 't' and i_board[row][col][1] == str:
                return (row, col)

def is_not_out_of_range(i_input, height, width):
    rs = True
    for i in i_input:
        rs = rs and i[0] >= 0 and i[1] >= 0 and i[0] < height and i[1] < width
    return rs

def is_equal(i_input, i_board, str, pos = 0):
    rs = True
    for i in i_input:
        rs = rs and get_string(i, i_board, pos) == str
    return rs

def get_string(i_block, i_board, pos = 0):
    return i_board[i_block[0]][i_block[1]][pos]

# In bàn cờ
def print_board(i_board, i_pos=((0, 0), (0, 0))):
    n_board = copy.deepcopy(i_board)
    n_board[i_pos[0][0]][i_pos[0][1]] = 'B'
    n_board[i_pos[1][0]][i_pos[1][1]] = 'B'
    for board in n_board:
        print(board)

# Giải thuật dfs
def dfs(direction, i_pos=((0, 0), (0, 0)), i_board=None):
    global avalMove
    global listMove
    if i_board is None:
        i_board = []
    n_input = move(direction, i_pos)
    state, n_board, n_input = valid_move(n_input, i_board)
    if state == 'N':
        for m in list(filter(lambda x: x != -direction, avalMove)):
            state = dfs(m, n_input, n_board)
            if state == 'W':
                break
    if state == 'W':
        listMove.append(n_input)
    return state

def bfs():
    return 0

# Phương thức chạy giải thuật

def run(i_method):
    for mv in list(reversed(listMove)):
        print('-------------')
        print_board(level1, mv)
        print('Block position: ', mv)
    if i_method == 'W':
        print("Won")
    else:
        print('Cannot find available path')


while True:
    method = input('Insert your method: ')
    if method == 'dfs':
        run(dfs(0, b_input, level1))
    elif method == 'bfs':
        pass
