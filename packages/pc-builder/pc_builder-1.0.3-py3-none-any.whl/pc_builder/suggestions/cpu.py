def suggestCompatibleCPUs(userBuild, cpuComp):
    from pc_builder.components.cpu import loadCPUsfromJSON

    suggested_cpus = []
    all_cpus = loadCPUsfromJSON()

    for cpu in all_cpus:
        is_compatible, compatibility = cpu.checkCompatibility(userBuild)

        if len(suggested_cpus) == 6:
            break
        if is_compatible:
            suggested_cpus.append(cpu)

    return suggested_cpus[:5]
