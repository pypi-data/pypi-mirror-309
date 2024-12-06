def suggestCompatibleGPUs(userBuild, gpuComp):
    from pc_builder.components.gpu import loadGPUsfromJSON

    suggested_gpus = []
    all_gpus = loadGPUsfromJSON()

    for gpu in all_gpus:
        is_compatible, compatibility = gpu.checkCompatibility(userBuild)

        if len(suggested_gpus) == 6:
            break
        if is_compatible:
            suggested_gpus.append(gpu)

    return suggested_gpus[:5]
