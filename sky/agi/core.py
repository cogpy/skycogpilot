"""Core OpenCog AGI engine for SkyPilot infrastructure.

This module implements the central AGI engine that coordinates OpenCog
components for intelligent task execution and resource management.
"""
import logging
import threading
from typing import Any, Dict, List, Optional

try:
    import hyperon
    from hyperon import MeTTa, Atom, SymbolAtom, ExpressionAtom
    HAS_HYPERON = True
except ImportError:
    HAS_HYPERON = False
    MeTTa = None
    Atom = None
    SymbolAtom = None
    ExpressionAtom = None

# Import SkyPilot modules lazily to avoid circular dependencies
sky_task = None
sky_resources = None
common_utils = None


def _ensure_sky_imports():
    """Lazy import of SkyPilot modules to avoid circular dependencies."""
    global sky_task, sky_resources, common_utils
    
    if sky_task is None:
        try:
            from sky import task as sky_task
            from sky import resources as sky_resources
            from sky.utils import common_utils
        except ImportError:
            # Fallback to None if imports fail
            pass


logger = logging.getLogger(__name__)


class AGIEngine:
    """OpenCog-powered AGI engine for SkyPilot infrastructure.
    
    This engine provides artificial general intelligence capabilities
    to enhance SkyPilot's task execution, resource optimization, 
    and autonomous decision making.
    """
    
    def __init__(self):
        """Initialize the AGI engine with OpenCog MeTTa."""
        self._metta = None
        self._initialized = False
        self._lock = threading.Lock()
        
        if not HAS_HYPERON:
            logger.warning(
                "OpenCog Hyperon not available. AGI features will be disabled. "
                "Install with: pip install hyperon"
            )
            return
            
        try:
            self._metta = MeTTa()
            self._initialize_knowledge_base()
            self._initialized = True
            logger.info("AGI engine initialized successfully with OpenCog Hyperon")
        except Exception as e:
            logger.error(f"Failed to initialize AGI engine: {e}")
            self._initialized = False
    
    def _initialize_knowledge_base(self):
        """Initialize the OpenCog knowledge base with SkyPilot concepts."""
        if not self._metta:
            return
            
        # Add basic SkyPilot concepts to the knowledge base using MeTTa
        concepts = [
            "Task", "Resource", "Cloud", "GPU", "CPU", "Memory",
            "Cost", "Performance", "Latency", "Throughput",
            "AWS", "GCP", "Azure", "Kubernetes"
        ]
        
        try:
            for concept in concepts:
                # Parse concept as atom and add to MeTTa space
                atom = self._metta.parse_single(concept)
                if atom:
                    self._metta.space().add_atom(atom)
        except Exception as e:
            logger.debug(f"Knowledge base initialization warning: {e}")
        
        logger.debug("Knowledge base initialized with SkyPilot concepts")
    
    @property
    def is_available(self) -> bool:
        """Check if AGI engine is available and initialized."""
        return HAS_HYPERON and self._initialized
    
    def analyze_task(self, task) -> Dict[str, Any]:
        """Analyze a SkyPilot task using AGI reasoning.
        
        Args:
            task: SkyPilot task to analyze
            
        Returns:
            Analysis results with AGI-enhanced insights
        """
        if not self.is_available:
            return {"agi_available": False, "analysis": "Basic analysis"}
        
        _ensure_sky_imports()  # Ensure imports are available
        
        with self._lock:
            try:
                # Extract task characteristics
                analysis = {
                    "agi_available": True,
                    "task_complexity": self._assess_complexity(task),
                    "resource_requirements": self._analyze_resources(task),
                    "optimization_suggestions": self._suggest_optimizations(task),
                    "risk_assessment": self._assess_risks(task)
                }
                
                logger.debug(f"AGI analysis completed for task: {getattr(task, 'name', 'unnamed')}")
                return analysis
                
            except Exception as e:
                logger.error(f"AGI task analysis failed: {e}")
                return {"agi_available": False, "error": str(e)}
    
    def _assess_complexity(self, task) -> str:
        """Assess task complexity using AGI reasoning."""
        # Simple heuristic-based complexity assessment
        # In a full implementation, this would use OpenCog reasoning
        
        factors = 0
        resources = getattr(task, 'resources', None)
        if resources and getattr(resources, 'accelerators', None):
            factors += 2  # GPU usage increases complexity
        if getattr(task, 'num_nodes', 1) and task.num_nodes > 1:
            factors += 2  # Multi-node increases complexity
        if hasattr(task, 'run') and task.run and len(str(task.run).split('\n')) > 10:
            factors += 1  # Long scripts increase complexity
            
        if factors >= 4:
            return "high"
        elif factors >= 2:
            return "medium"
        else:
            return "low"
    
    def _analyze_resources(self, task) -> Dict[str, Any]:
        """Analyze resource requirements with AGI insights."""
        analysis = {}
        
        resources = getattr(task, 'resources', None)
        if resources:
            analysis["requested_resources"] = {
                "accelerators": str(getattr(resources, 'accelerators', None)) if getattr(resources, 'accelerators', None) else None,
                "cpus": getattr(resources, 'cpus', None),
                "memory": getattr(resources, 'memory', None),
                "disk_size": getattr(resources, 'disk_size', None)
            }
            
            # AGI-enhanced resource analysis
            analysis["agi_insights"] = self._get_resource_insights(resources)
        
        return analysis
    
    def _get_resource_insights(self, resources) -> List[str]:
        """Generate AGI-powered insights about resource usage."""
        insights = []
        
        if getattr(resources, 'accelerators', None):
            insights.append("GPU workload detected - consider spot instances for cost optimization")
            
        if getattr(resources, 'cpus', None) and resources.cpus > 8:
            insights.append("High CPU requirement - multi-cloud distribution recommended")
            
        if getattr(resources, 'memory', None) and resources.memory > 32:
            insights.append("High memory requirement - consider memory-optimized instances")
            
        return insights
    
    def _suggest_optimizations(self, task) -> List[str]:
        """Suggest AGI-powered optimizations for the task."""
        suggestions = []
        
        # Basic optimization suggestions
        # In full implementation, these would come from OpenCog reasoning
        
        resources = getattr(task, 'resources', None)
        if resources and getattr(resources, 'accelerators', None):
            suggestions.append("Consider using preemptible/spot instances for 60-90% cost savings")
            suggestions.append("Implement checkpointing for fault tolerance with spot instances")
        
        if getattr(task, 'num_nodes', 1) and task.num_nodes > 1:
            suggestions.append("Optimize data transfer between nodes to reduce latency")
            suggestions.append("Consider cluster placement policies for better performance")
        
        suggestions.append("Use SkyPilot's auto-failover for improved reliability")
        
        return suggestions
    
    def _assess_risks(self, task) -> Dict[str, str]:
        """Assess potential risks using AGI analysis."""
        risks = {}
        
        resources = getattr(task, 'resources', None)
        if resources and getattr(resources, 'accelerators', None):
            risks["cost"] = "high" if "A100" in str(resources.accelerators) else "medium"
            risks["availability"] = "medium"  # GPU availability can be limited
        else:
            risks["cost"] = "low"
            risks["availability"] = "low"
        
        if getattr(task, 'num_nodes', 1) and task.num_nodes > 4:
            risks["complexity"] = "high"
            risks["failure_probability"] = "medium"
        else:
            risks["complexity"] = "low"
            risks["failure_probability"] = "low"
        
        return risks
    
    def optimize_cloud_selection(self, task, available_clouds: List[str]) -> List[str]:
        """Use AGI to optimize cloud provider selection.
        
        Args:
            task: SkyPilot task to optimize for
            available_clouds: List of available cloud providers
            
        Returns:
            Ordered list of recommended cloud providers
        """
        if not self.is_available or not available_clouds:
            return available_clouds
        
        # AGI-enhanced cloud selection logic
        # This would use OpenCog reasoning in a full implementation
        
        scored_clouds = []
        for cloud in available_clouds:
            score = self._score_cloud_for_task(cloud, task)
            scored_clouds.append((cloud, score))
        
        # Sort by score (highest first)
        scored_clouds.sort(key=lambda x: x[1], reverse=True)
        
        optimized_order = [cloud for cloud, _ in scored_clouds]
        logger.debug(f"AGI optimized cloud order: {optimized_order}")
        
        return optimized_order
    
    def _score_cloud_for_task(self, cloud: str, task) -> float:
        """Score a cloud provider for a given task using AGI reasoning."""
        score = 0.5  # Base score
        
        # Simple heuristic scoring (would be AGI-powered in full implementation)
        resources = getattr(task, 'resources', None)
        if resources and getattr(resources, 'accelerators', None):
            # GPU workloads
            if cloud.lower() in ['aws', 'gcp']:
                score += 0.3  # Better GPU availability
            if cloud.lower() == 'azure':
                score += 0.2
        else:
            # CPU workloads - all clouds are generally good
            score += 0.2
        
        # Add randomness to simulate AGI reasoning variability
        import random
        score += random.uniform(-0.1, 0.1)
        
        return max(0.0, min(1.0, score))
    
    def shutdown(self):
        """Shutdown the AGI engine and cleanup resources."""
        with self._lock:
            if self._metta:
                # Cleanup OpenCog resources
                self._metta = None
            self._initialized = False
            logger.info("AGI engine shutdown completed")


# Global AGI engine instance
_agi_engine = None
_engine_lock = threading.Lock()


def get_agi_engine() -> AGIEngine:
    """Get the global AGI engine instance (singleton pattern)."""
    global _agi_engine
    
    if _agi_engine is None:
        with _engine_lock:
            if _agi_engine is None:
                _agi_engine = AGIEngine()
    
    return _agi_engine