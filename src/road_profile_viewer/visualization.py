import numpy as np
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html

from .geometry import find_intersection
from .road import generate_road_profile


def create_dash_app() -> Dash:
    """
    Create and configure the Dash application.

    Returns:
    --------
    Dash
        Configured Dash application instance
    """
    # Initialize the Dash app
    app = Dash(__name__)

    # Define the layout
    app.layout = html.Div([
        html.H1(
            "Road Profile Viewer with Camera Ray Intersection",
            style={
                "textAlign": "center",
                "color": "#2c3e50",
                "marginBottom": "20px",
            },
        ),
        html.Div(
            [
                html.Label(
                    "Camera Ray Angle (degrees from horizontal):",
                    style={"fontWeight": "bold", "marginRight": "10px"},
                ),
                dcc.Input(  # pyright: ignore[reportPrivateImportUsage]
                    id="angle-input",
                    type="number",
                    value=-1.1,
                    step=0.1,
                    style={
                        "marginRight": "20px",
                        "padding": "5px",
                        "width": "100px",
                    },
                ),
                html.Span(
                    id="intersection-info",
                    style={"color": "#e74c3c", "fontWeight": "bold"},
                ),
            ],
            style={
                "textAlign": "center",
                "marginBottom": "20px",
                "padding": "10px",
            },
        ),
        dcc.Graph(id="road-profile-graph", style={"height": "400px"}),  # pyright: ignore[reportPrivateImportUsage]
        html.Div(
            [
                html.H3("Instructions:", style={"color": "#2c3e50"}),
                html.Ul([
                    html.Li("The dark grey line represents the road profile"),
                    html.Li("The red point at (0, 2.0) represents the camera position"),
                    html.Li("The blue line shows the camera ray at the specified angle"),
                    html.Li("The green point shows where the ray intersects the road"),
                    html.Li("Hover over the green point to see the distance from camera to intersection"),
                    html.Li("Adjust the angle to see how the intersection point changes"),
                    html.Li("Positive angles point downward, negative angles point upward"),
                ]),
            ],
            style={
                "margin": "20px",
                "padding": "20px",
                "backgroundColor": "#ecf0f1",
                "borderRadius": "5px",
            },
        ),
    ])

    # Define the callback to update the graph
    @app.callback(  # pyright: ignore[reportUnknownMemberType]
        [
            Output("road-profile-graph", "figure"),
            Output("intersection-info", "children"),
        ],
        [Input("angle-input", "value")],
    )
    def update_graph(angle: float | None) -> tuple[go.Figure, str]:  # pyright: ignore[reportUnusedFunction]
        """
        Update the graph based on the input angle.

        Parameters:
        -----------
        angle : float
            Camera ray angle in degrees

        Returns:
        --------
        tuple
            (plotly figure, info text)
        """
        if angle is None:
            angle = -1.1

        x_max = 80.0

        # Generate road profile
        x_road, y_road = generate_road_profile(num_points=100, x_max=x_max)

        # Camera position
        camera_x, camera_y = 0, 2.0

        # Find intersection first to determine ray length
        x_intersect, y_intersect, distance = find_intersection(x_road, y_road, angle, camera_x, camera_y)

        # Calculate adaptive ray line based on intersection
        if x_intersect is not None:
            # Ray goes from camera to intersection point
            x_ray = np.array([camera_x, x_intersect])
            y_ray = np.array([camera_y, y_intersect])
        else:
            # No intersection - show a short ray (20 units or to edge of plot)
            angle_rad = -np.deg2rad(angle)
            if np.abs(np.cos(angle_rad)) < 1e-10:
                # Vertical line
                x_ray = np.array([camera_x, camera_x])
                y_ray = np.array([camera_y, camera_y - 10])
            else:
                slope = np.tan(angle_rad)
                x_end = min(camera_x + 20, x_max)
                y_end = camera_y + slope * (x_end - camera_x)
                x_ray = np.array([camera_x, x_end])
                y_ray = np.array([camera_y, y_end])

        # Create figure
        fig = go.Figure()

        # Add road profile
        fig.add_trace(
            go.Scatter(
                x=x_road,
                y=y_road,
                mode="lines+markers",
                name="Road Profile",
                line={"color": "#4a4a4a", "width": 3},
                marker={"size": 4, "color": "#4a4a4a"},
                hovertemplate="Road<br>x: %{x:.2f}<br>y: %{y:.2f}<extra></extra>",
            )
        )

        # Add camera point
        fig.add_trace(
            go.Scatter(
                x=[camera_x],
                y=[camera_y],
                mode="markers",
                name="Camera",
                marker={
                    "size": 12,
                    "color": "red",
                    "symbol": "circle",
                },
                hovertemplate="Camera<br>Position: (%{x:.2f}, %{y:.2f})<extra></extra>",
            )
        )

        # Add camera ray - This comment previously exceeded the line length limit
        # specified in PEP8 style guide (79 chars) and ruff default (120 chars)
        fig.add_trace(
            go.Scatter(
                x=x_ray,
                y=y_ray,
                mode="lines",
                name=f"Camera Ray ({angle}°)",
                line={"color": "blue", "width": 2, "dash": "dash"},
                hovertemplate="Camera Ray<br>x: %{x:.2f}<br>y: %{y:.2f}<extra></extra>",
            )
        )

        # Add intersection point if it exists
        info_text = ""
        if x_intersect is not None:
            hover_text = (
                f"Intersection Point<br>Position: ({x_intersect:.2f}, {y_intersect:.2f})<br>"
                f"Distance from camera: {distance:.2f}<extra></extra>"
            )
            fig.add_trace(
                go.Scatter(
                    x=[x_intersect],
                    y=[y_intersect],
                    mode="markers",
                    name="Intersection",
                    marker={"size": 15, "color": "green", "symbol": "star"},
                    hovertemplate=hover_text,
                )
            )
            info_text = f"Intersection found at ({x_intersect:.2f}, {y_intersect:.2f}) | Distance: {distance:.2f} units"
        else:
            info_text = "No intersection found with current angle"

        # Update layout
        fig.update_layout(
            xaxis_title="X Position (m)",
            yaxis_title="Y Position (m)",
            hovermode="closest",
            showlegend=True,
            legend={
                "x": 1.02,
                "y": 1,
                "xanchor": "left",
                "yanchor": "top",
                "bgcolor": "rgba(255,255,255,0.8)",
                "bordercolor": "#dee2e6",
                "borderwidth": 1,
            },
            plot_bgcolor="#f8f9fa",
            xaxis={"gridcolor": "#dee2e6", "range": [-2, x_max + 2], "constrain": "domain"},
            yaxis={
                "gridcolor": "#dee2e6",
                "scaleanchor": "x",
                "scaleratio": 1,
                "range": [-0.5, 10],
                "constrain": "domain",
            },
            margin={"l": 50, "r": 150, "t": 30, "b": 50},
        )

        return fig, info_text

    return app
