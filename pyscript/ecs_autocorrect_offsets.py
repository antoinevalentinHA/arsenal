@service
def ecs_autocorrect_offsets():
    """
    Auto-ajustement des offsets ECS en fonction du dernier cycle valide.
    Ne modifie que les helpers input_number.ecs_off_*.
    Conditions d'activation :
      - input_boolean.ecs_autocorrect_active == on
      - Dernier cycle valide (flag 'oui')
      - Aucun boost
      - T0 < consigne
      - 0 < durée < 120 min
      - Erreur thermique hors zone morte [-0.3 ; +0.5]
    """

    import math

    log.info("ECS - Auto-ajustement des offsets : démarrage")

    # ------------------------------------------------------------------
    # 0) Vérifier si l'auto-ajustement est activé
    # ------------------------------------------------------------------
    if state.get("input_boolean.ecs_autocorrect_active") != "on":
        log.info("ECS - Auto-ajustement désactivé (input_boolean.ecs_autocorrect_active off)")
        return

    # ------------------------------------------------------------------
    # 1) Récupération du résumé figé du dernier cycle
    #    Format : date|mode|consigne|t0|boost|valide
    # ------------------------------------------------------------------
    resume = state.get("input_text.ecs_resume_dernier_cycle_fige") or ""
    if not resume or resume in ["unknown", "unavailable", "none"]:
        log.warning("ECS - Aucun résumé figé disponible, arrêt de l'auto-ajustement")
        return

    parts = resume.split("|")
    if len(parts) < 6:
        log.warning(f"ECS - Résumé figé incomplet ({resume}), arrêt de l'auto-ajustement")
        return

    date_str = parts[0].strip()
    mode_str = parts[1].strip().lower()
    consigne_str = parts[2].strip()
    t0_str = parts[3].strip()
    boost_flag = parts[4].strip().lower()
    valide_flag = parts[5].strip().lower()

    # ------------------------------------------------------------------
    # 2) Filtrage des cycles non pertinents
    # ------------------------------------------------------------------
    if valide_flag != "oui":
        log.info(f"ECS - Cycle non valide (flag={valide_flag}), aucune correction")
        return

    if boost_flag == "oui":
        log.info("ECS - Boost utilisé sur ce cycle, aucune correction appliquée")
        return

    # Conversion consigne / T0
    try:
        consigne = float(consigne_str)
        t0 = float(t0_str)
    except Exception as e:
        log.error(f"ECS - Impossible de convertir consigne/T0 en float ({consigne_str}/{t0_str}) : {e}")
        return

    if t0 >= consigne:
        log.info(f"ECS - T0 ({t0}) >= consigne ({consigne}), cycle non pertinent pour ajustement")
        return

    # Durée figée
    try:
        duree = float(state.get("input_number.ecs_duree_dernier_cycle_figee") or 0.0)
    except Exception as e:
        log.error(f"ECS - Erreur de conversion duree_dernier_cycle_figee : {e}")
        return

    if not (0.0 < duree < 120.0):
        log.info(f"ECS - Durée {duree} min hors plage [0;120], aucune correction")
        return

    # T° max figée
    try:
        tmax = float(state.get("input_number.ecs_temperature_max_figee") or 0.0)
    except Exception as e:
        log.error(f"ECS - Erreur de conversion ecs_temperature_max_figee : {e}")
        return

    # ------------------------------------------------------------------
    # 3) Calcul de l'erreur thermique
    # ------------------------------------------------------------------
    erreur = tmax - consigne
    log.info(f"ECS - Cycle {date_str} mode={mode_str}, consigne={consigne}, T0={t0}, Tmax={tmax}, erreur={erreur:+.2f} °C")

    # Zone morte pour éviter les oscillations
    deadband_min = -0.3
    deadband_max = 0.5

    if deadband_min <= erreur <= deadband_max:
        log.info(f"ECS - Erreur {erreur:+.2f} dans la zone morte [{deadband_min}; {deadband_max}], aucune correction")
        return

    # ------------------------------------------------------------------
    # 4) Détermination du bucket (tiny / medium / normal / desinfection)
    # ------------------------------------------------------------------
    delta_init = consigne - t0

    bucket = None
    offset_entity = None

    if mode_str in ["desinfection", "désinfection"]:
        bucket = "desinfection"
        offset_entity = "input_number.ecs_off_desinfection"
    else:
        if delta_init < 2.5:
            bucket = "tiny"
            offset_entity = "input_number.ecs_off_tiny"
        elif delta_init < 7.0:
            bucket = "medium"
            offset_entity = "input_number.ecs_off_medium"
        else:
            bucket = "normal"
            offset_entity = "input_number.ecs_off_normal"

    if not offset_entity:
        log.error("ECS - Impossible de déterminer le bucket / offset à corriger, arrêt")
        return

    if offset_entity not in state.names():
        log.error(f"ECS - Entité offset introuvable : {offset_entity}")
        return

    # ------------------------------------------------------------------
    # 5) Lecture de l'offset courant + attributs min/max/step
    # ------------------------------------------------------------------
    try:
        offset_actuel = float(state.get(offset_entity))
    except Exception as e:
        log.error(f"ECS - Impossible de lire la valeur actuelle de {offset_entity} : {e}")
        return

    attrs = state.getattr(offset_entity) or {}
    try:
        offset_min = float(attrs.get("min", 0.0))
        offset_max = float(attrs.get("max", 10.0))
        step = float(attrs.get("step", 0.1))
    except Exception as e:
        log.error(f"ECS - Erreur lecture attributs min/max/step de {offset_entity} : {e}")
        return

    # ------------------------------------------------------------------
    # 6) Calcul de la nouvelle valeur (correcteur proportionnel discret)
    # ------------------------------------------------------------------
    alpha = 0.25  # facteur d'apprentissage (lent et stable)

    offset_new = offset_actuel + alpha * erreur

    # Clamp dans les bornes physiques de l'input_number
    offset_new = max(offset_min, min(offset_max, offset_new))

    # Quantification selon le step
    if step > 0:
        offset_new = round(offset_new / step) * step

    # On arrondit proprement à 3 décimales pour éviter les 2.999999 etc.
    offset_new = float(f"{offset_new:.3f}")

    if math.isclose(offset_new, offset_actuel, rel_tol=1e-03, abs_tol=1e-03):
        log.info(f"ECS - Correction calculée négligeable pour {offset_entity} (reste à {offset_actuel})")
        return

    # ------------------------------------------------------------------
    # 7) Application de la correction
    # ------------------------------------------------------------------
    try:
        service.call(
            "input_number",
            "set_value",
            entity_id=offset_entity,
            value=offset_new,
        )
        log.info(
            f"ECS - Auto-ajustement bucket={bucket} sur {offset_entity} : "
            f"{offset_actuel:.2f} → {offset_new:.2f} (erreur {erreur:+.2f} °C)"
        )
    except Exception as e:
        log.error(f"ECS - Erreur lors de la mise à jour de {offset_entity} : {e}")
        return

    # --------------------------------------------------------------
    # 8) Écriture du dernier ajustement dans input_text.ecs_dernier_ajustement
    # --------------------------------------------------------------
    from datetime import datetime
    now_str = datetime.now().strftime("%d/%m %H:%M")

    ligne = (
        f"{now_str} • {bucket} • "
        f"{offset_actuel:.1f}→{offset_new:.1f} • "
        f"err {erreur:+.1f}°C"
    )

    try:
        service.call(
            "input_text",
            "set_value",
            entity_id="input_text.ecs_dernier_ajustement",
            value=ligne,
        )
        log.info(f"ECS - Dernier ajustement enregistré : {ligne}")
    except Exception as e:
        log.error(f"ECS - Impossible d'écrire dans ecs_dernier_ajustement : {e}")

    log.info("ECS - Auto-ajustement des offsets terminé avec succès")
