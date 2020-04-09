####################################################################################################
# Copyright (c) 2016 - 2020, EPFL / Blue Brain Project
#               Marwan Abdellah <marwan.abdellah@epfl.ch>
#
# This file is part of NeuroMorphoVis <https://github.com/BlueBrain/NeuroMorphoVis>
#
# This program is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This Blender-based tool is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.
####################################################################################################


import nmv.consts
import nmv.enums
import nmv.utilities


####################################################################################################
# @plot_per_arbor_result
####################################################################################################
def plot_per_arbor_result(analysis_results,
                          morphology,
                          options,
                          figure_name=None,
                          figure_title=None,
                          figure_xlabel=None,
                          add_percentage=False):
    """Plot the analysis result per arbor.

    :param analysis_results:
        A data structure containing the result.
    :param morphology:
        A given morphology file.
    :param options:
        System options.
    :param figure_name:
        The prefix of the figure image.
    :param figure_title:
        The title that will be written on the figure.
    :param figure_xlabel:
        The X-axis label of the figure.
    :param add_percentage:
        If this flag is True, a percentage text will be added on the right side of each bar.
    """

    # Installing dependencies
    try:
        import numpy
    except ModuleNotFoundError:
        print('Package *numpy* is not installed. Installing it.')
        nmv.utilities.pip_wheel(package_name='numpy')

    try:
        import matplotlib
    except ModuleNotFoundError:
        print('Package *matplotlib* is not installed. Installing it.')
        nmv.utilities.pip_wheel(package_name='matplotlib')

    try:
        import seaborn
    except ModuleNotFoundError:
        print('Package *seaborn* is not installed. Installing it.')
        nmv.utilities.pip_wheel(package_name='seaborn')

    # Plotting imports
    import numpy
    import seaborn
    import matplotlib.pyplot as pyplot
    from matplotlib import font_manager

    # Import the fonts
    font_dirs = [nmv.consts.Paths.FONTS_DIRECTORY]
    font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
    font_list = font_manager.createFontList(font_files)
    font_manager.fontManager.ttflist.extend(font_list)

    # Clean the figure
    pyplot.clf()

    # X-axis data
    x_data = list()

    # Y-axis data
    y_data = list()

    # Color palette
    palette = []

    # Apical dendrite
    if analysis_results.apical_dendrite_result is not None:
        x_data.append('Apical Dendrite')
        y_data.append(analysis_results.apical_dendrite_result)
        palette.append(morphology.apical_dendrite_color)

    # Basal dendrites
    if analysis_results.basal_dendrites_result is not None:
        for i, result in enumerate(analysis_results.basal_dendrites_result):
            x_data.append('Basal Dendrite %d' % i)
            y_data.append(result)
            palette.append(morphology.basal_dendrites_colors[i])

    # Collecting the lists, Axon
    if analysis_results.axon_result is not None:
        x_data.append('Axon')
        y_data.append(analysis_results.axon_result)
        palette.append(morphology.axon_color)

    # Total number of bars, similar to arbors
    total_number_of_bars = len(x_data)

    # The width of each bar
    bar_width = 0.65

    # Adjust seaborn configuration
    seaborn.set_style("white")

    # The color palette
    seaborn.set_palette(palette=palette)

    # Adjusting the matplotlib parameters
    pyplot.rcParams['axes.grid'] = 'False'
    pyplot.rcParams['font.family'] = 'NimbusSanL'
    pyplot.rcParams['axes.linewidth'] = 0.0
    pyplot.rcParams['axes.labelsize'] = bar_width * 10
    pyplot.rcParams['axes.labelweight'] = 'regular'
    pyplot.rcParams['xtick.labelsize'] = bar_width * 10
    pyplot.rcParams['ytick.labelsize'] = bar_width * 10
    pyplot.rcParams['legend.fontsize'] = 10
    pyplot.rcParams['axes.titlesize'] = bar_width * 1.25 * 10
    pyplot.rcParams['axes.axisbelow'] = True
    pyplot.rcParams['axes.edgecolor'] = '0.1'

    # numpy array from the lists
    x = numpy.asarray(x_data)
    y = numpy.asarray(y_data)

    # Adjusting the figure size
    pyplot.figure(figsize=(bar_width * 4, total_number_of_bars * 0.5 * bar_width))

    # Plot the bar plot
    ax = seaborn.barplot(x=y, y=x, edgecolor='none')

    # Title
    ax.set(xlabel=figure_xlabel, title=figure_title)
    ax.spines['left'].set_linewidth(0.5)
    ax.spines['left'].set_color('black')

    # Add percentage on the right side of the bar
    for bar in ax.patches:
        # Current Y center
        y = bar.get_y()

        # Current bar height
        height = bar.get_height()

        # Current center
        centre = y + height / 2.0

        # Set the new center
        bar.set_y(centre - bar_width / 2.0)

        # Set the new height
        bar.set_height(bar_width)

    # Create a list to collect the plt.patches data
    totals = []

    # Find the values and append to list
    for i in ax.patches:
        totals.append(i.get_width())

    # Set individual bar labels using above list
    total = sum(totals)

    # Set individual bar labels using above list
    for i, patch in enumerate(ax.patches):

        # Get the width of the bar and then add a little increment
        x = patch.get_width()
        y = patch.get_y() + (bar_width / 2.0) + (bar_width / 8.0)

        # Compute the percentage
        if total > 0:
            percentage = round((patch.get_width() / total) * 100, 2)
            if add_percentage:
                if 'float' in str(type(y_data[i])):
                    value = '  %2.1f (%2.1f%%)' % (y_data[i], percentage)
                else:
                    value = '  %d (%2.1f%%)' % (y_data[i], percentage)
            else:
                if 'float' in str(type(y_data[i])):
                    value = '  %2.1f' % y_data[i]
                else:
                    value = '  %d' % y_data[i]

            ax.text(x, y, value, fontsize=bar_width * 10, color='dimgrey')

    # Save a PNG figure
    pyplot.savefig('%s/%s/%s.png' % (options.io.analysis_directory, morphology.label, figure_name),
                   bbox_inches='tight', transparent=True, dpi=600)

    # Save a PDF figure
    pyplot.savefig('%s/%s/%s.pdf' % (options.io.analysis_directory, morphology.label, figure_name),
                   bbox_inches='tight', transparent=True, dpi=600)

    # Close the figures
    pyplot.close()


