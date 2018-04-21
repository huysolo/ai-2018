# Màn chơi mẫu
# 1: Vị trí hợp lệ
# 0: Vị trí không hợp lệ
# G: Vị trí block không thể đứng thẳng
# X: Đích
level1 = ['1110000000',
          '1111110000',
          '1111111110',
          '0111G11111',
          '0000GG1X11',
          '0000001110']

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
        return None

#Xử lý input với hướng nhận được
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
    height = len(i_board)
    width = len(i_board[0])
    if i_input[0][0] >= 0 and i_input[0][1] >= 0 and i_input[1][0] >= 0 and i_input[1][1] >= 0 and i_input[0][0] < height and i_input[1][0] < height and i_input[0][1] < width and i_input[1][1] < width:
        if i_board[i_input[0][0]][i_input[0][1]] == 'X' and i_board[i_input[1][0]][i_input[1][1]] == 'X':
            return 'W'
        elif (i_board[i_input[0][0]][i_input[0][1]] == '1' and i_board[i_input[1][0]][i_input[1][1]] == '1') \
                or (block_direction(i_input) != 0 and i_board[i_input[0][0]][i_input[0][1]] == 'G' and i_board[i_input[1][0]][i_input[1][1]] == 'G'):
            return 'N'
    return 'L'

# In bàn cờ
def print_board(i_board, i_pos=((0, 0), (0, 0))):
    n_board = i_board.copy()
    n_board[i_pos[0][0]] = n_board[i_pos[0][0]][:i_pos[0][1]] + 'B' + n_board[i_pos[0][0]][i_pos[0][1] + 1:]
    n_board[i_pos[1][0]] = n_board[i_pos[1][0]][:i_pos[1][1]] + 'B' + n_board[i_pos[1][0]][i_pos[1][1] + 1:]
    for board in n_board:
        print(board)

# Giải thuật dfs
def dfs(direction, i_pos=((0, 0), (0, 0)), i_board=None):
    global avalMove
    global listMove
    if i_board is None:
        i_board = []
    n_input = move(direction, i_pos)
    temp = valid_move(n_input, i_board)
    if temp == 'N':
        for m in list(filter(lambda x: x != -direction, avalMove)):
            temp = dfs(m, n_input, i_board)
            if temp == 'W':
                break
    if temp == 'W':
        listMove.append(n_input)
    return temp

def bfs():
    return 0

# Phương thứ xử lý giải thuật
def run(i_method):
    for mv in list(reversed(listMove)):
        print('Block position: ', mv)
        print_board(level1, mv)
        print('-------------')
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
