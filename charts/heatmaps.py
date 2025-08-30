import matplotlib.pyplot as plt
import numpy as np
import pickle

import sys
sys.path.insert(0, '..')

from containers import *
from analysis import Analysis

from functools import reduce
from operator import mul
from qdpy.utils import is_iterable

import matplotlib
import matplotlib as mpl

def getGpData():

    seed = 1
    objective = "density"

    analyse = Analysis()
    path = analyse.objectives.info[objective]["gp_url"]
    checkpoint_input_filename = path+str(seed)+"/checkpoint-"+objective+"-"+str(seed)+"-1000.pkl"

    with open(checkpoint_input_filename, "rb") as checkpoint_file:
        checkpoint = pickle.load(checkpoint_file)
    containers = checkpoint["containers"]
    grid = containers[0]
    population = grid.quality_array[..., 0]

    return rotateGrid(population)

def getQdpyData():

    seed = 1
    objective = "density"

    analyse = Analysis()
    path = analyse.objectives.info[objective]["qdpy_url"]
    checkpoint_input_filename = path+str(seed)+"/seed"+str(seed)+"-iteration1000.p"

    with open(checkpoint_input_filename, "rb") as checkpoint_file:
        checkpoint = pickle.load(checkpoint_file)
    container = checkpoint["container"]
    population = container.quality_array[..., 0]

    return rotateGrid(population)

def rotateGrid(population):
    
    # population shape = movement, rotations (x), conditionality (y)
    
    rotated_population = np.zeros((population.shape[2], population.shape[1], population.shape[0]))
    
    for i in range(population.shape[0]):
        for j in range(population.shape[1]):
            for k in range(population.shape[2]):
                rotated_population[i,j,k] = population[k,j,i]

    # rotated_population shape = conditionality, rotations (x), movement (y)
    
    return rotated_population

def drawColourBar(fig, ax, cax, figure_size):

    fig.subplots_adjust(right=0.9, wspace=0.40)
    colour_bar_axes = fig.add_axes([0.92, 0.3, 0.01, 0.4])
    cbar = fig.colorbar(cax, cax=colour_bar_axes, format="%.1f")
    cbar.ax.tick_params(labelsize=12)

def drawHeatmap():

    data = getQdpyData()
    
    colour_map="YlGnBu"
    colour_bar_label="Fitness"
    features_domain = [(0.0, 1.0), (-40.0, 40.0), (-40.0, 40.0)]
    fitness_domain = (np.nanmin(data), np.nanmax(data))
    ticks = 4
    bin_size_inches = 0.30

    bins = None
    if len(data.shape) % 2 == 1:
        data = data.reshape((data.shape[0], 1) + data.shape[1:])
        features_domain = (features_domain[0], (0., 0.)) + tuple(features_domain[1:]) 
        if bins != None:
            bins = (bins[0], 1) + bins[1:]
    if not bins:
        bins = data.shape

    horizontal_bins = bins[::2]
    vertical_bins = bins[1::2]
    horizontal_bins_total = reduce(mul, horizontal_bins, 1)
    vertical_bins_total = reduce(mul, vertical_bins, 1)

    figure_size = [2.1 + horizontal_bins_total * bin_size_inches, 1. + vertical_bins_total * bin_size_inches]

    fig, ax = plt.subplots(nrows=bins[1], ncols=bins[0], figsize=figure_size)

    for x in range(bins[0]):
        for y in range(bins[1]):
            ax = plt.subplot(bins[1], bins[0], (bins[1] - y - 1) * bins[0] + x + 1)
            cax = drawSubplot(ax,
                              data[x, y, 0:bins[2], 0:bins[3]],
                              colour_map=colour_map,
                              features_domain=features_domain[-2:],
                              fitness_domain=fitness_domain[-2:],
                              bins=(bins[2], bins[3]), ticks=ticks)


    plt.tight_layout()
    drawColourBar(fig, ax, cax, figure_size)
    plt.show()

def drawSubplot(ax, data, colour_map, features_domain, fitness_domain, bins=None, ticks = 4):
    
    vertical_min = fitness_domain[0]
    if np.isnan(vertical_min) or np.isinf(vertical_min):
        vertical_min = np.nanmin(data)

    vertical_max = fitness_domain[1]
    if np.isnan(vertical_max) or np.isinf(vertical_max):
        vertical_max = np.nanmax(data)

    cax = ax.imshow(data.T, interpolation="none", cmap=colour_map, vmin=vertical_min, vmax=vertical_max, aspect="equal")

    if is_iterable(ticks):
        if len(ticks) != 2:
            raise ValueError("ticks can be None, an Integer or a Sequence of size 2.")
        num_x_ticks, num_y_ticks = ticks
    elif ticks == None:
        num_x_ticks = round(pow(bins[0], 1./2.))
        num_x_ticks = num_x_ticks if num_x_ticks % 2 == 0 else num_x_ticks + 1
        num_y_ticks = round(pow(bins[1], 1./2.))
        num_y_ticks = num_y_ticks if num_y_ticks % 2 == 0 else num_y_ticks + 1
    else:
        if bins[0] > bins[1]:
            num_x_ticks = ticks
            num_y_ticks = int(num_x_ticks * bins[1] / bins[0])
        elif bins[1] > bins[0]:
            num_y_ticks = ticks
            num_x_ticks = int(num_y_ticks * bins[0] / bins[1])
        else:
            num_x_ticks = num_y_ticks = ticks

        if num_x_ticks > bins[0] or num_x_ticks < 1:
            num_x_ticks = min(bins[0], ticks)
        if num_y_ticks > bins[1] or num_y_ticks < 1:
            num_y_ticks = min(bins[1], ticks)

    ax.xaxis.set_tick_params(which='major', left=True, bottom=True, top=False, right=False)
    ax.yaxis.set_tick_params(which='major', left=True, bottom=True, top=False, right=False)

    xticks = list(np.arange(0, data.shape[0] + 1, data.shape[0] / num_x_ticks))
    yticks = list(np.arange(0, data.shape[1] + 1, data.shape[1] / num_y_ticks))
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)

    delta_x = features_domain[0][1] - features_domain[0][0]
    delta_y = features_domain[1][1] - features_domain[1][0]

    ax.set_xticklabels([f'{round(float(x / float(data.shape[0]) * delta_x + features_domain[0][0]), 2):1.0f}' for x in xticks], fontsize=10)
    ax.set_yticklabels([f'{round(float(y / float(data.shape[1]) * delta_y + features_domain[1][0]), 2):1.0f}' for y in yticks], fontsize=10)


    if bins[1] == 1:
        yticks = []

    plt.xticks(xticks, rotation='vertical')
    plt.yticks(yticks)

    ax.invert_yaxis()

    ax.xaxis.set_tick_params(which='minor', direction="in", left=False, bottom=False, top=False, right=False)
    ax.yaxis.set_tick_params(which='minor', direction="in", left=False, bottom=False, top=False, right=False)
    
    ax.autoscale_view()

    return cax



drawHeatmap()
