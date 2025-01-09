from typing import Optional

State = tuple[int, int]
Action = str


class Node:
    """Represents a node in a state-space tree for problem-solving.

    Each node tracks the current state, the action that led to this state,
    and a reference to its parent node.
    """

    def __init__(self, state: State, parent: Optional["Node"], action: Optional[Action]) -> None:
        """Initialize a Node instance.

        Parameters
        ----------
        state : State
            The current state represented as a tuple of integers (e.g., (row, col)).
        parent: Optional[Node]
            The parent node that generated this node, or None if this is the root node.
        action: Action
            The action that was applied to the parent node to reach this state,
            represented as a tuple (direction, (row_delta, col_delta)).
        """
        self.state = state
        self.parent = parent
        self.action = action
