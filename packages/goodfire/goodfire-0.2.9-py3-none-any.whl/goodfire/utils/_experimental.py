from typing import Dict, List, Optional, Union

import numpy as np

from ..api.client import Client
from ..features.features import Feature, FeatureGroup
from ..variants.variants import VariantInterface


class LatentExplorer:
    """Interactive visualization tool for exploring feature relationships in latent space.

    Uses PCA dimensionality reduction and interactive plotting to visualize feature
    neighborhoods and relationships. Supports clicking features to explore their local
    neighborhoods.

    Args:
        client (Client): Client instance for API communication
        model (Union[str, VariantInterface]): Model or variant to explore
    """

    def __init__(self, client: Client, model: Union[str, VariantInterface]):
        self.client = client
        self.model = model
        self.active_figure = None
        self.scatter_points: Dict[int, Feature] = {}
        self.active_annotation = None

    def _create_scatter_plot(
        self,
        dim_reduction: List[List[float]],
        all_features: FeatureGroup,
        origin: Feature,
        ax,
    ) -> None:
        import matplotlib.pyplot as plt

        """Create scatter plot with proper picking setup"""
        points = np.array(dim_reduction)

        # Use the extra dimension for coloring
        color_values = points[:, -1]
        normalized_colors = (color_values - color_values.min()) / (
            color_values.max() - color_values.min()
        )

        # Create colormap with viridis (better for continuous data)
        colors = plt.cm.viridis(normalized_colors)

        # Make origin point stand out with a different color
        origin_idx = None
        for idx, feature in enumerate(all_features):
            if feature.uuid == origin.uuid:
                origin_idx = idx
                colors[idx] = [1, 0, 0, 1]  # Bright red for origin
                break

        sizes = [100 if feature.uuid == origin.uuid else 50 for feature in all_features]

        display_points = points[:, :3]

        # Create scatter plot based on dimensions
        scatter = ax.scatter3D(
            display_points[:, 0],
            display_points[:, 1],
            display_points[:, 2],
            c=colors,
            s=sizes,
            picker=True,
            alpha=0.6,
        )

        # Add colorbar
        if origin_idx is not None:
            # Create a separate scatter for the colorbar that excludes the origin point
            non_origin_colors = color_values[np.arange(len(color_values)) != origin_idx]
            norm = plt.Normalize(non_origin_colors.min(), non_origin_colors.max())
            sm = plt.cm.ScalarMappable(cmap=plt.cm.viridis, norm=norm)
            sm.set_array([])
            plt.colorbar(sm, ax=ax)

        # Store mapping of point indices to features
        self.scatter_points = {idx: feature for idx, feature in enumerate(all_features)}

        # Store dimension reduction data for hover functionality
        self.dim_reduction = display_points

        return scatter

    def _handle_hover(self, event, ax):
        import matplotlib.pyplot as plt

        """Handle mouse hover events"""
        if not hasattr(self, "scatter") or event.inaxes != ax:
            if self.active_annotation:
                self.active_annotation.remove()
                self.active_annotation = None
                plt.draw()
            return

        cont, ind = self.scatter.contains(event)
        if cont:
            if self.active_annotation:
                self.active_annotation.remove()

            idx = ind["ind"][0]
            feature = self.scatter_points[idx]
            point = self.dim_reduction[idx]

            self.active_annotation = ax.text(
                point[0],
                point[1],
                point[2],
                feature.label,
                fontsize=8,
                alpha=0.9,
                bbox=dict(facecolor="white", alpha=0.7, edgecolor="none"),
            )

            plt.draw()
        elif self.active_annotation:
            self.active_annotation.remove()
            self.active_annotation = None
            plt.draw()

    def _handle_pick(self, event, horizon: int, origin: Feature):
        import matplotlib.pyplot as plt
        from matplotlib.collections import PathCollection

        """Handle pick events on scatter points"""
        if isinstance(event.artist, PathCollection):  # Verify it's a scatter point
            ind = event.ind[0]  # Get the index of picked point
            if ind in self.scatter_points:
                selected_feature = self.scatter_points[ind]
                # Store current window position
                old_geometry = self.active_figure.canvas.window().geometry()
                # Close current plot
                plt.close(self.active_figure)
                # Create new chart
                self.chart(
                    origin=selected_feature,
                    horizon=horizon,
                    _previous_feature=origin,
                    window_geometry=old_geometry,
                )

    def _setup_3d_controls(self, fig, ax):
        """Set up keyboard controls for 3D plot rotation"""

        def on_key(event):
            if event.key == "left":
                ax.view_init(elev=ax.elev, azim=ax.azim - 10)
            elif event.key == "right":
                ax.view_init(elev=ax.elev, azim=ax.azim + 10)
            elif event.key == "up":
                ax.view_init(elev=ax.elev + 10, azim=ax.azim)
            elif event.key == "down":
                ax.view_init(elev=ax.elev - 10, azim=ax.azim)
            fig.canvas.draw()

        fig.canvas.mpl_connect("key_press_event", on_key)

    def chart(
        self,
        origin: Feature,
        horizon: int = 100,
        _previous_feature: Optional[Feature] = None,
        window_geometry: Optional[object] = None,
    ):
        import matplotlib.pyplot as plt

        # Get neighboring features
        local_group = self.client.features._experimental.neighbors(
            origin, model=self.model, top_k=horizon
        )

        # Combine feature groups
        all_features = FeatureGroup([origin]) | local_group
        if _previous_feature:
            all_features = all_features | FeatureGroup([_previous_feature])

        # Perform dimension reduction
        dim_reduction = self.client.features._experimental.dimension_reduction(
            origin, local_group, self.model, 4, "pca"
        )

        # Create figure and axis
        fig = plt.figure(figsize=(10, 8))
        self.active_figure = fig

        ax = fig.add_subplot(111, projection="3d")
        self._setup_3d_controls(fig, ax)

        # Create scatter plot
        self.scatter = self._create_scatter_plot(dim_reduction, local_group, origin, ax)

        # Set up event handlers
        fig.canvas.mpl_connect(
            "pick_event", lambda event: self._handle_pick(event, horizon, origin)
        )
        fig.canvas.mpl_connect(
            "motion_notify_event", lambda event: self._handle_hover(event, ax)
        )

        # Customize plot
        ax.set_title(f"Latent Explorer: {origin.label}")
        ax.grid(True, alpha=0.3, linestyle="--")

        # Add legend with colorbar
        legend_elements = [
            plt.scatter([], [], c="red", alpha=0.6, s=100, label="Current Feature"),
            plt.scatter([], [], c="blue", alpha=0.6, s=50, label="Other Features"),
        ]
        ax.legend(handles=legend_elements, loc="upper right")

        plt.tight_layout()

        # Show the plot and restore window position if available
        plt.show()
        if window_geometry:
            self.active_figure.canvas.window().setGeometry(window_geometry)
