import bpy


bl_info = {
    "name": "Select Non-Deforming Bones",
    "author": "AstroDoge",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "Select > Select Non-Deforming Bones",
    "description": "Selects all bones in Edit Mode that have the deform property disabled.",
    "category": "Rigging"
}


class SelectNonDeformingBones(bpy.types.Operator):
    """Selects all bones in Edit Mode that have the deform property disabled"""
    bl_idname = "object.select_non_deforming_bones"
    bl_label = "Select Non-Deforming Bones"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.object and context.object.type == 'ARMATURE' and context.mode == 'EDIT_ARMATURE'

    def execute(self, context):
        armature = context.object.data
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.armature.select_all(action='DESELECT')
        for bone in armature.edit_bones:
            if not bone.use_deform:
                bone.select = True
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(SelectNonDeformingBones.bl_idname)


def register():
    bpy.utils.register_class(SelectNonDeformingBones)
    bpy.types.VIEW3D_MT_select_edit_armature.append(menu_func)


def unregister():
    bpy.utils.unregister_class(SelectNonDeformingBones)
    bpy.types.VIEW3D_MT_select_edit_armature.remove(menu_func)


if __name__ == "__main__":
    register()
