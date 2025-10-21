"""
Example demonstrating OpenCog AGI integration with SkyPilot.

This example shows how to use SkyPilot's AGI-enhanced optimization
for machine learning workloads with intelligent resource selection
and cloud provider optimization.
"""

import sky
from sky.agi import get_agi_engine


def main():
    """Demonstrate AGI-enhanced SkyPilot usage."""
    print("SkyPilot AGI Integration Example")
    print("=" * 40)
    
    # Check if AGI is available
    agi_engine = get_agi_engine()
    if agi_engine.is_available:
        print("✓ OpenCog AGI engine is available")
    else:
        print("⚠ OpenCog AGI engine not available (install with: pip install hyperon)")
    
    print()
    
    # Create a machine learning task
    task = sky.Task(name='ml_training')
    
    # Set resource requirements
    task.set_resources(sky.Resources(
        accelerators='T4:1',  # Single T4 GPU
        cpus=4,
        memory=16,  # 16 GB RAM
    ))
    
    # Add setup commands
    task.set_setup("""
        pip install torch torchvision
        pip install transformers datasets
    """)
    
    # Add the training script
    task.set_run("""
        python -c "
        import torch
        import time
        print('Training started with PyTorch', torch.__version__)
        print('CUDA available:', torch.cuda.is_available())
        if torch.cuda.is_available():
            print('GPU:', torch.cuda.get_device_name(0))
        
        # Simulate training
        for epoch in range(5):
            print(f'Epoch {epoch + 1}/5')
            time.sleep(2)  # Simulate training time
        
        print('Training completed!')
        "
    """)
    
    # Analyze the task with AGI if available
    if agi_engine.is_available:
        print("Analyzing task with AGI...")
        analysis = agi_engine.analyze_task(task)
        
        print("\nAGI Analysis Results:")
        print("-" * 20)
        
        if analysis.get('agi_available', False):
            print(f"Task Complexity: {analysis.get('task_complexity', 'unknown')}")
            
            # Show optimization suggestions
            suggestions = analysis.get('optimization_suggestions', [])
            if suggestions:
                print("\nOptimization Suggestions:")
                for i, suggestion in enumerate(suggestions, 1):
                    print(f"  {i}. {suggestion}")
            
            # Show resource insights
            resource_analysis = analysis.get('resource_requirements', {})
            insights = resource_analysis.get('agi_insights', [])
            if insights:
                print("\nResource Insights:")
                for insight in insights:
                    print(f"  • {insight}")
            
            # Show risk assessment
            risks = analysis.get('risk_assessment', {})
            if risks:
                print("\nRisk Assessment:")
                for risk_type, level in risks.items():
                    print(f"  {risk_type.capitalize()}: {level}")
        else:
            print("AGI analysis not available")
    
    print()
    
    # Test cloud optimization
    available_clouds = ['aws', 'gcp', 'azure', 'kubernetes']
    print(f"Available clouds: {available_clouds}")
    
    if agi_engine.is_available:
        optimized_clouds = agi_engine.optimize_cloud_selection(task, available_clouds)
        print(f"AGI recommended order: {optimized_clouds}")
    else:
        print("Using default cloud order (no AGI)")
    
    print()
    
    # Create a DAG with the task
    dag = sky.Dag()
    dag.add(task)
    
    # Optimize the DAG (will use AGI if available)
    print("Optimizing DAG...")
    try:
        optimized_dag = sky.optimize(dag, minimize=sky.OptimizeTarget.COST)
        print("✓ DAG optimization completed")
        
        # Show the optimized resources
        for task in optimized_dag.tasks:
            if task.best_resources:
                print(f"Task '{task.name}' optimized resources:")
                print(f"  Cloud: {task.best_resources.cloud}")
                print(f"  Instance: {task.best_resources.instance_type}")
                if task.best_resources.accelerators:
                    print(f"  Accelerators: {task.best_resources.accelerators}")
                print(f"  Cost estimate: ${task.best_resources.price:.2f}/hour")
    
    except Exception as e:
        print(f"✗ Optimization failed: {e}")
    
    print()
    print("Example completed!")
    print("\nTo run this task on your infrastructure:")
    print("  sky launch examples/agi/ml_training_task.yaml")


if __name__ == '__main__':
    main()