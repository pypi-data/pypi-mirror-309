"""Define the solara interface to run and control the HistoricalLetters model."""
from __future__ import annotations

import matplotlib.pyplot as plt
import mesa_geo as mg
import mesa_geo.visualization as mgv
import solara
import xyzservices.providers as xyz
from matplotlib import colors
from matplotlib.figure import Figure

from scicom.historicalletters.agents import (
    RegionAgent,
    SenderAgent,
)
from scicom.historicalletters.model import HistoricalLetters


def topic_draw(agent:mg.GeoAgent) -> dict:
    """Define visualization strategies for agents.

    Region agents get the main color as a mean of
    all region agents topic vectors.

    Sender agents have the color of their current
    topic vector.
    """
    portrayal = {}
    if isinstance(agent, RegionAgent):
        color = colors.to_hex(agent.has_main_topic())
        portrayal["color"] = color
    elif isinstance(agent, SenderAgent):
        colortuple = set(agent.topicVec)
        portrayal["marker_type"] = "AwesomeIcon"
        portrayal["name"] = "fas fa-male"
        portrayal["icon_properties"] = {
                "marker_color": "white",
                "icon_color": colors.to_hex(colortuple),
                }
        portrayal["description"] = str(agent.unique_id)
    return portrayal

model_params = {
    "population": {
        "type": "SliderInt",
        "value": 50,
        "label": "Number of agents",
        "min": 10,
        "max": 200,
        "step": 10,
    },
    "useSocialNetwork": {
        "type": "Select",
        "value": False,
        "label": "Choose if an initial social network exists.",
        "values": [True, False],
    },
    "useActivation": {
        "type": "Select",
        "value": False,
        "label": "Choose if agents have heterogeneous acitvations.",
        "values": [True, False],
    },
    "similarityThreshold": {
        "type": "SliderFloat",
        "value": 0.5,
        "label": "Threshold for similarity of topics.",
        "min": 0.0,
        "max": 1.0,
        "step": 0.1,
    },
    "moveRange": {
        "type": "SliderFloat",
        "value": 0.05,
        "label": "Range defining targets for movements.",
        "min": 0.0,
        "max": 0.5,
        "step": 0.1,
    },
    "letterRange": {
        "type": "SliderFloat",
        "value": 0.2,
        "label": "Range for sending letters.",
        "min": 0.0,
        "max": 0.5,
        "step": 0.1,
    },
}

def plot_data(model:mg.Model) -> solara.FigureMatplotlib:
    """Plot all data in one graph."""
    fig = Figure()
    ax = fig.subplots()
    df = model.datacollector.get_model_vars_dataframe()
    for m in ["Movements", "Letters", "Clusters"]:
        ax.plot(df.loc[:, m], label=m)
    ax.legend(loc="best")
    ax.set_xlabel("Step")
    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    return solara.FigureMatplotlib(fig)


page = mgv.GeoJupyterViz(
    HistoricalLetters,
    model_params,
    measures= [plot_data],
    name="Historical Letters ABM",
    agent_portrayal=topic_draw,
    zoom=4,
    tiles=xyz.OpenTopoMap,
    center_point=[47, 12],
    view=[1024,1024],
)
