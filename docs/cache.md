# Cache

## Cache API

```python
from sun.core import cache
# Usage example (API)
# Read cache 
cache.get(key)
# Set cache 
cache.set(key, value, timeout=10)
```

## cache memoize

```python
# Import the cache_memoize from sun core 
from sun.core import cache_memoize
# Attach decorator to cacheable function with a timeout of 100 seconds.
@cache_memoize(100)
def expensive_function(start, end):
    return random.randint(start, end)
```
