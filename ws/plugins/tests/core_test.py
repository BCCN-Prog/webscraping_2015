from .. import *

l = list_plugins()
print(l)

o = load_plugin(l[0]).build_url('test')
print(o)
