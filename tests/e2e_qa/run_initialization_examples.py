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
    print_examples_summary,
    print_error_highlights
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

def print_header():
    """Print script header"""
    print("\n" + "=" * 70)
    print("  Running Initialization Examples")
    print("=" * 70)
    print("  Each example runs in a separate process for proper initialization")
    print("-" * 70)
    
    # Show environment
    env, endpoint, use_console, endpoints = load_environment()
    print(f"  Environment: {env}")
    print(f"  Endpoint: {endpoint}")
    print(f"  Console Exporter: {use_console}")
    
    if use_console:
        print("\n  ⚠️  WARNING: Console exporter is enabled!")
        print("     Data will be printed to console but NOT sent to backend.")
        print("     Set OTEL_CONSOLE_EXPORTER=false for backend validation.")
    else:
        print("\n  ✓ Console exporter is disabled - data will be sent to backend")
    
    print("=" * 70 + "\n")


def run_example(script_path: str) -> Tuple[bool, List[str]]:
    """
    Run a single example script as a subprocess.
    
    Args:
        script_path: Path to the example script
        
    Returns:
        Tuple of (success: bool, errors: List[str])
    """
    return run_example_subprocess(script_path)


def print_summary(results: Dict[str, Tuple[bool, List[str]]], 
                  config_results: Dict[str, Tuple[bool, List[str]]] = None):
    """Print summary of all examples with error highlights"""
    print("\n" + "=" * 70)
    print("📋 SUMMARY")
    print("=" * 70)
    
    # Collect all errors
    all_errors = []
    all_error_by_example = {}
    
    # Check if console exporter is enabled
    _, _, use_console, _ = load_environment()
    if use_console:
        print("\n⚠️  CRITICAL WARNING:")
        print("   OTEL_CONSOLE_EXPORTER=true in .env")
        print("   Data is ONLY printed to console, NOT sent to backend!")
        print("   To validate in backend: Set OTEL_CONSOLE_EXPORTER=false")
        print("=" * 70)
    
    # Configuration examples summary
    config_success = 0
    if config_results:
        config_success, _, error_by_example = print_examples_summary(
            config_results, 
            title="Configuration Examples",
            emoji="📚"
        )
        all_error_by_example.update(error_by_example)
        for errors in error_by_example.values():
            all_errors.extend(errors)
    
    # Initialization examples summary
    success_count, total_count, error_by_example = print_examples_summary(
        results,
        title="Initialization Examples",
        emoji="🚀"
    )
    all_error_by_example.update(error_by_example)
    for errors in error_by_example.values():
        all_errors.extend(errors)
    
    # Overall summary
    total_all = total_count + (len(config_results) if config_results else 0)
    success_all = success_count + config_success
    
    # Print error highlights
    print_error_highlights(all_errors, all_error_by_example)
    
    # Final status
    if success_all == total_all:
        print("\n✅ All examples completed successfully!")
        
        if all_errors:
            print("   ⚠️  However, some HTTP errors were detected during execution")
            print("   ⚠️  See error details above")
        
        if not use_console:
            print("\n💡 To validate in backend:")
            print("   1. Wait 1-5 minutes for backend processing")
            print("   2. Query by service names:")
            print("      - example-01-all-signals")
            print("      - example-02-metrics-only")
            print("      - example-03-default")
            print("      - example-04-selective")
            print("      - example-05-complete")
            print("      - example-06-env-based")
            print("      - example-07-flush-test")
            print("   3. Each service should have 1 metric with value=1")
    else:
        print("\n❌ Some examples failed - check output above for errors")
    
    print("=" * 70 + "\n")


def run_config_example(script_path: str) -> Tuple[bool, List[str]]:
    """
    Run a configuration example script (doesn't initialize telemetry).
    
    Args:
        script_path: Path to the example script
        
    Returns:
        Tuple of (success: bool, errors: List[str])
    """
    return run_example_subprocess(script_path)


def main():
    """Main execution function"""
    print_header()
    
    # Track results (now includes errors)
    config_results = {}
    init_results = {}
    
    # Run configuration examples first (they don't initialize telemetry)
    print("\n" + "=" * 70)
    print("📚 CONFIGURATION EXAMPLES")
    print("=" * 70)
    print("These examples demonstrate configuration without initializing telemetry\n")
    
    for example in CONFIG_EXAMPLES:
        script_path = Path(__file__).parent / example
        
        if not script_path.exists():
            print(f"\n❌ Example not found: {example}")
            config_results[example] = (False, [f"File not found: {example}"])
            continue
        
        print(f"\n{'─' * 70}")
        print(f"Running: {example}")
        print(f"{'─' * 70}")
        
        success, errors = run_config_example(str(script_path))
        config_results[example] = (success, errors)
        
        if not success:
            print(f"\n⚠️  Example failed, but continuing with remaining examples...")
    
    # Run initialization examples (each in separate process)
    print("\n" + "=" * 70)
    print("🚀 INITIALIZATION EXAMPLES")
    print("=" * 70)
    print("Each example runs in a separate process for proper initialization\n")
    
    for example in EXAMPLES:
        script_path = Path(__file__).parent / example
        
        if not script_path.exists():
            print(f"\n❌ Example not found: {example}")
            init_results[example] = (False, [f"File not found: {example}"])
            continue
        
        print(f"\n{'─' * 70}")
        print(f"Running: {example}")
        print(f"{'─' * 70}")
        
        success, errors = run_example(str(script_path))
        init_results[example] = (success, errors)
        
        if not success:
            print(f"\n⚠️  Example failed, but continuing with remaining examples...")
    
    # Print summary
    print_summary(init_results, config_results)
    
    # Exit with error if any failed
    if not all(s for s, _ in config_results.values()) or not all(s for s, _ in init_results.values()):
        sys.exit(1)


if __name__ == "__main__":
    main()
