
import os

__all__ = []
for f in os.listdir('systems'):
    if f.endswith('.py') and f != 'base_sys.py':
        __all__.append(f[:-3])
