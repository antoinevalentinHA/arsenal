🧠 ARSENAL — ÉVOLUTION FUTURE

ECS — Petite Maison — Suppression du mode Eco Atlantic

📌 Statut

- Proposition d’évolution
- Domaine : ECS / Infrastructure thermique locale
- Impact : élevé (décisionnel + comportement matériel)

---

🎯 Objet

Supprimer l’utilisation du mode Eco / Eco+ embarqué Atlantic Linéo
au profit d’un pilotage déterministe intégral par Arsenal.

Cette évolution vise à :

- éliminer toute logique décisionnelle embarquée non maîtrisée,
- restaurer la traçabilité complète des actions ECS,
- garantir la conformité stricte au contrat métier ECS — Petite Maison.

---

⚠️ Constat

Analyse des comportements observés :

- cycles de chauffe irréguliers et non corrélés à un contexte métier,
- rechauffes fréquentes sans déclencheur explicite,
- comportement dépendant d’un algorithme d’apprentissage instable,
- impossibilité d’expliquer une action ECS à partir des états Arsenal.

Le mode Eco :

- anticipe les usages,
- déclenche des chauffes de manière probabiliste,
- privilégie le confort sur la sobriété,
- fonctionne correctement uniquement en cas d’usage régulier et stable.

Le contexte de la Petite Maison est :

- occupation sporadique,
- absence prolongée fréquente,
- usage imprévisible.

👉 Le mode Eco entre en apprentissage permanent non convergent.

---

❌ Non-conformités contractuelles

Le mode Eco viole plusieurs invariants du contrat ECS :

🔹 Autorité de décision

- Eco prend des décisions de chauffe localement
- Arsenal n’est plus l’unique autorité

🔹 Invariant d’autorisation

- des chauffes surviennent hors cadre explicite

🔹 Séparation des couches

- mélange observation / décision / action dans l’équipement

🔹 Traçabilité

- impossibilité d’expliquer une action ECS
- perte d’observabilité système

---

🧠 Principe de correction

Transformer le chauffe-eau en :

exécutant thermique passif

Et déplacer l’ensemble de la décision vers Arsenal :

Arsenal → décision
Linéo → exécution

---

🧭 Nouveaux états cibles

🔹 État interdit (inchangé)

Mode Absence

Implémentation :

away_mode: on
operation_mode: off

Comportement :

- aucune production ECS possible
- aucun déclenchement autonome

---

🔹 État autorisé (révisé)

Mode nominal

Implémentation cible :

away_mode: off
operation_mode: electric
temperature: 60

Caractéristiques :

- chauffe autorisée
- aucun algorithme prédictif
- comportement déterministe
- respect strict de la consigne

---

🚫 États exclus

Les modes suivants sont explicitement exclus :

eco
performance

Motifs :

- présence de logique embarquée non maîtrisée
- comportement non déterministe
- incompatibilité avec les invariants Arsenal

---

🔍 Validation attendue

Avant adoption définitive :

- observation du comportement en "electric" sur 24–72 h
- vérification :
  - absence de relance autonome imprévue
  - respect de la consigne
  - cohérence thermique (cycles lisibles)
- validation de la stabilité Overkiz

---

📈 Résultat attendu

Après migration :

- courbe thermique lisible et déterministe
- disparition des cycles incohérents
- corrélation directe :
  décision → action → effet
- amélioration de la compréhension système
- réduction du bruit décisionnel

---

🔒 Impact contractuel

Modification du contrat ECS :

- Autorisé — Mode Éco
+ Autorisé — Mode nominal

Sans modification :

- des invariants,
- de l’architecture,
- de la séparation des responsabilités.

---

🧩 Risques

- perte de confort en cas d’usage totalement imprévu
- nécessité éventuelle d’un mécanisme de boost explicite Arsenal

---

📌 Conclusion

Le mode Eco Atlantic constitue une logique concurrente non conforme
dans un système Arsenal.

Sa suppression permet de :

- restaurer l’autorité décisionnelle,
- garantir la traçabilité,
- aligner le comportement ECS avec les principes fondamentaux du système.

---

🔁 Suite

- validation terrain du mode "electric"
- adaptation du contrat ECS
- éventuelle introduction d’un mode boost Arsenal maîtrisé