####################################################################################################
# Copyright (c) 2019, EPFL / Blue Brain Project
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

# Blender imports
import bpy

# Internal imports
import nmv.consts
import nmv.enums
import nmv.utilities

# Meshing technique
bpy.types.Scene.NMV_MeshingTechnique = bpy.props.EnumProperty(
    items=[(nmv.enums.Meshing.Technique.PIECEWISE_WATERTIGHT,
            'Piecewise Watertight',
            'This approach (Abdellah et al., 2017) creates a piecewise watertight mesh that is '
            'composed of multiple mesh objects, where each object is a watertight component. '
            'This method is used to reconstruct high fidelity volumes from the generated meshes'),
           (nmv.enums.Meshing.Technique.SKINNING,
            'Skinning',
            'Skinning (Abdellah et al., 2019) uses the skin modifier to reconstruct the branches. '
            'This approach is guaranteed to reconstruct a nice looking branching compared to the '
            'other methods and also guarantees the fidelity of the mesh, but it does not '
            'guarantee watertightness. This technique is used when you need meshes for '
            'visualization with transparency'),
           (nmv.enums.Meshing.Technique.UNION,
            'Union',
            'This method uses the union boolean operator to join the different branches together '
            'in a single mesh. It is not guaranteed to generate a watertight or even a valid '
            'mesh, although it works in 90% of the cases'),
           (nmv.enums.Meshing.Technique.META_OBJECTS,
            'MetaBalls',
            'Creates watertight mesh models using MetaBalls. This approach is extremely slow if '
            'the axons are included in the meshing process, so it is always recommended to use '
            'first order branching for the axons when using this technique')],
    name='Method',
    description='The technique that will be used to create the mesh, by default the '
                'Piecewise Watertight one since it is the fastest one.',
    default=nmv.enums.Meshing.Technique.PIECEWISE_WATERTIGHT)

# Build soma
bpy.types.Scene.NMV_MeshingSomaType = bpy.props.EnumProperty(
    items=[(nmv.enums.Soma.Representation.META_BALLS,
            'MetaBalls',
            'Reconstruct a rough shape of the soma using MetaBalls. '
            'This approach is real-time and can reconstruct good shapes for the somata, but '
            'more accurate profiles could be reconstructed with the Soft Body option'),
           (nmv.enums.Soma.Representation.SOFT_BODY,
            'SoftBody',
            'Reconstruct a 3D profile of the soma using Soft Body physics.'
            'This method takes few seconds to reconstruct a soma mesh')],
    name='Soma',
    default=nmv.enums.Soma.Representation.META_BALLS)


# Is the soma connected to the first order branches or not !
bpy.types.Scene.NMV_SomaArborsConnection = bpy.props.EnumProperty(
    items=[(nmv.enums.Meshing.SomaConnection.CONNECTED,
            'Connected',
            'Connect the soma mesh to the arbors to make a nice mesh that can be used for any'
            'type of visualization that involves transparency.'),
           (nmv.enums.Meshing.SomaConnection.DISCONNECTED,
            'Disconnected',
            'Create the soma as a separate mesh and do not connect it to the arbors. This '
            'option is used to guarantee surface smoothing when a volume is reconstructed '
            'from the resulting mesh, but cannot be used for surface transparency rendering.')],
    name='Soma Connection',
    default=nmv.enums.Meshing.SomaConnection.DISCONNECTED)

# The skeleton of the union-based meshing algorithm
bpy.types.Scene.NMV_UnionMethodSkeleton = bpy.props.EnumProperty(
    items=[(nmv.enums.Meshing.UnionMeshing.QUAD_SKELETON,
            'Quad',
            'Use a quad skeleton for the union meshing algorithm'),
           (nmv.enums.Meshing.UnionMeshing.CIRCULAR_SKELETON,
            'Circle',
            'Use a circular skeleton for the union meshing algorithm')],
    name='Skeleton',
    default=nmv.enums.Meshing.UnionMeshing.QUAD_SKELETON)

