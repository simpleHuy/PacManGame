import pygame
import heapq
import random

# Hàm này để mở file maze và tạo maze
def open_maze():
    maze = []
    with open('input/maze.txt', 'r') as file:
        for line in file:
            maze.append(list(line.strip()))
    return maze

# Hàm này để chuyển maze nhỏ thành maze lớn có kích thước như cái map trong game 
def convmaze(MAZE, CELL_SIZE, WIDTH=744, HEIGHT=650):
    rows, cols = len(MAZE), len(MAZE[0])
    pixel_maze = [[" " for _ in range(WIDTH+4)] for _ in range(HEIGHT+4)] # L:ưu ý: +4 là do radius của vòng trong đỏ

    for row_idx, row in enumerate(MAZE):
        for col_idx, cell in enumerate(row):
            if cell == "#":
                start_y = row_idx * CELL_SIZE
                end_y = min(start_y + CELL_SIZE, HEIGHT)
                start_x = col_idx * CELL_SIZE
                end_x = min(start_x + CELL_SIZE, WIDTH)

                for y in range(start_y-4, end_y+4): # :Lưu ý: 4 là để trừ hao bán kính vòng tròn đỏ
                    for x in range(start_x-4, end_x+4):
                        pixel_maze[y][x] = "#"
    return pixel_maze

#Hàm này để lưu maze vào file
def save_pixel_maze_to_file(pixel_maze, output_path):
    with open(output_path, "w") as f:
        for row in pixel_maze:
            f.write("".join(row) + "\n")
  
# Hàm heuristic cho thuật toán A* dựa trên khoảng cách manhattan 
def manhattan_distance(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])

# Thuật toán A*
def astar(start, goal, grid):
    # Các danh sách để theo dõi các nút
    open_list = []  # Nút cần kiểm tra
    closed_list = set()  # Nút đã kiểm tra

    # Đánh dấu điểm bắt đầu
    heapq.heappush(open_list, (0, start))  # (f(n), điểm)

    # Đánh dấu chi phí g(n) và f(n) cho từng điểm
    g_costs = {start: 0}
    came_from = {}  # Lưu lịch sử di chuyển

    while open_list:
        # Lấy nút có f(n) thấp nhất
        _, current = heapq.heappop(open_list)

        if current == goal:
            # Nếu tìm được đích, hồi phục con đường đi
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        closed_list.add(current)

        # Kiểm tra các điểm xung quanh (4 hướng)
        for neighbor in [(current[0] - 1, current[1]), (current[0] + 1, current[1]), 
                         (current[0], current[1] - 1), (current[0], current[1] + 1)]:
            # Kiểm tra nếu neighbor hợp lệ (nằm trong lưới và không phải là vật cản)
            if 0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid[0]) and grid[neighbor[0]][neighbor[1]] != '#':
                if neighbor in closed_list:
                    continue
                
                tentative_g = g_costs[current] + 1  # Chi phí từ start đến neighbor (giả sử di chuyển theo 4 hướng)

                if neighbor not in g_costs or tentative_g < g_costs[neighbor]:
                    # Nếu tìm thấy đường đi tốt hơn đến neighbor
                    came_from[neighbor] = current
                    g_costs[neighbor] = tentative_g
                    f_cost = tentative_g + manhattan_distance(neighbor, goal)
                    heapq.heappush(open_list, (f_cost, neighbor))

    return None  # Nếu không tìm thấy đường đi

# Thiết lập lớp đối tượng RedGost
class RedGhost(pygame.sprite.Sprite):
    #Khởi tạo 
    def __init__(self, color, start_position, maze, size=(20,20),speed=2,cell_size =20):
        super().__init__()
        self.image = pygame.Surface((15, 15))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = start_position
        self.maze = convmaze(maze,cell_size)
        #self.maze = maze
        self.speed = speed
        self.path = []    
        self.CELL_SIZE = cell_size
        self.last_pos = None     
        self.direction = pygame.Vector2(1, 0)  # Bắt đầu di chuyển sang phải
    
    # Thiết lập di chuyển cho Ghost
    def move(self):
     if self.path:
        next_cell = self.path.pop(0)
        target_x = next_cell[1] # cột → x
        target_y = next_cell[0]  # hàng → y
       # target_x = next_cell[1] *self.CELL_SIZE# cột → x
       # target_y = next_cell[0] .self.CELL_SIZE # hàng → y
        self.rect.center = (target_x, target_y)
    # Vẽ Ghost ra màn hình
    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (int(self.rect.center[0]), int(self.rect.center[1])),radius =4)

    # Cập nhật lại con đường tìm pacman nhờ thuật toán A*
    def update(self, pacman_pos):
     #start = (self.rect.centery // self.CELL_SIZE, self.rect.centerx // self.CELL_SIZE)  # Hàng, cột
     # goal = (pacman_pos[1] // self.CELL_SIZE, pacman_pos[0] // self.CELL_SIZE)           # Hàng, cột
    
     start = (self.rect.centery, self.rect.centerx)
     goal = (pacman_pos[1], pacman_pos[0])
     
     self.path = astar(start, goal, self.maze)
     
       # Dùng A* tìm đường
     #if self.path:
       # self.path.pop(0)  # Bỏ vị trí hiện tại để không lặp lại
 
'''
Đoạn này để kiểm thử 
def main2():
    grid = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0]
 ]
    start = (0, 0)  # Điểm bắt đầu
    goal = (4, 4)   # Điểm đích

    maze = open_maze()
    maze = convmaze(maze,2)
    save_pixel_maze_to_file(maze,"output.txt")

if __name__ == "__main__":
   main2()

'''
