def suggestCompatibleMotherboards(userBuild, motherboardComp):
    from pc_builder.components.motherboard import loadMBsfromJSON
    
    suggested_motherboards = []
    all_motherboards = loadMBsfromJSON()

    for motherboard in all_motherboards:
        is_compatible, compatibility = motherboard.checkCompatibility(userBuild)

        if len(suggested_motherboards) == 6:
            break

        if is_compatible:
            suggested_motherboards.append(motherboard)
    
    return suggested_motherboards[:5]
