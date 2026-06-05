# 🔒 sensor.sejour_delta_30min

- Domaine : Blocages / Apports thermiques externes / Détection dynamique persistante
- Autorité : **CAPTEUR STRUCTURANT INDIRECT**

---

🎯 Rôle :
Mesurer l'**écart entre la température actuelle du séjour et sa moyenne glissante des 30 dernières minutes**,
afin d'identifier une **montée thermique récente et persistante** dans la pièce.

Ce capteur ne mesure pas un delta entre deux instants distants de 30 minutes.
Il mesure un écart par rapport à la baseline récente — il est donc sensible aux
**montées rapides**, pas aux dérives lentes et progressives.

Dans l'architecture Arsenal, `sensor.sejour_delta_30min` constitue la
**preuve d'amorce thermique** du mécanisme de détection poêle.

Associé à `sensor.sejour_delta_60min` (consolidation thermique),
il permet de distinguer une **dérive thermique durable**
d'une variation transitoire locale.

Il alimente `binary_sensor.signature_thermique_poele`
mais **ne suffit jamais seul à qualifier une influence poêle durable**.

---

🧭 Périmètre d'influence autorisé :
- Alimentation de `binary_sensor.signature_thermique_poele`
- Diagnostics thermiques structurants
- Protection indirecte des modèles thermiques

---

⛔ Interdictions absolues :
- Ne décide jamais d'un mode thermique
- Ne modifie jamais une consigne
- Ne modifie jamais un offset
- Ne conditionne jamais une autorisation thermostat
- Ne pilote jamais directement la chaudière
- Ne participe jamais à la table de décision
- Ne sert jamais de seuil thermique
- Ne déclenche jamais un blocage direct
- Ne produit jamais de calibration
- Ne déclenche jamais un auto-ajustement

---

🔒 Garanties exigées :
- Valeur numérique pure : `temperature_actuelle - moyenne_glissante_30min`
- Dépendance exclusive à `sensor.temperature_sejour` et `sensor.temperature_sejour_mean_30min`
- Aucun fallback à 0 : état `unknown` assumé honnêtement si données non prêtes
- Robustesse aux reloads et redémarrages
- Stabilité temporelle intra-régime
- Immunité aux fluctuations rapides non persistantes
- Aucune dépendance à des consignes, offsets ou décisions
- Absence totale d'effet matériel direct

---

🔗 Dépendances :

Sources :
- `sensor.temperature_sejour` (valeur actuelle)
- `sensor.temperature_sejour_mean_30min` (moyenne glissante 30 min — statistics platform)

Consommateurs contractuels :
- `binary_sensor.signature_thermique_poele` (consommateur principal)
- Diagnostics thermiques structurants
- Protections aval explicitement gouvernées

---

⚠️ Risques :
- Détection tardive si montée thermique très progressive
- **Faux négatifs sur montée lente prolongée** : si la température monte régulièrement
  depuis plus de 30 minutes, la moyenne glissante suit la valeur actuelle et le delta
  peut rester sous le seuil d'amorce malgré une influence poêle réelle —
  limite structurelle du mode de calcul, compensée par `sensor.sejour_delta_60min`
- Faux négatifs sur poêles à montée très lente
- Pollution thermique si seuils mal calibrés dans [`signature_thermique_poele.md`](signature_thermique_poele.md)
- Blocage prolongé si dérive persiste artificiellement
- Dérive critique s'il est utilisé comme signal décisionnel direct

---

❗ Statut particulier :
**CAPTEUR STRUCTURANT INDIRECT D'AMORCE THERMIQUE**
Source amont courte/moyenne portée de la signature thermique poêle.
Sensible aux montées rapides, pas aux dérives lentes prolongées.
Ne vaut jamais blocage direct.
Transite obligatoirement par `binary_sensor.signature_thermique_poele`.

---

⚠️ Classification :
INCLUS DANS [`03_capteurs_blocages_niveau1.md`](../03_capteurs_blocages_niveau1.md)
Section : Apports thermiques externes / Détection dynamique primaire
Classe : **STRUCTURANT INDIRECT**