# Edges, hard or smooth
bpy.types.Scene.NMV_MeshSmoothing = bpy.props.EnumProperty(
    items=[(nmv.enums.Meshing.Edges.HARD,
            'Sharp',
            'Make the edges between the segments sharp and hard'),
           (nmv.enums.Meshing.Edges.SMOOTH,
            'Curvy',
            'Make the edges between the segments soft and curvy')],
    name='Edges',
    default=nmv.enums.Meshing.Edges.HARD)

# Branching, is it based on angles or radii
bpy.types.Scene.NMV_MeshBranching = bpy.props.EnumProperty(
    items=[(nmv.enums.Skeleton.Branching.ANGLES,
            'Angles',
            'Make the branching based on the angles at branching points'),
           (nmv.enums.Skeleton.Branching.RADII,
            'Radii',
            'Make the branching based on the radii of the children at the branching points')],
    name='Branching Method',
    default=nmv.enums.Skeleton.Branching.ANGLES)

# Are the mesh objects connected or disconnected.
bpy.types.Scene.NMV_MeshObjectsConnection = bpy.props.EnumProperty(
    items=[(nmv.enums.Meshing.ObjectsConnection.CONNECTED,
            'Connected',
            'Connect all the objects of the mesh into one piece'),
           (nmv.enums.Meshing.ObjectsConnection.DISCONNECTED,
            'Disconnected',
            'Keep the different mesh objects of the neuron into separate pieces')],
    name='Mesh Objects',
    default=nmv.enums.Meshing.ObjectsConnection.DISCONNECTED)

# Is the output model for reality or beauty
bpy.types.Scene.NMV_SurfaceRoughness = bpy.props.EnumProperty(
    items=[(nmv.enums.Meshing.Surface.ROUGH,
            'Rough',
            'Create a mesh that looks like a real neuron reconstructed from microscope'),
           (nmv.enums.Meshing.Surface.SMOOTH,
            'Smooth',
            'Create a mesh that has smooth surface for visualization')],
    name='Model',
    default=nmv.enums.Meshing.Surface.SMOOTH)

# Spine sources can be random or from a BBP circuit
bpy.types.Scene.NMV_SpinesSourceCircuit = bpy.props.EnumProperty(
    items=[(nmv.enums.Meshing.Spines.Source.IGNORE,
            'Ignore',
            'Ignore creating the spines'),
           (nmv.enums.Meshing.Spines.Source.RANDOM,
            'Random',
            'The spines are generated randomly'),
           (nmv.enums.Meshing.Spines.Source.CIRCUIT,
            'Circuit',
            'The spines are generated following a BBP circuit'),],
    name='Spines Source',
    default=nmv.enums.Meshing.Spines.Source.IGNORE)

# Spine sources are only random
bpy.types.Scene.NMV_SpinesSourceRandom = bpy.props.EnumProperty(
    items=[(nmv.enums.Meshing.Spines.Source.IGNORE,
            'Ignore',
            'Ignore creating the spines'),
           (nmv.enums.Meshing.Spines.Source.RANDOM,
            'Random',
            'The spines are generated randomly')],
    name='Spines Source',
    default=nmv.enums.Meshing.Spines.Source.IGNORE)

# Spine meshes quality
bpy.types.Scene.NMV_SpineMeshQuality = bpy.props.EnumProperty(
    items=[(nmv.enums.Meshing.Spines.Quality.LQ,
            'Low',
            'Load low quality meshes'),
           (nmv.enums.Meshing.Spines.Quality.HQ,
            'High',
            'Load high quality meshes')],
    name='Spines Quality',
    default=nmv.enums.Meshing.Spines.Quality.LQ)

# Nucleus
bpy.types.Scene.NMV_Nucleus = bpy.props.EnumProperty(
    items=[(nmv.enums.Meshing.Nucleus.IGNORE,
            'Ignore',
            'The nucleus is ignored'),
           (nmv.enums.Meshing.Nucleus.INTEGRATED,
            'Integrated',
            'The nucleus is integrated')],
    name='Nucleus',
    default=nmv.enums.Meshing.Nucleus.IGNORE)

