from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import CoreSolver
import ImageProcessing

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/solve")
async def solve(image: UploadFile = File(...)):
    contents = await image.read()

    board, cells = ImageProcessing.create_board_from_image(contents)
    ui_grid = ImageProcessing.generate_ui_grid_from_image(cells)
    # for row in board:
    #     print(row)

    result, queens = CoreSolver.solve(board, printSteps=False)
    print("Solved:", result)
    np_img = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    if img is None:
        return {"error": "Invalid image"}

    h, w, _ = img.shape

    # Placeholder: plug vision + solver here
    return {
        "status": "image received",
        "width": w,
        "height": h,
        "cells": ui_grid,
        "queens": queens,
        "solved": result
    }
