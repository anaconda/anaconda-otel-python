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
    print_metrics_header,
    print_metrics_summary
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




def main():
    """Main execution function"""
    print_metrics_header()
    
    # Track results
    results = {}
    
    # Run each example
    for i, example in enumerate(EXAMPLES, 1):
        example_name = Path(example).stem
        print(f"\n[{i}/{len(EXAMPLES)}] Running: {example_name}")
        
        success, errors = run_example_subprocess(example)
        results[example] = (success, errors)
    
    # Print summary
    print_metrics_summary(results)
    
    # Exit with appropriate code
    all_success = all(success for success, _ in results.values())
    sys.exit(0 if all_success else 1)


if __name__ == "__main__":
    main()
