# Arsenal — Prompts Canoniques
**Usage interne · Workflow cognitif · v1.0 · Mars 2026**

---

## Règle transversale

Chaque prompt commence par `Mode libre` ou `Mode strict`.  
Ce signal aligne immédiatement l'outil — sans ambiguïté, sans friction.

- **Libre** → vitesse, exploration, imparfait accepté
- **Strict** → durabilité, opposabilité, relecture possible

---

## Exploration / réflexion libre

**ChatGPT**
```
Mode libre — Arsenal.
J'explore : [sujet/problème].
Réagis vite, pousse les idées, questionne si tu vois une incohérence.
On comprend — on ne produit pas encore.
```

**Claude** *(usage rare — lecture critique d'une réflexion déjà posée)*
```
Mode libre — Arsenal.
Je te soumets une réflexion en cours, pas un livrable.
Dis-moi ce qui tient et ce qui ne tient pas.
Pas de formalisation, pas de contrat, pas de YAML.
```

---

## Contrat normatif

**ChatGPT** *(cadrage avant rédaction)*
```
Mode strict — Arsenal, contrat normatif.
Sujet : [nom du contrat].
Je veux valider la structure : périmètre, décisions contractuelles, hors-scope.
Ne rédige pas encore — structure uniquement.
```

**Claude** *(rédaction finale)*
```
Mode strict — Arsenal, contrat normatif.
Sujet : [nom du contrat].
Structure validée : [axes].

Rédige en markdown Arsenal :
— Objet
— Périmètre
— Décisions contractuelles numérotées
— Hors-scope
— Références croisées si utile

Ton sobre, normatif, opposable. Aucun filler.
```

---

## YAML

**ChatGPT** *(si la logique n'est pas encore arrêtée)*
```
Mode strict — Arsenal, YAML.
Je veux produire : [description fonctionnelle].
Avant d'écrire : est-ce que la logique tient ?
[contexte ou structure envisagée]
```

**Claude — Production**
```
Mode strict — Arsenal, YAML.
Génère le YAML pour : [description fonctionnelle].

Contraintes :
— name / object_id / unique_id obligatoires sur chaque entité
— pas de logique implicite
— [contraintes spécifiques au domaine si besoin]
```

**Claude — Relecture**
```
Mode strict — Arsenal, YAML.
Relis ce YAML. Signale uniquement :
— indentation cassée
— unicité des IDs
— logique inversée
— garde manquante
— effet de bord silencieux

Pas de réécriture complète sauf si critique.

[YAML]
```

---

## Changelog

**ChatGPT** *(si le périmètre de la version n'est pas cadré)*
```
Mode strict — Arsenal, changelog.
Version : [vX.Y.Z].
Digest : [contenu].
Identifie les axes structurants avant de rédiger.
```

**Claude** *(rédaction finale)*
```
Mode strict — Arsenal, changelog.
Version : [vX.Y.Z] — [nom si applicable].
Digest : [contenu].

Rédige au format Arsenal :
— structure narrative par axe, pas de liste plate
— ton sobre et précis
— aucune reformulation du digest, synthèse directe
```

---

## Résumé opérationnel

| Outil | Usage | Mode |
|---|---|---|
| ChatGPT | Explorer, structurer, cadrer | Libre → Strict |
| Claude | Formaliser, produire, valider | Strict |
| Claude | Lecture critique légère | Libre (rare) |

> ChatGPT pense vite. Claude écrit propre.  
> Libre pour comprendre. Strict pour ce qui survit à la session.
