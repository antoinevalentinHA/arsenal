# ARSENAL — SYNTHÈSE DES CORRECTIONS POST-AUDIT
## Domaine : Aération → Blocage Chauffage
### Périmètre : contrats normatifs + code

---

## 🔴 À FAIRE ABSOLUMENT

Corrections critiques — comportements incorrects confirmés dans le code.

---

### 1. M0 Cas C — Levée de blocage légitime possible en suspension

**Fichier :** `script.aeration_m0_recover` — branche Cas C
**Problème :** La condition "blocage ON + timer idle" est vraie en M5 (suspension active, timer annulé). M0 appellerait M4 sur un blocage légitime.
**Correction :** Ajouter la condition :
```yaml
- condition: state
  entity_id: input_boolean.aeration_suspension_active
  state: "off"
```

---

### 2. M4 — `aeration_suspension_active` non remis à off

**Fichier :** `script.aeration_m4_fin_blocage_horaire`
**Problème :** Si M5 a été exécuté et que le cycle se termine sans passer par M6 (ex. via M0 Cas C), `aeration_suspension_active` reste `on` après clôture complète. Résidu invisible au détecteur KO.
**Correction :** Ajouter après le désarmement pipeline :
```yaml
- action: input_boolean.turn_off
  target:
    entity_id: input_boolean.aeration_suspension_active
```

---

### 3. Détecteur KO — Faux positif en M5

**Fichier :** `binary_sensor.chauffage_aeration_coherence_ko` — incohérence A
**Problème :** `ko_blocage_orphelin = blocage and not t_blocage_active` déclenche un KO en M5 (timer annulé, suspension active, datetime valide) — état canon valide.
**Correction :**
```yaml
{% set ko_blocage_orphelin = blocage and not t_blocage_active and not suspension %}
```

---

### 4. M0 Cas A — Timers non annulés

**Fichier :** `script.aeration_m0_recover` — branche Cas A
**Problème :** Le désarmement du pipeline ne s'accompagne pas d'une annulation des timers. Un timer résiduel actif dans un état zombie survit à M0 Cas A.
**Correction :** Ajouter avant le `turn_off` du pipeline :
```yaml
- action: timer.cancel
  target:
    entity_id:
      - timer.aeration_analyse_delta_t
      - timer.aeration_blocage
```

---

### 5. Sécurité démarrage & Mini-guard — Datetimes non neutralisées

**Fichiers :** `automation 10010000000022` et `automation 10010000000024`
**Problème :** Ces deux mécanismes annulent les timers et désarment le pipeline mais laissent `chauffage_fin_blocage_aeration` et `analyse_deltat_disponible` avec des valeurs non neutralisées. L'état résultant n'est pas l'état canon 1.
**Correction :** Ajouter dans les actions des deux automations :
```yaml
- action: input_datetime.set_datetime
  target:
    entity_id: input_datetime.chauffage_fin_blocage_aeration
  data:
    datetime: "{{ now().date().isoformat() ~ ' 00:00:00' }}"

- action: input_datetime.set_datetime
  target:
    entity_id: input_datetime.analyse_deltat_disponible
  data:
    datetime: "{{ now().date().isoformat() ~ ' 00:00:00' }}"
```

---

## 🟠 CORRECTIONS DOCUMENTAIRES OBLIGATOIRES

Contrats à mettre à jour pour refléter le code réel.

---

### 6. Contrat M3 calcul ΔT — Définition inversée

**Contrat :** `M3 — Calcul ΔT maximal`, section MÉTHODE
**Problème :** "température courante − référence snapshot M1" est faux. Le code implémente `max(ref - t, 0)`.
**Correction :**
> Chaque capteur ΔT représente : `max(référence snapshot M1 − température courante, 0)`. Les valeurs négatives sont impossibles par construction.

---

### 7. Contrat M3 calcul ΔT — Propriété robustesse asymétrique

