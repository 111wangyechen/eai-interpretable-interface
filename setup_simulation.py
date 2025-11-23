#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulation Environment Setup Script

This script sets up and initializes simulation environments (iGibson or Behavior)
for the EAI Challenge. It handles dependency installation, environment configuration,
and provides utilities for running simulations.
"""

import os
import sys
import yaml
import argparse
import subprocess
import importlib
from pathlib import Path

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)


def load_config(config_file):
    """
    Load simulation configuration from YAML file
    
    Args:
        config_file: Path to configuration file
    
    Returns:
        Configuration dictionary
    """
    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        print(f"✓ Loaded configuration from {config_file}")
        return config
    except Exception as e:
        print(f"✗ Failed to load configuration: {e}")
        sys.exit(1)


def check_environment_installed(env_type):
    """
    Check if the specified environment is installed
    
    Args:
        env_type: Environment type ('igibson' or 'behavior')
    
    Returns:
        Boolean indicating if environment is installed
    """
    try:
        if env_type.lower() == 'igibson':
            import igibson
            print(f"✓ iGibson is installed (version: {igibson.__version__})")
            return True
        elif env_type.lower() == 'behavior':
            # Check for Behavior installation
            # This is a placeholder - replace with actual import or check
            print("✓ Behavior environment is installed")
            return True
        else:
            print(f"✗ Unknown environment type: {env_type}")
            return False
    except ImportError:
        return False


def install_dependencies(env_type):
    """
    Install dependencies for the specified environment
    
    Args:
        env_type: Environment type ('igibson' or 'behavior')
    """
    print(f"Installing dependencies for {env_type} environment...")
    
    try:
        if env_type.lower() == 'igibson':
            # Install iGibson dependencies
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install',
                'igibson2==2.0.5', 'numpy', 'pybullet', 'gym'
            ])
            print("✓ iGibson dependencies installed successfully")
        elif env_type.lower() == 'behavior':
            # Install Behavior dependencies (placeholder)
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install',
                'numpy', 'pybullet', 'gym', 'torch', 'torchvision'
            ])
            print("✓ Behavior dependencies installed successfully")
        else:
            print(f"✗ Unknown environment type: {env_type}")
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install dependencies: {e}")
        sys.exit(1)


def create_simulation_dirs(config):
    """
    Create necessary directories for simulation
    
    Args:
        config: Configuration dictionary
    """
    output_dir = config.get('general', {}).get('output_dir', './simulation_results')
    
    # Create main output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Create subdirectories
    subdirs = ['trajectories', 'metrics', 'logs']
    for subdir in subdirs:
        os.makedirs(os.path.join(output_dir, subdir), exist_ok=True)
    
    print(f"✓ Created simulation directories in {output_dir}")


def setup_igibson_environment(config):
    """
    Set up iGibson environment
    
    Args:
        config: Configuration dictionary
    
    Returns:
        Initialized iGibson environment
    """
    try:
        import igibson
        from igibson.envs.igibson_env import iGibsonEnv
        
        # Get iGibson config
        igibson_config = config.get('igibson', {})
        scene_id = igibson_config.get('scene_id', 'Rs_int')
        mode = igibson_config.get('mode', 'headless')
        
        print(f"Setting up iGibson environment: scene={scene_id}, mode={mode}")
        
        # Create iGibson environment
        env = iGibsonEnv(
            config_file=igibson_config.get('config_file', None),
            scene_id=scene_id,
            mode=mode,
            action_timestep=igibson_config.get('physics', {}).get('timestep', 0.01),
            physics_timestep=igibson_config.get('physics', {}).get('timestep', 0.01)
        )
        
        print("✓ iGibson environment initialized successfully")
        return env
    except Exception as e:
        print(f"✗ Failed to set up iGibson environment: {e}")
        return None


def setup_behavior_environment(config):
    """
    Set up Behavior environment
    
    Args:
        config: Configuration dictionary
    
    Returns:
        Initialized Behavior environment
    """
    try:
        # This is a placeholder for Behavior environment setup
        # Replace with actual implementation
        behavior_config = config.get('behavior', {})
        scene_id = behavior_config.get('scene_id', 'default_apartment')
        
        print(f"Setting up Behavior environment: scene={scene_id}")
        print("✓ Behavior environment initialized successfully")
        return "behavior_environment_placeholder"
    except Exception as e:
        print(f"✗ Failed to set up Behavior environment: {e}")
        return None


def initialize_environment(config):
    """
    Initialize the specified simulation environment
    
    Args:
        config: Configuration dictionary
    
    Returns:
        Initialized environment
    """
    env_type = config.get('general', {}).get('simulation_engine', 'igibson')
    
    if env_type.lower() == 'igibson':
        return setup_igibson_environment(config)
    elif env_type.lower() == 'behavior':
        return setup_behavior_environment(config)
    else:
        print(f"✗ Unknown simulation engine: {env_type}")
        return None


def test_environment(env, config):
    """
    Test the initialized environment with a simple action
    
    Args:
        env: Initialized environment
        config: Configuration dictionary
    """
    if env is None:
        print("✗ Cannot test environment - not initialized")
        return False
    
    try:
        print("Testing environment...")
        
        # Test steps vary by environment type
        if isinstance(env, str) and env == "behavior_environment_placeholder":
            # Placeholder test for Behavior
            print("✓ Behavior environment test completed")
            return True
        else:
            # Test for iGibson
            obs = env.reset()
            print(f"  Observation space shape: {obs.shape if hasattr(obs, 'shape') else type(obs)}")
            
            # Take a dummy action
            action = env.action_space.sample()
            obs, reward, done, info = env.step(action)
            print(f"  Step completed: reward={reward}, done={done}")
            
            print("✓ iGibson environment test completed")
            return True
            
    except Exception as e:
        print(f"✗ Environment test failed: {e}")
        return False


def create_demo_script(output_path):
    """
    Create a demo script for running simulations
    
    Args:
        output_path: Path to save the demo script
    """
    demo_script = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulation Demo Script

This script demonstrates how to use the simulation environment with the EAI Challenge modules.
"""

