# ai-2018 - BLOXORZ
AI assignment in 2018
<h3>Nội dung chương trình: </h3>
Hiện thực bài toán trong trò chơi Bloxorz bằng 3 giải thuật: dfs, bfs, hill climbing

<h3>Cách sử dụng:</h3>
Nhập vào 1 trong 3 chuỗi ứng với tên của 3 giải thuật để chương trình bắt đầu chạy


<h3>Các giá trị khởi tạo:</h3>
<ul>
  <li>
    board: là bàn cờ mảng 2 chiều, với các giá trị:
    <ul>
          <li>1: Vị trí hợp lệ</li>
          <li>0: Vị trí không hợp lệ</li>
          <li>G: Vị trí block không thể đứng thẳng</li>
          <li>X: Đích</li>
          <li>LA: Cần gạt nhẹ cho vị trí A</li>
          <li>HA: Cần gạt nặng cho vị trí A</li>
          <li>1A, 0A: Vị trí thay đổi khi chạm vào cần gạt</li>
    </ul>
  </li>
  <li>input: là 1 tupple có dạng  ((,),(,)) dùng để vị trí của khối block trên bàn cờ
  </li>
</ul>

<h3>Cách hoạt động:</h3>
- Chương trình nhận vào 1 trong 3 input ứng với tên của 3 giải thuật
- Hàm run sẽ nhận 1 chuỗi có giá trị trả về là list các cặp input và board ứng với giải thuật đã chọn. Sau đó lần lượt in bàn cờ cùng input

<h3>Các phương thức chính:</h3>

- <strong>block_direction(input):</strong> Trả về hướng mặc định của block từ input (0, 1, -1, 2)

- <strong>move(direction, input):</strong> Nhận vào hướng của đi cho block và vị trí hiện tại của block. Trả về hướng đi vị trí

- <strong>execute_move(input, board):</strong> Nhận vào vị trí của block và bàn cờ. Trả về vị trí mới, bàn cờ mới, và trạng thái hiện tại của trò chơi (W, L, N)

- <strong>print_board(input, board):</strong>  In bàn lên màn hình từ input và board


