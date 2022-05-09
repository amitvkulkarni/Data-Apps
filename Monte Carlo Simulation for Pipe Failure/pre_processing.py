import numpy as np
import pandas as pd
import random
import os
import yaml
from dataclasses import dataclass
from statistics import NormalDist
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

# folder to load config file
CONFIG_PATH = "./"
# Function to load yaml configuration file


def load_config(config_name):
    """summary

    Args:
        config_name (str): The config file in the YAML format which has the defined values of diameter, thickness and yield

    Returns:
        dict: The function returns a dictionary object
    """
    with open(os.path.join(CONFIG_PATH, config_name)) as file:
        config = yaml.safe_load(file)
    return config


config = load_config("config.yaml")


@dataclass
class SimulationInputs:

    # Diameter
    diameter_mean: int = config['diameter_mean']
    diameter_cov: int = config['diameter_mean']
    diameter_std: float = (diameter_mean * diameter_cov) / 100

    # Thickness
    thickness_mean: int = config['diameter_mean']
    thickness_cov: int = config['diameter_mean']
    thickness_std: float = (thickness_mean * thickness_cov) / 100

    # Yield Strength
    yield_mean: int = config['yield_mean']
    yield_cov: int = config['yield_cov']
    yield_std: float = (yield_mean * yield_cov) / 100

    # Internal Pressure
    internal_pressure: int = config['internal_pressure']

    # Iterations
    iter_start: int = config['iter_start']
    iter_end: int = config['iter_end']
    iter_step: int = config['iter_step']


print("---------------------------------------Data CLass Object created ---------------------------------------")
simulation_data = SimulationInputs()


def initiate_simulation(
    # iter_start = simulation_data.iter_start,
    # iter_end = simulation_data.iter_end,
    # iter_step = simulation_data.iter_step,
    diameter_mean=simulation_data.diameter_mean,
    diameter_cov=simulation_data.diameter_cov,
    thickness_mean=simulation_data.thickness_mean,
    thickness_cov=simulation_data.thickness_cov,
    strength_mean=simulation_data.yield_mean,
    strength_cov=simulation_data.yield_cov,
    internal_pressure=simulation_data.internal_pressure


):
    """summary

    Args:
        iter_start (int, optional): define starting point for generating simulation values. Defaults to simulation_data.iter_start.
        iter_end (int, optional): define end point for generating simulation values. Defaults to simulation_data.iter_end.
        iter_step (int, optional): define the increment. Defaults to simulation_data.iter_step.
    """
    try:
        # print("---------------------------------------Initiating Simulations ---------------------------------------")
        runs = list(range(simulation_data.iter_start,
                    simulation_data.iter_end, simulation_data.iter_step))
        sim_res = []
        for run in runs:
            sim_results = run_simulation(run)
            sim_res.append(sim_results)
            # print(f'Simulation run for {run}: {sim_results}')
        # print(f'sim_res: {sim_res}')
        # print("Before plot generation")
        return plot_linechart(runs, sim_res)
        # plot_histogram(runs, sim_res)

    except Exception as e:
        print(
            f'An exception occurred while trying to initiate the simulation: {e}')


def run_simulation(iterations):
    """summary

    Returns:
        float: The function returns the number of negative values found in the simulation - negative value indicates that pipe failed

    Hoop Stress:
        int: Hoop stress =(Internal Pressure * Diameter)/(2 * Thickness)
    
    Objective:
        int: Failure = Yield - Hoop stress
    """
    try:

        lst_diameter = simulate_values(
            simulation_data.diameter_mean, simulation_data.diameter_std, iterations, False)

        lst_thickness = simulate_values(
            simulation_data.thickness_mean, simulation_data.thickness_std, iterations, False)

        lst_yield = simulate_values(
            simulation_data.yield_mean, simulation_data.yield_std, iterations, False)

        df_final = pd.DataFrame(list(zip(lst_diameter, lst_thickness, lst_yield)), columns=[
                                'Diameter', 'Thickness', 'Yield'])

        df_final['Hoop_Stress'] = simulation_data.internal_pressure * \
            df_final['Diameter'] / (2 * df_final['Thickness'])

        df_final['Objective'] = df_final['Yield'] - df_final["Hoop_Stress"]

        min_stress = df_final['Hoop_Stress'].min()

        max_stress = df_final['Hoop_Stress'].max()

        return df_final[df_final['Objective'] < 0].shape[0] / iterations

    except Exception as e:
      print(f'An exception occurred with running the simulation: {e}')


def simulate_values(mu, sigma, iterations, print_output=True):
    """summary

    Args:
        mu (int): Define the mean of the diameter, thickness and yield
        sigma (int): Define the standard deviation of the diameter, thickness and yield
        iterations (int): Define number of iterations the simulations to be run
        print_output (bool, optional): Set value to True to view the print statement at various stages and set False to skip the prints. Defaults to True.

    Returns:
        List: The function returns the list which has the simulation values for diameter, thickess and yield
    """
    try:
        result = []
        for i in range(iterations):
            prob_value = round(random.uniform(.01, 0.99), 3)
            sim_value = round(NormalDist(
                mu=mu, sigma=sigma).inv_cdf(prob_value), 3)

            if print_output:
                print(
                    f"The prob value is {prob_value} and the simulated value is {sim_value}")
            result.append(sim_value)
        return result
    except Exception as e:
        print(f'An exception occurred while generating simulation values: {e}')


def plot_linechart(runs, sim_res):
    try:
        # print("---------------------------------------Initiating Simulation plot ---------------------------------------")
        y_mean = np.mean(sim_res)
        # print(f'y_mean:{y_mean}')
        df_res = pd.DataFrame(zip(runs, sim_res), columns=['runs', 'sim_res'])
        fig = px.line(df_res, x="runs", y="sim_res", title='Monte Carlo Simulation - Probability Of Pipe Failure')
        fig.add_hline(y=y_mean, line_color="red",line_dash="dash")
        fig.add_annotation(x= simulation_data.iter_end/2 , y= y_mean,
                                    text= f'Mean Probability of failure ({round(y_mean,5)})',
                                    showarrow=True,
                                    arrowhead=1),
        fig.update_layout(
            showlegend=False,
            xaxis_title="No of iteration/simulations",
            yaxis_title= "Probability of failure")
        return fig

    except Exception as e:
      print(f'An error  occurred while trying to generate line chart {e}')


def plot_histogram(runs, sim_res):
    try:
        plt.hist(sim_res)
        plt.show()
    except Exception as e:
      print(
          f'An exception occurred while trying to generate the histogram: {e}')

