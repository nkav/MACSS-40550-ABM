import solara
from model import SchellingModel
from mesa.visualization import (  
    SolaraViz,
    make_space_component,
    make_plot_component,
)

## Define agent portrayal: color, shape, and size
def agent_portrayal(agent):
    transparency = agent.desired_share_alike  # make the agent more transparent if they are less polarized
    color = "blue" if agent.type == 1 else "red"
    return {
        "color": color,  
        "edgecolors": "black", # add edge colors to make agents more visible
        "linewidths": 1,
        "marker": "s",
        "size": 40,
        "alpha": transparency, 
    }

## Enumerate variable parameters in model: seed, grid dimensions, population density, agent preferences, vision, and relative size of groups.
model_params = {
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
    "width": {
        "type": "SliderInt",
        "value": 50,
        "label": "Width",
        "min": 5,
        "max": 100,
        "step": 1,
    },
    "height": {
        "type": "SliderInt",
        "value": 50,
        "label": "Height",
        "min": 5,
        "max": 100,
        "step": 1,
    },
    "density": {
        "type": "SliderFloat",
        "value": 0.7,
        "label": "Population Density",
        "min": 0,
        "max": 1,
        "step": 0.01,
    },
    "min_desired_share_alike": {
        "type": "SliderFloat",
        "value": 0,
        "label": "Min Desired Share Alike",
        "min": 0,
        "max": 1,
        "step": 0.01,
    },
    "max_desired_share_alike": {
        "type": "SliderFloat",
        "value": 1,
        "label": "Max Desired Share Alike",
        "min": 0,
        "max": 1,
        "step": 0.01,
    },
    "group_one_share": {
        "type": "SliderFloat",
        "value": 0.7,
        "label": "Share Type 1 Agents",
        "min": 0,
        "max": 1,
        "step": 0.01,
    },
    "radius": {
        "type": "SliderInt",
        "value": 1,
        "label": "Vision Radius",
        "min": 1,
        "max": 5,
        "step": 1,
    },
    "mimicry_effect": {
        "type": "SliderFloat",
        "value": 0.01,
        "label": "Mimicry Effect",
        "min": 0,
        "max": 0.1,
        "step": 0.01,
    },
    "depolarization_effect": {
        "type": "SliderFloat",
        "value": 0.01,
        "label": "Depolarization Effect",
        "min": 0,
        "max": 0.1,
        "step": 0.01,
    },
}

## Instantiate model
schelling_model = SchellingModel()

## Define happiness over time plot
HappyPlot = make_plot_component({"share_happy": "tab:green"})

## Define polarization over time plot
PolarizationPlot = make_plot_component({"avg_polarization": "tab:blue"})

## Define space component
SpaceGraph = make_space_component(agent_portrayal, draw_grid=False)

#@solara.component
def StatsDisplay(model):
    """Display current Share Happy and Avg Polarization levels"""
    # Get the dataframe of collected data
    df = model.datacollector.get_model_vars_dataframe()
    if not df.empty:
        share_happy = df["share_happy"].iloc[-1]
        avg_polarization = df["avg_polarization"].iloc[-1]
    else:
        share_happy = 0.0
        avg_polarization = 0.0
    return solara.Markdown(f"### Current Statistics\n\n**Share Happy:** {share_happy:.2f}%\n\n**Average Polarization:** {avg_polarization:.2f}")


## Instantiate page including all components
page = SolaraViz(
    schelling_model,
    components=[SpaceGraph, HappyPlot, PolarizationPlot, StatsDisplay],
    model_params=model_params,
    name="Schelling Segregation Model",
)
## Return page
page

