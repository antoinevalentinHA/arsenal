# 🔒 sensor.sejour_delta_60min

- Domaine : Blocages / Apports thermiques externes / Détection dynamique consolidée
- Autorité : **CAPTEUR STRUCTURANT INDIRECT**

---

🎯 Rôle :
Mesurer l'**écart entre la température actuelle du séjour et sa moyenne glissante des 60 dernières minutes**,
afin d'identifier une **montée thermique durable et installée**
compatible avec un apport poêle en régime réel.

Ce capteur ne mesure pas un delta entre deux instants distants de 60 minutes.
Il mesure un écart par rapport à une baseline plus longue — sa moyenne glissante
étant plus lente à suivre les variations, il est **plus résistant aux montées lentes prolongées**
que `sensor.sejour_delta_30min`, ce qui en fait le signal de consolidation naturel.

Dans l'architecture Arsenal, `sensor.sejour_delta_60min` constitue la
**preuve de consolidation thermique** du mécanisme de détection poêle.

Associé à `sensor.sejour_delta_30min` (amorce thermique),
il permet de distinguer une **dérive thermique durable**
d'une variation transitoire locale.

Il alimente `binary_sensor.signature_thermique_poele`
mais **ne déclenche jamais seul un blocage final**.

---

🧭 Périmètre d'influence autorisé :
- Consolidation de la signature thermique poêle
- Filtrage des hausses trop brèves ou non durables
- Alimentation exclusive de `binary_sensor.signature_thermique_poele`
- Diagnostics thermiques structurants

---

⛔ Interdictions absolues :
- Ne déclenche jamais seul un blocage absolu
- Ne décide jamais d'un mode thermique
- Ne modifie jamais une consigne
- Ne pilote jamais directement la chaudière
- Ne participe jamais à la table de décision

---

🔒 Garanties exigées :
- Valeur numérique pure : `temperature_actuelle - moyenne_glissante_60min`
- Dépendance exclusive à `sensor.temperature_sejour` et `sensor.temperature_sejour_mean_60min`
- Aucun fallback à `0` : état `unknown` assumé honnêtement si données non prêtes
- Aucune logique métier thermique
- Reload-safe / restart-safe / runtime-safe
- Absence totale d'effet matériel direct

---

🔗 Dépendances :

Sources :
- `sensor.temperature_sejour` (valeur actuelle)
- `sensor.temperature_sejour_mean_60min` (moyenne glissante 60 min — statistics platform)

Consommateurs contractuels :
- `binary_sensor.signature_thermique_poele` (unique consommateur autorisé)

---

⚠️ Risques :
- Détection plus lente que les fenêtres courtes — intentionnel, rôle de consolidation
- Faux négatifs si usage poêle très bref (fenêtre trop longue par rapport à la durée du pic)
- Dérive systémique s'il est interprété comme autorité finale

---

❗ Statut particulier :
**CAPTEUR STRUCTURANT INDIRECT DE CONSOLIDATION THERMIQUE**
Source de preuve durable de la signature thermique poêle.
Plus résistant aux montées lentes prolongées que [`sejour_delta_30min.md`](sejour_delta_30min.md)
grâce à une baseline glissante de 60 minutes.
Ne vaut jamais blocage direct.
Transite obligatoirement par `binary_sensor.signature_thermique_poele`.

---

⚠️ Classification :
INCLUS DANS [`03_capteurs_blocages_niveau1.md`](../03_capteurs_blocages_niveau1.md)
Section : Apports thermiques externes / Détection dynamique consolidée
Classe : **STRUCTURANT INDIRECT**
