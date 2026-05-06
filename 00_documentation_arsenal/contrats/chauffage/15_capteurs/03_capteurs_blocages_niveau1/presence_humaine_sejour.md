### 🔒 binary_sensor.presence_humaine_sejour

- Domaine : Blocages / Apports thermiques externes / Confirmation contextuelle
- Autorité : **CAPTEUR STRUCTURANT INDIRECT**

---

🎯 Rôle :
Détecter une **présence humaine probable dans le séjour** au moyen d'une
**hausse relative du CO2**,
afin de renforcer la vraisemblance causale d'un usage réel du poêle.

Ce capteur joue un rôle de **confirmation contextuelle**.
Il ne constitue jamais à lui seul une autorité de blocage.

---

🧭 Périmètre d'influence autorisé :
- Confirmation contextuelle du mécanisme poêle
- Réduction des faux positifs thermiques sans présence probable
- Alimentation amont exclusive de `binary_sensor.poele_en_fonction`

---

⛔ Interdictions absolues :
- Ne déclenche jamais seul un blocage absolu
- Ne décide jamais d'un mode thermique
- Ne remplace jamais un capteur de présence physique
- Ne participe jamais à la table de décision chauffage
- Ne pilote jamais directement un équipement

---

🔒 Garanties exigées :
- Détection basée exclusivement sur dynamique relative du CO2
- Hystérésis asymétrique : entrée 30 ppm/30min, maintien 10 ppm/30min — résistance aux faux positifs
- Inertie de sortie : `delay_off 10 min` — stabilisation de la présence probable
- Valeur binaire pure : présence probable / absence probable
- Aucune logique de confort
- Aucune dépendance à des consignes ou offsets
- Reload-safe / restart-safe / runtime-safe
- Absence totale d'effet matériel direct

---

🔗 Dépendances :

Source :
- `sensor.sejour_co2_delta_30min`

Consommateurs contractuels :
- `binary_sensor.poele_en_fonction` (unique consommateur autorisé)

---

⚠️ Risques :
- Faux négatifs si présence réelle sans hausse CO2 suffisante
- Faux positifs si hausse CO2 non liée à une présence humaine (ventilation, source externe)
- Dérive systémique si consommé directement comme présence canonique du logement

---

❗ Statut particulier :
**CAPTEUR STRUCTURANT INDIRECT DE CONFIRMATION CONTEXTUELLE**
Signal de vraisemblance humaine du sous-système poêle.
Ne vaut jamais blocage direct.
Transite obligatoirement par `binary_sensor.poele_en_fonction`.

---

⚠️ Classification :
INCLUS DANS `03_capteurs_blocages_niveau1.md`
Section : Apports thermiques externes / Confirmation contextuelle
Classe : **STRUCTURANT INDIRECT**
