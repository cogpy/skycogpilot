#!/usr/bin/env python3
"""
Test OpenCog integration with SkyPilot

This test validates that the OpenCog integration works correctly
and can be used in SkyPilot workflows.
"""

import unittest
import tempfile
import os
import sys


class TestOpenCogIntegration(unittest.TestCase):
    """Test cases for OpenCog integration."""

    def setUp(self):
        """Set up test environment."""
        self.test_dir = os.path.dirname(os.path.abspath(__file__))
        self.opencog_dir = os.path.join(self.test_dir, '..', 'llm', 'opencog')

    def test_opencog_yaml_files_exist(self):
        """Test that all required OpenCog YAML files exist."""
        required_files = [
            'basic.yaml',
            'dev.yaml',
            'jupyter.yaml',
            'gpu.yaml',
            'cluster.yaml'
        ]
        
        for filename in required_files:
            filepath = os.path.join(self.opencog_dir, filename)
            self.assertTrue(
                os.path.exists(filepath),
                f"Required OpenCog YAML file {filename} does not exist"
            )

    def test_opencog_readme_exists(self):
        """Test that OpenCog README exists."""
        readme_path = os.path.join(self.opencog_dir, 'README.md')
        self.assertTrue(
            os.path.exists(readme_path),
            "OpenCog README.md does not exist"
        )

    def test_opencog_example_exists(self):
        """Test that OpenCog example script exists."""
        example_path = os.path.join(self.opencog_dir, 'example.py')
        self.assertTrue(
            os.path.exists(example_path),
            "OpenCog example.py does not exist"
        )

    def test_yaml_syntax(self):
        """Test that YAML files have valid syntax."""
        import yaml
        
        yaml_files = [
            'basic.yaml',
            'dev.yaml',
            'jupyter.yaml',
            'gpu.yaml',
            'cluster.yaml'
        ]
        
        for filename in yaml_files:
            filepath = os.path.join(self.opencog_dir, filename)
            with open(filepath, 'r') as f:
                try:
                    yaml.safe_load(f)
                except yaml.YAMLError as e:
                    self.fail(f"YAML syntax error in {filename}: {e}")

    def test_yaml_required_fields(self):
        """Test that YAML files contain required SkyPilot fields."""
        import yaml
        
        yaml_files = [
            'basic.yaml',
            'dev.yaml',
            'jupyter.yaml',
            'gpu.yaml',
            'cluster.yaml'
        ]
        
        required_fields = ['resources', 'setup', 'run']
        
        for filename in yaml_files:
            filepath = os.path.join(self.opencog_dir, filename)
            with open(filepath, 'r') as f:
                config = yaml.safe_load(f)
                
                for field in required_fields:
                    self.assertIn(
                        field, config,
                        f"Required field '{field}' missing from {filename}"
                    )

    def test_example_script_syntax(self):
        """Test that the example script has valid Python syntax."""
        example_path = os.path.join(self.opencog_dir, 'example.py')
        
        with open(example_path, 'r') as f:
            code = f.read()
        
        try:
            compile(code, example_path, 'exec')
        except SyntaxError as e:
            self.fail(f"Python syntax error in example.py: {e}")

    def test_readme_content(self):
        """Test that README contains expected content."""
        readme_path = os.path.join(self.opencog_dir, 'README.md')
        
        with open(readme_path, 'r') as f:
            content = f.read()
        
        expected_sections = [
            'OpenCog',
            'Prerequisites',
            'Quick Start',
            'sky launch',
            'basic.yaml',
            'dev.yaml',
            'jupyter.yaml'
        ]
        
        for section in expected_sections:
            self.assertIn(
                section, content,
                f"Expected section '{section}' not found in README"
            )

    def test_dependencies_include_opencog(self):
        """Test that dependencies.py includes OpenCog extras."""
        # Import the dependencies module
        sys.path.insert(0, os.path.join(self.test_dir, '..', 'sky', 'setup_files'))
        
        try:
            import dependencies
            
            # Check that opencog extra is defined
            self.assertIn(
                'opencog', dependencies.extras_require,
                "OpenCog extras not found in dependencies"
            )
            
            # Check that opencog dependencies are reasonable
            opencog_deps = dependencies.extras_require['opencog']
            self.assertIn('opencog', opencog_deps)
            self.assertIn('atomspace', opencog_deps)
            self.assertIn('numpy', opencog_deps)
            
        finally:
            sys.path.pop(0)

    def test_integration_completeness(self):
        """Test that the OpenCog integration is complete."""
        # Test that all major components exist
        files_and_dirs = os.listdir(self.opencog_dir)
        
        expected_items = [
            'README.md',
            'basic.yaml',
            'dev.yaml',
            'jupyter.yaml',
            'gpu.yaml',
            'cluster.yaml',
            'example.py'
        ]
        
        for item in expected_items:
            self.assertIn(
                item, files_and_dirs,
                f"Expected file/directory '{item}' not found in OpenCog integration"
            )


class TestOpenCogConfigurations(unittest.TestCase):
    """Test OpenCog configuration details."""

    def setUp(self):
        """Set up test environment."""
        self.test_dir = os.path.dirname(os.path.abspath(__file__))
        self.opencog_dir = os.path.join(self.test_dir, '..', 'llm', 'opencog')

    def test_basic_config_resources(self):
        """Test basic configuration has appropriate resources."""
        import yaml
        
        basic_path = os.path.join(self.opencog_dir, 'basic.yaml')
        with open(basic_path, 'r') as f:
            config = yaml.safe_load(f)
        
        resources = config['resources']
        self.assertIn('cpus', resources)
        self.assertIn('memory', resources)
        self.assertGreaterEqual(resources['cpus'], 2)
        self.assertGreaterEqual(resources['memory'], 4)

    def test_gpu_config_has_accelerators(self):
        """Test GPU configuration specifies accelerators."""
        import yaml
        
        gpu_path = os.path.join(self.opencog_dir, 'gpu.yaml')
        with open(gpu_path, 'r') as f:
            config = yaml.safe_load(f)
        
        resources = config['resources']
        self.assertIn('accelerators', resources)

    def test_cluster_config_multi_node(self):
        """Test cluster configuration has multiple nodes."""
        import yaml
        
        cluster_path = os.path.join(self.opencog_dir, 'cluster.yaml')
        with open(cluster_path, 'r') as f:
            config = yaml.safe_load(f)
        
        self.assertIn('num_nodes', config)
        self.assertGreater(config['num_nodes'], 1)

    def test_jupyter_config_has_ports(self):
        """Test Jupyter configuration exposes ports."""
        import yaml
        
        jupyter_path = os.path.join(self.opencog_dir, 'jupyter.yaml')
        with open(jupyter_path, 'r') as f:
            config = yaml.safe_load(f)
        
        self.assertIn('ports', config)


if __name__ == '__main__':
    unittest.main()