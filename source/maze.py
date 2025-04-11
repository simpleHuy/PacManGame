import pygame

class Maze:
    def __init__(self, CELL_SIZE, maze, offset_x=0, offset_y=0):
        self.cell_size = CELL_SIZE
        self.layout = maze  # Use layout instead of maze for consistency
        self.offset_x = offset_x
        self.offset_y = offset_y

        self.walls = []
        self.dots = []

        self.initialize_game_objects()
        self.dots_remaining = self.count_dots()

    def initialize_game_objects(self):
        for y, row in enumerate(self.layout):
            for x, cell in enumerate(row):
                cell_x = x * self.cell_size + self.offset_x
                cell_y = y * self.cell_size + self.offset_y

                if cell == '#':
                    self.walls.append(pygame.Rect(cell_x, cell_y, self.cell_size, self.cell_size))
                elif cell == '.':
                    self.dots.append(pygame.Rect(
                        cell_x + self.cell_size // 2 - 2,
                        cell_y + self.cell_size // 2 - 2,
                        4, 4
                    ))

    def count_dots(self):
        return sum(row.count('.') for row in self.layout)

    def check_collision(self, rect):
        for wall in self.walls:
            if rect.colliderect(wall):
                return True
        return False

    def check_dot_collision(self, rect):
        dots_eaten = 0
        for dot in self.dots[:]:  # Make a copy while iterating
            if rect.colliderect(dot):
                self.dots.remove(dot)
                dots_eaten += 1
                self.dots_remaining -= 1
        return dots_eaten

    def are_all_dots_eaten(self):
        return self.dots_remaining <= 0

    def draw(self, screen):
        for wall in self.walls:
            pygame.draw.rect(screen, (0, 0, 255), wall)

        for dot in self.dots:
            pygame.draw.rect(screen, (255, 255, 255), dot)
