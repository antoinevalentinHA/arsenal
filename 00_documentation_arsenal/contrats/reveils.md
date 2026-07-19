# 🧠 ARSENAL — CONTRAT NORMATIF
## Réveils nocturnes enfants — Observabilité, cycle de vie et babyphone opt-in

---

**Version :** 1.0.0  
**Statut :** Actif  
**Domaine :** `reveils` (chambres Arnaud / Matthieu)  
**Chemin :** `00_documentation_arsenal/contrats/reveils.md`

---

## 📌 Statut

CONTRAT NORMATIF — FAIT FOI.

Ce document définit la doctrine officielle du domaine `reveils`. En cas de
divergence :

- le comportement réel des automatisations prévaut,
- les alias et descriptions ne font pas autorité.

Le domaine est documenté à partir du runtime observé (`11_automations/reveils/`
et helpers `*/reveils/`, `05_input_booleans/babyphone/`). Aucune entité, aucun
identifiant et aucune règle n'ont été inventés.

---

## 🎯 Rôle

Le domaine `reveils` couvre trois fonctions distinctes autour du bruit nocturne
dans les chambres des enfants (Arnaud, Matthieu), traitées **symétriquement** et
**par enfant** :

1. **Compteurs nocturnes** — observabilité passive du bruit la nuit.
2. **Reset quotidien** — cycle de vie des compteurs.
3. **Babyphone** — notification opt-in, **expérimentale et non garantie**.

Le domaine est aujourd'hui **autonome** : il ne pilote aucun état, ne décide
rien au sens d'un moteur d'arbitrage, et n'est couplé à aucun autre domaine
(voir §Découplage).

---

## 🧱 Sources de vérité (entités réelles)

**Réglages partagés (cadre, non causaux) :**
- `input_number.seuil_reveil_bruit` — seuil sonore (30–45 dB).
- `input_datetime.heure_reveil_nuit_debut` / `…_fin` — fenêtre nocturne.
- `input_datetime.heure_reset_reveils` — heure du reset quotidien.

**État par enfant :**
- `input_number.reveils_nocturnes_arnaud` / `…_matthieu` — compteur (0–10).
- `input_text.reveils_arnaud_heures` / `…_matthieu_heures` — historique horaire (texte, max 255).
- `input_boolean.babyphone_arnaud` / `…_matthieu` — activation babyphone.

**Perception (hors périmètre, lue) :** `sensor.bruit_chambre_enfants` / `…_matthieu`.
**Notification (hors périmètre, appelée) :** `script.notification_envoyer` vers `input_text.telephone_antoine_notify`.

---

## 1. Cadre / paramétrage

Les helpers de réglage partagés définissent **uniquement le cadre** ; les
modifier ne change jamais le comportement immédiat, seulement la définition du
seuil, de la fenêtre nocturne ou de l'heure de reset (doctrine déjà inscrite
dans les en-têtes des helpers).

- **INV-REV-1** — Le cadre est non causal : seuil, fenêtre nocturne et heure de
  reset sont des réglages ; ils ne déclenchent par eux-mêmes aucune action.
- **INV-REV-2** — Le seuil et la fenêtre nocturne sont **partagés** entre
  enfants ; les compteurs, historiques et activations babyphone sont **par
  enfant** et isolés.

## 2. Compteurs nocturnes (observabilité)

Sur dépassement du seuil sonore, **et uniquement dans la fenêtre nocturne**
(gestion du passage de minuit incluse), le compteur de l'enfant est incrémenté
(borné à 10) et l'heure est ajoutée à l'historique.

- **INV-REV-3** — Les compteurs sont une **observabilité passive** du bruit
  nocturne. Ils **ne constituent pas une preuve de réveil réel** : un dépassement
  sonore n'est pas un réveil confirmé.
- **INV-REV-4** — Aucun compteur ne déclenche de notification, ne pilote un état
  de présence, ni n'alimente une décision d'un autre domaine.
- **INV-REV-5** — Le compteur est borné à 10 (anti-spam). Au-delà, le bruit
  continue d'être journalisé dans l'historique sans incrémenter le compteur.

> **Historique indicatif.** `input_text.reveils_*_heures` est limité à 255
> caractères. Il est **indicatif et non exhaustif** : au-delà de la capacité du
> champ, l'historique peut être tronqué. Il ne doit pas être traité comme un
> journal complet ni comme une source de comptage indépendante.

## 3. Reset quotidien (cycle de vie)

À `input_datetime.heure_reset_reveils`, le compteur et l'historique de chaque
enfant sont remis à zéro / vidés.

- **INV-REV-6** — Le reset est un **événement de cycle de vie** : il efface les
  données d'observabilité de la journée écoulée et ne fait rien d'autre (aucune
  détection, aucune notification, aucune modification de seuil/fenêtre).

> **Configuration à éviter.** Régler `heure_reset_reveils` **à l'intérieur** de
> la fenêtre nocturne `[debut, fin]` efface les comptages en cours de nuit. Le
> runtime **n'empêche pas** cette configuration ; il s'agit d'une précaution de
> réglage, non d'une garantie technique.

## 4. Babyphone — notification opt-in, expérimentale et NON garantie

