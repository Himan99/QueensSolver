import heapq
import GameofCrownsBoardFetcher

testBoard = [
['C1', 'C1', 'C2', 'C2', 'C3', 'C4', 'C4'] ,
['C1', 'C2', 'C2', 'C2', 'C2', 'C2', 'C4'] ,
['C1', 'C5', 'C5', 'C5', 'C5', 'C4', 'C4'] ,
['C5', 'C5', 'C6', 'C6', 'C5', 'C5', 'C4'] ,
['C6', 'C6', 'C6', 'C6', 'C5', 'C4', 'C4'] ,
['C6', 'C6', 'C6', 'C6', 'C5', 'C5', 'C5']
]

testBoard2 = [
    ['C1', 'C1', 'C1', 'C1', 'C1', 'C2', 'C2', 'C2', 'C3'] ,
    ['C4', 'C5', 'C5', 'C5', 'C1', 'C5', 'C5', 'C5', 'C3'] ,
    ['C4', 'C5', 'C6', 'C5', 'C1', 'C5', 'C7', 'C5', 'C3'] ,
    ['C4', 'C5', 'C6', 'C5', 'C5', 'C5', 'C8', 'C5', 'C3'] ,
    ['C4', 'C5', 'C6', 'C6', 'C8', 'C8', 'C8', 'C5', 'C3'] ,
    ['C4', 'C5', 'C6', 'C5', 'C5', 'C5', 'C8', 'C5', 'C3'] ,
    ['C4', 'C5', 'C6', 'C5', 'C9', 'C5', 'C8', 'C5', 'C9'] ,
    ['C4', 'C5', 'C5', 'C5', 'C9', 'C5', 'C5', 'C5', 'C9'] ,
    ['C4', 'C4', 'C4', 'C9', 'C9', 'C9', 'C9', 'C9', 'C9'] 
]

testBoard3 = [
['C1', 'C1', 'C1', 'C1', 'C1', 'C2', 'C2'] ,
['C1', 'C3', 'C3', 'C3', 'C3', 'C3', 'C2'] ,
['C1', 'C3', 'C4', 'C4', 'C4', 'C3', 'C2'] ,
['C1', 'C3', 'C3', 'C3', 'C3', 'C3', 'C2'] ,
['C5', 'C3', 'C6', 'C6', 'C6', 'C3', 'C2'] ,
['C5', 'C3', 'C3', 'C3', 'C3', 'C3', 'C2'] ,
['C5', 'C7', 'C7', 'C2', 'C2', 'C2', 'C2']
]

def get_color_map(board):
    d = {}
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] not in d:
                d[board[i][j]] = []
            d[board[i][j]].append([i,j])
    return d

def check_and_append(ans, x, y, board):
    if x>=0 and x<len(board) and y>=0 and y<len(board[0]):
        ans.append([x,y])
    return ans

def get_xs_for_one_cell(x, y, board):
    height = len(board)
    width = len(board[0])
    ans = []
    for i in range(width):
        if i != y:
            ans.append([x,i])
    for i in range(height):
        if i != x:
            ans.append([i,y])

    ans = check_and_append(ans, x-1, y-1, board)
    ans = check_and_append(ans, x-1, y, board)
    ans = check_and_append(ans, x-1, y+1, board)
    ans = check_and_append(ans, x, y-1, board)
    ans = check_and_append(ans, x, y+1, board)
    ans = check_and_append(ans, x+1, y-1, board)
    ans = check_and_append(ans, x+1, y, board)
    ans = check_and_append(ans, x+1, y+1, board)
    return ans

def get_xs_for_one_color(color, colorMap, board):
    s = set()
    coords = colorMap[color]
    # get x for first point of a color
    if len(coords) == 0:
        return s
    xs = get_xs_for_one_cell(coords[0][0], coords[0][1], board)
    xs = set(map(tuple, xs))
    s = s | xs

    for i in range(1, len(coords)):
        xs = get_xs_for_one_cell(coords[i][0], coords[i][1], board)
        xs = set(map(tuple, xs))
        s = s & xs

    # draw(list(s), board)

    # for i in s:
    #     x,y = i
    #     color = board[x][y]
    #     if [x, y] in colorMap[color]:
    #         colorMap[color].remove([x,y])

    # eliminateCells(s, colorMap, board)

    return s

