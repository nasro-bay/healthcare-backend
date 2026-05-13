
# healthcare-navigation/search/base.py

from abc import ABC, abstractmethod

class BaseSearch(ABC):
    """
    Abstract base class for all search algorithms.
    """
    def __init__(self, problem):
        self.problem = problem

    @abstractmethod
    def search(self) -> list:
        """
        Executes the search and returns the path.
        Returns:
            list: A list of OSMID integers.
        """
        pass

def get_strategy_from_user():
    """
    Prompts the user to select a search strategy.
    """
    strategies = ["BFS", "DFS", "A_STAR", "Dijkstra"]
    print("\n" + "Select Search Strategy:".center(40))
    for i, s in enumerate(strategies):
        print(f"{i + 1}. {s}".center(40))
    
    while True:
        try:
            choice = int(input("\nEnter choice (1-4): "))
            if 1 <= choice <= len(strategies):
                return strategies[choice - 1]
            print(f"Please enter a number between 1 and {len(strategies)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")
