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

__author__      = "Marwan Abdellah"
__copyright__   = "Copyright (c) 2016 - 2018, Blue Brain Project / EPFL"
__credits__     = ["Ahmet Bilgili", "Juan Hernando", "Stefan Eilemann"]
__version__     = "1.0.0"
__maintainer__  = "Marwan Abdellah"
__email__       = "marwan.abdellah@epfl.ch"
__status__      = "Production"


####################################################################################################
# Add-on information
####################################################################################################
bl_info = {
    # The name of your add-on. This is shown in the add-on tab in Blender's user preferences
    "name" : "NeuroMorphoVis",
    # The author of this add-on
    "author" : "Marwan Abdellah",
    # A tuple, containing the add-on version
    "version" : (1, 0, 0),
    # The earliest Blender version this add-on will work with. If you're not sure what versions of
    # Blender this add-on is compatible with, use the version of Blender you're developing
    # the add-on with.
    "blender" : (2, 7, 9),
    # This is where users should look for this add-on.
    "location" : "View 3D",
    # Description
    "description": "This add-on is used to reconstruct surface meshes from three-dimensional "
    "neuronal morphologies and vasculature. The Add-on was developed for internal use by the "
    " Blue Brain Project at EPFL.",
    # Add-on category; shown on the left side of Blender's add-on list to make filtering simpler.
    # This must be one of the categories as listed in Blender's add-on tab; if it's not, it will
    # create a new category for your add-on (which may be good or bad.)
    # Don't create new categories to make your add-on stand out.
    "category": "3D View",
    # This support can be either 'OFFICIAL', 'COMMUNITY', or 'TESTING'. 'OFFICIAL' should only be
    # used if this add-on is included with Blender.
    # (If you're not sure, don't use 'OFFICIAL'.) 'COMMUNITY' and 'TESTING' are both fine to use.
    # Note that 'TESTING' add-ons aren't shown by default in Blender's add-on list.
    'support': 'COMMUNITY',
    # Optional: specifies the wiki URL for an add-on. 
    # This will appear in this add-on listing as "Documentation".
    'wiki_url': 'https://github.com/BlueBrain/NeuroMorphoVis',
    # Bug tracker: specifies the bug-tracker URL for an add-on.
    'tracker_url': 'https://github.com/BlueBrain/NeuroMorphoVis/issues?utf8=%E2%9C%93&q='
}


# System imports
import sys, os, imp

# Append the modules path to the system paths to be able to load the internal python modules
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

if "bpy" in locals():

    import neuromorphovis.interface.ui.io_panel
    import neuromorphovis.interface.ui.analysis_panel
    import neuromorphovis.interface.ui.soma_panel
    import neuromorphovis.interface.ui.morphology_panel
    import neuromorphovis.interface.ui.mesh_panel

    imp.reload(neuromorphovis.interface.ui.io_panel)
    imp.reload(neuromorphovis.interface.ui.analysis_panel)
    imp.reload(neuromorphovis.interface.ui.soma_panel)
    imp.reload(neuromorphovis.interface.ui.morphology_panel)
    imp.reload(neuromorphovis.interface.ui.mesh_panel)

else:

    import neuromorphovis.interface.ui.io_panel
    import neuromorphovis.interface.ui.analysis_panel
    import neuromorphovis.interface.ui.soma_panel
    import neuromorphovis.interface.ui.morphology_panel
    import neuromorphovis.interface.ui.mesh_panel

import bpy
from addon_utils import check, paths, enable
def get_all_addons(display=False):
    """
    Prints the addon state based on the user preferences.
    """
    import sys
    paths_list = paths()
    addon_list = []
    for path in paths_list:
        bpy.utils._sys_path_ensure(path)
        for mod_name, mod_path in bpy.path.module_names(path):
            is_enabled, is_loaded = check(mod_name)
            addon_list.append(mod_name)
            if display:  #for example
                print("%s default:%s loaded:%s " % (mod_name, is_enabled, is_loaded))
    return(addon_list)
get_all_addons(True)


####################################################################################################
# @register
####################################################################################################
def register():
    """Register the different modules of the interface.
    """

    # Register panels
    neuromorphovis.interface.ui.io_panel.register_panel()
    neuromorphovis.interface.ui.analysis_panel.register_panel()
    neuromorphovis.interface.ui.soma_panel.register_panel()
    neuromorphovis.interface.ui.morphology_panel.register_panel()
    neuromorphovis.interface.ui.mesh_panel.register_panel()


####################################################################################################
# @unregister
####################################################################################################
def unregister():
    """Unregister the different modules of the interface.
    """

    # Un-register panels
    neuromorphovis.interface.ui.io_panel.unregister_panel()
    neuromorphovis.interface.ui.analysis_panel.unregister_panel()
    neuromorphovis.interface.ui.soma_panel.unregister_panel()
    neuromorphovis.interface.ui.morphology_panel.unregister_panel()
    neuromorphovis.interface.ui.mesh_panel.unregister_panel()

print('HOLA')
####################################################################################################
# __main__
####################################################################################################
if __name__ == "__main__":

    register()

    is_enabled, is_loaded = check(neuromorphovis)
    if not is_enabled:
        print("%s enabled" % neuromorphovis)
        enable('neuromorphovis')



