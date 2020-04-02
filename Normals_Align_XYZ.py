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


import bpy, bmesh, itertools
import numpy as np
from bpy.props import FloatProperty
from bpy.props import EnumProperty
from mathutils import *

# Panel with buttons
class XYZ_PT_Panel(bpy.types.Panel):
    bl_idname = "XYZ_PT_Panel"
    bl_label = "XYZ_Panel"
    bl_category = "Align SN"    # name shown on the side panel
    bl_space_type = "VIEW_3D"   # this needs to be here since 2.80
    bl_region_type = "UI"       # show on the N panel

    def draw(self, context):    # this visualizes buttons in the UI
        layout = self.layout

        row = layout.row()
        row.scale_y = 2.0       # button height
        row.operator('obj.align', text = "X", icon = "AXIS_SIDE").action = 'X'
        row.operator('obj.align', text = "Y", icon = "AXIS_FRONT").action = 'Y'
        row.operator('obj.align', text = "Z", icon = "AXIS_TOP").action = 'Z'


# Main program
class Normals_OT_Operator(bpy.types.Operator):
    bl_idname = "obj.align"
    bl_label = "Align Normals"        # this is the phrase which can be searched in Blender search and activated from there
    bl_description = "Align Normals to Grid XYZ axis"

    # enumeration to make buttons recognize different axis
    action: EnumProperty(
        items=[
            ('X', 'align x', 'align x'),
            ('Y', 'align y', 'align y'),
            ('Z', 'align z', 'align z')
        ]
    )


    def execute(self, context):     

        obj = bpy.context.active_object
        axis = None

        # Finding which button was pressed
        # x = 0, y = 1, z = 2
        if self.action == 'X':
            axis = 0
        elif self.action == 'Y':
            axis = 1
        elif self.action == 'Z':
            axis = 2

        
        # Getting index of currently selected vertices

        def get_vertex_data(obj):
            # Any Rotation and Scale needs to be applied, or the program will glitch.
            bpy.ops.object.mode_set(mode = 'OBJECT')        
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=True) 
            bpy.ops.object.mode_set(mode = 'EDIT') 

            obj.update_from_editmode()
            bpy.context.view_layer.update()
            obj_matrix = obj.matrix_world
            mesh = obj.data
            mesh.calc_normals_split()
            bm = bmesh.from_edit_mesh(mesh)
            
            # --------------------------------------------------------------------------------

            # 1.0 Create list of all selected vertices (index)

            #create list: add vert for every vert in bm.verts that is selected
            selected_verts = [vert for vert in bm.verts if vert.select]     
            
            #print(selected_verts)

            if len(selected_verts) is 0:    # check if verts are selected
                self.report({'INFO'}, 'No vertices selected.')
                return {'CANCELLED'}


            # for every selected vertex...
            all_selected_vertices = []
            for v in selected_verts:

                # Calculate global coords of each vertex considering object's transform
                v_local = v.co                    # local vert coords
                v_global = obj_matrix @ v_local   # global vert coords


                # Get split normals...
                # Gather world space normal vectors associated with selected vertex
                # (I have no idea how this part works. If you have any suggestions on how to improve this add-on, 
                # please contact me on Raptolion@gmail.com I will appreciate it!)
                splitNs_onVertex = set(
                    (obj_matrix @ mesh.loops[loop.index].normal).to_tuple()
                    for loop in v.link_loops
                )
                splitNs_onVertex = list(splitNs_onVertex)     # convert gathered data into list []


                    # All the split normals on vertex have to be pointed together unfortunatelly. 
                    # I recommend using Alt-N -> Average -> Custom Normal to average their position first
                    # or splitting their faces using Y.


                # Average the direction in case there are multiple split normals on vertex.

                # add the corresponding axis of all split normals...
                OnlySplitNormal = Vector()
                avgx = 0
                avgy = 0
                avgz = 0
                for sn in splitNs_onVertex:
                    avgx = avgx + sn[0]
                    avgy = avgy + sn[1]
                    avgz = avgz + sn[2]
                # and divide each axis by amount of split normals
                avgx = avgx/len(splitNs_onVertex)
                avgy = avgy/len(splitNs_onVertex)
                avgz = avgz/len(splitNs_onVertex)
                
                # add xyz values to vector
                OnlySplitNormal.x = avgx
                OnlySplitNormal.y = avgy
                OnlySplitNormal.z = avgz


                #print('\033[90m' + 'loc: ' + str(v_local))
                #print('\033[90m' + 'glo: ' + str(v_global))
                #print('\033[93m' + 'split normals local: ' + str(nor_local))


                # to consider any transform of the object, we need to subtract object's location from split normal's vectors
                normal = []
                n = [b - a for a, b in zip(obj.location, OnlySplitNormal)]
                normal.append(Vector(n))
                

                # create dictionary of data for each vertex (index, coords, split normals)
                vertex = {'index': v.index, 'coords': v_global, 'normals': normal}
                print('\033[92m' + str(vertex))
                all_selected_vertices.append(vertex)    # add this vertex data to the list

            #print(all_selected_vertices)


            # 2.0 For every vertex normal create virtual target split normals will be pointing at

            # Select every vertex individually...
            for vert in all_selected_vertices:
                # Deselect all (To make this work properly, it seems like we need to re-enter Edit mode)
                bpy.ops.object.mode_set(mode = 'OBJECT')
                bpy.ops.object.mode_set(mode = 'EDIT') 
                bpy.ops.mesh.select_mode(type="VERT")
                bpy.ops.mesh.select_all(action = 'DESELECT')

                # Select next vertex (next index number in ascending order)
                # vertex selection can only be done in Object mode for some reason
                bpy.ops.object.mode_set(mode = 'OBJECT') 
                obj.data.vertices[vert['index']].select = True
                bpy.ops.object.mode_set(mode = 'EDIT')

                #print('\033[34m' + 'Vertex ' + str(vert['index']) + ' selected.')

                
                # Create virtual target for each split normal on the vertex
                # Note: later I figured out I can only point all split normals altogether on single vertex,
                # so the "for each split normal" method isn't really neccessary, but I keep it here if somebody 
                # finds out how to do it. If you have any suggestion how to point individual SplitNormal, please
                # contact me on Raptolion@gmail.com
                for split_normal in vert['normals']:
                    #print(split_normal)

                    target = Vector(vert['coords'] + split_normal)  # "target" is located next to the vertex in direction of split normal
                    #print('\033[93m' + "Target before: " + str(target))

                    # align target with selected axis of vertex depending on selected axis
                    # it simply copies the coord value on selected axis
                    if axis is 0:
                        target.x = vert['coords'].x
                    elif axis is 1:
                        target.y = vert['coords'].y
                    elif axis is 2:
                        target.z = vert['coords'].z

                    #print('\033[93m' + "Target after: " + str(target))


                    # 3.0 Aim at virtual target
                    # Let me know if there is better way to do this. 
                    # I just copied this from Blender when using Normals -> Point To Target (Alt-L) function
                    bpy.ops.mesh.point_normals(target_location=(target))
                

            # Reselect what was selected by user before operation
            for selected_verts in all_selected_vertices:
                bpy.ops.mesh.select_mode(type="VERT")
                bpy.ops.object.mode_set(mode = 'OBJECT') 
                obj.data.vertices[selected_verts['index']].select = True
                bpy.ops.object.mode_set(mode = 'EDIT') 

            # FINISHED
        
        
        # checking if user is in the edit mode
        if obj.mode == 'EDIT':
            get_vertex_data(obj)
        else:
            self.report({'INFO'}, 'This only works in Edit Mode')


        return{'FINISHED'}