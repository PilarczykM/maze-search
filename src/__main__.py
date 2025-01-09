import sys
from pathlib import Path

from frontier import QueueFrontier, StackFrontier
from maze import Maze


def main(maze_file: Path) -> None:
    """Bootstrap the maze."""
    frontier = StackFrontier()
    frontier = QueueFrontier()
    maze = Maze(maze_file)

    print("Maze:")
    maze.print()
    print("Solving...")
    maze.solve(frontier)
    print("States explored: ", maze.num_explored)
    print("Solution:")
    maze.print()
    current_directory = Path(__file__).parent
    maze.output_image(current_directory / ".." / Path("images/maze.png"), show_explored=True)


if __name__ == "__main__":
    num_args = 2
    if len(sys.argv) != num_args:
        pass
        sys.exit("Usage: python maze.py maze.txt")

    path = Path(sys.argv[1])
    main(path)
