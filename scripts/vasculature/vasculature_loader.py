####################################################################################################
# Copyright (c) 2018, EPFL / Blue Brain Project
#               Marwan Abdellah <marwan.abdellah@epfl.ch>
#
# This file is part of NeuroMorphoVis <https://github.com/BlueBrain/NeuroMorphoVis>
#
# This library is free software; you can redistribute it and/or modify it under the terms of the
# GNU Lesser General Public License version 3.0 as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along with this library;
# if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA.
####################################################################################################

__author__      = "Marwan Abdellah"
__copyright__   = "Copyright (c) 2016 - 2018, Blue Brain Project / EPFL"
__credits__     = ["Ahmet Bilgili", "Juan Hernando", "Stefan Eilemann"]
__version__     = "1.0.0"
__maintainer__  = "Marwan Abdellah"
__email__       = "marwan.abdellah@epfl.ch"
__status__      = "Production"


# System imports
import h5py

# Blender imports
import bpy
from mathutils import Vector


####################################################################################################
# VasculatureLoader
####################################################################################################
class VasculatureLoader:
    """ A simple loader to load the vasculature data from h5 files. """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 dataset):
        """Constructor

        :param dataset:
            A path to the data set to load.
        """

        # Section index
        self.dataset = dataset

        # A list of all the points in the data set
        self.points_list = list()

        # A list of all the segments in the data set
        self.segments_list = list()

        # A list of all the sections in the data set
        self.sections_list = list()

        # A list of all the connections in the data set
        self.connections_list = list()

        # Load the dataset directly
        self.load_dataset_from_file()

    ################################################################################################
    # @load_dataset_from_file
    ################################################################################################
    def load_dataset_from_file(self):
        """Loads the dataset from the file.
        """

        print('STATUS: Loading dataset')

        # Read the h5 file using the python module into a data array
        data = h5py.File(self.dataset, 'r')

        # A list of all the samples in the data set
        self.points_list = data['points'].value

        # A list of all the edges or 'segments' in the data set
        self.segments_list = data['edges'].value

        # A list of all the sections (called structures) in the data set
        self.sections_list = data['chains']['structure'].value

        # A list of all the connections between the different sections in the data set
        self.connections_list = data['chains']['connectivity'].value
