import cv2
import numpy as np
from typing import List, Tuple
import os


def load_and_preprocess_image_from_bytes(contents):
    np_img = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
    
    if img is None:
        return None, None
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
    thresh = cv2.adaptiveThreshold(
        blur,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY_INV,
        11,
        2
    )
    
    return img, thresh


def load_and_preprocess_image_from_path(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    thresh = cv2.adaptiveThreshold(
        blur,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY_INV,
        11,
        2
    )

    return img, thresh

def extract_grid_lines(thresh):
    h_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
    v_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))

    horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, h_kernel)
    vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, v_kernel)

    return horizontal, vertical

def get_intersections(horizontal, vertical):
    intersections = cv2.bitwise_and(horizontal, vertical)
    coords = cv2.findNonZero(intersections)
    return coords.reshape(-1, 2)

def cluster_points(points, tolerance=10):
    points = sorted(points)
    clusters = [[points[0]]]

    for p in points[1:]:
        if abs(p - clusters[-1][-1]) <= tolerance:
            clusters[-1].append(p)
        else:
            clusters.append([p])

    return [int(np.mean(c)) for c in clusters]

def build_grid(intersections):
    xs = intersections[:, 0]
    ys = intersections[:, 1]

    cols = cluster_points(sorted(xs))
    rows = cluster_points(sorted(ys))

    return rows, cols
def extract_cells(image, rows, cols):
    cells = []
    for r in range(len(rows) - 1):
        row_cells = []
        for c in range(len(cols) - 1):
            cell = image[
                rows[r]:rows[r + 1],
                cols[c]:cols[c + 1]
            ]
            row_cells.append(cell)
        cells.append(row_cells)

    return cells

def build_logical_grid(cells):
    rows = len(cells)
    cols = len(cells[0])

    grid = [[{"row": r, "col": c, "image": cells[r][c]}
             for c in range(cols)]
            for r in range(rows)]

    return grid

def cell_mean_color(cell, margin_ratio=0.2):
    h, w, _ = cell.shape
    mh = int(h * margin_ratio)
    mw = int(w * margin_ratio)

    core = cell[mh:h-mh, mw:w-mw]
    lab = cv2.cvtColor(core, cv2.COLOR_BGR2LAB)

    return lab.mean(axis=(0, 1))

def extract_cell_colors(cells):
    rows = len(cells)
    cols = len(cells[0])

    colors = np.zeros((rows, cols, 3), dtype=np.float32)

    for r in range(rows):
        for c in range(cols):
            colors[r, c] = cell_mean_color(cells[r][c])

    return colors

def cluster_colors(color_matrix, threshold=12.0):
    rows, cols, _ = color_matrix.shape

    region_ids = -np.ones((rows, cols), dtype=int)
    cell_colors = np.zeros((rows, cols, 3), dtype=np.float32)

    region_colors = []
    current_region = 0

    for r in range(rows):
        for c in range(cols):
            color = color_matrix[r, c]

            assigned_region = None
            for idx, ref_color in enumerate(region_colors):
                if np.linalg.norm(color - ref_color) < threshold:
                    assigned_region = idx
                    break

            if assigned_region is None:
                region_colors.append(color)
                assigned_region = current_region
                current_region += 1

            region_ids[r, c] = assigned_region
            cell_colors[r, c] = region_colors[assigned_region]

    return region_ids

def format_region_matrix(region_ids):
    return [
        [f"C{region_ids[r, c] + 1}" for c in range(region_ids.shape[1])]
        for r in range(region_ids.shape[0])
    ]

def generate_color_map(region_matrix, seed=42):
    np.random.seed(seed)

    regions = sorted({cell for row in region_matrix for cell in row})
    color_map = {}

    for r in regions:
        color_map[r] = tuple(np.random.randint(40, 220, size=3).tolist())

    return color_map


def group_regions_by_color(cells):
    color_matrix = extract_cell_colors(cells)
    region_ids = cluster_colors(color_matrix)
    return format_region_matrix(region_ids)

def generate_color_map(region_matrix, seed=42):
    np.random.seed(seed)

    regions = sorted({cell for row in region_matrix for cell in row})
    color_map = {}

    for r in regions:
        color_map[r] = tuple(np.random.randint(40, 220, size=3).tolist())

    return color_map

def grid_to_color_image(region_matrix, cell_size=50):
    rows = len(region_matrix)
    cols = len(region_matrix[0])

    color_map = generate_color_map(region_matrix)

    img = np.zeros((rows * cell_size, cols * cell_size, 3), dtype=np.uint8)

    for r in range(rows):
        for c in range(cols):
            color = color_map[region_matrix[r][c]]

            y1 = r * cell_size
            y2 = (r + 1) * cell_size
            x1 = c * cell_size
            x2 = (c + 1) * cell_size

            img[y1:y2, x1:x2] = color

    return img

def draw_grid_lines(img, cell_size, thickness=1):
    h, w, _ = img.shape

    for y in range(0, h, cell_size):
        cv2.line(img, (0, y), (w, y), (0, 0, 0), thickness)

    for x in range(0, w, cell_size):
        cv2.line(img, (x, 0), (x, h), (0, 0, 0), thickness)

    return img

def cell_mean_bgr(cell, margin_ratio=0.2):
    h, w, _ = cell.shape
    mh = int(h * margin_ratio)
    mw = int(w * margin_ratio)

    core = cell[mh:h-mh, mw:w-mw]
    return core.mean(axis=(0, 1))

def cluster_cells_bgr(cells, threshold=25.0):
    rows = len(cells)
    cols = len(cells[0])

    region_ids = -np.ones((rows, cols), dtype=int)
    region_colors = []

    current_region = 0

    for r in range(rows):
        for c in range(cols):
            bgr = cell_mean_bgr(cells[r][c])

            assigned = None
            for i, ref in enumerate(region_colors):
                if np.linalg.norm(bgr - ref) < threshold:
                    assigned = i
                    break

            if assigned is None:
                region_colors.append(bgr)
                assigned = current_region
                current_region += 1

            region_ids[r, c] = assigned

    return region_ids, region_colors

def build_ui_grid_from_bgr(region_ids, region_colors):
    rows, cols = region_ids.shape
    ui_grid = []

    for r in range(rows):
        row = []
        for c in range(cols):
            bgr = region_colors[region_ids[r, c]]
            rgb = [int(bgr[2]), int(bgr[1]), int(bgr[0])]

            row.append({
                "region": int(region_ids[r, c]),
                "color": rgb
            })
        ui_grid.append(row)

    return ui_grid


def generate_ui_grid_from_image(cells):
    region_ids, region_colors = cluster_cells_bgr(cells)
    return build_ui_grid_from_bgr(region_ids, region_colors)



def create_board_from_image(contents):
    img, thresh = load_and_preprocess_image_from_bytes(contents)

    horizontal, vertical = extract_grid_lines(thresh)
    intersections = get_intersections(horizontal, vertical)

    rows, cols = build_grid(intersections)
    cells = extract_cells(img, rows, cols)
    regions = group_regions_by_color(cells)
    return regions, cells


if __name__ == "__main__":
    img, thresh = load_and_preprocess_image_from_path("image2.png")

    horizontal, vertical = extract_grid_lines(thresh)
    intersections = get_intersections(horizontal, vertical)

    rows, cols = build_grid(intersections)
    cells = extract_cells(img, rows, cols)
    regions = group_regions_by_color(cells)

    for row in regions:
        print(row,',')

    
    img = grid_to_color_image(regions, cell_size=60)
    img = draw_grid_lines(img, cell_size=60)

    cv2.imwrite("regions.png", img)
