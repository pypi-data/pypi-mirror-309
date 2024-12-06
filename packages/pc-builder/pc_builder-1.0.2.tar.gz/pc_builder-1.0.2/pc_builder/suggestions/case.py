def suggestCompatibleCases(userBuild, caseComp):
    from pc_builder.components.case import loadCasesfromJSON

    suggested_cases = []
    all_cases = loadCasesfromJSON()

    for case in all_cases:
        is_compatible, compatibility = case.checkCompatibility(userBuild)

        if len(suggested_cases) == 6:
            break
        if is_compatible:
            suggested_cases.append(case)

    return suggested_cases[:5]
