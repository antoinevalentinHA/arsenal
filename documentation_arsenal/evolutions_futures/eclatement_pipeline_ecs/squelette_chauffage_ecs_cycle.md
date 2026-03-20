# ==========================================================
# 🧠 ARSENAL — SCRIPT : ECS – Cycle thermique unifié
# ----------------------------------------------------------
# 📌 STATUT DE CE FICHIER
#   Squelette cible — état final post phase 5.
#   Non exécutable tel quel avant la fin de la migration.
#   Durant les phases 1 à 4, la branche boost (étape 7)
#   reste inline dans le monolithe en cours de refactor.
#
# ----------------------------------------------------------
# 🎯 ROLE
#   Orchestrateur du cycle ECS refactorisé.
#
# ----------------------------------------------------------
# 🧱 PERIMETRE
#
#   - ouverture de session via script dédié
#   - calcul thermique inline
#   - validation inline
#   - application consigne haute/basse via exécuteur confirmé
#   - attente thermique inline
#   - boost via sous-script dédié (phase 5)
#   - vérification retour bas inline
#   - armement gardien via script dédié
#   - fermeture de session via script dédié
#
# ----------------------------------------------------------
# 🔗 DEPENDANCES
#
#   Scripts extraits :
#   - script.ecs_cycle_session_open
#   - script.ecs_appliquer_consigne_confirmee
#   - script.ecs_cycle_boost_si_necessaire      [phase 5]
#   - script.ecs_armer_gardien_post_prelevement
#   - script.ecs_cycle_session_close
#
#   Helpers :
#   - input_text.ecs_cycle_last_action_status
#   - input_text.ecs_target_temp_session
#   - sensor.ecs_temperature_ballon_securisee
#   - sensor.boiler_dhw_setpoint
# ==========================================================

