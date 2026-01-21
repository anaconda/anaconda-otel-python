#!/usr/bin/env python3
"""
Run Metrics Examples

This script runs all metrics examples in sequence. Each example demonstrates
different aspects of metrics with OpenTelemetry.

Usage:
    python run_metrics_examples.py

Examples included:
    1. 14_metrics_counters.py - Counter metrics for monotonically increasing values
    2. 15_metrics_histogram.py - Histogram metrics for distributions
    3. 16_metrics_updown.py - Up/down counters for values that can increase or decrease
    4. 17_metrics_attributes.py - Multi-dimensional metrics with attributes
    5. 18_metrics_patterns.py - Real-world metrics patterns and best practices
    6. 19_metrics_flush.py - Explicit flush for short-lived processes

Backend Validation:
    After running, you should see 6 services in the backend:
    - example-14-metrics-counters
    - example-15-metrics-histogram
    - example-16-metrics-updown
    - example-17-metrics-attributes
    - example-18-metrics-patterns
    - example-19-metrics-flush
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
    "examples/14_metrics_counters.py",
    "examples/15_metrics_histogram.py",
    "examples/16_metrics_updown.py",
    "examples/17_metrics_attributes.py",
    "examples/18_metrics_patterns.py",
    "examples/19_metrics_flush.py",
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
    print_header("Running Metrics Examples")
    print("This will run all metrics examples in sequence.")
    print("Each example demonstrates different metrics capabilities.")
    
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
        title="Metrics Examples",
        emoji="📊"
    )
    
    # Print error highlights
    print_error_highlights(all_errors, error_by_example)
    
    # Final status
    if success_count == total_count:
        print("\n✅ All metrics examples completed successfully!")
        
        if all_errors:
            print("   ⚠️  However, some HTTP errors were detected during execution")
            print("   ⚠️  See error details above")
    else:
        print("\n❌ Some examples failed - check output above for errors")
    
    # Backend validation info
    print("\n💡 To validate in backend:")
    print("   Expected services:")
    print("     1. example-14-metrics-counters")
    print("     2. example-15-metrics-histogram")
    print("     3. example-16-metrics-updown")
    print("     4. example-17-metrics-attributes")
    print("     5. example-18-metrics-patterns")
    print("     6. example-19-metrics-flush")
    print("\n   Each service should have metrics with:")
    print("     • Proper metric types (counter, histogram, up/down counter)")
    print("     • Resource attributes")
    print("     • Metric-level attributes (where applicable)")
    print("     • Correct values and aggregations")
    
    print("=" * 80 + "\n")
    
    # Exit with appropriate code
    all_success = all(success for success, _ in results.values())
    sys.exit(0 if all_success else 1)


if __name__ == "__main__":
    main()
