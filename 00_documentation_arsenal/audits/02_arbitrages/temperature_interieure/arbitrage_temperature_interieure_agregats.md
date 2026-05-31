# Note d'arbitrage — Durcissement des agrégats `temperature_min/max_chambres`

> Type : note d'arbitrage — aide à la décision métier, préalable à l'implémentation
> Portée : couche d'agrégation thermique intérieure
>          (`sensor.temperature_min_chambres`, `sensor.temperature_max_chambres`)
> Origine : audit officiel « Températures intérieures / façades thermiques internes »,
>           note de validation du risque, plan d'action agrégats
> Statut : non normatif — fixe les choix à trancher avant tout chantier

---

## 1. TTL agrégat

| Option | Avantages | Inconvénients | Impact métier | Cohérence Arsenal |
|---|---|---|---|---|
| **Identique aux façades (1800 s)** | Symétrie de nommage, simple à expliquer | **Double comptage** : la péremption par zone (1800 s dans `consolidation.yaml`) est déjà épuisée avant que les façades tombent → jusqu'à ~60 min de gel avant tout signal | Détection tardive du gel | Apparente, mais sémantiquement fausse (empile deux TTL) |
| **Plus court** | Bornage serré ; l'agrégat signale peu après que l'indisponibilité totale est confirmée en aval | Introduit une constante distincte à justifier | Fenêtre de gel courte, alerte rapide | **Bonne** : reconnaît que la péremption est en couches |
| **Plus long** | Moins d'alertes, tolère de longues coupures sans bruit | Prolonge précisément le défaut qu'on corrige | Fenêtre de décision sur données figées allongée | Faible : contredit l'objectif de bornage |
| **Autre — fraîcheur événementielle** : mesurer « la durée depuis que les trois façades sont simultanément indisponibles » | Sémantiquement exact, pas de nombre arbitraire, réutilise le pattern `input_datetime.humidite_relative_last_valid_ts_<zone>` (v12.1.1) | Nécessite un helper de fraîcheur | Aucun changement tant que la condition n'est pas remplie | **Maximale** : aligné sur l'humidité et la logique événementielle d'Arsenal |

---

## 2. Politique après expiration

| Option | Chauffage | Climatisation | Aération | Risques |
|---|---|---|---|---|
| **Continuité infinie + alerte** | Inchangé : décide sur valeur figée ; alerte seule | Inchangé | Inchangé | Décisions sur données périmées **indéfiniment** ; protection 100 % dépendante de l'humain |
| **Continuité bornée + alerte** (valeur publiée maintenue, statut `périmé` + alerte au-delà du TTL, **valeur d'état inchangée**) | Inchangé dans la fenêtre ; au-delà, signal sans coupure | Inchangé ; signal sans coupure | Inchangé ; signal sans coupure | Faible : le bornage porte sur la **confiance**, pas la valeur → **zéro changement métier** |
| **Abstention après TTL** (valeur → `unknown`) | `cible → unknown → desired_mode = neutre → « Stop si mode neutre »` → **le chauffage cesse de s'ajuster** (programme chaudière figé) | `seuil_*_atteint` → gardes activées → autorisation `off` → **clim s'arrête** | Recommandation abstient | **Nouveau mode de défaillance** : perte d'ajustement climatique pendant la panne — écarté par la note de risque |
| **Autre — hybride par domaine** (continuité chauffage / abstention clim+aération) | Continuité (l'arrêt serait risqué l'hiver) | Abstention (l'arrêt est conservateur) | Abstention | Cohérent au plan sécurité mais **complexe** : contrats par domaine, raisonnement éclaté |

---

## 3. Statut : attributs vs entité compagnon

| Critère | Attributs sur entités existantes | Entité compagnon dédiée |
|---|---|---|
| **Observabilité** | Correcte (lisible via `state_attr`, en carte) mais non historisable comme état | Forte : état de premier rang, historisable, consommable proprement par l'alerte |
| **Simplicité** | Élevée : aucune nouvelle entité | Moindre : une entité par agrégat (justifiée par symétrie) |
| **Cohérence avec `sensor.temperature_jardin_statut`** | Partielle : l'extérieur utilise justement un **compagnon séparé**, pas des attributs | **Maximale** : reproduit exactement le canal valeur/statut de l'extérieur |
| **Maintenance** | Surface réduite, mais signal moins découvrable | Propriété claire, davantage d'entités |

Lecture : les attributs sont le **MVP léger** ; l'entité compagnon est le choix
**cohérent** dès lors qu'une automatisation d'alerte doit consommer le statut, et
qu'on veut respecter la doctrine valeur/statut déjà posée pour `temperature_jardin`.

---

## 4. Recommandation finale

**Option recommandée.**

- **TTL** : fraîcheur **événementielle, courte** — fondée sur « durée depuis
  indisponibilité simultanée des trois façades », via le pattern
  `input_datetime.*_last_valid_ts` déjà déployé. Ni identique (double comptage), ni
  longue (gel prolongé).
- **Politique** : **continuité bornée + alerte** — la valeur d'état des
  `temperature_min_chambres` / `temperature_max_chambres` reste publiée et
  inchangée ; seul le canal confiance (statut `périmé` + notification) se déclenche
  au-delà du TTL. **Zéro changement métier** pour chauffage / climatisation /
  aération.
- **Statut** : **entité compagnon** sur le modèle de `sensor.temperature_jardin_statut`
  (attributs acceptables comme première étape si l'on veut limiter le footprint).

**Raisons.** Respecte la contrainte dure (ne pas modifier le métier) ; borne et rend
visible le gel silencieux ; réutilise deux patterns Arsenal existants (statut
extérieur, fraîcheur humidité) plutôt que d'inventer ; évite le nouveau mode de
défaillance que l'abstention introduirait.

**Compromis acceptés.**

- Pendant la fenêtre (courte) de continuité bornée, les décisions tournent encore
  sur une donnée figée — accepté car **borné, alerté, et rare** (double panne
  corrélée).
- Deux entités/helpers nouveaux (fraîcheur + statut compagnon) — accepté au nom de
  l'observabilité.
- La question « le chauffage doit-il finir par s'abstenir sur panne longue ? » est
  **volontairement laissée ouverte** (option hybride différée).

**Points restant ouverts.**

1. Valeur numérique exacte du seuil de fraîcheur.
2. Compagnon dédié vs attributs (footprint vs cohérence).
3. Abstention hybride par domaine — phase ultérieure, hors de ce chantier.
4. Réconciliation de plausibilité `axe_temperature.md` (8-40) vs
   runtime/`consolidation.md` (5-45) — adjacent, à traiter avec le contrat
   d'agrégation.
