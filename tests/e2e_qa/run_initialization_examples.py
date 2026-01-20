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

# Add examples directory to sys.path for utils imports
examples_dir = Path(__file__).parent / "examples"
sys.path.insert(0, str(examples_dir))

from utils import load_environment

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

def print_header():
    """Print script header"""
    print("\n" + "=" * 70)
    print("  Running Initialization Examples")
    print("=" * 70)
    print("  Each example runs in a separate process for proper initialization")
    print("-" * 70)
    
    # Show environment
    env, endpoint, use_console = load_environment()
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


def run_example(script_path: str) -> bool:
    """
    Run a single example script as a subprocess.
    
    Args:
        script_path: Path to the example script
        
    Returns:
        True if successful, False otherwise
    """
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            check=True,
            capture_output=False,  # Show output in real-time
            text=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Example failed: {script_path}")
        print(f"   Exit code: {e.returncode}")
        return False
    except Exception as e:
        print(f"\n❌ Error running example: {script_path}")
        print(f"   Error: {e}")
        return False


def print_summary(results: dict):
    """Print summary of all examples"""
    print("\n" + "=" * 70)
    print("📋 BACKEND VALIDATION SUMMARY")
    print("=" * 70)
    
    # Check if console exporter is enabled
    _, _, use_console = load_environment()
    if use_console:
        print("\n⚠️  CRITICAL WARNING:")
        print("   OTEL_CONSOLE_EXPORTER=true in .env")
        print("   Data is ONLY printed to console, NOT sent to backend!")
        print("   To validate in backend: Set OTEL_CONSOLE_EXPORTER=false")
        print("=" * 70)
    
    print("\n📊 Examples Run:")
    success_count = 0
    total_count = len(results)
    
    for script, success in results.items():
        status = "✓" if success else "❌"
        print(f"   {status} {script}")
        if success:
            success_count += 1
    
    print(f"\n   Total: {success_count}/{total_count} successful")
    
    if success_count == total_count:
        print("\n✅ All examples completed successfully!")
        
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
            print("\n   See BACKEND_VALIDATION_GUIDE.md for detailed instructions")
    else:
        print("\n❌ Some examples failed - check output above for errors")
    
    print("=" * 70 + "\n")


def main():
    """Main execution function"""
    print_header()
    
    # Track results
    results = {}
    
    # Run each example
    for example in EXAMPLES:
        script_path = Path(__file__).parent / example
        
        if not script_path.exists():
            print(f"\n❌ Example not found: {example}")
            results[example] = False
            continue
        
        print(f"\n{'─' * 70}")
        print(f"Running: {example}")
        print(f"{'─' * 70}")
        
        success = run_example(str(script_path))
        results[example] = success
        
        if not success:
            print(f"\n⚠️  Example failed, but continuing with remaining examples...")
    
    # Print summary
    print_summary(results)
    
    # Exit with error if any failed
    if not all(results.values()):
        sys.exit(1)


if __name__ == "__main__":
    main()
