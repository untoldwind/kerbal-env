from lib.recipes import find_dependencies

def dependency_tree(config):
    sorted_names = sorted(config.keys())

    for name in sorted_names:
        dump_dependencies("", name)

def dump_dependencies(indent, name):
    dependencies = sorted(find_dependencies(name))
    print(indent + name)
    for dependency in dependencies:
        dump_dependencies(indent + "  ", dependency)
