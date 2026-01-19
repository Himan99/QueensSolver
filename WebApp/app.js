const fileInput = document.getElementById("fileInput");
const sendBtn = document.getElementById("sendBtn");
const canvas = document.getElementById("boardCanvas");
const ctx = canvas.getContext("2d");
const fileName = document.getElementById("fileName");
const pasteName = document.getElementById("pasteName");
const pasteArea = document.getElementById("pasteArea");
const status = document.getElementById("status");

let selectedFile = null;

fileInput.addEventListener("change", () => {
  selectedFile = fileInput.files[0];
  if (selectedFile) {
    fileName.textContent = selectedFile.name;
    pasteName.textContent = "";
    pasteArea.classList.remove("active");
    sendBtn.disabled = false;
  } else {
    fileName.textContent = "";
    sendBtn.disabled = selectedFile === null;
  }
});

// Paste area click to focus
pasteArea.addEventListener("click", () => {
  document.focus();
});

// Handle paste event
document.addEventListener("paste", (e) => {
  const items = e.clipboardData?.items;
  if (!items) return;

  for (let item of items) {
    if (item.kind === "file" && item.type.startsWith("image/")) {
      selectedFile = item.getAsFile();
      fileName.textContent = "";
      pasteName.textContent = "Image pasted ✓";
      pasteArea.classList.add("active");
      sendBtn.disabled = false;
      break;
    }
  }
});


// Send image to backend
sendBtn.addEventListener("click", async () => {
  if (!selectedFile) {
    setStatus("Select an image first", "error");
    return;
  }

  sendBtn.disabled = true;
  setStatus("Solving...", "loading");

  try {
    const formData = new FormData();
    formData.append("image", selectedFile);

    const response = await fetch("http://localhost:8000/solve", {
      method: "POST",
      body: formData
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    console.log("Backend response:", result);

    if (result.error) {
      setStatus(`Error: ${result.error}`, "error");
      return;
    }

    if (!result.cells) {
      setStatus("Invalid response from server", "error");
      console.error("Invalid backend response", result);
      return;
    }

    drawGrid(result.cells);
    if (result.queens) {
      drawQueens(result.queens);
    }

    setStatus(
      result.solved ? "✓ Solution found!" : "✗ No solution exists",
      result.solved ? "success" : "error"
    );
  } catch (error) {
    console.error("Error:", error);
    setStatus(`Error: ${error.message}`, "error");
  } finally {
    sendBtn.disabled = false;
  }
});

function setStatus(message, type = "") {
  status.textContent = message;
  status.className = "status " + type;
}

function drawGrid(uiGrid, cellSize = 70) {
  const rows = uiGrid.length;
  const cols = uiGrid[0].length;

  // Set canvas resolution for high DPI
  const dpr = window.devicePixelRatio || 1;
  canvas.width = cols * cellSize * dpr;
  canvas.height = rows * cellSize * dpr;
  canvas.style.width = cols * cellSize + "px";
  canvas.style.height = rows * cellSize + "px";
  ctx.scale(dpr, dpr);

  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      let [red, green, blue] = uiGrid[r][c].color;

      // Subtle desaturation for a softer look
      const brightness = (red + green + blue) / 3;
      const factor = 0.75;
      red = Math.round(red * factor + brightness * (1 - factor));
      green = Math.round(green * factor + brightness * (1 - factor));
      blue = Math.round(blue * factor + brightness * (1 - factor));

      // Lighten slightly
      red = Math.min(255, Math.round(red * 1.1));
      green = Math.min(255, Math.round(green * 1.1));
      blue = Math.min(255, Math.round(blue * 1.1));

      ctx.fillStyle = `rgb(${red},${green},${blue})`;
      ctx.fillRect(
        c * cellSize,
        r * cellSize,
        cellSize,
        cellSize
      );

      // Clear grid lines
      ctx.strokeStyle = "#666";
      ctx.lineWidth = 1.5;
      ctx.strokeRect(
        c * cellSize,
        r * cellSize,
        cellSize,
        cellSize
      );
    }
  }
}

function drawQueens(queens, cellSize = 70) {
  ctx.fillStyle = "#000";
  ctx.font = `${cellSize * 0.7}px Arial, sans-serif`;
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.shadowColor = "rgba(0, 0, 0, 0.15)";
  ctx.shadowBlur = 3;
  ctx.shadowOffsetX = 0;
  ctx.shadowOffsetY = 1;

  for (const q of queens) {
    const x = q.col * cellSize + cellSize / 2;
    const y = q.row * cellSize + cellSize / 2;
    ctx.fillText("🜲", x, y);
  }

  ctx.shadowColor = "transparent";
}
