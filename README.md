## Overview
A real-time 3D Graphing calculator built using Python and ModernGL

<img width="1590" height="892" alt="Screenshot 2026-10-25 020539" src="https://github.com/user-attachments/assets/a2072542-57e3-4358-84be-72062544ac2c" />
<img width="1592" height="892" alt="Screenshot 2026-10-25 021514" src="https://github.com/user-attachments/assets/63028679-e1a2-49d4-8716-a5af25922398" />

## Features
- **Real-time 3D surface plotting:** Draws implicit surfaces `f(x, y, z) = 0` using the Marching Cubes algorithm on a 30 x 30 x 30 grid.
- **Built-in static graphs:** sphere, torus, gyroid.
- **Animated metaballs:** 2 to 20 blobs bounce inside the box and merge smoothly as they move.
- **Adjustable parameters:** Sliders control radius, major and minor radius, frequency and metaball count. The surface redraws when you release a slider.
- **Persistent saved graphs:** Save any graph under a custom name, then load or delete it later. Saved graphs are kept in a local SQLite file (`graphs.db`) and are still there after you restart.
- **Accessibility:** A six directional free-fly first person camera, a menu mode to change settings, and a X,Y,Z reference grid.

## Controls

| Input | Action |
|-------|--------|
|`W` / `S` | Move forward and backward |
|`A` / `D` | Move left and right |
|`Q` / `E` | Move up and down |
|`Space` | Switch between camera mode and menu mode (the mouse pointer appears for using the menu) |
|Mouse movement | Turn the camera (look around) |
|`G` | Show/hide the reference grid |
