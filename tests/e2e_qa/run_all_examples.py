#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0

"""
Run All E2E QA Examples

This script runs all example modules to demonstrate the complete
Anaconda OpenTelemetry SDK functionality.

IMPORTANT: Initialization examples run via subprocess to ensure proper
telemetry initialization (OpenTelemetry only allows one init per process).
"""

import sys
import time
import subprocess
from pathlib import Path

# Add examples directory to sys.path for dynamic imports
examples_dir = Path(__file__).parent / "examples"
sys.path.insert(0, str(examples_dir))

from utils import print_example_header, print_success, print_info


def run_example_module(module_name: str, description: str):
    """
    Run a single example module.
    
    Args:
        module_name: Name of the module to import and run
        description: Description of what the module demonstrates
    """
    print_example_header(f"Running: {module_name}", description)
    
    try:
        # Import the module
        module = __import__(module_name.replace('.py', ''))
        
        # Run the examples
        if hasattr(module, 'run_all_examples'):
            module.run_all_examples()
        else:
            print_info(f"Warning: {module_name} does not have run_all_examples() function")
        
        print_success(f"Completed: {module_name}\n")
        return True
        
    except Exception as e:
        print(f"\n❌ Error running {module_name}: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_initialization_examples():
    """
    Run initialization examples via subprocess.
    
    CRITICAL: Must run in separate processes because OpenTelemetry
    only allows one initialization per process.
    """
    print_info("Starting initialization examples (via subprocess)...")
    
    try:
        script_path = Path(__file__).parent / "run_initialization_examples.py"
        result = subprocess.run(
            [sys.executable, str(script_path)],
            check=True,
            capture_output=False
        )
        print_success("Completed: initialization examples\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error running initialization examples: exit code {e.returncode}")
        return False
    except Exception as e:
        print(f"\n❌ Error running initialization examples: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main entry point for running all examples"""
    print("\n" + "=" * 70)
    print("  Anaconda OpenTelemetry SDK - E2E QA Examples")
    print("=" * 70)
    print("\n  This script demonstrates all SDK functionality through")
    print("  simple, runnable examples.\n")
    print("=" * 70 + "\n")
    
    # Define examples to run (modules that can run in same process)
    examples = [
        ("01_config_examples", "Configuration class and methods"),
        ("02_attributes_examples", "ResourceAttributes class and methods"),
    ]
    
    results = {}
    
    # Run each example module
    for module_name, description in examples:
        print_info(f"Starting {module_name}...")
        success = run_example_module(module_name, description)
        results[module_name] = success
        
        print_info("Waiting before next example...\n")
        time.sleep(2)
    
    # Run initialization examples (must be in separate processes)
    success = run_initialization_examples()
    results["initialization_examples"] = success
    
    # Print summary
    print("\n" + "=" * 70)
    print("  SUMMARY")
    print("=" * 70)
    
    total = len(results)
    passed = sum(1 for success in results.values() if success)
    failed = total - passed
    
    print(f"\n  Total examples: {total}")
    print(f"  Passed: {passed}")
    print(f"  Failed: {failed}\n")
    
    for module_name, success in results.items():
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"  {status}: {module_name}")
    
    print("\n" + "=" * 70)
    
    if failed > 0:
        print_info("\n⚠️  Some examples failed. Check the output above for details.")
        sys.exit(1)
    else:
        print_success("\n🎉 All examples completed successfully!")
        print_info("You can now run individual example categories:")
        print_info("  python examples/01_config_examples.py")
        print_info("  python examples/02_attributes_examples.py")
        print_info("  python run_initialization_examples.py")
        print("\n" + "=" * 70 + "\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
