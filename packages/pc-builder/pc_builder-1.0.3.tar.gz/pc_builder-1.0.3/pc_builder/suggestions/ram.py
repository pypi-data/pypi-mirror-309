def suggestCompatibleRAMs(userBuild, ramComp):
    from pc_builder.components.ram import loadRAMsfromJSON

    suggested_rams = []
    all_rams = loadRAMsfromJSON()

    for ram in all_rams:
        is_compatible, compatibility = ram.checkCompatibility(userBuild)

        if len(suggested_rams) == 6:
            break
        if is_compatible:
            suggested_rams.append(ram)

    return suggested_rams[:5]
