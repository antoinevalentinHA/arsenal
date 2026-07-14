"""Lot 5.1 — Oracle structurel de la politique d'absence COOL (contrat 15, C20).

Famille 5_x : analyseur structurel borné (behavior/cool_veto_gate.py). Il vérifie
que la matière YAML **encode** les invariants opposables du contrat 15. Les tests
utilisent des **fixtures inline pré/post correction** (mutation-style) : la forme
CIBLE (post) est conforme (0 violation) ; une forme MUTÉE (pré / dérive) est
détectée (>= 1 violation). Aucun runtime réel n'est lu ici — le branchement
contre les VRAIS fichiers est ajouté au Lot 3, une fois le runtime conforme.

Frontière assumée : cet oracle ne simule pas Jinja ; il prouve la structure, pas
le rendu. Le comportement runtime complet est validé au Lot 5 (terrain).
"""
from arsenal_ci.behavior.cool_veto_gate import (
    check_autorisation_consumes_composite,
    check_composite_formula,
    check_extinction_horodatage,
    check_helper_no_initial,
    check_horodatage_single_writer,
    check_no_fixed_duration,
    check_no_preparation,
    load_docs,
)

# --------------------------------------------------------------- fixtures CIBLE

COOL_POST = """
- binary_sensor:
    - name: "Autorisation refroidissement climatisation"
      unique_id: autorisation_clim_cool
      state: >
        {{
          states('sensor.temperature_jardin') | float(0)
            >= states('input_number.clim_seuil_temperature_exterieure_minimum') | float(99)
          and is_state('binary_sensor.clim_blocage_aeration_etage_reel', 'off')
          and is_state('binary_sensor.fenetre_ouverte_maison_avec_delai', 'off')
          and is_state('binary_sensor.clim_blocage_horaire_reel', 'off')
          and is_state('binary_sensor.clim_veto_absence_vacances', 'off')
        }}
"""

VETO_POST = """
- binary_sensor:
    - name: "Clim - Veto absence / Vacances (composite)"
      unique_id: clim_veto_absence_vacances
      state: >
        {{
          is_state('binary_sensor.clim_extinction_absence_prolongee_autorisee', 'on')
          or is_state('binary_sensor.vacances_actives', 'on')
        }}
"""

ABSENCE_POST = """
- binary_sensor:
    - name: "Clim - Extinction autorisee (absence prolongee)"
      unique_id: clim_extinction_absence_prolongee_autorisee
      state: >
        {% set debut = states('input_datetime.clim_debut_absence') %}
        {% set duree = states('input_number.clim_duree_absence_longue') | float(14) %}
        {{
          is_state('binary_sensor.presence_confort_thermique_stabilisee', 'off')
          and debut not in ['unknown','unavailable','']
          and as_timestamp(now()) >= as_timestamp(debut) + duree * 3600
        }}
"""

HELPER_POST = """
clim_duree_absence_longue:
  name: "Duree absence longue"
  min: 8
  max: 48
  step: 1
  unit_of_measurement: "heures"
  mode: box
"""

AUTO_POST = load_docs("""
- id: "10030000000122"
  alias: "Climatisation - Absence - Horodatage et reconciliation"
  action:
    - service: input_datetime.set_datetime
      target:
        entity_id: input_datetime.clim_debut_absence
      data:
        timestamp: "{{ as_timestamp(now()) | int(0) }}"
""")


# ------------------------------------------------------ conformité de la CIBLE

def test_post_autorisation_consumes_composite_ok():
    assert check_autorisation_consumes_composite(COOL_POST) == []


def test_post_composite_formula_ok():
    assert check_composite_formula(VETO_POST) == []


def test_post_extinction_horodatage_ok():
    assert check_extinction_horodatage(ABSENCE_POST) == []


def test_post_helper_no_initial_ok():
    assert check_helper_no_initial(HELPER_POST) == []


def test_post_no_fixed_duration_ok():
    assert check_no_fixed_duration(ABSENCE_POST, VETO_POST, COOL_POST) == []


def test_post_horodatage_single_writer_ok():
    assert check_horodatage_single_writer(AUTO_POST) == []


def test_post_no_preparation_ok():
    assert check_no_preparation(COOL_POST, VETO_POST, ABSENCE_POST) == []


# ----------------------------------------------- détection des dérives (mutants)

def test_pre_autorisation_reads_extinction_direct_flagged():
    """Dérive : l'autorisation lit l'extinction en direct (état actuel pré-C20)."""
    cool_pre = COOL_POST.replace(
        "is_state('binary_sensor.clim_veto_absence_vacances', 'off')",
        "is_state('binary_sensor.clim_extinction_absence_prolongee_autorisee', 'off')",
    )
    violations = check_autorisation_consumes_composite(cool_pre)
    # extinction lue en direct => duplication, ET composite non consommé.
    assert any("duplication" in v for v in violations)
    assert any("ne consomme pas" in v for v in violations)


def test_mutant_autorisation_duplicates_vacances_flagged():
    cool_mut = COOL_POST.replace(
        "is_state('binary_sensor.clim_veto_absence_vacances', 'off')",
        "is_state('binary_sensor.clim_veto_absence_vacances', 'off')\n"
        "          and is_state('binary_sensor.vacances_actives', 'off')",
    )
    assert any("vacances_actives" in v for v in check_autorisation_consumes_composite(cool_mut))


def test_mutant_composite_without_vacances_flagged():
    veto_mut = VETO_POST.replace(
        "\n          or is_state('binary_sensor.vacances_actives', 'on')", ""
    )
    violations = check_composite_formula(veto_mut)
    assert any("vacances_actives" in v for v in violations)


def test_mutant_extinction_uses_timer_flagged():
    absence_mut = """
- binary_sensor:
    - name: "Clim - Extinction autorisee (absence prolongee)"
      unique_id: clim_extinction_absence_prolongee_autorisee
      state: >
        {{
          is_state('binary_sensor.presence_confort_thermique_stabilisee', 'off')
          and is_state('timer.absence_longue_clim', 'idle')
        }}
"""
    violations = check_extinction_horodatage(absence_mut)
    assert any("timer" in v for v in violations)
    assert any("clim_debut_absence" in v for v in violations)


def test_mutant_helper_with_initial_flagged():
    helper_mut = HELPER_POST.replace("  mode: box\n", "  mode: box\n  initial: 14\n")
    assert any("initial" in v for v in check_helper_no_initial(helper_mut))


def test_mutant_fixed_8h_duration_flagged():
    absence_mut = ABSENCE_POST + '\n# duration: "08:00:00"\n'
    assert check_no_fixed_duration(absence_mut) != []


def test_mutant_horodatage_wrong_writer_id_flagged():
    autos = load_docs("""
- id: "99999999999999"
  alias: "faux ecrivain"
  action:
    - service: input_datetime.set_datetime
      target:
        entity_id: input_datetime.clim_debut_absence
""")
    assert any("inattendu" in v for v in check_horodatage_single_writer(autos))


def test_mutant_two_writers_flagged():
    autos = load_docs("""
- id: "10030000000122"
  action:
    - service: input_datetime.set_datetime
      target:
        entity_id: input_datetime.clim_debut_absence
- id: "10030000000199"
  action:
    - service: input_datetime.set_datetime
      target:
        entity_id: input_datetime.clim_debut_absence
""")
    assert any("multiples" in v for v in check_horodatage_single_writer(autos))


def test_mutant_preparation_present_flagged():
    assert check_no_preparation("is_state('input_boolean.preparation_cool_active','on')") != []