chauffage_ecs_cycle:
  alias: "Chauffage ECS - Cycle unifié"
  mode: single
  max_exceeded: silent

  fields:
    mode:
      name: Mode
      description: "Type de cycle : 'ponctuel', 'vaisselle' ou 'desinfection'"
      required: true

  sequence:

    # ======================================================
    # 🟢 ETAPE 1 : Ouverture session ECS
    # ======================================================
    - action: script.ecs_cycle_session_open

    # ======================================================
    # 📊 ETAPE 2 : Calcul métier de session
    # ======================================================
    - variables:
        sensor_temp: sensor.ecs_temperature_ballon_securisee
        retour_temp: 10

        # --- Lectures source ---
        start_temp: "..."
        target_temp: "..."       # objectif thermique de session — utilisé pour wait_template et epsilon
        delta_t: "..."

        # --- Offsets ---
        off_tiny: "..."
        off_medium: "..."
        off_normal: "..."
        off_desinf: "..."
        eps_ponctuel: "..."
        eps_desinf: "..."
        trig_ceiling_tm: "..."

        # --- Cible effective ---
        raw_effective_target: "..."
        min_target: "{{ (start_temp | float) + (trig_ceiling_tm | float) }}"
        effective_target: "..."
        effective_target_int: "..."   # consigne chaudière appliquée — base du calcul boost
        epsilon: "..."

    # ======================================================
    # 🚫 ETAPE 3 : Validation inline
    # Deux branches séparées pour conserver les messages
    # de diagnostic distincts du monolithe.
    # ======================================================
    - choose:
        - conditions:
            - condition: template
              value_template: "{{ mode not in ['ponctuel', 'vaisselle', 'desinfection'] }}"
          sequence:
            - action: script.ecs_cycle_session_close
            - stop: "Mode ECS invalide (mode={{ mode }})"

        - conditions:
            - condition: template
              value_template: >
                {{
                  not is_number(target_temp)
                  or not is_number(start_temp)
                  or (target_temp | float) <= 0
                  or (start_temp | float) < 0
                  or not is_number(effective_target_int)
                  or (effective_target_int | float) < 15
                }}
          sequence:
            - action: script.ecs_cycle_session_close
            - stop: >
                Consigne ECS cible invalide
                (mode={{ mode }}, target={{ target_temp }}, start={{ start_temp }}, effective={{ effective_target_int }})

    # ======================================================
    # 💾 ETAPE 4 : Mémorisation cible de session
    # ======================================================
    - action: input_text.set_value
      target:
        entity_id: input_text.ecs_target_temp_session
      data:
        value: "{{ effective_target_int }}"

    # ======================================================
    # 📤 ETAPE 5 : Application consigne haute confirmée
    # ======================================================
    - action: script.ecs_appliquer_consigne_confirmee
      data:
        target_temp: "{{ effective_target_int }}"
        contexte: "consigne_haute"

    - choose:
        - conditions:
            - condition: template
              value_template: >
                {{ states('input_text.ecs_cycle_last_action_status') != 'applied' }}
          sequence:
            - action: script.ecs_cycle_session_close
            - stop: >
                Echec application consigne ECS haute
                (status={{ states('input_text.ecs_cycle_last_action_status') }},
                target={{ effective_target_int }})

    # ======================================================
    # ♻️ ETAPE 6 : Attente d'atteinte thermique réelle
    # ======================================================
    - wait_template: >
        {{ states(sensor_temp) | float(0) >= (target_temp | float) - (epsilon | float) }}
      timeout: >
        {% if mode == 'desinfection' %}
          00:40:00
        {% else %}
          00:20:00
        {% endif %}
      continue_on_timeout: true

    # ======================================================
    # 🚑 ETAPE 7 : Boost si nécessaire
    # L'orchestrateur établit l'éligibilité.
    # Le script boost ne rejuge pas son propre appel.
    # NOTE : cet appel n'est actif qu'après extraction du
    # script boost en phase 5. Avant cela, la branche boost
    # reste inline dans le monolithe en cours de refactor.
    # ======================================================
    - choose:
        - conditions:
            - condition: template
              value_template: >
                {{ states(sensor_temp) | float(0) < (target_temp | float) - (epsilon | float) }}
          sequence:
            - action: script.ecs_cycle_boost_si_necessaire
              data:
                mode: "{{ mode }}"
                sensor_temp: "{{ sensor_temp }}"
                target_temp: "{{ target_temp }}"
                epsilon: "{{ epsilon }}"
                effective_target_int: "{{ effective_target_int }}"

    # ======================================================
    # 🔽 ETAPE 8 : Application consigne basse confirmée
    # ======================================================
    - action: script.ecs_appliquer_consigne_confirmee
      data:
        target_temp: "{{ retour_temp }}"
        contexte: "retour_basse"

    - choose:
        - conditions:
            - condition: template
              value_template: >
                {{ states('input_text.ecs_cycle_last_action_status') != 'applied' }}
          sequence:
            - action: script.ecs_cycle_session_close
            - stop: >
                Echec application consigne ECS basse
                (status={{ states('input_text.ecs_cycle_last_action_status') }})

    # ======================================================
    # ✅ ETAPE 8B : Vérification retour bas observé
    # NOTE : session_close ajouté avant stop — delta vs
    # monolithe actuel (à valider explicitement via X3).
    # ======================================================
    - wait_template: >
        {{
          is_number(states('sensor.boiler_dhw_setpoint'))
          and (states('sensor.boiler_dhw_setpoint') | float) == (retour_temp | float)
        }}
      timeout: "00:01:30"
      continue_on_timeout: true

    - choose:
        - conditions:
            - condition: template
              value_template: >
                {{
                  not is_number(states('sensor.boiler_dhw_setpoint'))
                  or (states('sensor.boiler_dhw_setpoint') | float) != (retour_temp | float)
                }}
          sequence:
            - action: logbook.log
              data:
                name: "ECS"
                message: >
                  Retour consigne ECS basse non observé
                  (attendu={{ retour_temp }}, lu={{ states('sensor.boiler_dhw_setpoint') }})
            - action: script.ecs_cycle_session_close
            - stop: "Retour consigne ECS basse non observé"

    # ======================================================
    # ⏱️ ETAPE 9 : Armement gardien post-prélèvement
    # ======================================================
    - action: script.ecs_armer_gardien_post_prelevement
      data:
        mode: "{{ mode }}"

    # ======================================================
    # 🧹 ETAPE 10 : Fermeture session ECS
    # ======================================================
    - action: script.ecs_cycle_session_close