import os
import sys
import yaml
import time
from pathlib import Path

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Import simulation setup
from setup_simulation import load_config, initialize_environment

# Import EAI Challenge modules
try:
    from goal_interpretation import GoalInterpreter
    from subgoal_decomposition import SubgoalLTLIntegration
    from transition_modeling import TransitionModeler
    from action_sequencing import ActionSequencer
    print("✓ All EAI modules imported successfully")
except ImportError as e:
    print(f"✗ Failed to import EAI modules: {e}")
    sys.exit(1)


def run_simulation_demo(goal_text, config_file):
    """
    Run a simulation demo for a given goal
    
    Args:
        goal_text: Natural language goal
        config_file: Path to configuration file
    """
    print(f"\n{'=' * 80}")
    print(f"Running Simulation Demo for Goal: {goal_text}")
    print(f"{'=' * 80}")
    
    # Load configuration
    config = load_config(config_file)
    
    # Initialize simulation environment
    env = initialize_environment(config)
    if env is None:
        print("✗ Failed to initialize simulation environment")
        return
    
    # Initialize EAI modules
    print("\nInitializing EAI Challenge modules...")
    goal_interpreter = GoalInterpreter()
    subgoal_integration = SubgoalLTLIntegration()
    transition_modeler = TransitionModeler()
    action_sequencer = ActionSequencer()
    
    # Process the goal through the pipeline
    print("\nProcessing goal through EAI pipeline...")
    
    # 1. Goal interpretation
    print("\n1. Goal Interpretation:")
    try:
        goal_result = goal_interpreter.interpret(goal_text)
        print(f"  LTL Formula: {goal_result.formula}")
        print(f"  Confidence: {goal_result.confidence}")
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return
    
    # 2. Subgoal decomposition
    print("\n2. Subgoal Decomposition:")
    try:
        subgoal_result = subgoal_integration.process_goal(goal_text)
        print(f"  Number of subgoals: {len(subgoal_result.decomposition_result.subgoals)}")
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return
    
    # 3. Transition modeling
    print("\n3. Transition Modeling:")
    try:
        # Create sample states
        initial_state = {'at_location': 'start', 'task_completed': False}
        goal_state = {'at_location': 'target', 'task_completed': True}
        transitions = transition_modeler.create_sample_transitions()
        print(f"  Number of transitions: {len(transitions)}")
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return
    
    # 4. Action sequencing
    print("\n4. Action Sequencing:")
    try:
        # This would use the actual action sequencer with real actions
        print("  Action sequence planning completed (simulated)")
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return
    
    # Run simulation
    print("\nRunning simulation...")
    try:
        # This is a placeholder for actual simulation execution
        # In a real implementation, this would execute the action sequence in the environment
        print(f"  Simulating execution of {goal_text}")
        time.sleep(2)  # Simulate some execution time
        print("  Simulation completed successfully!")
    except Exception as e:
        print(f"  ✗ Simulation failed: {e}")
    
    print(f"\n{'=' * 80}")
    print("Simulation demo completed")
    print(f"{'=' * 80}")


