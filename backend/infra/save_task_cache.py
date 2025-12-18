from collections import OrderedDict
import threading
from typing import Dict, Any
from .cache_service import task_cache, get_task_status as _get_task_status, update_tasks_cache as _update_tasks_cache, update_task_field as _update_task_field, update_task_fields as _update_task_fields, increment_task_field as _increment_task_field, create_task as _create_task

# Re-export singleton
DRAFT_TASKS = task_cache

def get_task_status(task_id: str) -> Dict[str, Any]:
    return _get_task_status(task_id)

def update_tasks_cache(task_id: str, task_status: dict) -> None:
    _update_tasks_cache(task_id, task_status)

def update_task_field(task_id: str, field: str, value: Any) -> None:
    _update_task_field(task_id, field, value)

def update_task_fields(task_id: str, **fields) -> None:
    _update_task_fields(task_id, fields)

def increment_task_field(task_id: str, field: str, increment: int = 1) -> None:
    _increment_task_field(task_id, field, increment)

def create_task(task_id: str) -> None:
    _create_task(task_id)

        else:
            task_status[field] = increment
        # Delete the old item and add the updated item
        DRAFT_TASKS.pop(task_id)
        DRAFT_TASKS[task_id] = task_status

def get_task_status(task_id: str) -> dict:
    """Get task status
    
    :param task_id: Task ID
    :return: Task status information dictionary
    """
    task_status = DRAFT_TASKS.get(task_id, {
        "status": "not_found",
        "message": "Task does not exist",
        "progress": 0,
        "completed_files": 0,
        "total_files": 0,
        "draft_url": ""
    })
    
    # If the task is found, update its position in the LRU cache
    if task_id in DRAFT_TASKS:
        # First delete, then add to the end, implementing LRU update
        update_tasks_cache(task_id, task_status)
        
    return task_status

def create_task(task_id: str) -> None:
    """Create a new task and initialize its status
    
    :param task_id: Task ID
    """
    task_status = {
        "status": "initialized",
        "message": "Task initialized",
        "progress": 0,
        "completed_files": 0,
        "total_files": 0,
        "draft_url": ""
    }
    update_tasks_cache(task_id, task_status)