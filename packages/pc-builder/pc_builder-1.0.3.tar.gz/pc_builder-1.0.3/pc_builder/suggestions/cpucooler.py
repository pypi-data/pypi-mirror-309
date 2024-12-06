def suggestCompatibleCPUcoolers(userBuild, cpucoolerComp):
    from pc_builder.components.cpucooler import loadCPUCoolersfromJSON
    suggested_coolers = []
    all_coolers = loadCPUCoolersfromJSON()

    for cooler in all_coolers:
        is_compatible, compatibility = cooler.checkCompatibility(userBuild)

        if len(suggested_coolers) == 6:
            break
        if is_compatible:
            suggested_coolers.append(cooler)
            
    return suggested_coolers[:5]