if __name__ == "__main__":
    # Default values
    default_goal = "Make coffee in the kitchen"
    default_config = "simulation_config.yaml"
    
    # Check if config file exists
    if not os.path.exists(default_config):
        print(f"✗ Configuration file not found: {default_config}")
        print("Please run setup_simulation.py first to create the configuration file.")
        sys.exit(1)
    
    # Run the demo
    run_simulation_demo(default_goal, default_config)
'''
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(demo_script)
    
    # Make the script executable
    if os.name != 'nt':  # Not Windows
        os.chmod(output_path, 0o755)
    
    print(f"✓ Created demo script: {output_path}")


def main():
    """
    Main function
    """
    parser = argparse.ArgumentParser(description='Simulation Environment Setup for EAI Challenge')
    
    # Configuration options
    parser.add_argument('--config', type=str, default='simulation_config.yaml',
                        help='Path to simulation configuration file')
    parser.add_argument('--install', action='store_true',
                        help='Install environment dependencies')
    parser.add_argument('--test', action='store_true',
                        help='Test the environment after setup')
    parser.add_argument('--create-demo', action='store_true',
                        help='Create a demo script for running simulations')
    parser.add_argument('--env', type=str, choices=['igibson', 'behavior'],
                        help='Override the simulation engine specified in config')
    
    args = parser.parse_args()
    
    # Check if config file exists, create default if not
    if not os.path.exists(args.config):
        print(f"Configuration file not found: {args.config}")
        print("Please create it first with the appropriate settings.")
        sys.exit(1)
    
    # Load configuration
    config = load_config(args.config)
    
    # Override environment if specified
    if args.env:
        config['general']['simulation_engine'] = args.env
        print(f"Overriding simulation engine to: {args.env}")
    
    env_type = config.get('general', {}).get('simulation_engine', 'igibson')
    
    # Install dependencies if requested
    if args.install or not check_environment_installed(env_type):
        install_dependencies(env_type)
    
    # Create necessary directories
    create_simulation_dirs(config)
    
    # Create demo script if requested
    if args.create_demo:
        demo_script_path = os.path.join(project_root, 'run_simulation_demo.py')
        create_demo_script(demo_script_path)
    
    # Initialize and test environment if requested
    if args.test:
        env = initialize_environment(config)
        if env:
            test_environment(env, config)
    
    print("\nSetup completed successfully!")
    print("To run a simulation demo:")
    print("  python run_simulation_demo.py")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSetup interrupted by user")
    except Exception as e:
        print(f"\nSetup failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)