**Contrat :** `M3 — Calcul ΔT maximal`, section ROBUSTESSE
**Problème :** "Une indisponibilité ne peut jamais produire une prolongation" est faux pour `temperature_*`.
**Correction :**
> Une indisponibilité de `ref_temp_*` produit un ΔT nul — pas de prolongation.
> Une indisponibilité de `temperature_*` produit un ΔT égal à T_REF entière — biais conservateur vers la prolongation assumé.

---

### 8. Contrat M3 prolonger — Type de prolongation_heures

**Contrat :** `M3 — Prolonger blocage`, section ENTRÉES
**Problème :** `h = prolongation_heures | int(0)` — le code utilise `float(0)`.
**Correction :**
> `h = prolongation_heures | float(0)` — valeur en heures, fraction possible.

---

### 9. Contrat M4 — Invariant post-M4 incomplet

**Contrat :** `M4 — Désarmement final`, section INVARIANT POST-M4
**Problème :** `aeration_suspension_active` absent des conditions post-M4.
**Correction :** Ajouter à la liste :
> - `aeration_suspension_active = off`

---

### 10. Contrat timers — Comportement M5/M6 mal décrit

**Contrat :** `Timers V3 Pro`, sections 8 et 9
**Problème :** Section 8 décrit "annulé ou redémarré" — M5 annule toujours. Section 9 conditionne M6 à "durée strictement positive" — M6 redémarre toujours.
**Corrections :**
> Section 8 : M5 annule systématiquement les timers sans redémarrage. La reprise est exclusivement réalisée par M6.
>
> Section 9 : M6 redémarre systématiquement les timers. Si l'échéance est expirée, le timer repart sur la durée minimale (`delai_stabilisation_capteurs`). M6 garantit toujours un timer actif à la sortie.

---

### 11. Contrat détecteur KO — Incohérence A à préciser

**Contrat :** `Cohérence — Détecteur KO`, section incohérence A
**Problème :** La définition n'exclut pas le cas M5 valide.
**Correction :**
> Ajouter : `ET aeration_suspension_active = off`
> Note : en M5, timer idle + datetime valide + suspension active est un état canon — pas une incohérence.

---

### 12. Contrat M2 — Interdit mal formulé

**Contrat :** `M2 — Calcul & Programmation monotone`, section INTERDIT
**Problème :** "M2 ne doit pas modifier les échéances une fois le blocage actif" — violé littéralement par la séquence M2 elle-même (blocage posé avant datetimes).
**Correction :**
> M2 ne doit pas être rappelé une fois le blocage actif.

---

### 13. Contrat helpers — Deux helpers UI non documentés

**Contrat :** `Helpers du domaine`, nouvelle section à ajouter
**Problème :** `aeration_reference_thermique_utilisee` et `aeration_delta_t_utilise` absents.
**Correction :** Ajouter section **Helpers de restitution UI** :
> `input_number.aeration_reference_thermique_utilisee`
> — Moyenne des six `ref_temp_*` post-snapshot M1. Écrit par M1. Rôle : UI uniquement.
>
> `input_number.aeration_delta_t_utilise`
> — ΔT maximum monotone sur l'épisode. Écrit par M3 orchestrateur. Rôle : UI uniquement.

---

## 🟡 AMÉLIORATIONS FACULTATIVES

Lacunes non critiques — à traiter selon priorité Arsenal.

---

### 14. Risque timezone — M2 et M3 prolonger

**Fichiers :** `script.aeration_m2_fin_episode`, `script.aeration_m3_prolonger_blocage`
**Problème :** Ces scripts utilisent `now().replace(tzinfo=None)` pour construire des datetimes, puis les comparent à des datetimes issus de `as_datetime` potentiellement timezone-aware. Selon la configuration HA d'Arsenal, cela peut lever une exception silencieuse.
**Amélioration :** Homogénéiser sur le pattern de M6 : `now() | as_datetime` partout.
**Priorité :** À traiter si Arsenal est configuré en timezone non-UTC ou si des anomalies de calcul d'échéances sont observées.

---

### 15. Lacune post-boot — Incohérences préexistantes silencieuses

