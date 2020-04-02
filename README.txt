Thanks for downloading my addon!

Feel free to use or modify any parts of this program to your liking.
I am publishing it to help others who may find this little addon 
useful. I am total noob developer, so please do not judge my skills,
however if you have any suggestions, please feel free to 
contact me via Raptolion@gmail.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

Hope my addon will save someone's time before Blender devs will publish 
something official to address current split normals limitation.

Thanks to guys in Blender community forum for help!

-----------------------------------------------------------------------

This addon is designed for Blender 2.80. Was not tested in other versions.

INSTALLATION:

1. In Blender go to Edit > Preferences... > Add-ons tab
2. Click "Install..."
3. Locate the Split_Normals_Align_XYZ.zip file
4. Enable the addon and it will show up in your side panel (N panel)
5. Enjoy


HOW DOES IT WORK:

I found it quite complicated to target split normals to certain direction.
In my case I needed the selected vertice's split normals to get perpendicular
with selected axis.

This addon is created for that one purpose (but you can play with the code, if
you want to adjust something).

1. In Edit mode select vertices you want to modify split normals on 
   (works for multiple selected vertices).
2. In the right ("N") panel open tab called Align SN.
3. Click which axis you want your split normals to align on.


KNOWN ISSUES:

- If there is more than one split normal on selected vertex, their directions WILL BE
  AVERAGED INTO SINGLE VECTOR and then processed by addon. I did not find a way 
  to edit split normals on single vertex individually. (If you know how to do this,
  feel free to contact me.) If you need to modify split normals individually,
  you need to cut the object into pieces or maybe somehow use "Mark Sharp edge" function.
  
- Any Scale or Rotation transforms on Object will be applied by addon. 
  Location transform will remain untouched.
  
- Undo sometimes rotates the object and I have no idea why, but it will be fixed if you
  undo it once again. It has something to do with rotations done to object before.

- Also if your split normal is pointing directly for example UP, don't try to align it 
  with Z axis because that will squish it into zero and your normals will be messed up.
  The split normals should always be at least little bit pointing to the direction
  you intend the result to go. Just try it on your own on the default cube :)

