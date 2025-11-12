"""
A* Priority Queue for ranking traffic objects by urgency.
Objects are ranked by: f(n) = distance + time_to_arrival + biases
"""

import heapq
from typing import Any, List, Optional


class AStarPriorityQueue:
    """
    Min-heap based priority queue for A* algorithm.
    Lower priority = higher urgency (popped first)
    """
    
    def __init__(self) -> None:
        self._queue: List[tuple] = []
        self._counter: int = 0
    
    def push(self, priority: float, obj: Any) -> None:
        """Push object with priority"""
        heapq.heappush(self._queue, (priority, self._counter, obj))
        self._counter += 1
    
    def pop(self) -> Optional[Any]:
        """Pop and return most urgent object"""
        if not self._queue:
            return None
        _, _, obj = heapq.heappop(self._queue)
        return obj
    
    def pop_all(self, k: Optional[int] = None) -> List[Any]:
        """Pop top-k objects"""
        result = []
        max_k = min(k or len(self._queue), len(self._queue))
        for _ in range(max_k):
            obj = self.pop()
            if obj is not None:
                result.append(obj)
        return result
    
    def peek(self) -> Optional[Any]:
        """Peek at most urgent object without removing"""
        if not self._queue:
            return None
        return self._queue[0][2]
    
    def clear(self) -> None:
        """Clear queue"""
        self._queue.clear()
        self._counter = 0
    
    def is_empty(self) -> bool:
        """Check if queue is empty"""
        return len(self._queue) == 0
    
    def size(self) -> int:
        """Return queue size"""
        return len(self._queue)
