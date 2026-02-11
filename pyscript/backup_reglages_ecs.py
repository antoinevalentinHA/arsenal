@service
def ecs_sauvegarde_reglages():
    """
    Sauvegarde compacte (≤255 caractères) des réglages ECS.
    """
    import json
    from datetime import datetime, timezone

    log.info("ECS - Début sauvegarde réglages ECS")

    mapping = {
        "input_number.ecs_off_tiny": "tiny",
        "input_number.ecs_off_medium": "med",
        "input_number.ecs_off_normal": "nor",
        "input_number.ecs_off_desinfection": "des",
        "input_number.ecs_eps_ponctuel": "eps",
        "input_number.ecs_eps_desinfection": "epsd",
        "input_number.ecs_trigger_ceiling_tiny_medium": "ceil",
    }

    data = {}

    for ent, key in mapping.items():
        if ent in state.names():
            try:
                data[key] = float(state.get(ent))
            except:
                log.error(f"ECS - Valeur non numérique pour {ent}")
        else:
            log.warning(f"ECS - Entité introuvable : {ent}")

    payload = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "v": data,
    }

    try:
        json_payload = json.dumps(payload, separators=(",", ":"))
        state.set("input_text.ecs_reglages_backup", json_payload)
        log.info("ECS - Sauvegarde OK")
    except Exception as e:
        log.error(f"ECS - Erreur lors de la sauvegarde : {e}")
