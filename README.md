# Crowns / Queens Puzzle Solver

A computer-vision and constraint-based solver for Crowns (Queens) logic puzzles.

The system takes a puzzle screenshot as input, reconstructs the grid and regions using OpenCV, solves the puzzle via constraint logic, and re-renders the board from scratch with queen placements using Canvas.

## Key Features

- 📸 Screenshot-based puzzle input
- 🔍 Automatic grid detection and cell segmentation
- 🎨 Region detection via color clustering
- 🧩 Constraint solver for queen placement
- 🎭 Clean board re-rendering (Canvas)
- 🏗️ Clear separation of vision, solver, and UI layers

## How It Works

1. Frontend uploads a puzzle screenshot
2. Backend extracts the grid using OpenCV
3. Cells are grouped into regions by color
4. Solver applies constraint rules
5. UI renders a clean puzzle board and queen positions

*The screenshot is used only as input.*

## Tech Stack

### Backend
- Python
- OpenCV
- NumPy
- FastAPI

### Frontend
- HTML
- JavaScript
- Canvas API

## Quick Start

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the web app:

```bash
cd WebApp/
uvicorn main:app --reload 
```

The application will be available in your browser. Upload a puzzle screenshot and click **Solve**.

3. (Optional) Run tests:

```bash
python Tester.py
```

## API Output (Simplified)

```json
{
  "cells": [
    [{ "region": 0, "color": [214, 181, 92] }]
  ],
  "queens": [
    { "row": 0, "col": 1, "region": "C1" }
  ]
}
```

- `cells` → UI-ready color grid
- `queens` → solved queen positions

## Project Structure

```
├── CoreSolver.py              # N-Queens constraint solver
├── ImageProcessing.py         # Grid detection & cell segmentation
├── GameofCrownsBoardFetcher.py # Board data fetching
├── Tester.py                  # Test suite
├── requirements.txt           # Python dependencies
├── images/                    # Sample puzzle screenshots
└── WebApp/
    ├── main.py                # Flask/FastAPI backend
    ├── index.html             # Web UI
    ├── app.js                 # Canvas rendering + API calls
    └── __init__.py
```

## Design Highlights

- **No screenshot overlays** → no alignment bugs
- **Separate color pipelines** for solver and UI
- **Deterministic rendering**
- **Canvas-based drawing** for precision

## Output
<img width="1509" height="1358" alt="image" src="https://github.com/user-attachments/assets/9cc5a786-fd52-47ee-b65c-c4323eff0dc7" />


## Limitations

- Requires a clear grid in the screenshot
- Similar region colors may need threshold tuning
- Square grids only (for now)

## Roadmap

- [ ] Step-by-step solver visualization
- [ ] Adding DFS to core solver as additional mechanism
- [ ] Export solved boards as images

## License

MIT