def draw_color_map(colorMap, board, draw = True):
    
    rows, cols = len(board), len(board[0])
    drawBoard = [['X  ' for _ in range(cols)] for _ in range(rows)]

    for color in colorMap:
        for i in colorMap[color]:
            x,y = i
            drawBoard[x][y] = color + ' '
    if draw:
        for row in drawBoard:
            print(''.join(row))
        print()
    return drawBoard

def draw(l, board, c='X'):
    rows, cols = len(board), len(board[0])
    drawBoard = [['O' for _ in range(cols)] for _ in range(rows)]

    for x, y in l:
        drawBoard[x][y] = c

    for row in drawBoard:
        print(''.join(row))
    print()

def eliminate_cells(s, colorMap, board):
    numberOfCellsEliminated = 0
    for i in s:
        x,y = i
        color = board[x][y]
        if [x, y] in colorMap[color]:
            colorMap[color].remove([x,y])
            numberOfCellsEliminated += 1
    return numberOfCellsEliminated


def get_color_count(colorMap):
    c = {}
    for i in colorMap:
        c[i] = len(colorMap[i])
    return c

def verify_board(colorMap, board):
    xcord = set()
    ycord = set()
    for color in colorMap:
        if len(colorMap[color]) != 1:
            return False
        xcord.add(colorMap[color][0][0])
        ycord.add(colorMap[color][0][1])

    if len(xcord) != len(board) or len(ycord) != len(board[0]):
        return False
    return True

def eliminate_row_column_surrounding_cells_for_each_color(colorMap, board):
    colorCount = get_color_count(colorMap)
    pq = []
    for c in colorCount:
        heapq.heappush(pq, (colorCount[c], c))
    while len(pq) > 0:
        prio, col = heapq.heappop(pq)
        s = get_xs_for_one_color(col, colorMap, board)
        nEli = eliminate_cells(s, colorMap, board) #number of cells eliminated
        if nEli == 0:
            continue
        colorCount = get_color_count(colorMap)
        # print(colorCount)
        pq = []
        for c in colorCount:
            if colorCount[c]!=1 and c!=col:
                heapq.heappush(pq, (colorCount[c], c))
            else:
                s = get_xs_for_one_color(c, colorMap, board)
                eliminate_cells(s, colorMap, board)


def eliminate_by_contained_regions(colorMap, board):
    rows, cols = len(board), len(board[0])
    
    # Check for colors completely contained in rows
    for row_subset_size in range(1, rows + 1):
        for start_row in range(rows - row_subset_size + 1):
            end_row = start_row + row_subset_size
            # Get all colors in this row range
            colors_in_rows = set()
            for i in range(start_row, end_row):
                for j in range(cols):
                    colors_in_rows.add(board[i][j])
            
            # Find colors that are completely contained in these rows
            contained_colors = []
            for color in colors_in_rows:
                all_in_range = True
                for pos in colorMap[color]:
                    x, y = pos
                    if x < start_row or x >= end_row:
                        all_in_range = False
                        break
                if all_in_range and len(colorMap[color]) > 0:
                    contained_colors.append(color)
            
            # If x colors are contained in x rows, eliminate other colors from those rows
            if len(contained_colors) == row_subset_size and len(contained_colors) > 0:
                for i in range(start_row, end_row):
                    for j in range(cols):
                        color = board[i][j]
                        if color not in contained_colors:
                            if [i, j] in colorMap[color]:
                                if len(colorMap[color]) > 1:
                                    colorMap[color].remove([i, j])
    
    # Check for colors completely contained in columns
    for col_subset_size in range(1, cols + 1):
        for start_col in range(cols - col_subset_size + 1):
            end_col = start_col + col_subset_size
            # Get all colors in this column range
            colors_in_cols = set()
            for i in range(rows):
                for j in range(start_col, end_col):
                    colors_in_cols.add(board[i][j])
            
            # Find colors that are completely contained in these columns
            contained_colors = []
            for color in colors_in_cols:
                all_in_range = True
                for pos in colorMap[color]:
                    x, y = pos
                    if y < start_col or y >= end_col:
                        all_in_range = False
                        break
                if all_in_range and len(colorMap[color]) > 0:
                    contained_colors.append(color)
            
            # If x colors are contained in x columns, eliminate other colors from those columns
            if len(contained_colors) == col_subset_size and len(contained_colors) > 0:
                for i in range(rows):
                    for j in range(start_col, end_col):
                        color = board[i][j]
                        if color not in contained_colors:
                            if [i, j] in colorMap[color]:
                                if len(colorMap[color]) > 1:
                                    colorMap[color].remove([i, j])

