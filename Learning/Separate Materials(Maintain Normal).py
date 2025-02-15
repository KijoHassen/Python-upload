bl_info = {
    "name": "分离材质(维持法向)",
    "author": "_Alicia, Kijo Hassen",
    "description": "复制当前网格对象，并按材质分离各部分，保留原法向信息，同时按 PMX 材质顺序重命名对象",
    "blender": (4, 3, 2),
    "version": (1, 0, 2),
    "location": "3D View > UI > MMD Tools（杂项）",
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
    "category": "3D View"
}

import bpy
import bpy.utils.previews

# 全局预览集合（如果需要自定义图标，这里初始化）
_icons = None

def duplicate_object_based_on_materials():
    """
    根据当前活动对象的材质数量，
    复制对象并对每个复制对象：
      1. 进入编辑模式后选择对应材质的面，
      2. 反选删除其他面，
      3. 移除其他材质槽，
    最后删除原始对象，并根据 PMX 材质顺序重命名对象。
    """
    obj = bpy.context.active_object
    if obj and obj.type == 'MESH':
        material_count = len(obj.data.materials)
        if material_count > 0:
            # 获取 PMX 材质顺序
            pmx_material_names = [mat.name for mat in obj.data.materials]
            
            duplicates = []
            for i in range(material_count):
                # 复制对象和数据
                new_obj = obj.copy()
                new_obj.data = obj.data.copy()
                bpy.context.collection.objects.link(new_obj)
                duplicates.append(new_obj)
                print(f"Created duplicate {i+1} of {obj.name}")
            
            # 删除原始对象
            bpy.data.objects.remove(obj)
            bpy.ops.object.select_all(action='DESELECT')
            
            # 对每个复制对象处理：选择对应材质的面、删除其它面、移除其它材质，并重命名对象
            for i, duplicate in enumerate(duplicates):
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = duplicate
                duplicate.select_set(True)
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.ops.mesh.select_mode(type='FACE')
                
                if i < len(duplicate.data.materials):
                    bpy.context.object.active_material_index = i
                    bpy.ops.object.material_slot_select()
                    bpy.ops.mesh.select_all(action='INVERT')
                    bpy.ops.mesh.delete(type='FACE')
                    bpy.ops.object.mode_set(mode='OBJECT')
                    
                    # 保留当前材质，移除其他材质槽
                    for j in range(len(duplicate.data.materials) - 1, -1, -1):
                        if j != i:
                            duplicate.active_material_index = j
                            bpy.ops.object.material_slot_remove()
                    
                    # 重新命名对象为 "索引_材质名称"
                    if i < len(pmx_material_names):
                        new_name = f"{i:03d}_{pmx_material_names[i]}"
                        duplicate.name = new_name
                        duplicate.data.name = new_name
                        print(f"Renamed object to {new_name}")
        else:
            print("Object has no materials, no duplicates created.")
    else:
        print("No valid mesh object selected.")

# 自定义操作符，调用 duplicate_object_based_on_materials() 函数
class MMD_OT_separate_materials(bpy.types.Operator):
    bl_idname = "mmd.separate_materials"
    bl_label = "分离材质操作"
    bl_description = "复制当前网格对象，并按材质分离各部分，保留原法向信息，同时按 PMX 材质顺序重命名对象"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        duplicate_object_based_on_materials()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)

# 自定义绘制函数，将按钮添加到 MMD Tools 模型设定面板中“杂项”部分
def my_draw_func(self, context):
    layout = self.layout
    layout.operator(MMD_OT_separate_materials.bl_idname, text="分离材质(维持法向)", icon='MATERIAL')

# 注册时将自定义绘制函数追加到已有的 MMD Tools 模型设定面板上
def register():
    global _icons
    _icons = bpy.utils.previews.new()
    bpy.utils.register_class(MMD_OT_separate_materials)
    # 将绘制函数追加到 MMD Tools 模型设定面板（例如 OBJECT_PT_mmd_tools_model_setup）中
    bpy.types.OBJECT_PT_mmd_tools_model_setup.append(my_draw_func)
    print("分离材质插件已注册。")

def unregister():
    global _icons
    bpy.utils.previews.remove(_icons)
    bpy.types.OBJECT_PT_mmd_tools_model_setup.remove(my_draw_func)
    bpy.utils.unregister_class(MMD_OT_separate_materials)
    print("分离材质插件已注销。")

if __name__ == "__main__":
    register()
