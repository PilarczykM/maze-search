from abc import ABC, abstractmethod

from src.node import Node, State


class EmptyFrontierError(Exception):
    """Exception raised when attempting to remove a node from an empty frontier."""

    def __init__(self, message: str = "Cannot remove from an empty frontier.") -> None:
        """Initialize error."""
        super().__init__(message)


class Frontier(ABC):
    """Abstract base class representing a frontier in a search algorithm.

    A frontier is a collection of nodes that are available for exploration
    during the search process. This class defines the common interface that
    all frontier implementations must adhere to.
    """

    def __init__(self) -> None:
        """Initialize the frontier.

        Creates an empty list to store nodes that are part of the frontier.
        """
        self._frontier: list[Node] = []

    @abstractmethod
    def add(self, node: Node) -> None:
        """Add a node to the frontier.

        Parameters
        ----------
        node : Node
            The node to be added to the frontier.
        """
        self._frontier.append(node)

    @abstractmethod
    def is_empty(self, state: State) -> bool:
        """Check if the frontier is empty.

        Returns
        -------
        bool
            True if the frontier contains no nodes; otherwise, False.
        """
        return len(self._frontier) == 0

    @abstractmethod
    def contains_state(self, state: State) -> bool:
        """Check if a state is in the frontier.

        Parameters
        ----------
        state : StateType
            The state to be checked.

        Returns
        -------
        bool
            True if the state is in the frontier; otherwise, False.
        """
        return any(node.state == state for node in self._frontier)

    @abstractmethod
    def remove(self) -> Node:
        """Remove and returns the next node from the frontier.

        Returns
        -------
        Node
            The next node to be explored.

        Raises
        ------
        EmptyFrontierError
            If the frontier is empty when trying to remove a node.
        """
        pass


class StackFrontier(Frontier):
    """Stack frontier implementation representing a frontier in a search algorithm."""

    def remove(self) -> Node:
        """Stack remove implementation.

        Returns
        -------
        Node
            The next node to be explored.

        Raises
        ------
        EmptyFrontierError
            If the frontier is empty when trying to remove a node.
        """
        if self.empty():
            raise EmptyFrontierError()

        node = self._frontier[-1]
        self._frontier = self._frontier[:-1]
        return node


class QueueFrontier(Frontier):
    """Queue frontier implementation representing a frontier in a search algorithm."""

    def remove(self) -> Node:
        """Stack remove implementation.

        Returns
        -------
        Node
            The next node to be explored.

        Raises
        ------
        EmptyFrontierError
            If the frontier is empty when trying to remove a node.
        """
        if self.empty():
            raise EmptyFrontierError()

        node = self._frontier[0]
        self._frontier = self._frontier[1:]
        return node
