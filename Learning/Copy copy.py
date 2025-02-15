bl_info = {
    "name": "PMX材质复制插件（修订版）",
    "author": "FK",
    "version": (1, 2),
    "blender": (4, 2, 0),
    "location": "视图3D > 属性面板 > PMX材质复制",
    "description": "基于选择顺序复制和粘贴PMX模型的材质，忽略对象名称，并支持顶点组和UV映射的复制",
    "category": "Object",
}

import bpy

# 全局变量，用于存储复制的材质和相关数据
copied_data = []

class PMXMaterialCopyPanel(bpy.types.Panel):
    bl_label = "PMX材质复制"
    bl_idname = "VIEW3D_PT_pmx_material_copy"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'MMD'

    def draw(self, context):
        layout = self.layout
        layout.label(text="by FK")
        row = layout.row()
        row.operator("object.copy_pmx_materials", text="复制材质")
        row = layout.row()
        row.operator("object.paste_pmx_materials", text="粘贴材质")
        row = layout.row()
        row.operator("object.clear_copied_pmx_materials", text="清空复制材质")

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
                materials = [mat.copy() if mat else None for mat in obj.data.materials]
                material_indices = [poly.material_index for poly in obj.data.polygons]
                vertex_groups = {vg.name: [v.index for v in obj.data.vertices if vg.index in [g.group for g in v.groups]] for vg in obj.vertex_groups}
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

            for vg_name, v_indices in source_data['vertex_groups'].items():
                if vg_name not in target_obj.vertex_groups:
                    vg = target_obj.vertex_groups.new(name=vg_name)
                else:
                    vg = target_obj.vertex_groups[vg_name]
                vg.add(v_indices, 1.0, 'REPLACE')

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

classes = (
    PMXMaterialCopyPanel,
    CopyPMXMaterialsOperator,
    PastePMXMaterialsOperator,
    ClearCopiedPMXMaterialsOperator,
)

def register(): 
    bpy.utils.register_class(PMXMaterialCopyPanel) 
    bpy.utils.register_class(CopyPMXMaterialsOperator) 
    bpy.utils.register_class(PastePMXMaterialsOperator) 
    bpy.utils.register_class(ClearCopiedPMXMaterialsOperator) # 注册新添加的操作类 
def unregister(): 
    bpy.utils.unregister_class(PMXMaterialCopyPanel) 
    bpy.utils.unregister_class(CopyPMXMaterialsOperator) 
    bpy.utils.unregister_class(PastePMXMaterialsOperator) 
    bpy.utils.unregister_class(ClearCopiedPMXMaterialsOperator) # 注销新添加的操作类 
    
if __name__ == "__main__": register()


