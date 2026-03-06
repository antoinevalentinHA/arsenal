# 🧠 Arsenal — Modèle d’état interne

## Principe

Arsenal repose sur un **modèle d’état interne riche, persistant et multi-dimensionnel**.

Le système est :

- **stateful**
- **hysteretic**
- **invariant-driven**
- **watchdog-protected**

Le comportement global ne dépend pas uniquement des capteurs instantanés,
mais d’un **état interne construit et maintenu dans le temps**.

---

# Helpers persistants

Volume total :

- input_number : **149**
- input_boolean : **84**
- input_text : **56**
- input_datetime : **57**
- input_select : **10**
- timer : **30**

Total : **386 mémoires persistantes**

Ces entités constituent la **mémoire structurelle du système**.

---

# Rôle du modèle d’état

Chaque helper peut représenter :

- offset thermique
- seuil dynamique
- inhibition logique
- état figé
- watchdog
- anti-rebond
- cycle en cours
- invariant validé
- temporisation structurelle

Le modèle interne agit comme une **couche de stabilisation**
entre perception brute et logique décisionnelle.

---

# Propriétés du modèle

Le modèle d’état interne possède plusieurs propriétés clés :

- **mémoire longue**
- **indépendance du runtime**
- **résilience aux redémarrages**
- **stabilité multi-heures / multi-jours**
- **découplage décision / capteur**

Ainsi, une décision ne dépend jamais uniquement d’un capteur instantané,
mais d’un **état système consolidé**.

---

# Rôle des timers

Les `timer` participent pleinement au modèle d’état :

- temporisations contractuelles
- délais de stabilisation
- fenêtres d’observation
- watchdogs

Ils constituent une **mémoire temporelle active**.

---

# Conclusion

Le modèle interne constitue :

- le **cœur fonctionnel d’Arsenal**
- la **source unique de vérité**
- le socle de la **souveraineté décisionnelle**

La perception décrit le réel,
mais c’est le **modèle interne qui définit l’état du système**.