bl_info = {
    "name": "复制和分离材质(维持法向)",
    "author": "_Alicia, FK, Kijo Hassen",
    "version": (1, 1, 1),
    "blender": (4, 3, 2),
    "location": "视图3D > 属性面板 > 复制和分离材质(维持法向)",
    "description": "基于选择顺序复制和粘贴PMX模型的材质，忽略对象名称，并支持顶点组和UV映射的复制",
    "category": "Object",
}

import bpy

# 全局变量，用于存储复制的材质和相关数据
copied_data = []

class PMXMaterialCopyPanel(bpy.types.Panel):
    bl_label = "复制和分离材质(维持法向)"
    bl_idname = "VIEW3D_PT_pmx_material_copy"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'MMD'

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("object.copy_pmx_materials", text="复制材质")
        row = layout.row()
        row.operator("object.paste_pmx_materials", text="粘贴材质")
        row = layout.row()
        row.operator("object.clear_copied_pmx_materials", text="清空复制材质")
        row = layout.row()
        row.operator("mmd.separate_materials", text="分离材质(维持法向)")

class CopyPMXMaterialsOperator(bpy.types.Operator):
    bl_idname = "object.copy_pmx_materials"
    bl_label = "复制材质"
    bl_description = "从选择的源对象复制材质、材质分配、顶点组和UV映射"

    def execute(self, context):
        global copied_data

        selected_objects = context.selected_objects

        if not selected_objects:
            self.report({'WARNING'}, "请至少选择一个源对象")
            return {'CANCELLED'}

        copied_data = []

        for obj in selected_objects:
            if obj.type == 'MESH':
                # 直接引用原始材质球，而不是复制
                materials = [mat for mat in obj.data.materials]
                material_indices = [poly.material_index for poly in obj.data.polygons]
                
                # 复制顶点组及其权重
                vertex_groups = []
                for vg in obj.vertex_groups:
                    vg_data = {
                        'name': vg.name,
                        'index': vg.index,
                        'weights': {}
                    }
                    for v in obj.data.vertices:
                        for g in v.groups:
                            if g.group == vg.index:
                                vg_data['weights'][v.index] = g.weight
                    vertex_groups.append(vg_data)
                
                uv_layers = {uv.name: [loop.uv.copy() for loop in uv.data] for uv in obj.data.uv_layers}
                copied_data.append({
                    'name': obj.name,
                    'materials': materials,
                    'material_indices': material_indices,
                    'vertex_groups': vertex_groups,
                    'uv_layers': uv_layers,
                    'poly_count': len(obj.data.polygons),
                    'vertex_count': len(obj.data.vertices),
                    'edge_count': len(obj.data.edges)
                })
            else:
                self.report({'INFO'}, f"跳过非网格对象：{obj.name}")

        if not copied_data:
            self.report({'WARNING'}, "没有选中的网格对象可供复制")
            return {'CANCELLED'}

        self.report({'INFO'}, f"已从 {len(copied_data)} 个对象复制材质、顶点组和UV映射")
        return {'FINISHED'}

class PastePMXMaterialsOperator(bpy.types.Operator):
    bl_idname = "object.paste_pmx_materials"
    bl_label = "粘贴材质"
    bl_description = "将材质、材质分配、顶点组和UV映射粘贴到选择的目标对象"

    def execute(self, context):
        global copied_data

        if not copied_data:
            self.report({'WARNING'}, "没有复制的材质，请先点击'复制材质'")
            return {'CANCELLED'}

        selected_objects = context.selected_objects

        if not selected_objects:
            self.report({'WARNING'}, "请至少选择一个目标对象")
            return {'CANCELLED'}

        if len(selected_objects) != len(copied_data):
            self.report({'WARNING'}, "选择的目标对象数量与复制的源对象数量不一致")
            return {'CANCELLED'}

        pasted_objects = 0

        for index, target_obj in enumerate(selected_objects):
            if target_obj.type != 'MESH':
                self.report({'INFO'}, f"跳过非网格对象：{target_obj.name}")
                continue

            source_data = copied_data[index]

            if (len(target_obj.data.polygons) != source_data['poly_count'] or
                len(target_obj.data.vertices) != source_data['vertex_count'] or
                len(target_obj.data.edges) != source_data['edge_count']):
                self.report({'WARNING'}, f"对象 {target_obj.name} 的几何结构与源对象不匹配，未粘贴材质")
                continue

            target_obj.data.materials.clear()
            for mat in source_data['materials']:
                target_obj.data.materials.append(mat)

            for i, poly in enumerate(target_obj.data.polygons):
                poly.material_index = source_data['material_indices'][i]

            # 粘贴顶点组及其权重
            for vg_data in source_data['vertex_groups']:
                vg_name = vg_data['name']
                vg_weights = vg_data['weights']
                
                if vg_name not in target_obj.vertex_groups:
                    vg = target_obj.vertex_groups.new(name=vg_name)
                else:
                    vg = target_obj.vertex_groups[vg_name]
                
                for v_index, weight in vg_weights.items():
                    vg.add([v_index], weight, 'REPLACE')

            # 粘贴UV映射
            for uv_name, uv_data in source_data['uv_layers'].items():
                if uv_name not in target_obj.data.uv_layers:
                    uv_layer = target_obj.data.uv_layers.new(name=uv_name)
                else:
                    uv_layer = target_obj.data.uv_layers[uv_name]
                for loop, uv in zip(target_obj.data.loops, uv_data):
                    uv_layer.data[loop.index].uv = uv

            pasted_objects += 1

        if pasted_objects == 0:
            self.report({'WARNING'}, "没有粘贴任何材质。请检查目标对象是否与源对象匹配")
            return {'CANCELLED'}

        self.report({'INFO'}, f"已将材质、顶点组和UV映射粘贴到 {pasted_objects} 个对象")
        return {'FINISHED'}

class ClearCopiedPMXMaterialsOperator(bpy.types.Operator):
    bl_idname = "object.clear_copied_pmx_materials"
    bl_label = "清空复制材质"
    bl_description = "清空已复制的材质数据"

    def execute(self, context):
        global copied_data
        copied_data = []
        self.report({'INFO'}, "已清空复制的材质数据")
        return {'FINISHED'}

def duplicate_object_based_on_materials():
    """
    根据当前活动对象的材质数量，
    复制对象并对每个复制对象：
      1. 进入编辑模式后选择对应材质的面，
      2. 反选删除其他面，
      3. 移除其他材质槽，
    最后删除原始对象，并根据 PMX 材质顺序重命名对象。
    确保分离后的对象保留在原始集合中。
    """
    obj = bpy.context.active_object
    if obj and obj.type == 'MESH':
        material_count = len(obj.data.materials)
        if material_count > 0:
            # 获取 PMX 材质顺序
            pmx_material_names = [mat.name for mat in obj.data.materials]
            
            # 获取原始对象的父集合
            original_collections = obj.users_collection
            
            duplicates = []
            for i in range(material_count):
                # 复制对象和数据
                new_obj = obj.copy()
                new_obj.data = obj.data.copy()
                
                # 将新对象链接到原始对象的父集合中
                for coll in original_collections:
                    coll.objects.link(new_obj)
                
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

classes = (
    PMXMaterialCopyPanel,
    CopyPMXMaterialsOperator,
    PastePMXMaterialsOperator,
    ClearCopiedPMXMaterialsOperator,
    MMD_OT_separate_materials,
)

def register(): 
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister(): 
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__": 
    register()
