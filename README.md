# EAI Challenge: Interpretable Interface Implementation

## Project Overview

This project implements an interpretable interface for the EAI (Embodied AI) Challenge. The system processes natural language goals, decomposes them into subgoals, creates LTL (Linear Temporal Logic) specifications, models state transitions, and generates executable action sequences for embodied agents in simulated environments. The project leverages state-of-the-art tools and technologies, including InterPreT for natural language understanding, AuDeRe for adaptive planning, and LogicGuard for transition validation.

## GitHub-Based Iterative Management

The project follows a structured GitHub workflow to ensure transparent progress tracking and collaborative development:

- **Main Branch**: Contains stable, tested code ready for integration
- **Feature Branches**: Created for each module and major task
- **Pull Requests**: Changes merged via PRs with code reviews
- **Issues**: Tasks tracked with labels (enhancement, bug, testing)
- **Releases**: Key deliverables tagged as GitHub Releases

## Directory Structure

```
eai-interpretable-interface/
├── action_sequencing/          # Action sequencing module with AuDeRe integration
├── config/                     # Configuration files
├── data/                       # Dataset files (behavior and virtualhome)
├── docs/                       # Documentation files
├── embodied-agent-interface/   # Embodied agent interface library
├── goal_interpretation/        # Goal interpretation module with InterPreT
├── integration/                # Module integration code
├── results/                    # Test and execution results
├── scripts/                    # Utility scripts
├── subgoal_decomposition/      # Subgoal decomposition module
├── submission_outputs/         # Final submission outputs
├── tests/                      # Integration and unit tests
├── transition_modeling/        # Transition modeling with LogicGuard
├── utils/                      # Utility functions
├── CODE_REVIEW_INTEGRATION_ANALYSIS.md  # Code review and integration analysis
├── README.md                   # This documentation file
├── environment.yml             # Conda environment configuration
├── final_submission.py         # Final submission script
├── main.py                     # Main entry point
├── requirements.txt            # Python dependencies
├── run_tests.py                # Test runner script
└── work_summary_and_plan.md    # Work summary and planning
```

## Dataset Analysis

The system analyzes and processes two primary datasets located in the `data/` directory:

1. **Behavior Dataset** (`behavior-00000-of-00001.parquet`)
   - Contains 100 rows of data
   - 8 columns including scene_id, task_id, task_name, natural_language_description, etc.
   - Provides diverse household tasks and action sequences

2. **VirtualHome Dataset** (`virtualhome-00000-of-00001.parquet`)
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

Processes natural language goals to extract entities, relations, and intent using InterPreT:
- Parses input text to identify key components
- Maps natural language to formal representations (LTL formulas)
- Handles ambiguity and provides clarification when needed
- Supports English language processing

### 2. Subgoal Decomposition

Decomposes complex goals into subgoals and creates LTL specifications:
- Breaks down multi-step tasks into manageable components
- Formulates temporal constraints using LTL logic
- Ensures subgoals maintain correct ordering and dependencies
- Generates human-understandable subgoals with explicit preconditions and effects

### 3. Transition Modeling

Models state transitions between actions and environments using LogicGuard:
- Creates state space representation of environments
- Defines valid transitions between states
- Maps actions to state changes
- Validates transitions to ensure safety and correctness

### 4. Action Sequencing

Produces executable action sequences with AuDeRe adaptive planning:
- Generates step-by-step plans to achieve goals
- Validates actions against environment constraints
- Optimizes for efficiency and correctness
- Adapts planning algorithms (A* vs BFS) based on task complexity

## Technical Innovation

1. **Adaptive Planning**: The action sequencing module dynamically selects optimal algorithms based on task complexity and environment constraints
2. **Interpretable Subgoal Decomposition**: Generates human-understandable subgoals with explicit LTL formulas for transparency
3. **Integrated Error Detection**: Leverages LogicGuard for state transition validation and error recovery
4. **Robust Testing Framework**: Multi-layered testing strategy including unit, integration, and performance tests

## Implementation Details

### Tools & Dependencies

- **InterPreT**: Natural language understanding and formal representation
- **AuDeRe**: Adaptive planning and action sequencing
- **LogicGuard**: State transition validation and error detection
- **pytest**: Testing framework
- **parquet**: Dataset storage format

### English-Language Support

All key components have been implemented with full English language support:
- English comments and documentation throughout the codebase
- English output formatting and error messages
- Support for English natural language goals

### Simulation Environment Support

The system supports multiple simulation environments:
- **Behavior**: Behavior simulation environment with diverse household tasks
- **VirtualHome**: Virtual home environment with detailed 3D scenes

## Usage Instructions

### Setup

1. Ensure Python 3.8+ is installed
2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. For Conda users, create the environment:
   ```
   conda env create -f environment.yml
   ```

### Running the System

1. Process natural language goals from parquet files:
   ```
   python final_submission.py
   ```

2. Run the main integration:
   ```
   python main.py
   ```

3. Execute tests:
   ```
   python run_tests.py
   ```

### Configuration Options

Key configuration parameters are available in:
- `enhanced_config.yaml`: Module-specific configuration
- `simulation_config.yaml`: Environment and simulation settings
- Command-line arguments for running scripts

## Testing Framework

The project includes a comprehensive testing framework:

- **Unit Tests**: Validate individual modules and components
- **Integration Tests**: Verify module collaboration and end-to-end workflows
- **Performance Tests**: Assess stability and efficiency (memory usage, execution time)
- **Simulation Tests**: Test system behavior in simulated environments

Test results are systematically logged in the `results/` directory and documented in `test_report.md`.

## Evaluation Metrics

The system tracks the following metrics during testing:
- Success rate: Percentage of goals completed successfully
- Execution time: Time taken to complete each goal
- Steps taken: Number of actions executed
- Action accuracy: Correctness of performed actions
- Plan quality: Efficiency and optimality of generated plans

## Results

The system has been extensively tested with both behavior and virtualhome datasets, demonstrating strong performance in processing diverse natural language goals. Key results include:

- Successful processing of complex multi-step tasks
- Adaptive planning for tasks of varying complexity
- Robust handling of errors and edge cases
- Interpretable outputs with clear LTL specifications

Detailed results can be found in the `results/` directory and in the final report.

## Limitations and Future Work

### Current Limitations
- Partial support for complex conditional goals
- Limited BEHAVIOR action library coverage
- Occasional delays in action sequencing for high-complexity tasks

### Future Improvements
- Enhance subgoal decomposition for complex temporal goals
- Expand BEHAVIOR action library to cover more household tasks
- Implement real-time feedback loops for dynamic environment adaptation
- Optimize performance for large-scale datasets

## Team Information

This project is submitted for the EAI Challenge with the goal of creating an interpretable interface for embodied AI agents that can understand and execute complex household tasks specified in natural language.

## License

This project is licensed under the MIT License. See LICENSE file for details.

---

**Last Updated:** December 2024
**Version:** 2.0.0
