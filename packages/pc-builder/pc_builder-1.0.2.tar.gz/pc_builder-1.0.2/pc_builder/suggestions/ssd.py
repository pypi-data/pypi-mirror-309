def suggestCompatibleSSDs(userBuild, ssdComp):
    from pc_builder.components.ssd import loadSSDsfromJSON

    suggested_ssds = []
    all_ssds = loadSSDsfromJSON()

    for ssd in all_ssds:
        is_compatible, compatibility = ssd.checkCompatibility(userBuild)

        if len(suggested_ssds) == 6:
            break
        if is_compatible:
            suggested_ssds.append(ssd)

    return suggested_ssds[:5]
