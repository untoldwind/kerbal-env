from lib.receips import find_dependencies

def sort_dependencies(mod_configs):
    order = []

    for name, config in mod_configs.items():
        if not config.enabled:
            continue

        dependends = collect_dependends(mod_configs, set(), name)
        if not all(mod_configs[dependend].enabled for dependend in dependends):
            continue

        for dependend in dependends:
            if not [existing for existing in order if existing[0] == dependend]:
                order.append((dependend, mod_configs[dependend]))
        if not [existing for existing in order if existing[0] == name]:
            order.append((name, config))
    
    return order

def collect_dependends(mod_configs, stack, name):
    if not name in mod_configs:
        raise NameError("Dependency not found: %s" % name)
    stack.add(name)
    dependends = []
    for dependency in find_dependencies(name):
        if not dependency in stack:
            dependends.extend(collect_dependends(mod_configs, stack, dependency))
            dependends.append(dependency)

    return dependends

