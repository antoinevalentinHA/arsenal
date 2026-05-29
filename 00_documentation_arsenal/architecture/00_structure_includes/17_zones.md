# Structure — zones

## Rôle

Déclaration des zones géographiques Home Assistant.

Les zones servent à :
- définir des périmètres géographiques,
- matérialiser des contextes spatiaux,
- qualifier une présence,
- exposer des transitions géographiques,
- fournir des cadres de raisonnement géolocalisés.

Une zone ne représente jamais :
- une présence réelle validée,
- une décision métier,
- une autorisation,
- une preuve d’occupation.

---

## Doctrine Arsenal

Les zones constituent une couche
de contexte géographique brut.

Elles peuvent :
- définir un périmètre,
- qualifier une proximité,
- fournir un contexte spatial,
- servir de base à des raisonnements métiers,
- matérialiser des cadres de sécurité ou d’anticipation.

Mais elles ne doivent jamais :
- porter une logique métier,
- décider d’une présence,
- remplacer une fusion de présence,
- devenir une autorité de sécurité,
- produire directement une action système.

---

## Include

```yaml
zone: !include_dir_merge_list zones/
```

---

## Invariants

- Les noms doivent rester stables
- Le slug Home Assistant doit rester maîtrisé
- Toute zone métier doit avoir un périmètre explicitement justifié
- Les rayons doivent être cohérents avec l’usage métier déclaré
- Une zone ne constitue jamais à elle seule une preuve de présence
- Toute logique de présence doit être externalisée
- Toute logique décisionnelle doit être externalisée
- Les zones passives doivent être explicitement justifiées

---

## Typologies Arsenal

- presence_stricte
- presence_elargie
- approche_geographique
- zone_metier
- zone_technique
- perimetre_securite
- zone_transition
- contexte_spatial
- anticipation_presence

---

## Structure

```yaml
- name: <nom_sans_accent>

  latitude: <decimal>
  longitude: <decimal>

  radius: <metres>

  icon: <icone>

  passive: <true|false>                  # optionnel
```

---

## Clés courantes

- name
- latitude
- longitude
- radius
- icon
- passive

---

## Modèle d’en-tête recommandé

```yaml
# ==========================================================
# 🧠 ARSENAL — ZONE
#     <Domaine> — <Fonction>
# ----------------------------------------------------------
# 🎯 RÔLE
#   <Finalité système exacte — une phrase>
#
# 🧩 PÉRIMÈTRE
#   - Contexte géographique brut uniquement
#   - Aucune logique métier
#   - Aucune décision de présence
#   - Aucune action directe
#
# 🔖 NATURE
#   <presence_stricte | presence_elargie | approche_geographique
#    | zone_metier | zone_technique | perimetre_securite
#    | zone_transition | contexte_spatial | anticipation_presence>
#
# 📋 PARAMÈTRES
#   latitude  : <decimal>
#   longitude : <decimal>
#   radius    : <mètres — justification métier obligatoire>
#   passive   : <true|false — justification si true>
#
# 🚫 INTERDITS
#   - Constituer une preuve de présence
#   - Servir d'autorité décisionnelle
#   - Remplacer une fusion de présence
#   - Déclencher directement une action système
#   - Laisser un rayon non justifié par l'usage métier
#
# 🏷️ STATUT
#   Contexte spatial — Arsenal v14.x
# ==========================================================
```