def apply_line_complete_region_elimination(colorMap, board):
    rows, cols = len(board), len(board[0])
    for i in range(rows):
        row_colors = set()
        for j in range(cols):
            row_colors.add(board[i][j])
        if len(row_colors) == 1:
            col = row_colors.pop()
            for i1 in range(rows):
                if i1 == i:
                    continue
                for j1 in range(cols):
                    if col == board[i1][j1]:
                        if [i1, j1] in colorMap[col]:
                            colorMap[col].remove([i1, j1])
    for j in range(cols):
        col_colors = set()
        for i in range(rows):
            col_colors.add(board[i][j])
        if len(col_colors) == 1:
            col = col_colors.pop()
            for j1 in range(cols):
                if j1 == j:
                    continue
                for i1 in range(rows):
                    if col == board[i1][j1]:
                        if [i1, j1] in colorMap[col]:
                            colorMap[col].remove([i1, j1])

def apply_single_viable_cell_in_line(colorMap, board):
    rows, cols = len(board), len(board[0])
    drawboard = draw_color_map(colorMap, board, False)
    xcoords = {}
    ycoords = {}
    for color in colorMap:
        for pos in colorMap[color]:
            x, y = pos
            if x not in xcoords:
                xcoords[x] = []
            if y not in ycoords:
                ycoords[y] = []
            xcoords[x].append((color, pos))
            ycoords[y].append((color, pos))
    for x in xcoords:
        if len(xcoords[x]) == 1:
            color, pos = xcoords[x][0]
            colorMap[color] = [pos]
    for y in ycoords:
        if len(ycoords[y]) == 1:
            color, pos = ycoords[y][0]
            colorMap[color] = [pos]

def color_map_to_queens(color_map):
    queens = []

    for region, positions in color_map.items():
        for row, col in positions:
            queens.append({
                "row": int(row),
                "col": int(col),
                "region": region
            })

    return queens


def solve(board, printSteps=False):
    colorMap = get_color_map(board)
    if printSteps:
        draw_color_map(colorMap, board)
    apply_line_complete_region_elimination(colorMap, board)

    colorCount = sum(get_color_count(colorMap).values())

    while verify_board(colorMap, board) == False:
        apply_single_viable_cell_in_line(colorMap, board)
        eliminate_row_column_surrounding_cells_for_each_color(colorMap, board)
        eliminate_by_contained_regions(colorMap, board)
        
        if printSteps:
            draw_color_map(colorMap, board)

        newColorCount = sum(get_color_count(colorMap).values())
        if newColorCount == colorCount:
            print("No progress made, stopping to avoid infinite loop.")
            break

        colorCount = newColorCount

    if(verify_board(colorMap, board)):
        if printSteps:
            draw_color_map(colorMap, board)
            print("Solved Successfully!")
        return True, color_map_to_queens(colorMap)

    if printSteps:
        draw_color_map(colorMap, board)
    return False, 0


def solve_manually(board):
    
    colorMap = get_color_map(board)
    # print(colorMap)
    # xs = getXs(3,3, testBoard)
    # draw(xs, testBoard)
    s = get_xs_for_one_color('C2', colorMap, board)
    eliminate_cells(s, colorMap, board)
    s = get_xs_for_one_color('C3', colorMap, board)
    eliminate_cells(s, colorMap, board)
    s = get_xs_for_one_color('C1', colorMap, board)
    eliminate_cells(s, colorMap, board)
    s = get_xs_for_one_color('C4', colorMap, board)
    eliminate_cells(s, colorMap, board)
    s = get_xs_for_one_color('C1', colorMap, board)
    eliminate_cells(s, colorMap, board)
    s = get_xs_for_one_color('C6', colorMap, board)
    eliminate_cells(s, colorMap, board)
    s = get_xs_for_one_color('C5', colorMap, board)
    eliminate_cells(s, colorMap, board)
    s = get_xs_for_one_color('C6', colorMap, board)
    eliminate_cells(s, colorMap, board)
    s = get_xs_for_one_color('C2', colorMap, board)
    eliminate_cells(s, colorMap, board)
    draw_color_map(colorMap, board)

def main():
    # board = GameofCrownsBoardFetcher.gameofcrowns_get_board(8)#, rotate=True)
    # solve(board, printSteps=True)
    solve(testBoard2, printSteps=True)
    # solveManually(testBoard)

if __name__=="__main__":
    main()
