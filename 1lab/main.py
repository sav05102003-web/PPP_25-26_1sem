import random

def generate_game_field(rows, cols):
    field = []
    for _ in range(rows):
        row = [random.randint(0, 1) for _ in range(cols)]
        field.append(row)
    return field

def get_island_sizes(field):
    rows = len(field)
    cols = len(field[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    island_sizes = []

    def find(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or visited[r][c] or field[r][c] == 0:
            return 0
        
        visited[r][c] = True
        size = 1
        size += find(r + 1, c)
        size += find(r - 1, c)
        size += find(r, c + 1)
        size += find(r, c - 1)
        return size

    for r in range(rows):
        for c in range(cols):
            if field[r][c] == 1 and not visited[r][c]:
                size = find(r, c)
                if size > 0:
                    island_sizes.append(size)
                    
    return island_sizes

def count_rows_cols_with_many_ones(field):
    rows = len(field)
    cols = len(field[0])
    rows_with_many = 0
    cols_with_many = 0

    for r in range(rows):
        if field[r].count(1) > 3:
            rows_with_many += 1
            
    for c in range(cols):
        col_ones_count = 0
        for r in range(rows):
            if field[r][c] == 1:
                col_ones_count += 1
        if col_ones_count > 3:
            cols_with_many += 1
            
    return rows_with_many, cols_with_many


N = int(input("Введите N:"))
M =  int(input("Введите M:"))

game_field = generate_game_field(N, M)

print("Сгенерированное игровое поле:")
for row in game_field:
    print(row)

sizes = get_island_sizes(game_field)
print(f"Размеры островов: {sizes}")

rows_many, cols_many = count_rows_cols_with_many_ones(game_field)
print(f"Количество строк, где более 3 единиц: {rows_many}")
print(f"Количество столбцов, где более 3 единиц: {cols_many}")
