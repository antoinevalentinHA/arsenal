### 🔒 sensor.sejour_co2_delta_30min

- Domaine : Blocages / Apports thermiques externes / Confirmation contextuelle CO2
- Autorité : **CAPTEUR STRUCTURANT INDIRECT**

---

🎯 Rôle :
Mesurer l'**écart entre la valeur actuelle du CO2 et sa moyenne glissante des 30 dernières minutes**
afin d'identifier une **hausse récente compatible avec une présence humaine réelle**
dans le séjour.

Ce capteur ne mesure pas une variation entre deux instants distants de 30 minutes.
Il mesure un écart par rapport à la baseline récente — il est donc sensible aux
**variations rapides**, pas aux montées lentes et prolongées.

Ce capteur ne constitue jamais une autorité de blocage finale.
Il sert exclusivement de base numérique à `binary_sensor.presence_humaine_sejour`.

---

🧭 Périmètre d'influence autorisé :
- Quantification de l'écart CO2 par rapport à la baseline glissante locale
- Base de confirmation contextuelle humaine
- Alimentation exclusive de `binary_sensor.presence_humaine_sejour`

---

⛔ Interdictions absolues :
- Ne déclenche jamais seul un blocage absolu
- Ne vaut jamais présence canonique du logement
- Ne décide jamais d'un mode thermique
- Ne participe jamais à la table de décision

---

🔒 Garanties exigées :
- Valeur numérique relative pure : `co2_actuel - moyenne_glissante_30min`
- Dépendance exclusive à `sensor.co2_sejour` et `sensor.co2_sejour_mean_30min`
- Indisponible si l'une des deux sources est indisponible (pas de repli mensonger)
- Aucune logique de confort
- Reload-safe / restart-safe / runtime-safe
- Absence totale d'effet matériel direct

---

🔗 Dépendances :

Sources :
- `sensor.co2_sejour` (valeur actuelle)
- `sensor.co2_sejour_mean_30min` (moyenne glissante 30 min — statistics platform)

Consommateurs contractuels :
- `binary_sensor.presence_humaine_sejour` (unique consommateur autorisé)

---

⚠️ Risques :
- Faux positifs si dérive CO2 non liée à une présence humaine (source externe, ventilation perturbée)
- Faux négatifs si aération ou renouvellement d'air comprime le signal
- **Faux négatifs sur présence prolongée** : si le CO2 monte lentement depuis plus de 30 minutes,
  la moyenne glissante suit la valeur actuelle et le delta peut repasser sous le seuil d'entrée
  malgré une présence réelle et continue — limite structurelle du mode de calcul
- Dérive systémique si utilisé comme signal décisionnel final

---

❗ Statut particulier :
**CAPTEUR STRUCTURANT INDIRECT DE CONFIRMATION CONTEXTUELLE CO2**
Brique numérique amont du mécanisme de vraisemblance humaine poêle.
Sensible aux hausses rapides, pas aux montées lentes prolongées.
Ne vaut jamais blocage direct.
Transite obligatoirement par `binary_sensor.presence_humaine_sejour`.

---

⚠️ Classification :
INCLUS DANS `03_capteurs_blocages_niveau1.md`
Section : Apports thermiques externes / Confirmation contextuelle CO2
Classe : **STRUCTURANT INDIRECT**
