# EAI Challenge: Interpretable Interface Implementation

## Project Overview

This project implements an interpretable interface for the EAI (Embodied AI) Challenge. The system processes natural language goals, decomposes them into subgoals, creates LTL (Linear Temporal Logic) specifications, models state transitions, and generates executable action sequences for embodied agents in simulated environments.

## Directory Structure

```
eai-interpretable-interface/
├── analyze_datasets.py        # Script to analyze dataset files
├── combine_results.py         # Main submission script (Chinese version)
├── combine_results_en.py      # Main submission script (English version)
├── dataset_analyze_result.md  # Dataset analysis results
├── dataset_summary.json       # Summary of analyzed datasets
├── final_submission.json      # Final submission configuration file
├── sample_goals_en.json       # Sample goals in English
├── simulation_config.yaml     # Configuration for simulation environments
├── setup_simulation.py        # Script to set up simulation environments
├── run_simulation_tests.py    # Script to run simulation tests
└── README.md                  # This documentation file
```

## Dataset Analysis

The system analyzes and processes two primary datasets:

1. **Behavior Dataset** (`behavior.parquet`)
   - Contains 100 rows of data
   - 8 columns including scene_id, task_id, task_name, natural_language_description, etc.
   - Provides diverse household tasks and action sequences

2. **VirtualHome Dataset** (`virtualhome.parquet`)
   - Contains 338 rows of data
   - 8 columns with similar structure to behavior dataset
   - Includes 26 unique task types
   - Features detailed action trajectories and transition models

Key observations from dataset analysis:
- Both datasets use consistent schema with scene_id, task_id, and natural language descriptions
- Tasks range from simple actions to complex multi-step processes
- Action trajectories are encoded as structured data for execution
- The combined dataset contains 438 unique task instances across various household domains

## Core Components

### 1. Goal Interpretation Module

Processes natural language goals to extract entities, relations, and intent. This module:
- Parses input text to identify key components
- Maps natural language to formal representations
- Handles ambiguity and provides clarification when needed

### 2. Subgoal LTL Integration

Decomposes complex goals into subgoals and creates LTL specifications:
- Breaks down multi-step tasks into manageable components
- Formulates temporal constraints using LTL logic
- Ensures subgoals maintain correct ordering and dependencies

### 3. Transition Model Construction

Models state transitions between actions and environments:
- Creates state space representation of environments
- Defines valid transitions between states
- Maps actions to state changes

### 4. Action Sequence Generation

Produces executable action sequences:
- Generates step-by-step plans to achieve goals
- Validates actions against environment constraints
- Optimizes for efficiency and correctness

## Implementation Details

### English-Language Support

All key components have been implemented with English language support:
- `combine_results_en.py`: Main submission script with English comments and output
- `sample_goals_en.json`: Example goals in English format
- Comprehensive English documentation and error messages

### Simulation Environment Configuration

The system supports multiple simulation environments:
- **iGibson**: Interactive Gibson environment with photorealistic 3D scenes
- **Behavior**: Behavior simulation environment with diverse household tasks

Configuration options include:
- Environment parameters and settings
- Physics engine configuration
- Task-specific parameters
- Integration with evaluation tools

### Test Framework

The project includes a robust testing framework:
- `run_simulation_tests.py`: Simulates testing in configured environments
- Supports multiple trials per goal
- Generates detailed test reports in JSON and Markdown formats
- Provides success metrics and execution statistics

## Usage Instructions

### Setup

1. Ensure Python 3.8+ is installed
2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Configure the simulation environment:
   ```
   python setup_simulation.py
   ```

### Running the System

1. Process natural language goals using the English script:
   ```
   python combine_results_en.py --goals sample_goals_en.json --output results.json
   ```

2. Run simulation tests:
   ```
   python run_simulation_tests.py --env both --trials 3
   ```

3. Check the results in the `simulation_results` directory

### Configuration Options

Key configuration parameters are available in:
- `simulation_config.yaml`: Environment and simulation settings
- Command-line arguments for running scripts

## Evaluation Metrics

The system tracks the following metrics during testing:
- Success rate: Percentage of goals completed successfully
- Execution time: Time taken to complete each goal
- Steps taken: Number of actions executed
- Path length: Distance traveled by the agent
- Action accuracy: Correctness of performed actions
- Collision count: Number of physical collisions

## Limitations and Future Work

### Current Limitations
- Simulation may not fully replicate real-world physics constraints
- Natural language understanding limited to specific domains
- Environment configuration requires manual setup

### Future Improvements
- Enhanced natural language understanding for more complex instructions
- Integration with additional simulation environments
- Real-time visualization of the planning process
- Automated parameter tuning for optimal performance

## Team Information

This project is submitted for the EAI Challenge with the goal of creating an interpretable interface for embodied AI agents that can understand and execute complex household tasks specified in natural language.

## License

This project is licensed under the MIT License. See LICENSE file for details.

---

**Last Updated:** June 2023
**Version:** 1.0.0
