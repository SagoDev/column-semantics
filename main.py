"""Column Semantics - Main Launcher

This script serves as a launcher for running different examples
of column_semantics library.
"""

import importlib.util
from pathlib import Path


def run_example_file(filename: str):
    """Run an example file by importing and executing its main function."""
    examples_dir = Path(__file__).parent / "examples"
    file_path = examples_dir / filename

    # Load the module from file
    spec = importlib.util.spec_from_file_location("example_module", file_path)
    if spec is None:
        raise ImportError(f"Could not load spec from {file_path}")

    module = importlib.util.module_from_spec(spec)

    # Execute the module
    if spec.loader is None:
        raise ImportError(f"Could not get loader for {file_path}")

    spec.loader.exec_module(module)

    # Run the main function if it exists
    if hasattr(module, "main"):
        module.main()


def main():
    """Main launcher for examples."""

    print("Column Semantics - Example Launcher")
    print("=" * 40)
    print("\nAvailable examples:")
    print("1. Basic Analysis - Learn fundamental usage")
    print("2. Report Generation - Generate PDF, JSON, and text reports")
    print("3. Practical Recommendations - Data engineering best practices")
    print("4. Complete Analysis - Comprehensive example with all features")
    print("5. Run All Examples - Execute all examples sequentially")
    print("0. Exit")

    while True:
        try:
            choice = input("\nSelect an example (1-5, 0 to exit): ").strip()

            if choice == "0":
                print("Goodbye!")
                break
            elif choice == "1":
                print("\n--- Running Basic Analysis Example ---")
                run_example_file("01_basic_analysis.py")
            elif choice == "2":
                print("\n--- Running Report Generation Example ---")
                run_example_file("02_report_generation.py")
            elif choice == "3":
                print("\n--- Running Practical Recommendations Example ---")
                run_example_file("03_practical_recommendations.py")
            elif choice == "4":
                print("\n--- Running Complete Analysis Example ---")
                run_example_file("04_complete_analysis.py")
            elif choice == "5":
                print("\n--- Running All Examples ---")

                examples = [
                    ("Basic Analysis", "01_basic_analysis.py"),
                    ("Report Generation", "02_report_generation.py"),
                    ("Practical Recommendations", "03_practical_recommendations.py"),
                    ("Complete Analysis", "04_complete_analysis.py"),
                ]

                for name, filename in examples:
                    print(f"\n{'='*50}")
                    print(f"Running {name}")
                    print("=" * 50)

                    try:
                        run_example_file(filename)
                        print(f"✓ {name} completed successfully")
                    except Exception as e:
                        print(f"✗ Error in {name}: {e}")

                    input("\nPress Enter to continue to next example...")

                print("\n✓ All examples completed!")
            else:
                print("Invalid choice. Please enter 1-5, or 0 to exit.")

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