# Nucleus mesh quality
bpy.types.Scene.NMV_NucleusMeshQuality = bpy.props.EnumProperty(
    items=[(nmv.enums.Meshing.Nucleus.Quality.LQ,
            'Low',
            'Low quality nucleus mesh'),
           (nmv.enums.Meshing.Nucleus.Quality.HQ,
            'High',
            'High quality nucleus mesh')],
    name='Nucleus Mesh Quality',
    default=nmv.enums.Meshing.Nucleus.Quality.LQ)

# Fix artifacts flag
bpy.types.Scene.NMV_FixMorphologyArtifacts = bpy.props.BoolProperty(
    name='Fix Morphology Artifacts',
    description='Fixes the morphology artifacts during the mesh reconstruction process',
    default=True)

# Mesh tessellation flag
bpy.types.Scene.NMV_TessellateMesh = bpy.props.BoolProperty(
    name='Tessellation',
    description='Tessellate the reconstructed mesh to reduce the geometry complexity',
    default=False)

# Mesh tessellation level
bpy.types.Scene.NMV_MeshTessellationLevel = bpy.props.FloatProperty(
    name='Factor',
    description='Mesh tessellation level (between 0.1 and 1.0)',
    default=1.0, min=0.1, max=1.0)

# Random spines percentage
bpy.types.Scene.NMV_NumberSpinesPerMicron = bpy.props.FloatProperty(
    name='Density',
    description='The number of spines per micron',
    default=50, min=1.0, max=100.0)

bpy.types.Scene.NMV_MeshMaterial = bpy.props.EnumProperty(
    items=nmv.enums.Shader.MATERIAL_ITEMS,
    name="Shading",
    default=nmv.enums.Shader.LAMBERT_WARD)

# Use single color for the all the objects in the mesh
bpy.types.Scene.NMV_MeshHomogeneousColor = bpy.props.BoolProperty(
    name="Homogeneous Color",
    description="Use a single color for rendering all the objects of the mesh",
    default=False)

# A homogeneous color for all the objects of the mesh (membrane and spines)
bpy.types.Scene.NMV_NeuronMeshColor = bpy.props.FloatVectorProperty(
    name="Membrane Color", subtype='COLOR',
    default=nmv.enums.Color.SOMA, min=0.0, max=1.0,
    description="The homogeneous color of the reconstructed mesh membrane")

# The color of the reconstructed soma mesh
bpy.types.Scene.NMV_SomaMeshColor = bpy.props.FloatVectorProperty(
    name="Soma Color", subtype='COLOR',
    default=nmv.enums.Color.SOMA, min=0.0, max=1.0,
    description="The color of the reconstructed soma mesh")

# The color of the reconstructed axon mesh
bpy.types.Scene.NMV_AxonMeshColor = bpy.props.FloatVectorProperty(
    name="Axon Color", subtype='COLOR',
    default=nmv.enums.Color.AXONS, min=0.0, max=1.0,
    description="The color of the reconstructed axon mesh")

# The color of the reconstructed basal dendrites meshes
bpy.types.Scene.NMV_BasalDendritesMeshColor = bpy.props.FloatVectorProperty(
    name="Basal Dendrites Color", subtype='COLOR',
    default=nmv.enums.Color.BASAL_DENDRITES, min=0.0, max=1.0,
    description="The color of the reconstructed basal dendrites")

# The color of the reconstructed apical dendrite meshes
bpy.types.Scene.NMV_ApicalDendriteMeshColor = bpy.props.FloatVectorProperty(
    name="Apical Dendrite Color", subtype='COLOR',
    default=nmv.enums.Color.APICAL_DENDRITES, min=0.0, max=1.0,
    description="The color of the reconstructed apical dendrite")

# The color of the spines meshes
bpy.types.Scene.NMV_SpinesMeshColor = bpy.props.FloatVectorProperty(
    name="Spines Color", subtype='COLOR',
    default=nmv.enums.Color.SPINES, min=0.0, max=1.0,
    description="The color of the spines")

# The color of the nucleus mesh
bpy.types.Scene.NMV_NucleusMeshColor = bpy.props.FloatVectorProperty(
    name="Nucleus Color", subtype='COLOR',
    default=nmv.enums.Color.NUCLEI, min=0.0, max=1.0,
    description="The color of the nucleus")

