#!/usr/bin/env python3
"""
Run Logging Examples

This script runs all logging examples in sequence. Each example demonstrates
different aspects of logging with OpenTelemetry.

Usage:
    python run_logging_examples.py

Examples included:
    1. 08_logging_basic.py - Basic logging with telemetry handler
    2. 09_logging_levels.py - All Python logging levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    3. 10_logging_structured.py - Structured logging with attributes
    4. 11_logging_multiple.py - Multiple named loggers for different components
    5. 12_logging_integration.py - Integration with metrics and traces
    6. 13_logging_flush.py - Explicit flush for short-lived processes

Backend Validation:
    After running, you should see 6 services in the backend:
    - example-08-logging-basic
    - example-09-logging-levels
    - example-10-logging-structured
    - example-11-logging-multiple
    - example-12-logging-integration
    - example-13-logging-flush
"""

import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Add examples directory to sys.path for utils imports
examples_dir = Path(__file__).parent / "examples"
sys.path.insert(0, str(examples_dir))

from utils.print_utils import (
    run_example_subprocess,
    print_examples_summary,
    print_error_highlights
)

# Examples to run (in order)
EXAMPLES = [
    "examples/08_logging_basic.py",
    "examples/09_logging_levels.py",
    "examples/10_logging_structured.py",
    "examples/11_logging_multiple.py",
    "examples/12_logging_integration.py",
    "examples/13_logging_flush.py",
]


def print_header(title: str):
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_section(section_name: str):
    """Print a formatted section header."""
    print(f"\n--- {section_name} ---")


def run_example(example_path: str) -> Tuple[bool, List[str]]:
    """
    Run a single example script.
    
    Args:
        example_path: Path to the example script
        
    Returns:
        Tuple of (success: bool, errors: List[str])
    """
    return run_example_subprocess(example_path)


def main():
    print_header("Running Logging Examples")
    print("This will run all logging examples in sequence.")
    print("Each example demonstrates different logging capabilities.")
    
    # Track results (now includes errors)
    results = {}
    all_errors = []
    
    # Run each example
    for i, example in enumerate(EXAMPLES, 1):
        example_name = Path(example).stem
        print_section(f"Example {i}/{len(EXAMPLES)}: {example_name}")
        
        success, errors = run_example(example)
        results[example] = (success, errors)
        all_errors.extend(errors)
        
        if success:
            print(f"✓ {example_name} completed successfully")
        else:
            print(f"✗ {example_name} failed")
    
    # Print summary with error highlights
    print("\n" + "=" * 80)
    print("📋 SUMMARY")
    print("=" * 80)
    
    # Use utility function for consistent summary
    success_count, total_count, error_by_example = print_examples_summary(
        results,
        title="Logging Examples",
        emoji="📝"
    )
    
    # Print error highlights
    print_error_highlights(all_errors, error_by_example)
    
    # Final status
    if success_count == total_count:
        print("\n✅ All logging examples completed successfully!")
        
        if all_errors:
            print("   ⚠️  However, some HTTP errors were detected during execution")
            print("   ⚠️  See error details above")
    else:
        print("\n❌ Some examples failed - check output above for errors")
    
    # Backend validation info
    print("\n💡 To validate in backend:")
    print("   Expected services:")
    print("     1. example-08-logging-basic")
    print("     2. example-09-logging-levels")
    print("     3. example-10-logging-structured")
    print("     4. example-11-logging-multiple")
    print("     5. example-12-logging-integration")
    print("     6. example-13-logging-flush")
    print("\n   Each service should have log records with:")
    print("     • Proper severity levels")
    print("     • Resource attributes")
    print("     • Structured attributes (where applicable)")
    print("     • Logger names (where applicable)")
    
    print("=" * 80 + "\n")
    
    # Exit with appropriate code
    all_success = all(success for success, _ in results.values())
    sys.exit(0 if all_success else 1)


if __name__ == "__main__":
    main()
