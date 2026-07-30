# Arbitrage — Descente immédiate en régime manuel VMC

| Champ | Valeur |
|---|---|
| **Domaine** | VMC — politique temporelle d'exécution (§8) sous autorité de domaine (§16) |
| **Nature** | Trace d'**arbitrage propriétaire** + amendement de contrat. Runtime associé : `11_automations/vmc/gestion_auto.yaml` |
| **Déclencheur** | Incident du 30/07/2026 — VMC bloquée en haute vitesse, prise manuelle « basse » sans effet perçu — voir [`../../../../../arsenal-runtime/analyses/vmc_incident_co2_verrou_20260730/SYNTHESE.md`](../../../../../arsenal-runtime/analyses/vmc_incident_co2_verrou_20260730/SYNTHESE.md) |
| **Contrat** | [`../../../contrats/vmc.md`](../../../contrats/vmc.md) **v2.8** — §8.2 + §8.3 + §16.5 (amendés) |

## Contexte

La durée minimale de retour en basse vitesse (§8.2, §8.3) était **commune aux deux
régimes**. Combinée au verrou d'un besoin (incident du 30/07 : besoin CO₂ armé sur
un unique pic 1005 ppm, jamais libéré dans la bande morte 800–1000), elle produit
un **ressenti de panne** : l'utilisateur prend l'autorité manuelle, commande
« basse », et la VMC reste en haute jusqu'à quinze minutes. Faute d'effet perçu,
l'utilisateur a contourné au niveau du relais MQTT.

## Décision

- En **régime manuel**, la descente en basse vitesse est **immédiate et
  inconditionnelle**. La durée mini n'est ni appliquée ni lue.
- En **régime automatique**, comportement **inchangé** : descente différée par la
  durée mini sur la seule transition de décision (immédiate au démarrage et sur
  récupération).
- Le régime est lu sur le **seul attribut `titulaire`** de la décision exécutoire
  `binary_sensor.vmc_haute_vitesse_commandee` — aucune lecture des helpers, aucune
  reconstruction (principe « l'application ne lit QUE la décision exécutoire »).

## Fondement doctrinal

- **§16.1 — unicité de l'autorité, révocabilité de sa délégation.** En régime
  manuel, le titulaire est l'utilisateur ; une règle d'exécution du régime
  automatique ne saurait s'imposer à sa consigne.
- **§8.3 — la durée mini ne définit aucun besoin** ; elle protège le matériel
  contre les **commutations rapprochées de la boucle automatique**. Un geste humain
  délibéré n'est pas une commutation rapprochée.
- **Précédent v2.7 (§17).** Le veto sanitaire pollution s'efface déjà devant la
  consigne manuelle. La durée mini était la **dernière** règle d'exécution du
  régime automatique qui débordait encore sur le manuel ; l'amendement **harmonise**
  §16.5 avec cette doctrine.

## Portée

- La **protection impérative XOR** (§16.5 niveau a — jamais deux relais actifs)
  reste **commune aux deux régimes**, inchangée. Elle demeure la seule protection
  matérielle *dure*.
- `binary_sensor.vmc_haute_vitesse_requise` (§3.1), les voies (§5, §6) et la
  décision exécutoire (§16.2) restent **strictement inchangées**.
- La montée en haute vitesse reste **immédiate** dans les deux régimes.

## Contreparties assumées

- En régime manuel, l'anti-court-cycle de la descente n'est plus garanti : un
  utilisateur peut enchaîner haute → basse sans délai. Risque borné par la
  **cadence humaine** et par le XOR ; jugé négligeable au regard du bénéfice.
- Une descente manuelle aboutit désormais **même si le helper de durée est
  illisible** (le paramètre n'est plus lu sur ce chemin) — strictement plus robuste.

## Exclusions

Aucune modification du régime automatique, de la décision métier, des voies, du
watchdog XOR, ni de la récupération après fail-safe. Aucune exemption manuelle de
la protection impérative (niveau a). Aucun nouveau helper, aucune UI.
