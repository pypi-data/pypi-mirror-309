def suggestCompatibleHDDs(userBuild, hddComp):
    from pc_builder.components.hdd import loadHDDsfromJSON

    suggested_hdds = []
    all_hdds = loadHDDsfromJSON()

    for hdd in all_hdds:
        is_compatible, compatibility = hdd.checkCompatibility(userBuild)

        if len(suggested_hdds) == 6:
            break
        if is_compatible:
            suggested_hdds.append(hdd)

    return suggested_hdds[:5]
