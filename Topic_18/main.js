// Constants
const GRID_SIZE = 50;
const CELL_SIZE = 10;
const WALL_PROB = 0.45;

const { DataFrame } = pandasjs;

// State
let automatonType = 'life';
let running = false;
let animationFrame = null;
let grid = null;

// DOM
const canvas = document.getElementById('automaton-canvas');
const ctx = canvas.getContext('2d');
const automatonSelect = document.getElementById('automaton-select');
const currentAutomaton = document.getElementById('current-automaton');
const startBtn = document.getElementById('start-btn');
const pauseBtn = document.getElementById('pause-btn');
const resetBtn = document.getElementById('reset-btn');
const stepBtn = document.getElementById('step-btn');

// Helpers
function randomGrid(type) {
  if (type === 'life') {
    return new DataFrame(Array(GRID_SIZE).fill(0).map(() =>
      Array(GRID_SIZE).fill(0).map(() => Math.random() > 0.5 ? 1 : 0)
    ));
  } else if (type === 'maze') {
    return new DataFrame(Array(GRID_SIZE).fill(0).map(() =>
      Array(GRID_SIZE).fill(0).map(() => Math.random() < WALL_PROB ? 1 : 0)
    ));
  }
}

function drawGrid(df) {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  for (let r = 0; r < GRID_SIZE; r++) {
    for (let c = 0; c < GRID_SIZE; c++) {
      let val = df.iloc(r, c);
      if (automatonType === 'life') {
        ctx.fillStyle = val ? '#222' : '#fafafa';
      } else {
        ctx.fillStyle = val ? '#222' : '#fafafa';
      }
      ctx.fillRect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE);
    }
  }
}

function countNeighbors(df, r, c) {
  let count = 0;
  for (let dr = -1; dr <= 1; dr++) {
    for (let dc = -1; dc <= 1; dc++) {
      if (dr === 0 && dc === 0) continue;
      let nr = r + dr;
      let nc = c + dc;
      if (nr >= 0 && nr < GRID_SIZE && nc >= 0 && nc < GRID_SIZE) {
        count += df.iloc(nr, nc);
      }
    }
  }
  return count;
}

function stepLife(df) {
  let next = df.copy();
  for (let r = 0; r < GRID_SIZE; r++) {
    for (let c = 0; c < GRID_SIZE; c++) {
      let neighbors = countNeighbors(df, r, c);
      let cell = df.iloc(r, c);
      if (cell) {
        if (neighbors < 2 || neighbors > 3) next.iat(r, c, 0);
        else next.iat(r, c, 1);
      } else {
        if (neighbors === 3) next.iat(r, c, 1);
        else next.iat(r, c, 0);
      }
    }
  }
  return next;
}

function stepMaze(df) {
  let next = df.copy();
  for (let r = 0; r < GRID_SIZE; r++) {
    for (let c = 0; c < GRID_SIZE; c++) {
      let neighbors = countNeighbors(df, r, c);
      if (neighbors >= 4) next.iat(r, c, 1);
      else next.iat(r, c, 0);
    }
  }
  return next;
}

function stepAutomaton() {
  if (automatonType === 'life') {
    grid = stepLife(grid);
  } else if (automatonType === 'maze') {
    grid = stepMaze(grid);
  }
  drawGrid(grid);
}

function loop() {
  if (running) {
    stepAutomaton();
    animationFrame = requestAnimationFrame(loop);
  }
}

function start() {
  if (!running) {
    running = true;
    animationFrame = requestAnimationFrame(loop);
  }
}

function pause() {
  running = false;
  if (animationFrame) cancelAnimationFrame(animationFrame);
}

function reset() {
  pause();
  grid = randomGrid(automatonType);
  drawGrid(grid);
}

function step() {
  pause();
  stepAutomaton();
}

// UI Event Listeners
automatonSelect.addEventListener('change', (e) => {
  automatonType = e.target.value;
  currentAutomaton.textContent = automatonType === 'life' ? "Conway's Game of Life" : 'Maze Generation';
  reset();
});

startBtn.addEventListener('click', start);
pauseBtn.addEventListener('click', pause);
resetBtn.addEventListener('click', reset);
stepBtn.addEventListener('click', step);

// Canvas click to toggle cell
canvas.addEventListener('click', (e) => {
  const rect = canvas.getBoundingClientRect();
  const x = e.clientX - rect.left;
  const y = e.clientY - rect.top;
  const c = Math.floor(x / CELL_SIZE);
  const r = Math.floor(y / CELL_SIZE);
  if (r >= 0 && r < GRID_SIZE && c >= 0 && c < GRID_SIZE) {
    let val = grid.iloc(r, c);
    grid.iat(r, c, val ? 0 : 1);
    drawGrid(grid);
  }
});

// Init
grid = randomGrid(automatonType);
drawGrid(grid); 