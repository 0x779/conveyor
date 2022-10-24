# Very small add on to start from

bl_info = {
    "name" : "Conveyor",
    "description" : "A nifty little 3D file format converter addon for Blender",
    "author" : "0x779",
    "version" : (0, 0, 1),
    "blender" : (2, 80, 0),
    "location" : "View3D",
    "warning" : "",
    "support" : "COMMUNITY",
    "doc_url" : "https://github.com/0x779/conveyor",
    "category" : "3D View"
}

import bpy
from pathlib import Path

from bpy.props import (StringProperty,
                       PointerProperty,
                       EnumProperty,
                       )

from bpy.types import (Panel,
                       Operator,
                       AddonPreferences,
                       PropertyGroup,
                       )
import os

inputPath = outputPath = inputFormat = outputFormat = ''


# ------------------------------------------------------------------------
#    Scene Properties
# ------------------------------------------------------------------------

class ConveyorProperties(PropertyGroup):

    pathIn : StringProperty(
        name="",
        description="Input path to Directory",
        default="",
        maxlen=1024,
        subtype='DIR_PATH')
    
    pathOut : StringProperty(
        name="",
        description="Output path to Directory",
        default="",
        maxlen=1024,
        subtype='DIR_PATH')

    formatIn: EnumProperty(
        items=(
            ("fbx", "FBX", ""),
            ("obj", "OBJ", ""),
            ("gltf", "GLTF/GLB", ""),
            ("dae", "DAE", ""),
        ),
        name="Imported formats",
        default="fbx",
        description="Imported formats",
    )

    formatOut: EnumProperty(
        items=(
            ("fbx", "FBX", ""),
            ("obj", "OBJ", ""),
            ("gltf", "GLTF (Embedded)", ""),
            ("gltfs", "GLTF (Separate)", ""),
            ("glb", "GLB", ""),
            ("dae", "DAE", ""),
        ),
        name="Exported formats",
        default="obj",
        description="Exported formats",
    )

# ------------------------------------------------------------------------
#    Panel in Object Mode
# ------------------------------------------------------------------------

class OBJECT_PT_CustomPanel(Panel):
    bl_idname = "OBJECT_PT_CustomPanel"
    bl_label = "Conveyor"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "Conveyor"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Input")
        scn = context.scene
        col = layout.column(align=True)
        box = layout.box()
        box.prop(scn.conveyor_tool, "pathIn", text="Folder")
        box.prop(scn.conveyor_tool, "formatIn", text="Format")

        layout.label(text="Output")
        scn = context.scene
        col = layout.column(align=True)
        box = layout.box()
        box.prop(scn.conveyor_tool, "pathOut", text="Folder")
        box.prop(scn.conveyor_tool, "formatOut", text="Format")

        layout.operator(Conveyor_OT_custom.bl_idname)

        # print the path to the console
        #print (scn.conveyor_tool.pathIn)
        

class Conveyor_OT_custom(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.convert"
    bl_label = "Convert"

    def execute(self, context):
        # Your code here 
        # ...

        convertor(
            str(context.scene.conveyor_tool.pathIn),
            str(context.scene.conveyor_tool.formatIn),
            str(context.scene.conveyor_tool.pathOut),
            str(context.scene.conveyor_tool.formatOut)
            ) 
       # print ("input dir: " + str(context.scene.conveyor_tool.pathIn))
       # print ("input format: " + str(context.scene.conveyor_tool.formatIn))
       # print ("output dir: " + str(context.scene.conveyor_tool.pathOut))
       # print ("output format: " + str(context.scene.conveyor_tool.formatOut))
        return {'FINISHED'}

# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

classes = (
    ConveyorProperties,
    OBJECT_PT_CustomPanel,
    Conveyor_OT_custom,
    
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.conveyor_tool = PointerProperty(type=ConveyorProperties)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.conveyor_tool


if __name__ == "__main__":
    register()


def convertor(pathIn, formatIn, pathOut, formatOut):
    for root, dirs, files in os.walk(pathIn):
        for f in files:
            if f.lower().endswith('.' + str(formatIn)) :
                in_file = os.path.join(pathIn, f)
                if (formatOut == "gltfs"):
                    out_file = os.path.join(pathOut, Path(in_file).stem + ".gltf")
                else:
                    out_file = os.path.join(pathOut, Path(in_file).stem + "." + str(formatOut))


                print (out_file)
            

                bpy.ops.object.select_all(action='SELECT')
                bpy.ops.object.delete()
                match formatIn:
                    case 'fbx':
                        bpy.ops.import_scene.fbx(filepath=in_file)
                    case 'obj':
                        bpy.ops.import_scene.obj(filepath=in_file)
                    case 'gltf':
                        bpy.ops.import_scene.gltf(filepath=in_file)
                    case 'dae':
                        bpy.ops.wm.collada_import(filepath = in_file, auto_connect = True, find_chains = True, fix_orientation = True)
                    case _:
                        bpy.ops.object.select_all(action='SELECT')
                        bpy.ops.object.delete()

                bpy.ops.object.select_all(action='SELECT')

                match formatOut:
                    case 'fbx':
                        bpy.ops.export_scene.fbx(filepath=out_file)
                    case 'obj':
                        bpy.ops.export_scene.obj(filepath=out_file)
                    case 'gltf':
                        bpy.ops.export_scene.gltf(filepath=out_file, export_format='GLTF_EMBEDDED')
                    case 'gltfs':
                        bpy.ops.export_scene.gltf(filepath=out_file, export_format='GLTF_SEPARATE')
                    case 'glb':
                        bpy.ops.export_scene.gltf(filepath=out_file, export_format='GLB')
                    case 'dae':
                        bpy.ops.wm.collada_export(filepath = out_file, use_texture_copies=False)
                    case _:
                        bpy.ops.object.select_all(action='SELECT')
                        bpy.ops.object.delete()

    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()