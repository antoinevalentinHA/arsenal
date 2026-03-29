# Arsenal — Workflow Cognitif
**Document normatif v1.0 · Mars 2026**

---

## 1. Problème fondamental

Ce document ne répond pas à : *« comment découper proprement ses outils »*.

Il répond à :

> **Comment réduire la friction quand je travaille ?**

Un découpage qui augmente la friction est mauvais, même s'il est logiquement cohérent.

---

## 2. Écosystème à trois cerveaux

| Acteur | Rôle | Posture |
|---|---|---|
| **Toi** | Chef d'orchestre | Vision, arbitrage, décision finale, intuition |
| **ChatGPT** | Accélérateur de pensée | Exploration rapide, structuration, mise en trajectoire |
| **Claude** | Linter intelligent | Formalisation propre, relecture critique, opposabilité |

Chaque acteur a des forces réelles, non théoriques. Les utiliser de manière interchangeable dégrade la qualité et la vitesse.

---

## 3. Modèle à deux modes

Le flux de travail est régi par deux modes — non par des domaines techniques.

### Mode LIBRE

- **Posture** : explorer, douter, comprendre, brouillonner
- **Acteurs** : Toi + ChatGPT
- Aucune contrainte de forme
- Imparfait accepté, efficacité maximisée
- Zéro obligation de structuration immédiate

### Mode STRICT

- **Posture** : produire, formaliser, valider, rendre opposable
- **Acteurs** : Toi + Claude
- YAML propre, contrats rédigés, changelogs formalisés
- Strict ≠ parfait — Strict = suffisamment propre pour être fiable
- Éviter l'équation : Strict = alourdi = évité

---

## 4. Triggers de bascule

### 4.1 Basculer en STRICT

> **Si ce que je produis va survivre à cette session → mode Strict.**

Le critère n'est pas la complexité — c'est la **durabilité**.

| Reste en LIBRE | Bascule en STRICT |
|---|---|
| Tester une idée | Écrire un YAML qui va en production |
| Comprendre un problème | Formaliser un contrat |
| Structurer une réflexion | Refactorer une inclusion |
| Brouillonner | Produire quelque chose d'opposable |

Variante : si ça va *probablement* survivre → basculer sans attendre la certitude.

### 4.2 Revenir en LIBRE

> **Si je bloque ou si je sur-spécifie → retour en Libre.**

Le retour en Libre n'est pas un échec — c'est une **correction de trajectoire**.

| Signal détecté | Lecture |
|---|---|
| Reformuler la même chose pour la 3e fois | Problème non encore compris |
| Spécifier un détail avant d'avoir la structure | Entrée en Strict trop tôt |
| Se demander si c'est « assez propre » | Perte de temps sur une non-décision |
| Ne plus avancer | Mode inadapté à l'état réel |

---

## 5. Relecture Claude — cas non négociables

Claude est positionné comme linter intelligent, pas comme cerveau principal. La relecture est asynchrone et légère par défaut — mais obligatoire dans trois cas.

| Cas | Raison |
|---|---|
| YAML avec effet physique direct (chauffage, ECS, alarme) | L'erreur n'est pas théorique — elle est opérationnelle |
| Nouveau contrat ou modification de contrat existant | Un contrat mal formalisé crée de la dette invisible |
| Refactoring structurel (include, IDs, object_id) | Les bugs silencieux se cachent là |

**Périmètre libre — pas de relecture systématique :**
- YAML purement déclaratif sans logique métier
- Changelogs et docs narratives
- Exploration et brouillons en cours

---

## 6. Garde-fous

| Garde-fou | Question mentale |
|---|---|
| Sortie du mode STRICT | Est-ce que c'est compréhensible dans 2 semaines ? |
| Dérive silencieuse en LIBRE | Est-ce que je peaufine (alors que je bloque) ? |

---

## 7. Boucle de pilotage complète

```
ÉTAT RÉEL
    │
    ▼
┌─────────────────────────────────────────────────┐
│                    LIBRE                        │
│  Explorer · Douter · Comprendre · Brouillonner  │
│                Toi + ChatGPT                    │
└─────────────────────────────────────────────────┘
    │
    │  ça va survivre ?  →  OUI
    ▼
┌─────────────────────────────────────────────────┐
│                    STRICT                       │
│   Produire · Formaliser · Valider · Opposable   │
│              Toi + Claude                       │
└─────────────────────────────────────────────────┘
    │                           │
    │  je bloque / je tourne    │  YAML à effet réel
    │  en rond ?  →  OUI        │  contrat / refactoring
    ▼                           ▼
  ← LIBRE                    RELECTURE CLAUDE
                              (non négociable)
```

---

## 8. Principes directeurs

1. Le critère n'est pas la complexité — c'est la **durabilité**
2. Revenir en Libre n'est pas un échec — c'est une **correction de trajectoire**
3. Claude n'est pas un cerveau principal — c'est un **linter intelligent**
4. Garde-fou Strict : *est-ce que c'est compréhensible dans 2 semaines ?*

---

## 9. Test de résistance

| Condition | Résistance | Raison |
|---|---|---|
| Fatigue / pression | ✓ | Une seule question de bascule |
| Fougue / vitesse | ✓ | Libre = totalement permissif |
| Production critique | ✓ | Relecture Claude non négociable |
| Dérive lente | ✓ | Signaux faibles intégrés |

---

## 10. Signal optionnel

Nommer explicitement le mode en début de session :
- `mode libre :` …
- `mode strict :` …

Effet : aligne immédiatement l'outil, évite les malentendus, accélère la production.

---

*Document normatif Arsenal · Usage interne · v1.0 · Mars 2026*
