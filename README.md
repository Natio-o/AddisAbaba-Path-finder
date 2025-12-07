# AddisAbaba-Path-finder

A Python-based pathfinding visualization tool for Addis Ababa, Ethiopia. This application uses various search algorithms to find optimal routes between city locations, considering distance, traffic, and elevation.

SECTION 2 
GROUP MEMBERS

1, Nathan Berhanu
2, Natnael tibebu
3, Yafet aklilu


## Features

- **Interactive Map**: Visualizes the city network and calculated paths using Matplotlib.
- **Multiple Algorithms**:
  - **A* Search**: Finds the optimal path using heuristics and costs.
  - **Greedy Best-First Search**: Prioritizes paths that appear closer to the destination.
  - **Hill Climbing**: Local search algorithm based on elevation and cost.
- **Real-world Constraints**:
  - **Traffic Analysis**: Considers traffic intensity for travel time estimation.
  - **Road Blocking**: Simulate blocked roads to find alternative routes.
  - **Elevation**: Accounts for terrain height in pathfinding.
- **User-Friendly Interface**: Built with Tkinter for easy interaction.

## Prerequisites

Ensure you have Python installed along with the following libraries:

```bash
pip install networkx matplotlib numpy pillow ttkthemes requests
```

*Note: `tkinter` is usually included with Python installations.*

## How to Run

1.  Clone the repository or download `AddisPath_search.py`.
2.  Run the script:

    ```bash
    python AddisPath_search.py
    ```

## Usage

1.  **Select City**: Currently supports "Addis Ababa".
2.  **Choose Locations**: Select your **Starting Point** and **Destination**.
3.  **Select Algorithm**: Choose between Hill Climbing, Greedy, or A*.
4.  **Set Constraints**:
    - Toggle **Time/Cost Optimization**.
    - Optionally specify a **Blocked Road** segment.
5.  **Find Path**: Click "Find Path" to visualize the route and view details.
6.  **Navigate**: If multiple paths are found, use "Previous Path" and "Next Path" to explore alternatives.
