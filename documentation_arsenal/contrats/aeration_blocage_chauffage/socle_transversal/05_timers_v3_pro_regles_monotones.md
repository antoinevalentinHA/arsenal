# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF (SOCLE TRANSVERSAL)
#     TIMERS V3 PRO — RÈGLES MONOTONES & ANTI FANTÔMES
# ==========================================================

## 🎯 OBJET

Définir les règles opposables concernant :

- timer.aeration_blocage
- timer.aeration_analyse_delta_t

Ces timers sont des cadres temporels,
jamais des décideurs.

---

# ⏱️ 1️⃣ PRINCIPE FONDAMENTAL

> Le timer définit le temps.  
> L’interprétation est externe.

Les timers :

- ne déclenchent aucune action métier automatique
- servent uniquement de déclencheur événementiel

---

# 📈 2️⃣ RÈGLE DE MONOTONICITÉ

Un timer actif :

- ne peut jamais être raccourci
- peut uniquement être maintenu ou prolongé

Implémentation :

- comparaison sur remaining
- ou comparaison sur datetime cible

Applicable à :

- M2 (programmation initiale)
- M3_prolonger (extension)

---

# 🛑 3️⃣ INTERDICTION DE RÉDUCTION

Il est strictement interdit :

- de démarrer un timer avec une durée inférieure à son remaining actuel
- de réduire une échéance datetime déjà valide

---

# 🔄 4️⃣ ANNULATION EXPLICITE OBLIGATOIRE

Les timers doivent être explicitement annulés :

- en M4 (clôture totale)
- en mini-guard anti-zombie
- en sécurité démarrage (si incohérence)

Aucun timer ne doit survivre en état résiduel après clôture.

---

# 👻 5️⃣ ANTI TRIGGERS FANTÔMES

Les cas couverts :

- reboot
- pipeline zombie
- blocage orphelin

Stratégie :

- timer.cancel systématique dans les gardes
- jamais de dépendance implicite au state restauré

---

# 🔁 6️⃣ TIMER.FINISHED N’EST PAS UNE VÉRITÉ MÉTIER

L’événement `timer.finished` :

- n’est qu’un déclencheur technique
- ne prouve rien
- doit être validé par des conditions strictes (pipeline armé, blocage actif, etc.)

C’est le pipeline maître qui décide si l’étape est autorisée.

---

# 🧱 7️⃣ LIEN AVEC LES DATETIMES

Les timers et les input_datetime doivent rester cohérents :

- un blocage actif implique :
  - timer actif OU datetime valide
- un blocage levé implique :
  - timers annulés
  - datetimes neutralisés

---

# 🛑 INTERDITS ABSOLUS

- Déclencher une reprise chauffage sur timer.finished.
- Considérer un timer actif comme preuve métier.
- Laisser un timer actif après M4.

# ==========================================================