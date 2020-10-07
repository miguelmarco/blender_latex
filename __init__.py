import os
import tempfile
import bpy
from mathutils import Vector


bl_info = {
	'name': 'LaTeX in Blender',
	'description': "Create curves from latex expressions ",
	'author': 'Miguel Marco',
	'version': (0, 0, 0, 1),
	'blender': (2, 83, 2),
	'location': 'View3D > Add > Curve > LaTeX expression',
	'warning': 'Depends on having latex and cairotopdf installes',
	'support': 'COMMUNITY',
	'category': 'AddCurve'}



TEMPLATE = r"""\documentclass{standalone}
\begin{document}
$\displaystyle{ {{TEXT}} }$
\end{document}"""

class AddLatexCurve(bpy.types.Operator):
    """Add a new curve from the latex command"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.add_latex"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Add LaTeX Curve"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    latex_string: bpy.props.StringProperty(name="String Value")

    def execute(self, context):        # execute() is called when running the operator.

        S = self.latex_string
        print(TEMPLATE.replace('{{TEXT}}', S))
        with tempfile.TemporaryDirectory() as td:
            with open('{}/file.tex'.format(td),'w') as fd:
                fd.write(TEMPLATE.replace('{{TEXT}}', S))
            print("tex file created")
            os.system('cd {} && pdflatex file.tex'.format(td))
            print("pdf file created")
            os.system('cd {} && pdftocairo -svg file.pdf file.svg '.format(td))
            print("svg file created")
            old_collections = bpy.data.collections.items()
            bpy.ops.import_curve.svg(filepath='{}/file.svg'.format(td))
            for Collection in bpy.data.collections.items():
                if not Collection in old_collections:
                    for Object in Collection[1].objects:
                        Object.scale=Vector((500,500,500))

        return {'FINISHED'}


def menu_func(self, context):
    layout = self.layout
    layout.operator_context = 'INVOKE_REGION_WIN'
    layout.separator()
    oper = layout.operator("object.add_latex", text='LaTeX expression')
    oper.change = False



def register():
    bpy.utils.register_class(AddLatexCurve)
    bpy.types.VIEW3D_MT_curve_add.append(menu_func)


def unregister():
    bpy.types.VIEW3D_MT_curve_add.remove(menu_func)
    bpy.utils.unregister_class(AddLatexCurve)

if __name__ == "__main__":
    register()