**Fichier :** `automation 10010000000029` (signal recover)
**Problème :** Le trigger est exclusivement sur front montant de `coherence_ko`. Une incohérence présente avant le boot et toujours active après ne produit pas de nouveau front — elle reste silencieuse.
**Amélioration :** Ajouter un second trigger sur `systeme_stable → on` dans l'automation signal recover, avec vérification de l'état courant de `coherence_ko` en condition.
**Priorité :** Faible — la sécurité démarrage et le mini-guard couvrent les cas les plus dangereux au boot.

---

### 16. Détecteur KO — Incohérences 4, 5 et 7 non couvertes

**Fichier :** `binary_sensor.chauffage_aeration_coherence_ko`
**Problème :** Trois états impossibles du contrat États canons ne sont pas détectés :
- Incohérence 4 : timer actif + blocage OFF
- Incohérence 5 : analyse disponible valide + blocage OFF
- Incohérence 7 : déjà couverte par `ko_suspension_manquante` dans le code — à corriger dans le contrat
**Amélioration :** Ajouter les incohérences 4 et 5 au détecteur.
**Priorité :** Moyenne — ces cas sont peu probables dans le chemin nominal mais peuvent apparaître après une interruption partielle.

---

### 17. M0 Cas C — Vérification enveloppe et datetime

**Fichier :** `script.aeration_m0_recover` — branche Cas C
**Problème :** Au-delà de la correction critique (exclusion suspension), M0 Cas C ne vérifie pas que l'enveloppe est fermée ni que la datetime est neutralisée ou dépassée. M4 appelé fenêtre ouverte ou avant terme est contractuellement incorrect.
**Amélioration :** Ajouter :
```yaml
- condition: state
  entity_id: binary_sensor.contact_fenetres_maison
  state: "off"
```
**Priorité :** Moyenne — le cas "fenêtre ouverte + blocage orphelin" est rare mais possible.

---

### 18. M0 — Priorisation des cas documentée

**Contrat :** `M0 — Cadre général`
**Problème :** L'ordre de traitement des cas (A → B → C) est implicite dans le `choose` du code mais non documenté contractuellement.
**Amélioration :** Documenter explicitement l'ordre de priorisation et le comportement en cas d'incohérences multiples simultanées (une seule remédiation par appel, retry au cycle suivant).

---

### 19. Couplage blocage_initial = délai_analyse + 1 min

**Fichier :** `script.aeration_m2_fin_episode`
**Problème :** La durée du blocage initial est dérivée mécaniquement du délai d'analyse. Ajuster l'un modifie l'autre.
**Amélioration :** Introduire un paramètre `input_number.blocage_initial_min` indépendant, ou documenter explicitement le couplage comme décision de conception assumée.

---

### 20. `sensor.temperature_min_chambres` non contractualisé

**Problème :** Ce capteur alimente `chute_temp_reference` via M1 mais son périmètre et son mode de calcul ne sont définis dans aucun contrat. `chute_temp_reference` lui-même n'a pas de consommateur identifié dans M2→M6.
**Amélioration :** Soit contractualiser ce capteur et documenter son rôle dans la logique décisionnelle, soit le déclasser en helper UI et le documenter comme tel.

---

## ✅ OBSERVATIONS RÉSOLUES PAR LE CODE

Ces lacunes identifiées dans les contrats n'existent pas dans l'implémentation réelle.

| Observation | Résolution |
|-------------|-----------|
| OBS-010 — M6 blocage orphelin sur échéance expirée | M6 redémarre avec durée minimale si échéance expirée |
| OBS-013 — "Réouverture qualifiée" non définie | Toute ouverture `contact_fenetres_maison off→on` pendant blocage déclenche M5 |
| OBS-014 — Comportement timer M5 ambigu | M5 annule toujours, M6 redémarre toujours |
| OBS-023 — `blocage_chauffage_aeration_active` non documenté | Présent comme condition globale du pipeline maître — interrupteur général |
| OBS-028 — Définition ΔT inversée dans contrat M3 | Code implémente `max(ref - t, 0)` — contrat erroné, code correct |
| OBS-031 — `prolongation_heures` tronqué en int | Code utilise `float(0)` — contrat erroné, code correct |

---

*Synthèse produite après audit complet des contrats normatifs et du code associé.*
