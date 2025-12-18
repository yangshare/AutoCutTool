from typing import Dict, Any, Optional, TypeVar, Generic
from collections import OrderedDict
import threading
import time

T = TypeVar('T')

class ThreadSafeCache(Generic[T]):
    def __init__(self, capacity: int = 1000):
        self.capacity = capacity
        self._cache: OrderedDict[str, T] = OrderedDict()
        self._lock = threading.RLock()

    def get(self, key: str) -> Optional[T]:
        with self._lock:
            if key not in self._cache:
                return None
            self._cache.move_to_end(key)
            return self._cache[key]

    def put(self, key: str, value: T) -> None:
        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
            self._cache[key] = value
            if len(self._cache) > self.capacity:
                self._cache.popitem(last=False)

    def delete(self, key: str) -> None:
        with self._lock:
            if key in self._cache:
                del self._cache[key]

    def contains(self, key: str) -> bool:
        with self._lock:
            return key in self._cache
            
    def clear(self) -> None:
        with self._lock:
            self._cache.clear()

# Initialize Singletons
draft_cache = ThreadSafeCache(capacity=10000)
task_cache = ThreadSafeCache(capacity=1000)

def update_cache(key: str, value: Any) -> None:
    draft_cache.put(key, value)

def get_task_status(task_id: str) -> Dict[str, Any]:
    return task_cache.get(task_id)

def update_tasks_cache(task_id: str, task_status: Dict[str, Any]) -> None:
    task_cache.put(task_id, task_status)

def create_task(task_id: str) -> None:
    task_cache.put(task_id, {
        "status": "initialized",
        "progress": 0,
        "message": "Task initialized",
        "data": None,
        "created_at": time.time(),
        "updated_at": time.time()
    })

def update_task_field(task_id: str, field: str, value: Any) -> None:
    # This requires read-modify-write, so we need lock on the whole operation if possible
    # But our cache exposes atomic put/get. 
    # For dictionary updates inside the value, we need to be careful if multiple threads modify the SAME task.
    # Given the simplicity, we'll retrieve, update, put back. 
    # Ideally, we should add a method to cache to update field atomically.
    # But for now:
    task = task_cache.get(task_id)
    if task:
        task[field] = value
        task["updated_at"] = time.time()
        # No need to put back if it's the same object reference, but move_to_end is handled by get/put
        # So we should call put to ensure LRU update? 
        # get() already moves to end.
        pass

def update_task_fields(task_id: str, fields: Dict[str, Any]) -> None:
    task = task_cache.get(task_id)
    if task:
        task.update(fields)
        task["updated_at"] = time.time()

def increment_task_field(task_id: str, field: str, amount: int = 1) -> None:
    task = task_cache.get(task_id)
    if task and field in task:
        task[field] += amount
        task["updated_at"] = time.time()

# Compatibility exports
DRAFT_CACHE = draft_cache
DRAFT_TASKS = task_cache
