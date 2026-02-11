@service
def generate_next_id_from_prefix():
    """
    Lit input_text.prefix_id,
    calcule le prochain ID correspondant,
    écrit dans input_text.next_id_result.
    """

    # ----- Récupération et validation du préfixe -----
    prefix = state.get("input_text.prefix_id")

    if not prefix:
        log.error("Préfixe vide dans input_text.prefix_id")
        return

    prefix = prefix.strip()

    if not prefix.isdigit():
        log.error(f"Préfixe invalide : '{prefix}' (doit être numérique)")
        return

    # ----- Récupération de toutes les automatisations -----
    auto_ids = []
    for entity in state.names():
        if entity.startswith("automation."):
            attrs = state.getattr(entity) or {}
            aid = str(attrs.get("id", ""))
            if aid.startswith(prefix):
                try:
                    numeric_part = int(aid[len(prefix):])
                    auto_ids.append(numeric_part)
                except ValueError:
                    continue

    # ----- Calcul du prochain ID -----
    next_suffix = max(auto_ids) + 1 if auto_ids else 1
    next_id = f"{prefix}{next_suffix:010d}"

    # ----- Écriture dans l'input_text de résultat -----
    service.call(
        "input_text",
        "set_value",
        entity_id="input_text.next_id_result",
        value=next_id
    )

    # ----- Log dans le logbook via événement (aucun conflit avec 'name') -----
    event.fire(
        "logbook_entry",
        name="Arsenal - Gestion ID",
        message=f"ID généré : {next_id} (préfixe {prefix})",
        domain="automation",
        entity_id="input_text.next_id_result"
    )

    # ----- Log console -----
    log.info(f"NEXT ID : {next_id} pour prefix {prefix}")
