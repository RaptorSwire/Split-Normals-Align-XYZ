#
# Feel free to use or modify any parts of this program to your liking.
# I am publishing it to help others who may find this little addon 
# useful. I am total noob developer, so please do not judge my skills,
# however if you have any suggestions, please feel free to 
# contact me via Raptolion@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# Thanks guys in Blender community forum for help.


bl_info = {
    "name" : "Split Normals Align XYZ",
    "author" : "Raptor",
    "description" : "Align vector split normals to the grid using X,Y, or Z axis.",
    "blender" : (2, 80, 0),
    "version" : (1, 0, 0),
    "location" : "View3D",
    "warning" : "",
    "category" : "Mesh"
}

import bpy

from . Normals_Align_XYZ   import XYZ_PT_Panel, Normals_OT_Operator


# defining what are the classes to register
classes = (Normals_OT_Operator, XYZ_PT_Panel) 

# registering classes
register, unregister = bpy.utils.register_classes_factory(classes)