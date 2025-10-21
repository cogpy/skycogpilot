"""AGI-enhanced scheduler for SkyPilot task scheduling.

This module provides intelligent task scheduling capabilities using
OpenCog artificial general intelligence for optimal resource allocation
and execution planning.
"""
import logging
import threading
import time
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta

from sky import task as sky_task
from sky import dag as sky_dag
from sky.agi.core import get_agi_engine


logger = logging.getLogger(__name__)


@dataclass
class SchedulingDecision:
    """Represents an AGI-powered scheduling decision."""
    task_id: str
    recommended_cloud: str
    estimated_cost: float
    estimated_duration: float
    confidence: float
    reasoning: List[str]
    scheduling_time: datetime


class AGIScheduler:
    """AGI-enhanced intelligent scheduler for SkyPilot tasks.
    
    This scheduler uses OpenCog artificial general intelligence to make
    optimal scheduling decisions based on historical data, current conditions,
    and predictive analysis.
    """
    
    def __init__(self):
        """Initialize the AGI scheduler."""
        self.agi_engine = get_agi_engine()
        self.scheduling_history = []
        self.active_tasks = {}
        self.lock = threading.Lock()
        
        # Scheduling parameters (would be learned by AGI in full implementation)
        self.cost_weight = 0.6
        self.performance_weight = 0.3
        self.reliability_weight = 0.1
        
        logger.info("AGI scheduler initialized")
    
    def schedule_task(self,
                     task: sky_task.Task,
                     available_clouds: List[str],
                     constraints: Optional[Dict[str, Any]] = None) -> SchedulingDecision:
        """Schedule a task using AGI-enhanced decision making.
        
        Args:
            task: SkyPilot task to schedule
            available_clouds: List of available cloud providers
            constraints: Optional scheduling constraints
            
        Returns:
            AGI-powered scheduling decision
        """
        logger.info(f"AGI scheduling task: {task.name}")
        
        if not self.agi_engine.is_available:
            return self._fallback_scheduling(task, available_clouds)
        
        with self.lock:
            decision = self._make_agi_scheduling_decision(
                task, available_clouds, constraints
            )
            
            # Record the decision
            self.scheduling_history.append(decision)
            self.active_tasks[task.name] = decision
            
            logger.info(f"AGI scheduled {task.name} on {decision.recommended_cloud} "
                       f"(confidence: {decision.confidence:.2f})")
            
            return decision
    
    def _make_agi_scheduling_decision(self,
                                    task: sky_task.Task,
                                    available_clouds: List[str],
                                    constraints: Optional[Dict[str, Any]]) -> SchedulingDecision:
        """Make an AGI-powered scheduling decision."""
        # Get AGI analysis of the task
        analysis = self.agi_engine.analyze_task(task)
        
        # Get cloud recommendations from AGI
        cloud_recommendations = self.agi_engine.optimize_cloud_selection(
            task, available_clouds
        )
        
        # Score each cloud option
        cloud_scores = []
        for cloud in cloud_recommendations:
            score = self._score_cloud_option(task, cloud, analysis, constraints)
            cloud_scores.append((cloud, score))
        
        # Select the best cloud
        best_cloud, best_score = max(cloud_scores, key=lambda x: x[1])
        
        # Generate reasoning
        reasoning = self._generate_scheduling_reasoning(
            task, best_cloud, analysis, best_score
        )
        
        # Estimate cost and duration
        estimated_cost = self._estimate_cost(task, best_cloud)
        estimated_duration = self._estimate_duration(task, best_cloud)
        
        # Calculate confidence based on AGI analysis quality
        confidence = self._calculate_confidence(analysis, best_score)
        
        decision = SchedulingDecision(
            task_id=task.name or f"task_{int(time.time())}",
            recommended_cloud=best_cloud,
            estimated_cost=estimated_cost,
            estimated_duration=estimated_duration,
            confidence=confidence,
            reasoning=reasoning,
            scheduling_time=datetime.now()
        )
        
        return decision
    
    def _score_cloud_option(self,
                           task: sky_task.Task,
                           cloud: str,
                           analysis: Dict[str, Any],
                           constraints: Optional[Dict[str, Any]]) -> float:
        """Score a cloud option for the given task using AGI insights."""
        base_score = 0.5
        
        # Factor in task complexity from AGI analysis
        complexity = analysis.get("task_complexity", "medium")
        if complexity == "low":
            base_score += 0.1
        elif complexity == "high":
            base_score -= 0.1
        
        # Factor in AGI resource insights
        insights = analysis.get("resource_requirements", {}).get("agi_insights", [])
        for insight in insights:
            if "spot instances" in insight and cloud.lower() in ["aws", "gcp"]:
                base_score += 0.15  # These clouds have good spot instance support
            elif "multi-cloud" in insight:
                base_score += 0.1   # Reward clouds that support distribution
        
        # Apply constraints
        if constraints:
            if "preferred_clouds" in constraints:
                if cloud in constraints["preferred_clouds"]:
                    base_score += 0.2
            if "blocked_clouds" in constraints:
                if cloud in constraints["blocked_clouds"]:
                    base_score = 0.0
        
        # Historical performance factor
        historical_score = self._get_historical_performance(cloud)
        base_score = 0.7 * base_score + 0.3 * historical_score
        
        return max(0.0, min(1.0, base_score))
    
    def _get_historical_performance(self, cloud: str) -> float:
        """Get historical performance score for a cloud provider."""
        # Simple implementation - would use AGI learning in full version
        cloud_performance = {
            "aws": 0.85,
            "gcp": 0.82,
            "azure": 0.78,
            "kubernetes": 0.80,
            "lambda": 0.75
        }
        
        return cloud_performance.get(cloud.lower(), 0.70)
    
    def _generate_scheduling_reasoning(self,
                                     task: sky_task.Task,
                                     cloud: str,
                                     analysis: Dict[str, Any],
                                     score: float) -> List[str]:
        """Generate human-readable reasoning for the scheduling decision."""
        reasoning = []
        
        reasoning.append(f"Selected {cloud} with confidence score {score:.2f}")
        
        if analysis.get("agi_available", False):
            complexity = analysis.get("task_complexity", "unknown")
            reasoning.append(f"Task complexity assessed as: {complexity}")
            
            suggestions = analysis.get("optimization_suggestions", [])
            if suggestions:
                reasoning.append(f"AGI suggests: {suggestions[0]}")
        
        # Add cloud-specific reasoning
        if cloud.lower() == "aws":
            reasoning.append("AWS selected for robust GPU availability and spot instances")
        elif cloud.lower() == "gcp":
            reasoning.append("GCP selected for competitive pricing and performance")
        elif cloud.lower() == "azure":
            reasoning.append("Azure selected for enterprise integration capabilities")
        elif cloud.lower() == "kubernetes":
            reasoning.append("Kubernetes selected for containerized workload optimization")
        
        return reasoning
    
    def _estimate_cost(self, task: sky_task.Task, cloud: str) -> float:
        """Estimate the cost of running the task on the given cloud."""
        # Simplified cost estimation - would use AGI prediction in full implementation
        base_cost = 1.0  # Base cost per hour
        
        if task.resources:
            if task.resources.accelerators:
                base_cost *= 10  # GPU multiplier
            if task.resources.cpus:
                base_cost *= max(1, task.resources.cpus / 4)
            if task.resources.memory:
                base_cost *= max(1, task.resources.memory / 16)
        
        # Cloud-specific cost factors
        cloud_factors = {
            "aws": 1.0,
            "gcp": 0.9,      # Typically 10% cheaper
            "azure": 1.05,   # Slightly more expensive
            "kubernetes": 0.7,  # Using existing cluster
            "lambda": 0.8
        }
        
        factor = cloud_factors.get(cloud.lower(), 1.0)
        estimated_cost = base_cost * factor
        
        return round(estimated_cost, 2)
    
    def _estimate_duration(self, task: sky_task.Task, cloud: str) -> float:
        """Estimate the duration of running the task on the given cloud."""
        # Simplified duration estimation
        base_duration = 1.0  # Base duration in hours
        
        if task.resources:
            if task.resources.accelerators:
                base_duration *= 0.5  # GPUs speed up computation
            if task.num_nodes and task.num_nodes > 1:
                base_duration *= 0.8  # Multi-node can be faster
        
        # Cloud-specific performance factors
        cloud_factors = {
            "aws": 1.0,
            "gcp": 0.95,     # Slightly faster network
            "azure": 1.05,   # Slightly slower
            "kubernetes": 0.9,  # Local cluster advantage
            "lambda": 1.1
        }
        
        factor = cloud_factors.get(cloud.lower(), 1.0)
        estimated_duration = base_duration * factor
        
        return round(estimated_duration, 2)
    
    def _calculate_confidence(self, analysis: Dict[str, Any], score: float) -> float:
        """Calculate confidence in the scheduling decision."""
        base_confidence = 0.7
        
        if analysis.get("agi_available", False):
            base_confidence += 0.2  # Higher confidence with AGI
            
            # Factor in risk assessment
            risks = analysis.get("risk_assessment", {})
            high_risk_count = sum(1 for risk in risks.values() if risk == "high")
            base_confidence -= high_risk_count * 0.1
        
        # Factor in score quality
        if score > 0.8:
            base_confidence += 0.1
        elif score < 0.5:
            base_confidence -= 0.1
        
        return max(0.1, min(0.95, base_confidence))
    
    def _fallback_scheduling(self,
                           task: sky_task.Task,
                           available_clouds: List[str]) -> SchedulingDecision:
        """Fallback scheduling when AGI is not available."""
        logger.warning("Using fallback scheduling - AGI not available")
        
        # Simple fallback: choose first available cloud
        cloud = available_clouds[0] if available_clouds else "aws"
        
        decision = SchedulingDecision(
            task_id=task.name or f"task_{int(time.time())}",
            recommended_cloud=cloud,
            estimated_cost=5.0,   # Conservative estimate
            estimated_duration=2.0,  # Conservative estimate
            confidence=0.5,       # Low confidence without AGI
            reasoning=[f"Fallback scheduling selected {cloud}", "AGI engine not available"],
            scheduling_time=datetime.now()
        )
        
        return decision
    
    def get_scheduling_statistics(self) -> Dict[str, Any]:
        """Get statistics about AGI scheduling performance."""
        with self.lock:
            if not self.scheduling_history:
                return {"no_data": True}
            
            total_decisions = len(self.scheduling_history)
            avg_confidence = sum(d.confidence for d in self.scheduling_history) / total_decisions
            
            cloud_usage = {}
            for decision in self.scheduling_history:
                cloud = decision.recommended_cloud
                cloud_usage[cloud] = cloud_usage.get(cloud, 0) + 1
            
            stats = {
                "total_decisions": total_decisions,
                "average_confidence": round(avg_confidence, 3),
                "cloud_usage_distribution": cloud_usage,
                "agi_availability": self.agi_engine.is_available,
                "active_tasks": len(self.active_tasks)
            }
            
            return stats
    
    def task_completed(self, 
                      task_id: str, 
                      actual_cost: float, 
                      actual_duration: float,
                      success: bool):
        """Record task completion for AGI learning.
        
        Args:
            task_id: ID of the completed task
            actual_cost: Actual cost incurred
            actual_duration: Actual duration taken
            success: Whether the task completed successfully
        """
        with self.lock:
            if task_id in self.active_tasks:
                decision = self.active_tasks[task_id]
                
                # Calculate prediction accuracy
                cost_accuracy = 1.0 - abs(decision.estimated_cost - actual_cost) / max(decision.estimated_cost, actual_cost, 1.0)
                duration_accuracy = 1.0 - abs(decision.estimated_duration - actual_duration) / max(decision.estimated_duration, actual_duration, 1.0)
                
                # Store feedback for AGI learning
                feedback = {
                    "task_id": task_id,
                    "predicted_cost": decision.estimated_cost,
                    "actual_cost": actual_cost,
                    "predicted_duration": decision.estimated_duration,
                    "actual_duration": actual_duration,
                    "cost_accuracy": cost_accuracy,
                    "duration_accuracy": duration_accuracy,
                    "success": success,
                    "cloud": decision.recommended_cloud
                }
                
                logger.info(f"Task {task_id} completed: cost_accuracy={cost_accuracy:.2f}, "
                           f"duration_accuracy={duration_accuracy:.2f}, success={success}")
                
                # Remove from active tasks
                del self.active_tasks[task_id]
                
                # In a full implementation, this feedback would be used to
                # update the AGI knowledge base and improve future predictions
    
    def optimize_scheduler_parameters(self):
        """Optimize scheduler parameters using AGI learning."""
        if not self.agi_engine.is_available:
            return
        
        logger.info("Optimizing AGI scheduler parameters")
        
        # In a full implementation, this would use OpenCog reasoning
        # to optimize the cost_weight, performance_weight, and reliability_weight
        # based on historical performance and user preferences
        
        # Simple parameter adjustment based on recent performance
        if len(self.scheduling_history) >= 10:
            recent_decisions = self.scheduling_history[-10:]
            avg_confidence = sum(d.confidence for d in recent_decisions) / len(recent_decisions)
            
            if avg_confidence < 0.7:
                # Reduce confidence requirements
                self.cost_weight = max(0.1, self.cost_weight - 0.05)
                self.performance_weight = min(0.8, self.performance_weight + 0.05)
                logger.debug("Adjusted scheduler parameters for better performance")


# Global AGI scheduler instance
_agi_scheduler = None
_scheduler_lock = threading.Lock()


def get_agi_scheduler() -> AGIScheduler:
    """Get the global AGI scheduler instance (singleton pattern)."""
    global _agi_scheduler
    
    if _agi_scheduler is None:
        with _scheduler_lock:
            if _agi_scheduler is None:
                _agi_scheduler = AGIScheduler()
    
    return _agi_scheduler