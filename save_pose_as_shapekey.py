bl_info = {
    "name": "Save Pose as Shape Key",
    "blender": (2, 80, 0),
    "category": "3D View",
    "author": "AstroDoge",
    "version": (1, 0),
}

import bpy

class OBJECT_OT_save_pose_as_shape_key(bpy.types.Operator):
    bl_idname = "object.save_pose_as_shape_key"
    bl_label = "Save Pose as Shape Key"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Saves the current pose to the Target Mesh as a Shape Key"
    
    def execute(self, context):
        scene = context.scene
        target_mesh = scene.target_mesh
        shape_key_name = scene.shape_key_name
        keep_pose = scene.keep_pose_after_saving
        
        # Check if target_mesh is valid and has an armature modifier
        if target_mesh is None or target_mesh.type != 'MESH':
            self.report({'ERROR'}, "Please select a valid mesh object.")
            return {'CANCELLED'}
        
        armature_modifier = None
        for mod in target_mesh.modifiers:
            if mod.type == 'ARMATURE':
                armature_modifier = mod
                break
        
        if armature_modifier is None:
            self.report({'ERROR'}, "Selected mesh does not have an Armature modifier.")
            return {'CANCELLED'}
        
        # Check if the shape key name already exists
        if target_mesh.data.shape_keys and shape_key_name in target_mesh.data.shape_keys.key_blocks:
            self.report({'ERROR'}, "Shape key name already in use.")
            return {'CANCELLED'}
        
        # Save the current pose as shape key
        armature = armature_modifier.object
        
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.view_layer.objects.active = target_mesh
        target_mesh.select_set(True)
        
        bpy.ops.object.modifier_apply_as_shapekey(keep_modifier=True, modifier=armature_modifier.name)
        
        # Rename the new shape key
        shape_keys = target_mesh.data.shape_keys.key_blocks
        new_shape_key = shape_keys[-1]
        new_shape_key.name = shape_key_name
        
        if not keep_pose:
            # Reset pose of the armature to rest pose
            bpy.context.view_layer.objects.active = armature
            bpy.ops.object.mode_set(mode='POSE')
            bpy.ops.pose.select_all(action='SELECT')
            bpy.ops.pose.transforms_clear()
            bpy.ops.pose.select_all(action='DESELECT')
        
        # Set back to Pose Mode
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='POSE')
        
        return {'FINISHED'}

class OBJECT_OT_fix_basis_shape_key(bpy.types.Operator):
    bl_idname = "object.fix_basis_shape_key"
    bl_label = "Fix Basis Shape Key"
    bl_description = "Creates a Basis shape key for the target mesh"
    
    def execute(self, context):
        scene = context.scene
        target_mesh = scene.target_mesh
        
        if target_mesh is None or target_mesh.type != 'MESH':
            self.report({'ERROR'}, "Please select a valid mesh object.")
            return {'CANCELLED'}
        
        if target_mesh.data.shape_keys is None:
            target_mesh.shape_key_add(name="Basis")
        
        return {'FINISHED'}
    
class VIEW3D_PT_save_pose_as_shape_key_panel(bpy.types.Panel):
    bl_label = "Save Pose as Shape Key"
    bl_idname = "VIEW3D_PT_save_pose_as_shape_key_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Pose to Shape Key'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        layout.label(text="Target Mesh:")
        layout.prop_search(scene, "target_mesh", scene, "objects", text="")
        
        target_mesh = scene.target_mesh
        if target_mesh and target_mesh.type == 'MESH':
            shape_keys = target_mesh.data.shape_keys
            if shape_keys is None or "Basis" not in shape_keys.key_blocks:
                layout.label(text="Warning: No Basis Shape Key found!", icon='ERROR')
                layout.operator("object.fix_basis_shape_key", text="Fix")
        
        layout.label(text="Shape Key Name:")
        layout.prop(scene, "shape_key_name", text="")
        
        shape_key_name = scene.shape_key_name
        if target_mesh and target_mesh.data.shape_keys and shape_key_name in target_mesh.data.shape_keys.key_blocks:
            layout.label(text="Warning: Shape Key name already in use!", icon='ERROR')
            layout.prop(scene, "keep_pose_after_saving", text="Keep Pose After Saving")
            save_button = layout.operator("object.save_pose_as_shape_key", text="Save Pose as Shape Key")
            save_button.enabled = False
        else:
            layout.prop(scene, "keep_pose_after_saving", text="Keep Pose After Saving")
            layout.operator("object.save_pose_as_shape_key", text="Save Pose as Shape Key")

def register():
    bpy.utils.register_class(OBJECT_OT_save_pose_as_shape_key)
    bpy.utils.register_class(OBJECT_OT_fix_basis_shape_key)
    bpy.utils.register_class(VIEW3D_PT_save_pose_as_shape_key_panel)
    bpy.types.Scene.shape_key_name = bpy.props.StringProperty(name="Shape Key Name")
    bpy.types.Scene.target_mesh = bpy.props.PointerProperty(name="Target Mesh", type=bpy.types.Object)
    bpy.types.Scene.keep_pose_after_saving = bpy.props.BoolProperty(name="Keep Pose After Saving", default=False)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_save_pose_as_shape_key)
    bpy.utils.unregister_class(OBJECT_OT_fix_basis_shape_key)
    bpy.utils.unregister_class(VIEW3D_PT_save_pose_as_shape_key_panel)
    del bpy.types.Scene.shape_key_name
    del bpy.types.Scene.target_mesh
    del bpy.types.Scene.keep_pose_after_saving

if __name__ == "__main__":
    register()
