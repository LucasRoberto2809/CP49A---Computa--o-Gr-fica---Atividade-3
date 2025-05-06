import winged_edge

# abre obj e o divide em classes
parser = winged_edge.Objeto("cube.obj")
parser.abrir()

builder = winged_edge.ConstrutorObj(parser)
builder.constroi()

