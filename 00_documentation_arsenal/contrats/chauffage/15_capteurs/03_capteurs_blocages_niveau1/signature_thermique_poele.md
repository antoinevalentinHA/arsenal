# 🔒 binary_sensor.signature_thermique_poele

- Domaine : Blocages / Apports thermiques externes / Détection thermique candidate
- Autorité : **CAPTEUR STRUCTURANT INDIRECT**

---

🎯 Rôle :
Détecter une **signature thermique compatible avec un fonctionnement de poêle**,
par combinaison d'une :

- **amorce de montée thermique sur 30 minutes** (`sejour_delta_30min`),
- **consolidation thermique sur 60 minutes** (`sejour_delta_60min`).

Ce capteur ne constitue **jamais** une frontière finale de blocage.
Il fournit uniquement une **preuve thermique candidate** d'apport exogène,
destinée à être consommée par `binary_sensor.poele_en_fonction`.

---

🧭 Périmètre d'influence autorisé :
- Détection thermique candidate d'apport poêle
- Validation amont du mécanisme poêle
- Protection contre les hausses thermiques trop faibles ou non consolidées
- Alimentation exclusive de `binary_sensor.poele_en_fonction`

---

⛔ Interdictions absolues :
- Ne déclenche jamais seul un blocage absolu
- Ne sert jamais de frontière finale NIVEAU 1
- Ne décide jamais d'un mode thermique
- Ne modifie jamais une consigne
- Ne pilote jamais directement la chaudière
- Ne participe jamais à la table de décision

---

🔒 Garanties exigées :
- Détection basée exclusivement sur dynamiques thermiques locales
- Double critère temporel obligatoire : `sejour_delta_30min` (amorce) + `sejour_delta_60min` (consolidation)
- Hystérésis asymétrique : seuils d'entrée plus élevés que seuils de maintien — résistance aux faux positifs
- Inertie de sortie : `delay_off 5 min` — stabilisation de la signature candidate
- Valeur binaire pure : signature présente / absente
- Aucune dépendance à des consignes ou offsets
- Reload-safe / restart-safe / runtime-safe
- Absence totale d'effet matériel direct

---

🔗 Dépendances :

Sources :
- `sensor.sejour_delta_30min` (amorce thermique)
- `sensor.sejour_delta_60min` (consolidation thermique)

Consommateurs contractuels :
- `binary_sensor.poele_en_fonction` (unique consommateur autorisé)

---

⚠️ Risques :
- Faux positifs si exposition solaire locale rapide mal filtrée
- **Faux négatifs sur montée lente prolongée** : si la température monte régulièrement
  depuis plus de 60 minutes, les deux deltas peuvent rester compressés sous leurs seuils
  malgré une influence poêle réelle — limite structurelle héritée des capteurs amont
- Faux négatifs si montée thermique très lente (poêle à allumage progressif)
- Oscillations si hystérésis affaiblie
- Dérive systémique s'il est utilisé comme autorité finale

---

❗ Statut particulier :
**CAPTEUR STRUCTURANT INDIRECT DE SIGNATURE THERMIQUE**
Preuve amont candidate d'un apport thermique exogène.
Ne vaut jamais blocage direct.
Transite obligatoirement par `binary_sensor.poele_en_fonction`.

---

⚠️ Classification :
INCLUS DANS `03_capteurs_blocages_niveau1.md`
Section : Apports thermiques externes / Détection thermique candidate
Classe : **STRUCTURANT INDIRECT**
