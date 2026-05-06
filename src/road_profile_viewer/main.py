"""
Road Profile Viewer - Interactive 2D Visualization
===================================================
This module contains the entire application in a single file (intentionally monolithic
for educational purposes). It creates an interactive Dash application that visualizes:
- A road profile represented by a clothoid-like curve
- A camera mounted at position (0, 1.5)
- A ray from the camera that can be rotated by the user
- The intersection point between the ray and the road profile
- Distance information on hover
"""

from road_profile_viewer.visualization import create_dash_app

# =============================================================================
# MAIN ENTRY POINT
# =============================================================================


def main() -> None:
    """
    Main function to run the Dash application.
    """
    app = create_dash_app()
    print("Starting Road Profile Viewer...")
    print("Open your browser and navigate to: http://127.0.0.1:8050/")
    print("Press Ctrl+C to stop the server.")
    app.run(debug=True)  # pyright: ignore[reportUnknownMemberType]


if __name__ == "__main__":
    main()
