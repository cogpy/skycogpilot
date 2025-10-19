"""Configuration for OpenCog AGI integration in SkyPilot."""
import os
from typing import Dict, Any, Optional

from sky.utils import config_utils


# AGI configuration keys
AGI_CONFIG_KEYS = {
    'agi_enabled': bool,
    'agi_optimization_level': str,
    'agi_cost_weight': float,
    'agi_performance_weight': float,
    'agi_reliability_weight': float,
    'agi_confidence_threshold': float,
    'agi_fallback_mode': str,
}

# Default AGI configuration
DEFAULT_AGI_CONFIG = {
    'agi_enabled': True,
    'agi_optimization_level': 'medium',  # low, medium, high
    'agi_cost_weight': 0.6,
    'agi_performance_weight': 0.3,
    'agi_reliability_weight': 0.1,
    'agi_confidence_threshold': 0.7,
    'agi_fallback_mode': 'conservative',  # conservative, aggressive
}


def get_agi_config() -> Dict[str, Any]:
    """Get AGI configuration from SkyPilot config.
    
    Returns:
        Dictionary with AGI configuration settings
    """
    try:
        skypilot_config = config_utils.get_config()
        agi_config = skypilot_config.get('agi', {})
        
        # Merge with defaults
        config = DEFAULT_AGI_CONFIG.copy()
        config.update(agi_config)
        
        # Validate configuration
        config = _validate_agi_config(config)
        
        return config
    except Exception:
        # Fallback to defaults if config reading fails
        return DEFAULT_AGI_CONFIG.copy()


def _validate_agi_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """Validate AGI configuration values."""
    validated = {}
    
    for key, expected_type in AGI_CONFIG_KEYS.items():
        value = config.get(key, DEFAULT_AGI_CONFIG[key])
        
        if expected_type == bool:
            validated[key] = bool(value)
        elif expected_type == str:
            validated[key] = str(value)
        elif expected_type == float:
            try:
                validated[key] = float(value)
            except (ValueError, TypeError):
                validated[key] = DEFAULT_AGI_CONFIG[key]
    
    # Validate specific constraints
    if validated['agi_optimization_level'] not in ['low', 'medium', 'high']:
        validated['agi_optimization_level'] = 'medium'
    
    if validated['agi_fallback_mode'] not in ['conservative', 'aggressive']:
        validated['agi_fallback_mode'] = 'conservative'
    
    # Ensure weights sum to approximately 1.0
    total_weight = (validated['agi_cost_weight'] + 
                   validated['agi_performance_weight'] + 
                   validated['agi_reliability_weight'])
    
    if abs(total_weight - 1.0) > 0.1:
        # Normalize weights
        validated['agi_cost_weight'] = DEFAULT_AGI_CONFIG['agi_cost_weight']
        validated['agi_performance_weight'] = DEFAULT_AGI_CONFIG['agi_performance_weight']
        validated['agi_reliability_weight'] = DEFAULT_AGI_CONFIG['agi_reliability_weight']
    
    # Clamp confidence threshold
    validated['agi_confidence_threshold'] = max(0.1, min(0.95, validated['agi_confidence_threshold']))
    
    return validated


def is_agi_enabled() -> bool:
    """Check if AGI features are enabled."""
    config = get_agi_config()
    return config.get('agi_enabled', True) and _check_agi_dependencies()


def _check_agi_dependencies() -> bool:
    """Check if AGI dependencies are available."""
    try:
        import hyperon
        return True
    except ImportError:
        return False


def get_agi_optimization_level() -> str:
    """Get the AGI optimization level setting."""
    config = get_agi_config()
    return config.get('agi_optimization_level', 'medium')


def should_use_agi_for_task(task_complexity: str = 'medium') -> bool:
    """Determine if AGI should be used for a given task complexity.
    
    Args:
        task_complexity: Task complexity level ('low', 'medium', 'high')
        
    Returns:
        True if AGI should be used for this task
    """
    if not is_agi_enabled():
        return False
    
    optimization_level = get_agi_optimization_level()
    
    if optimization_level == 'high':
        return True
    elif optimization_level == 'medium':
        return task_complexity in ['medium', 'high']
    elif optimization_level == 'low':
        return task_complexity == 'high'
    
    return False


def get_example_agi_config() -> str:
    """Get an example AGI configuration for documentation.
    
    Returns:
        YAML string with example AGI configuration
    """
    return """
# OpenCog AGI Configuration for SkyPilot
agi:
  # Enable/disable AGI features
  agi_enabled: true
  
  # AGI optimization level: low, medium, high
  # - low: Use AGI only for complex tasks
  # - medium: Use AGI for medium and complex tasks (default)
  # - high: Use AGI for all tasks
  agi_optimization_level: medium
  
  # Weights for AGI decision making (should sum to 1.0)
  agi_cost_weight: 0.6        # Weight for cost optimization
  agi_performance_weight: 0.3  # Weight for performance optimization
  agi_reliability_weight: 0.1  # Weight for reliability optimization
  
  # Minimum confidence threshold for AGI decisions (0.1 - 0.95)
  agi_confidence_threshold: 0.7
  
  # Fallback mode when AGI confidence is low
  # - conservative: Use safe, proven options
  # - aggressive: Take calculated risks for better optimization
  agi_fallback_mode: conservative
"""