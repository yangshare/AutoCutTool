from collections import OrderedDict
import domain.pyJianYingDraft as draft
from typing import Dict
from .cache_service import draft_cache

# Backward compatibility using singleton instance
# We wrap it to behave like a dict for read access if needed, but the original code used DRAFT_CACHE[key] = value.
# The original code exposed DRAFT_CACHE as a Dict.
# Now we want to use the thread-safe service.
# Ideally we should update usages, but to support `from infra.draft_cache import DRAFT_CACHE`, we can point DRAFT_CACHE to the service's internal dict? 
# NO, that breaks thread safety.
# We must update the usages.
# But for now, let's just make this file re-export the new service methods.

DRAFT_CACHE = draft_cache  # This is an object now, not a dict. 
# Code using DRAFT_CACHE[key] will fail unless we implement __getitem__/__setitem__ on ThreadSafeCache.
# Let's check usages of DRAFT_CACHE.

def update_cache(key: str, value: draft.Script_file) -> None:
    """Update LRU cache"""
    draft_cache.put(key, value)
