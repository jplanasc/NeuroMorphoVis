####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
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

# System imports
import random
import time

# Blender imports
import bpy
from mathutils import Vector, Matrix

# Internal imports
import nmv
import nmv.bmeshi
import nmv.enums
import nmv.geometry
import nmv.mesh
import nmv.scene
import nmv.skeleton
import nmv.utilities


####################################################################################################
# get_subtree_leaves
####################################################################################################
def get_subtree_leaves(section,
                       leaves):
    """Returns a list with all the leaves of a subtree where the given section is considered
    the root.

    :param section:
        The root section of the subtree.
    :param leaves:
        The list that will be used to collect the subtree.
    :return:
    """

    # If the section is leaf, then append it to the leaves list
    if section.is_leaf():
        leaves.append(section)

    # Otherwise, go recursively
    for child in section.children:
        get_subtree_leaves(section=child, leaves=leaves)


####################################################################################################
# get_arbor_leaves
####################################################################################################
def get_arbor_leaves(arbor):
    """Returns a list with all the leaves of the given arbor.

    :param arbor:
        A given arbor to get its leaf nodes.
    :return:
        A list of nodes (or sections) that represent the leaves of the arbor tree.
    """

    # Leaves list
    leaves = list()

    # Arbor must not be None, otherwise return an empty list
    if arbor is None:
        return leaves

    # Start from the arbor root and go recursively
    get_subtree_leaves(section=arbor, leaves=leaves)

    # Return the list
    return leaves


####################################################################################################
# compute_dendrogram_x_coordinates_for_parents
####################################################################################################
def compute_dendrogram_x_coordinates_for_parents(section):
    """This function computes the X-coordinates of the dendrogram points starting from a given
    section and goes recursively up to the maximum possible parent in the arbor tree.
    If the @dendrogram_x parameter of any of the sections along the path is None, the function
    returns immediately.

    The first call of this function should be used for a leaf section, and then propagates up to
    the maximum possible parent.

    :param section:
        An entry section to start computing the X-axis values of the dendrograms.
    """

    # If the section is None, return please
    if section is None:
        return

    # The parent section must not be None
    if section.parent is not None:

        # Compute X-coordinates for all the children
        x = 0
        for child in section.parent.children:

            # If the X-coordinate of any of the children section is not computed, return
            if child.dendrogram_x is None:
                return

            # Otherwise add the value
            x += child.dendrogram_x

        # Normalize to get the center point
        x /= len(section.parent.children)

        # Do it
        section.parent.dendrogram_x = x

    # Go recursively
    compute_dendrogram_x_coordinates_for_parents(section=section.parent)


####################################################################################################
# compute_dendrogram_y_coordinates_for_children
####################################################################################################
def compute_dendrogram_y_coordinates_for_children(section):

    # The actual Y-coordinate is equivalent to the path length of the section
    section.dendrogram_y = section.compute_path_length()

    # Go recursively
    for child in section.children:
        compute_dendrogram_y_coordinates_for_children(section=child)


####################################################################################################
# compute_arbor_dendrogram
####################################################################################################
def compute_arbor_dendrogram(arbor,
                             delta=10):
    """Computes the dendrogram of a given arbor and consider the delta between the leaves.

    :param arbor:
        A given arbor to compute its dendrogram.
    :param delta:
        The distance between the leaves.
    """
    # Get a list of all the leaf nodes in the arbor
    leaves = get_arbor_leaves(arbor=arbor)

    # Assuming that the leaves will start at 0.0 on the x-axis
    for i, leaf in enumerate(leaves):

        # Compute the X-coordinates of the leaves
        leaf.dendrogram_x = i * delta

    # Compute the X-coordinates of the rest of the arbor tree
    for leaf in leaves:
        compute_dendrogram_x_coordinates_for_parents(leaf)

    # Compute the Y-coordinates starting from the parent node
    compute_dendrogram_y_coordinates_for_children(section=arbor)


####################################################################################################
# compute_morphology_dendrogram
####################################################################################################
def compute_morphology_dendrogram(morphology,
                                  delta):
    """Computes the dendrogram of the entire morphology.

    :param morphology:
        A morphology to compute its dendrogram.
    :param delta:
        The distance between the leaves.
    """

    # Apical dendrite
    if morphology.apical_dendrite is not None:
        compute_arbor_dendrogram(arbor=morphology.apical_dendrite, delta=delta)

    # Basal dendrites
    if morphology.dendrites is not None:
        for basal_dendrite in morphology.dendrites:
            compute_arbor_dendrogram(arbor=basal_dendrite, delta=delta)

    # Axon
    if morphology.axon is not None:
        compute_arbor_dendrogram(arbor=morphology.axon, delta=delta)
