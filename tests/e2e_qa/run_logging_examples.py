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
    print_logging_header,
    print_logging_summary
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




def main():
    """Main execution function"""
    print_logging_header()
    
    # Track results
    results = {}
    
    # Run each example
    for i, example in enumerate(EXAMPLES, 1):
        example_name = Path(example).stem
        print(f"\n[{i}/{len(EXAMPLES)}] Running: {example_name}")
        
        success, errors = run_example_subprocess(example)
        results[example] = (success, errors)
    
    # Print summary
    print_logging_summary(results)
    
    # Exit with appropriate code
    all_success = all(success for success, _ in results.values())
    sys.exit(0 if all_success else 1)


if __name__ == "__main__":
    main()
