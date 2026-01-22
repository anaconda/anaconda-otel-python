#!/usr/bin/env python3
"""
Run All Initialization Examples

Executes each initialization example as a separate process to ensure
proper telemetry initialization for each service.

CRITICAL: Each example MUST run in its own process because OpenTelemetry
only allows one initialization per process. Running all examples in a
single script would cause only the first initialization to succeed.
"""

import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Add examples directory to sys.path for utils imports
examples_dir = Path(__file__).parent / "examples"
sys.path.insert(0, str(examples_dir))

from utils import load_environment
from utils.print_utils import (
    run_example_subprocess,
    print_initialization_header,
    print_initialization_summary
)

# Example scripts to run (in order)
EXAMPLES = [
    "examples/01_all_signals.py",
    "examples/02_metrics_only.py",
    "examples/03_default.py",
    "examples/04_selective.py",
    "examples/05_complete.py",
    "examples/06_env_based.py",
    "examples/07_flush_test.py",
]

# Configuration/demonstration examples (run without subprocess)
CONFIG_EXAMPLES = [
    "examples/01_config_examples.py",
    "examples/02_attributes_examples.py",
]





def main():
    """Main execution function"""
    # Load environment and print header
    env, endpoint, use_console, endpoints = load_environment()
    print_initialization_header(env, endpoint, use_console)
    
    # Track results (now includes errors)
    config_results = {}
    init_results = {}
    
    # Run configuration examples first (they don't initialize telemetry)
    print("\n" + "=" * 70)
    print("[CONFIG] CONFIGURATION EXAMPLES")
    print("=" * 70)
    print("These examples demonstrate configuration without initializing telemetry\n")
    
    for example in CONFIG_EXAMPLES:
        script_path = Path(__file__).parent / example
        
        if not script_path.exists():
            print(f"\n[FAIL] Example not found: {example}")
            config_results[example] = (False, [f"File not found: {example}"])
            continue
        
        print(f"\nRunning: {example}")
        success, errors = run_example_subprocess(str(script_path))
        config_results[example] = (success, errors)
    
    # Run initialization examples (each in separate process)
    print("\n" + "=" * 70)
    print("[INIT] INITIALIZATION EXAMPLES")
    print("=" * 70)
    print("Each example runs in a separate process for proper initialization\n")
    
    for example in EXAMPLES:
        script_path = Path(__file__).parent / example
        
        if not script_path.exists():
            print(f"\n[FAIL] Example not found: {example}")
            init_results[example] = (False, [f"File not found: {example}"])
            continue
        
        print(f"\nRunning: {example}")
        success, errors = run_example_subprocess(str(script_path))
        init_results[example] = (success, errors)
    
    # Print summary
    print_initialization_summary(init_results, config_results, use_console)
    
    # Exit with error if any failed
    if not all(s for s, _ in config_results.values()) or not all(s for s, _ in init_results.values()):
        sys.exit(1)


if __name__ == "__main__":
    main()
