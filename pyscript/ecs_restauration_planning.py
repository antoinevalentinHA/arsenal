@service
def ecs_restore_planning():
    import json

    log.info("ECS - Restauration matin + soir (Variante B)")

    # 1. Lire les sauvegardes MATIN & SOIR
    raw_matin = state.get("input_text.ecs_planning_sauvegarde_matin")
    raw_soir = state.get("input_text.ecs_planning_sauvegarde_soir")

    if raw_matin is None:
        raw_matin = ""
    if raw_soir is None:
        raw_soir = ""

    try:
        matin = json.loads(raw_matin) if raw_matin else {}
        soir = json.loads(raw_soir) if raw_soir else {}
    except Exception as e:
        log.error(f"Erreur JSON lors de la lecture : {e}")
        return

    log.info(f"Matin restaurés : {matin}")
    log.info(f"Soir restaurés : {soir}")

    # 2. Désactiver tous les MATINS
    for e in state.names(domain="input_boolean"):
        if e.startswith("input_boolean.ecs_") and e.endswith("_matin_active"):
            service.call("input_boolean", "turn_off", entity_id=e)

    # 3. Activer matins sauvegardés + restaurer heure
    for jour, h in matin.items():
        ent_bool = f"input_boolean.ecs_{jour}_matin_active"
        ent_time = f"input_datetime.ecs_{jour}_matin_heure"

        if ent_bool in state.names():
            service.call("input_boolean", "turn_on", entity_id=ent_bool)

        if ent_time in state.names():
            service.call("input_datetime", "set_datetime",
                         entity_id=ent_time, time=h)

    # 4. Désactiver tous les SOIRS
    for e in state.names(domain="input_boolean"):
        if e.startswith("input_boolean.ecs_") and e.endswith("_soir_active"):
            service.call("input_boolean", "turn_off", entity_id=e)

    # 5. Activer soirs sauvegardés + restaurer heure
    for jour, h in soir.items():
        ent_bool = f"input_boolean.ecs_{jour}_soir_active"
        ent_time = f"input_datetime.ecs_{jour}_soir_heure"

        if ent_bool in state.names():
            service.call("input_boolean", "turn_on", entity_id=ent_bool)

        if ent_time in state.names():
            service.call("input_datetime", "set_datetime",
                         entity_id=ent_time, time=h)

    log.info("ECS - Restauration complète terminée.")
