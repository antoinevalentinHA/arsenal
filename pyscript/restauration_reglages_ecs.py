@service
def ecs_restore_reglages():
    """
    Restauration compacte des réglages ECS.
    """
    import json
    from datetime import datetime, timezone

    raw = state.get("input_text.ecs_reglages_backup") or ""

    if not raw:
        log.warning("ECS - Backup vide, restauration annulée")
        return

    try:
        data = json.loads(raw)
        values = data.get("v", {})
    except Exception as e:
        log.error(f"ECS - Erreur JSON backup : {e}")
        return

    log.info("ECS - Début restauration réglages")

    mapping = {
        "tiny": "input_number.ecs_off_tiny",
        "med": "input_number.ecs_off_medium",
        "nor": "input_number.ecs_off_normal",
        "des": "input_number.ecs_off_desinfection",
        "eps": "input_number.ecs_eps_ponctuel",
        "epsd": "input_number.ecs_eps_desinfection",
        "ceil": "input_number.ecs_trigger_ceiling_tiny_medium",
    }

    for key, ent in mapping.items():
        if key in values and ent in state.names():
            try:
                new = float(values[key])
                old = float(state.get(ent))
                if new != old:
                    service.call("input_number", "set_value", entity_id=ent, value=new)
                    log.info(f"{ent}: {old} → {new}")
            except Exception as e:
                log.error(f"ECS - Erreur restauration {ent}: {e}")

    # trace de restauration
    try:
        restore_info = {
            "restored_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "source": data.get("ts", "inconnu"),
        }
        state.set("input_text.ecs_reglages_last_restore",
                  json.dumps(restore_info, separators=(",", ":")))
    except Exception as e:
        log.error(f"ECS - Erreur écriture restore log : {e}")

    log.info("ECS - Restauration OK")
