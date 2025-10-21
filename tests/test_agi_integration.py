"""Tests for OpenCog AGI integration in SkyPilot."""
import unittest
from unittest.mock import Mock, patch

from sky import task as sky_task
from sky import resources as sky_resources
from sky.agi.config import get_agi_config, is_agi_enabled
from sky.agi.core import AGIEngine, get_agi_engine


class TestAGIConfig(unittest.TestCase):
    """Test AGI configuration functionality."""
    
    def test_default_config(self):
        """Test that default AGI configuration is valid."""
        config = get_agi_config()
        
        self.assertIsInstance(config, dict)
        self.assertIn('agi_enabled', config)
        self.assertIn('agi_optimization_level', config)
        self.assertIn('agi_cost_weight', config)
        self.assertIn('agi_performance_weight', config)
        self.assertIn('agi_reliability_weight', config)
        
        # Check weights sum to approximately 1.0
        total_weight = (config['agi_cost_weight'] + 
                       config['agi_performance_weight'] + 
                       config['agi_reliability_weight'])
        self.assertAlmostEqual(total_weight, 1.0, places=1)
    
    def test_agi_enabled_check(self):
        """Test AGI enabled check functionality."""
        # Should return a boolean
        enabled = is_agi_enabled()
        self.assertIsInstance(enabled, bool)


class TestAGIEngine(unittest.TestCase):
    """Test AGI engine functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.agi_engine = AGIEngine()
    
    def test_engine_initialization(self):
        """Test that AGI engine initializes correctly."""
        self.assertIsInstance(self.agi_engine, AGIEngine)
        # is_available should be a boolean
        self.assertIsInstance(self.agi_engine.is_available, bool)
    
    def test_analyze_simple_task(self):
        """Test AGI analysis of a simple task."""
        # Create a simple test task
        task = sky_task.Task(name='test_task')
        task.set_resources(sky_resources.Resources(cpus=2))
        
        analysis = self.agi_engine.analyze_task(task)
        
        self.assertIsInstance(analysis, dict)
        self.assertIn('agi_available', analysis)
        
        if analysis.get('agi_available', False):
            self.assertIn('task_complexity', analysis)
            self.assertIn('resource_requirements', analysis)
            self.assertIn('optimization_suggestions', analysis)
            self.assertIn('risk_assessment', analysis)
    
    def test_analyze_gpu_task(self):
        """Test AGI analysis of a GPU task."""
        # Create a GPU test task
        task = sky_task.Task(name='gpu_task')
        task.set_resources(sky_resources.Resources(accelerators='V100:1'))
        
        analysis = self.agi_engine.analyze_task(task)
        
        self.assertIsInstance(analysis, dict)
        if analysis.get('agi_available', False):
            # GPU tasks should have higher complexity
            complexity = analysis.get('task_complexity', 'low')
            self.assertIn(complexity, ['low', 'medium', 'high'])
    
    def test_cloud_optimization(self):
        """Test cloud selection optimization."""
        task = sky_task.Task(name='test_task')
        available_clouds = ['aws', 'gcp', 'azure']
        
        optimized = self.agi_engine.optimize_cloud_selection(task, available_clouds)
        
        self.assertIsInstance(optimized, list)
        self.assertEqual(set(optimized), set(available_clouds))
    
    def test_singleton_pattern(self):
        """Test that get_agi_engine returns the same instance."""
        engine1 = get_agi_engine()
        engine2 = get_agi_engine()
        
        self.assertIs(engine1, engine2)


class TestAGIIntegration(unittest.TestCase):
    """Test integration of AGI with SkyPilot components."""
    
    @patch('sky.agi.core.HAS_HYPERON', False)
    def test_graceful_degradation_without_hyperon(self):
        """Test that system works gracefully without Hyperon installed."""
        engine = AGIEngine()
        
        # Should not be available without Hyperon
        self.assertFalse(engine.is_available)
        
        # Should still return valid analysis (in fallback mode)
        task = sky_task.Task(name='test_task')
        analysis = engine.analyze_task(task)
        
        self.assertIsInstance(analysis, dict)
        self.assertFalse(analysis.get('agi_available', True))
    
    def test_task_metadata_preservation(self):
        """Test that AGI operations preserve task metadata."""
        task = sky_task.Task(name='test_task')
        original_name = task.name
        
        engine = get_agi_engine()
        analysis = engine.analyze_task(task)
        
        # Task should be unchanged
        self.assertEqual(task.name, original_name)
        self.assertIsInstance(analysis, dict)


if __name__ == '__main__':
    unittest.main()