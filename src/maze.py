from pathlib import Path
from typing import Optional

import PIL.Image
from PIL.ImageDraw import ImageDraw

from frontier import Frontier, State
from node import Node


class InvalidMazeError(Exception):
    """Exception raised when a maze is missing a start or goal point."""

    def __init__(self, message: str) -> None:
        """Initialize the InvalidMazeError."""
        super().__init__(message)


class SolutionNotFoundError(Exception):
    """Exception raised when a maze has no solution."""

    def __init__(self, message: str = "no solution") -> None:
        """Initialize the SolutionNotFoundError."""
        super().__init__(message)


class Maze:
    """Maze class."""

    def __init__(self, file: Path) -> None:
        """Initialize the maze.

        Parameters
        ----------
        file : Path
            The file containing maze.
        """
        # Initialize maze variables
        self._solution: Optional[tuple[list, list]] = None
        self._height: int
        self._width: int
        self.num_explored: int = 0
        self._explored = set()
        self._walls: list[list[bool]] = []

        # Read file and set content
        with file.open() as f:
            contents = f.read()

        # Validate start and goal
        if contents.count("A") != 1:
            err_msg = "Maze must have exactly one start point"
            raise InvalidMazeError(err_msg)
        if contents.count("B") != 1:
            err_msg = "Maze must have exactly one goal"
            raise InvalidMazeError(err_msg)

        # Determine height and width of maze
        contents = contents.splitlines()
        self._height = len(contents)
        self._width = max(len(line) for line in contents)

        # Keep track of walls
        self._walls = []
        for i in range(self._height):
            row = []
            for j in range(self._width):
                try:
                    cell = contents[i][j]
                    if cell == "A":
                        self._start = (i, j)
                        row.append(False)
                    elif cell == "B":
                        self._goal = (i, j)
                        row.append(False)
                    elif cell == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:  # noqa: PERF203, RUF100
                    row.append(False)
            self._walls.append(row)

    def print(self) -> None:
        """Print maze to console."""
        solution = self._solution[1] if self._solution is not None else None
        print()
        for i, row in enumerate(self._walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == self._start:
                    print("A", end="")
                elif (i, j) == self._goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()

    def neighbors(self, state: State) -> list[tuple[str, tuple[int, int]]]:
        """Find all valid neighbors of a given state.

        Parameters
        ----------
        state : State
            The current state, represented as a tuple (row, col).

        Returns
        -------
        list[tuple[str, tuple[int, int]]]
            A list of tuples, where each tuple contains:
            - A string representing the action ("up", "down", "left", "right").
            - A tuple representing the neighbor's state (row, col).
        """
        row, col = state
        candidates: list[tuple[str, tuple[int, int]]] = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1)),
        ]

        result: list[tuple[str, tuple[int, int]]] = []
        for action, (new_row, new_col) in candidates:
            if 0 <= new_row < self._height and 0 <= new_col < self._width and not self._walls[new_row][new_col]:
                result.append((action, (new_row, new_col)))

        return result

    def solve(self, frontier: Frontier) -> None:
        """Solve the maze.

        Parameters
        ----------
        frontier: Frontier
            Implementation of abstract base class representing a frontier in a search algorithm.
        """
        # Keep track of number of states explored
        self.num_explored = 0

        # Initialize the frontier to just a starting point
        start = Node(state=self._start, parent=None, action=None)
        frontier.add(start)

        # Initialize an empty explored set
        self._explored = set()

        # Keep looping until solution found
        while True:
            # If nothing left in frontier then no path
            if frontier.is_empty():
                raise SolutionNotFoundError()

            # Chose the node from frontier
            node = frontier.remove()
            self.num_explored += 1

            # If node is the goal, then we have solution
            if node.state == self._goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent

                actions.reverse()
                cells.reverse()
                self._solution = (actions, cells)
                return

            # Mark node as explored
            self._explored.add(node.state)

            # Add neighbors to frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self._explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)

    def output_image(self, filename: Path, show_solution: bool=True, show_explored: bool=False):
        cell_size = 50
        cell_border = 2

        if not filename.parent.exists():
            filename.parent.mkdir(parents=True)

        # Create a blank canvas
        img = PIL.Image.new(
            "RGBA",
            (self._width * cell_size, self._height * cell_size),
            "black"
        )
        draw = PIL.ImageDraw.Draw(img)

        solution = self._solution[1] if self._solution is not None else None
        for i, row in enumerate(self._walls):
            for j, col in enumerate(row):

                # Walls
                if col:
                    fill = (40, 40, 40)

                # Start
                elif (i, j) == self._start:
                    fill = (255, 0, 0)

                # Goal
                elif (i, j) == self._goal:
                    fill = (0, 171, 28)

                # Solution
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)

                # Explored
                elif solution is not None and show_explored and (i, j) in self._explored:
                    fill = (212, 97, 85)

                # Empty cell
                else:
                    fill = (237, 240, 252)

                # Draw cell
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )

        img.save(filename)