"""
Smoke Tests: Verify basic refactoring structure

These tests check that:
1. All modules can be imported without errors
2. Expected functions exist and are callable
3. Basic module structure is correct

Note: These are NOT unit tests (you'll learn those in Lecture 5).
These are just "smoke tests" to verify the refactoring didn't break imports.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def test_imports_work():
    """Test that all refactored modules can be imported."""
    try:
        from road_profile_viewer import geometry, main, road, visualization  # pyright: ignore[reportMissingImports] # noqa: F401
    except ImportError as e:
        raise AssertionError(f"Import failed: {e}")  # noqa: B904

    print("✅ All modules import successfully!")


def test_geometry_functions_exist():
    """Test that geometry module has expected functions."""
    from road_profile_viewer.geometry import calculate_ray_line, find_intersection # pyright: ignore[reportMissingImports]

    assert callable(calculate_ray_line), "calculate_ray_line should be callable"
    assert callable(find_intersection), "find_intersection should be callable"

    print("✅ geometry.py exports correct functions!")


def test_road_functions_exist():
    """Test that road module has expected functions."""
    from road_profile_viewer.road import generate_road_profile # pyright: ignore[reportMissingImports]

    assert callable(generate_road_profile), "generate_road_profile should be callable"

    print("✅ road.py exports correct functions!")


def test_visualization_functions_exist():
    """Test that visualization module has expected functions."""
    from road_profile_viewer.visualization import create_dash_app # pyright: ignore[reportMissingImports]

    assert callable(create_dash_app), "create_dash_app should be callable"

    print("✅ visualization.py exports correct functions!")


def test_main_function_exists():
    """Test that main module has main() function."""
    from road_profile_viewer.main import main # pyright: ignore[reportMissingImports]

    assert callable(main), "main() should be callable"

    print("✅ main.py has main() function!")


if __name__ == "__main__":
    # Allow running tests directly
    print("Running smoke tests...")
    print()

    test_imports_work()
    test_geometry_functions_exist()
    test_road_functions_exist()
    test_visualization_functions_exist()
    test_main_function_exists()

    print()
    print("🎉 All smoke tests passed!")
    print("Your refactoring structure is correct!")
