### Тема 18
### Cursor Ai
При помощи этой программы был создана web игра "Жизнь" основанная на клеточных автоматах.

### Промт к ИИ
```
Create a web-based project using **pandas-js** (JavaScript implementation of pandas) that allows users to simulate two cellular automata:
1. **Conway's Game of Life**
2. **Maze Generation Cellular Automaton**

### Requirements:
1. **User Interface**:
   - A dropdown/buttons to switch between "Conway's Game of Life" and "Maze" automata.
   - Canvas for rendering the automaton grid (size: 50x50 cells).
   - Control buttons: "Start", "Pause", "Reset", and "Step".
   - Display current automaton type prominently.

2. **Core Functionality**:
   - **Conway's Game of Life Rules**:
     - Any live cell with < 2 neighbors dies (underpopulation).
     - Any live cell with 2-3 neighbors survives.
     - Any live cell with > 3 neighbors dies (overpopulation).
     - Any dead cell with exactly 3 neighbors becomes alive (reproduction).
   - **Maze Automaton Rules**:
     - Cells can be walls (`1`) or paths (`0`).
     - Initial state: Random grid with 45% walls.
     - Evolution rule: 
       ```js
       if (aliveNeighbors >= 4) cell = 1; // Wall survives/forms
       else cell = 0; // Path forms
       ```

3. **Technical Implementation**:
   - Use `pandas-js` (`npm: pandas-js`) to:
     - Store grid state as a `DataFrame`.
     - Apply automaton rules using vectorized operations where possible.
   - Use `Canvas API` for rendering.
   - Simulation loop with configurable speed (use `requestAnimationFrame`).

4. **Code Structure**:
   - `index.html`: Basic structure with canvas/controls.
   - `main.js`:
     - Initialize pandas-js DataFrame for grid state.
     - Implement automaton rule logic using DataFrame operations.
     - Handle simulation loop and user interactions.
     - Render grid to canvas (1 cell = 10x10 px).
   - `styles.css`: Minimal styling for clarity.

5. **Dependencies**:
   - Include `pandas-js` via CDN: 
     ```html
     <script src="https://cdn.jsdelivr.net/npm/pandas-js@0.3.1/dist/index.min.js"></script>
     ```

### Example Code Snippets (for guidance):
1. **Initialize DataFrame Grid**:
   ```javascript
   const { DataFrame } = pandasjs;
   let grid = new DataFrame(Array(50).fill(0).map(() => 
     Array(50).fill(0).map(() => Math.random() > 0.5 ? 1 : 0)
   ));
```