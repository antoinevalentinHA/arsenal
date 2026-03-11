### 🔒 binary_sensor.poele_en_fonction

- Domaine : Blocages / Contexte thermique externe / Apports exogènes non pilotés
- Autorité : **FRONTIÈRE NIVEAU 1 FINALE**

---

🎯 Rôle :
Fournir le **signal canonique final** attestant qu'un **apport thermique compatible avec un usage réel du poêle**
influence effectivement le séjour.

Ce capteur constitue la **frontière officielle d'interdiction thermique NIVEAU 1**
pour le sous-système poêle.

Il synthétise exclusivement une **triple preuve causale** :

- une **signature thermique compatible poêle** (amorce 30 min + consolidation 60 min),
- une **présence humaine probable dans le séjour** (hausse CO2),
- la **confirmation que la chaudière n'est pas en cause** (`bruleur_mode_chauffage = off`).

Toute consommation directe des signaux amont (`signature_thermique_poele`, `presence_humaine_sejour`, `bruleur_mode_chauffage`) à des fins de blocage poêle est interdite.

Seul `binary_sensor.poele_en_fonction` peut être consommé comme frontière de blocage poêle pour :
- bloquer le chauffage pour cause d'apport poêle,
- invalider les cycles thermiques pollués,
- empêcher toute reprise thermique illégitime,
- protéger les diagnostics et modèles contre une influence externe non pilotée.

---

🧭 Périmètre d'influence autorisé :
- Déclenchement du blocage absolu NIVEAU 1 lié au poêle
- Interdiction de reprise chauffage pendant influence poêle
- Invalidation des diagnostics thermiques pollués
- Protection des offsets et modèles inertiels
- Alimentation des mécanismes mémoire / stabilisation aval
- Signal maître pour :
  - `40_blocages.md`
  - invalidation de cycles thermiques
  - protection auto-ajustement
  - diagnostics thermiques structurants

---

⛔ Interdictions absolues :
- Ne décide jamais d'un mode confort / réduit
- Ne modifie jamais une consigne
- Ne modifie jamais un offset
- Ne conditionne jamais une autorisation thermostat
- Ne pilote jamais directement la chaudière
- Ne participe jamais à la table de décision
- Ne produit jamais de calibration
- Ne déclenche jamais d'action matérielle directe

---

🔒 Garanties exigées :
- Frontière finale binaire pure : influence poêle présente / absente
- Triple preuve causale :
  - signature thermique candidate (`binary_sensor.signature_thermique_poele`)
  - présence humaine probable (`binary_sensor.presence_humaine_sejour`)
  - chaudière hors cause (`binary_sensor.bruleur_mode_chauffage = off`)
- Confirmation avant activation : `delay_on 3 min` — résistance aux faux positifs
- Inertie à la désactivation : `delay_off 5 min` — protection post-poêle
- La fenêtre de récence de 5 min de `bruleur_mode_chauffage` protège contre
  une exclusion chaudière prématurée après arrêt récent du brûleur
- Dépendance exclusive à des signaux amont structurants explicitement gouvernés
- Hystérésis et stabilisation locales robustes
- Reload-safe / restart-safe / runtime-safe
- Absence totale d'effet de bord

---

🔗 Dépendances :

Capteurs amont structurants :
- `binary_sensor.signature_thermique_poele` (capteur structurant indirect — couche N1 blocages)
- `binary_sensor.presence_humaine_sejour` (capteur structurant indirect — couche N1 blocages)
- `binary_sensor.bruleur_mode_chauffage` (exclusion causale chaudière — durci localement)

Consommateurs contractuels :
- `40_blocages.md` (blocage poêle événementiel temporisé — section 4.3)
- invalidation cycles thermiques
- protection auto-ajustement et modèles inertiels
- diagnostics thermiques structurants

---

⚠️ Risques :
- Faux positifs si les seuils thermiques ou CO2 sont mal calibrés
- Faux négatifs si présence humaine non détectée (séjour vide pendant allumage poêle)
- Sous-détection si montée poêle très lente (en dessous des seuils d'amorce)
- Blocage illégitime si `bruleur_mode_chauffage` reste `on` anormalement longtemps
- Dérive systémique majeure s'il est consommé autrement que comme frontière N1 finale

---

❗ Statut particulier :
**FRONTIÈRE FINALE NIVEAU 1 D'APPORT THERMIQUE EXTERNE NON PILOTÉ**
**Source normative finale du blocage poêle consommée par la décision centrale.**
Toute consommation directe des signaux amont hors de cette frontière est interdite.

---

⚠️ Classification :
INCLUS DANS `03_capteurs_blocages_niveau1.md`
Section : Apports thermiques externes / Frontière finale poêle
Classe : **FRONTIÈRE NIVEAU 1 FINALE**
