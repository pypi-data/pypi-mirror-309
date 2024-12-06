def suggestCompatiblePSUs(userBuild, psuComp):
    from pc_builder.components.psu import loadPSUsfromJSON

    suggested_psus = []
    all_psus = loadPSUsfromJSON()

    for psu in all_psus:
        is_compatible, compatibility = psu.checkCompatibility(userBuild)

        if len(suggested_psus) == 6:
            break
        if is_compatible:
            suggested_psus.append(psu)

    return suggested_psus[:5]