Lorsque `input_boolean.babyphone_<enfant>` est actif, un dépassement du seuil
sonore déclenche une notification vers Antoine (chemin canonique
`script.notification_envoyer` → `input_text.telephone_antoine_notify`). Cette
fonction **n'a pas de condition de fenêtre horaire** : elle opère tant que le
booléen est actif.

**Statut explicite :**

- **Mécanisme de notification opt-in**, activé manuellement par enfant.
- **Expérimental / non garanti.** Le babyphone **ne constitue pas une
  surveillance fiable** et ne doit pas être présenté ni utilisé comme tel.
- **Dépendant de capteurs bruit Netatmo insuffisamment réactifs** pour garantir
  une fonction babyphone opérationnelle (latence / réactivité non adaptées à une
  alerte temps réel fiable).
- **Aucun invariant de surveillance fiable** n'est défini, volontairement.

- **INV-REV-7** — Le babyphone est **strictement opt-in** : aucune notification
  sans `input_boolean.babyphone_<enfant>` actif ; il n'est jamais auto-activé.
- **INV-REV-8** — Le destinataire **observé** est Antoine via le chemin canonique
  existant. Le contrat n'introduit ni destinataire familial ni destinataire
  configurable.
- **INV-REV-9** — Le babyphone **n'offre aucune garantie** de détection, de
  délai ou de couverture. Il ne doit pas devenir un service opposable de
  surveillance tant que la chaîne de perception n'est pas qualifiée pour cela.

## 5. Découplage (état actuel)

Le domaine `reveils` est aujourd'hui **totalement découplé** :

- aucun couplage avec l'**alarme** ni le **chauffage** ;
- aucune dépendance à **Vacances**, **Babysitting**, **présence famille** ou
  **mode Maison** ;
- la « nuit » est définie **uniquement** par les `input_datetime` de la fenêtre
  nocturne, et non par un mode présence/nuit.

- **INV-REV-10** — Le comptage et le babyphone **ne dépendent jamais** de l'état
  de l'alarme ou du chauffage et ne pilotent aucun de leurs états.

> Aucune règle de suspension ou d'adaptation en Vacances / Babysitting /
> présence n'est inventée ici. Si une telle interaction est souhaitée, elle
> relève d'un arbitrage explicite ultérieur (voir §Dettes).

## 6. Hors périmètre

Référencés mais **non définis** par ce contrat :

- la **source** `sensor.bruit_chambre_<enfant>` (perception Netatmo / système) ;
- le **mécanisme de notification** `script.notification_envoyer` (voir
  [`notifications.md`](notifications.md)) ;
- les **capteurs couleur** dérivés du bruit (couche `couleurs` / UI) ;
- les **surfaces UI** (`18_lovelace/dashboards/sommeil/principal.yaml` et
  `…/reglages/sommeil.yaml`), co-localisées avec le contexte « sommeil » sans
  appartenir au domaine `reveils`.

## 7. Dettes / points à arbitrer

Ces points sont **signalés, non corrigés** par ce contrat (aucune modification
du runtime n'est faite). Ils n'ont pas de valeur normative tant qu'ils ne sont
pas arbitrés.

- **DETTE-REV-1 — Fallback `float(0)` du babyphone.** Le babyphone applique un
  fallback de seuil `float(0)` (contre `float(40)` pour le compteur) : si
  `seuil_reveil_bruit` devient indisponible, le babyphone devient hypersensible.
  Signalé comme **dette / anomalie potentielle**, **pas** comme comportement
  normatif souhaité.
- **DETTE-REV-2 — Historique vs compteur.** L'historique s'alimente à chaque
  dépassement alors que le compteur est borné à 10 ; combiné à la limite de 255
  caractères, l'historique peut diverger du compteur et être tronqué. À arbitrer
  (bornage / élagage) si une cohérence stricte est souhaitée.
- **DETTE-REV-3 — Reset dans la fenêtre nocturne.** Configuration possible et
  destructrice (cf. §3), non empêchée par le runtime. À arbitrer si une garde
  doit être imposée.
- **ARB-REV-1 — Vacances / Babysitting.** Aucun couplage actuel. À arbitrer :
  suspendre, adapter ou laisser actif le comptage et/ou le babyphone selon ces
  modes.
- **ARB-REV-2 — Qualification du babyphone.** Tant que la réactivité des capteurs
  Netatmo n'est pas qualifiée, le babyphone reste expérimental (cf. §4) ; toute
  promotion en service de surveillance opposable nécessite une révision formelle.

---

## 🔗 Renvois

- Notifications : [`notifications.md`](notifications.md)
- Contexte sommeil / santé (UI co-localisée) : [`sante/sommeil.md`](sante/sommeil.md), [`sante/cardio_nuit.md`](sante/cardio_nuit.md)

---

## 🔒 Statut d'autorité

Contrat normatif d'un domaine autonome de faible criticité. Le babyphone y est
documenté comme mécanisme **opt-in non garanti**, jamais comme service de
surveillance opposable. Toute évolution (couplage de modes, garde de reset,
qualification du babyphone) requiert une révision formelle de ce contrat.