# Rendering resolution
bpy.types.Scene.NMV_MeshRenderingResolution = bpy.props.EnumProperty(
    items=[(nmv.enums.Rendering.Resolution.FIXED,
            'Fixed',
            'Renders an image of the mesh at a specific resolution'),
           (nmv.enums.Rendering.Resolution.TO_SCALE,
            'To Scale',
            'Renders an image of the mesh at factor of the exact scale in (um)')],
    name='Type',
    default=nmv.enums.Rendering.Resolution.FIXED)

# Rendering view
bpy.types.Scene.NMV_MeshRenderingView = bpy.props.EnumProperty(
    items=[(nmv.enums.Rendering.View.WIDE_SHOT,
            'Wide Shot',
            'Renders an image of the full view'),
           (nmv.enums.Rendering.View.MID_SHOT,
            'Mid Shot',
            'Renders an image of the reconstructed arbors only'),
           (nmv.enums.Rendering.View.CLOSE_UP,
            'Close Up',
            'Renders a close up image the focuses on the soma')],
    name='View', default=nmv.enums.Rendering.View.MID_SHOT)

# Keep cameras
bpy.types.Scene.NMV_KeepMeshCameras = bpy.props.BoolProperty(
    name="Keep Cameras & Lights in Scene",
    description="Keep the cameras in the scene to be used later if this file is saved",
    default=False)

# Image format
bpy.types.Scene.NMV_MeshImageFormat = bpy.props.EnumProperty(
    items=nmv.enums.Image.Extension.IMAGE_EXTENSION_ITEMS,
    name='',
    default=nmv.enums.Image.Extension.PNG)

# Image resolution
bpy.types.Scene.NMV_MeshFrameResolution = bpy.props.IntProperty(
    name='Resolution',
    description='The resolution of the image generated from rendering the mesh',
    default=512, min=128, max=1024 * 10)

# Frame scale factor 'for rendering to scale option '
bpy.types.Scene.NMV_MeshFrameScaleFactor = bpy.props.FloatProperty(
    name="Scale", default=1.0, min=1.0, max=100.0,
    description="The scale factor for rendering a mesh to scale")

# Mesh rendering close up size
bpy.types.Scene.NMV_MeshCloseUpSize = bpy.props.FloatProperty(
    name='Size',
    description='The size of the view that will be rendered in microns',
    default=20, min=5, max=100,)

# Soma rendering progress bar
bpy.types.Scene.NMV_NeuronMeshRenderingProgress = bpy.props.IntProperty(
    name="Rendering Progress",
    default=0, min=0, max=100, subtype='PERCENTAGE')

# Individual components export flag
bpy.types.Scene.NMV_ExportIndividuals = bpy.props.BoolProperty(
    name='Export Components',
    description='Export each component of the neuron as a separate mesh. This feature is '
                'important to label reconstructions with machine learning applications',
    default=False)

# Exported mesh file formats
bpy.types.Scene.NMV_ExportedMeshFormat = bpy.props.EnumProperty(
    items=[(nmv.enums.Meshing.ExportFormat.PLY,
            'Stanford (.ply)',
            'Export the mesh to a .ply file'),
           (nmv.enums.Meshing.ExportFormat.OBJ,
            'Wavefront (.obj)',
            'Export the mesh to a .obj file'),
           (nmv.enums.Meshing.ExportFormat.STL,
            'Stereolithography CAD (.stl)',
            'Export the mesh to an .stl file'),
           (nmv.enums.Meshing.ExportFormat.BLEND,
            'Blender File (.blend)',
            'Export the mesh as a .blend file')],
    name='Format', default=nmv.enums.Meshing.ExportFormat.PLY)

# Reconstruction time
bpy.types.Scene.NMV_MeshReconstructionTime = bpy.props.FloatProperty(
    name="Reconstruction (Sec)",
    description="The time it takes to reconstruct the mesh and draw it to the viewport",
    default=0, min=0, max=1000000)

# Rendering time
bpy.types.Scene.NMV_MeshRenderingTime = bpy.props.FloatProperty(
    name='Rendering (Sec)',
    description='The time it takes to render the mesh into an image',
    default=0, min=0, max=1000000)

