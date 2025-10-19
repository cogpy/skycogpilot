"""OpenCog AGI infrastructure for SkyPilot.

This module provides artificial general intelligence capabilities to SkyPilot
using the OpenCog Hyperon framework for enhanced task optimization,
intelligent scheduling, and autonomous workload management.
"""

# Import only the core functionality to avoid dependency issues
try:
    from sky.agi.core import AGIEngine, get_agi_engine
    AGI_CORE_AVAILABLE = True
except ImportError:
    AGI_CORE_AVAILABLE = False
    AGIEngine = None
    get_agi_engine = None

# Lazy imports for other components to avoid circular dependencies
def get_agi_optimizer():
    """Get AGI optimizer (lazy import)."""
    try:
        from sky.agi.optimizer import AGIOptimizer
        return AGIOptimizer
    except ImportError:
        return None

def get_agi_scheduler():
    """Get AGI scheduler (lazy import)."""
    try:
        from sky.agi.scheduler import AGIScheduler, get_agi_scheduler
        return get_agi_scheduler()
    except ImportError:
        return None

__all__ = [
    'AGIEngine',
    'get_agi_engine',
    'get_agi_optimizer', 
    'get_agi_scheduler',
]