####################################################################################################
# @plot_per_arbor_range
####################################################################################################
def plot_per_arbor_range(minimum_results,
                         average_results,
                         maximum_results,
                         morphology,
                         options,
                         figure_name=None,
                         figure_xlabel=None,
                         figure_title=None):
    """Plots the analysis range per arbor.

    :param minimum_results:
        A list containing the minimum values per arbor.
    :param average_results:
        A list containing the average values per arbor.
    :param maximum_results:
        A list containing the maximum values per arbor.
    :param morphology:
        A given morphology file.
    :param options:
        System options.
    :param figure_name:
        The prefix of the figure image.
    :param figure_title:
        The title that will be written on the figure.
    :param figure_xlabel:
        The X-axis label of the figure.
    """

    # Installing dependencies
    try:
        import numpy
    except ModuleNotFoundError:
        print('Package *numpy* is not installed. Installing it.')
        nmv.utilities.pip_wheel(package_name='numpy')

    try:
        import matplotlib
    except ModuleNotFoundError:
        print('Package *matplotlib* is not installed. Installing it.')
        nmv.utilities.pip_wheel(package_name='matplotlib')

    try:
        import seaborn
    except ModuleNotFoundError:
        print('Package *seaborn* is not installed. Installing it.')
        nmv.utilities.pip_wheel(package_name='seaborn')

    try:
        import pandas
    except ModuleNotFoundError:
        print('Package *pandas* is not installed. Installing it.')
        nmv.utilities.pip_wheel(package_name='pandas')

    import numpy
    import seaborn
    from matplotlib import pyplot
    from matplotlib import font_manager

    # Clear any figure
    pyplot.clf()

    # Import the fonts
    font_dirs = [nmv.consts.Paths.FONTS_DIRECTORY]
    font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
    font_list = font_manager.createFontList(font_files)
    font_manager.fontManager.ttflist.extend(font_list)

    # Labels on the independent axis
    labels = list()

    # The list of the minimum, average and maximum data
    min_list = list()
    avg_list = list()
    max_list = list()

    # Color palette
    palette = []

    # Apical dendrite
    if minimum_results.apical_dendrite_result is not None:
        labels.append('Apical Dendrite')
        min_list.append(minimum_results.apical_dendrite_result)
        avg_list.append(average_results.apical_dendrite_result)
        max_list.append(maximum_results.apical_dendrite_result)
        palette.append(morphology.apical_dendrite_color)

    # Basal dendrites
    if minimum_results.basal_dendrites_result is not None:
        for i in range( len(minimum_results.basal_dendrites_result)):
            labels.append('Basal Dendrite %d' % i)
            min_list.append(minimum_results.basal_dendrites_result[i])
            avg_list.append(average_results.basal_dendrites_result[i])
            max_list.append(maximum_results.basal_dendrites_result[i])
            palette.append(morphology.basal_dendrites_colors[i])

    # Collecting the lists, Axon
    if minimum_results.axon_result is not None:
        labels.append('Axon')
        min_list.append(minimum_results.axon_result)
        avg_list.append(average_results.axon_result)
        max_list.append(maximum_results.axon_result)
        palette.append(morphology.axon_color)

    # Total number of bars, similar to arbors
    total_number_of_bars = len(labels)

    # The width of each bar
    bar_width = 0.65

    # Adjust seaborn configuration
    seaborn.set_style("white")

    # The color palette
    # palette = seabron.cubehelix_palette(2 * total_number_of_bars)
    # palette = seaborn.color_palette("pastel", total_number_of_bars)
    seaborn.set_palette(palette=palette)

    # Adjusting the matplotlib parameters
    pyplot.rcParams['axes.grid'] = 'False'
    pyplot.rcParams['font.family'] = 'NimbusSanL'
    pyplot.rcParams['axes.linewidth'] = 0.0
    pyplot.rcParams['axes.labelsize'] = bar_width * 10
    pyplot.rcParams['axes.labelweight'] = 'regular'
    pyplot.rcParams['xtick.labelsize'] = bar_width * 10
    pyplot.rcParams['ytick.labelsize'] = bar_width * 10
    pyplot.rcParams['legend.fontsize'] = 10
    pyplot.rcParams['axes.titlesize'] = bar_width * 1.25 * 10
    pyplot.rcParams['axes.axisbelow'] = True
    pyplot.rcParams['axes.edgecolor'] = '0.1'

    # Adjusting the figure size
    pyplot.figure(figsize=(bar_width * 4, total_number_of_bars * 0.5 * bar_width))

    # Compile the list
    min_data = numpy.array(min_list)
    avg_data = numpy.array(avg_list)
    max_data = numpy.array(max_list)

    # Compute the range
    xerr = numpy.array([avg_data - min_data, max_data - avg_data])

    # Plot the bar plot
    ax = seaborn.barplot(x=avg_data, y=labels, xerr=xerr, edgecolor='none',
                         error_kw={'elinewidth': 0.75, 'capsize': 1.0})

    # Title
    ax.set(xlabel=figure_xlabel, title=figure_title)
    ax.spines['left'].set_linewidth(0.5)
    ax.spines['left'].set_color('black')

    # Save a PNG figure
    pyplot.savefig('%s/%s/%s.png' % (options.io.analysis_directory, morphology.label, figure_name),
                   bbox_inches='tight', transparent=True, dpi=300)

    # Save a PDF figure
    pyplot.savefig('%s/%s/%s.pdf' % (options.io.analysis_directory, morphology.label, figure_name),
                   bbox_inches='tight', transparent=True, dpi=300)

    # Close the figures
    pyplot.close()
