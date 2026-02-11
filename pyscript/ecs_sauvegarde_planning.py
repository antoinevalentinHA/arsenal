@service
def ecs_sauvegarde_planning():
    import json

    log.info("ECS - Sauvegarde matin + soir")

    # ----------- MATIN -----------
    matin = {}
    for e in state.names(domain="input_boolean"):
        if e.startswith("input_boolean.ecs_") and e.endswith("_matin_active"):
            if state.get(e) == "on":
                jour = e.replace("input_boolean.ecs_", "").replace("_matin_active", "")
                dt = f"input_datetime.ecs_{jour}_matin_heure"
                if dt in state.names():
                    matin[jour] = state.get(dt)

    # Écriture JSON dans input_text
    state.set("input_text.ecs_planning_sauvegarde_matin", json.dumps(matin))

    # ----------- SOIR -----------
    soir = {}
    for e in state.names(domain="input_boolean"):
        if e.startswith("input_boolean.ecs_") and e.endswith("_soir_active"):
            if state.get(e) == "on":
                jour = e.replace("input_boolean.ecs_", "").replace("_soir_active", "")
                dt = f"input_datetime.ecs_{jour}_soir_heure"
                if dt in state.names():
                    soir[jour] = state.get(dt)

    # Écriture JSON dans input_text
    state.set("input_text.ecs_planning_sauvegarde_soir", json.dumps(soir))

    log.info("ECS - Sauvegarde terminée")
