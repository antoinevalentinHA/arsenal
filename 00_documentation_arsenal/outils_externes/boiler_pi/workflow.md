# Workflow Git — boiler-bridge

<!-- audit:scope=doc -->
## PC → GitHub → Pi

> **Objectif** : zéro bricolage, zéro surprise, rollback trivial.  
> **Principe** : toute modification naît sur le PC, transite par GitHub, est déployée sur le Pi. Jamais l'inverse.

---

## 0. Structure cible

```
boiler-bridge/
├── boiler_mqtt.py
├── boiler_guard.sh
├── deploy.sh
├── backup_boiler_bridge.sh
├── README.md
├── systemd/
│   ├── boiler_bridge.service
│   ├── boiler-guard.service
│   └── boiler-guard.timer
└── .gitignore
```

---

## 1. PC — Initialisation

### 1.0 Dossier de travail PC (obligatoire)

Toutes les opérations sont réalisées dans le dossier dédié :

```bash
cd C:/boiler
```

> Ce dossier est la racine unique des dépôts liés au boiler bridge. Structure locale : `C:/boiler/boiler-bridge/`.

### 1.1 Créer le dépôt local

```bash
mkdir boiler-bridge
cd boiler-bridge
git init
```

### 1.2 Capturer l'état initial depuis le Pi

```bash
scp pi@192.168.1.119:/home/pi/boiler-bridge/boiler_mqtt.py .
ls -l boiler_mqtt.py
```

> Cette copie constitue la capture de l'état de production initial du boiler bridge.  
> Nécessite OpenSSH (installé par défaut sur Windows 10/11).

### 1.3 `.gitignore` (obligatoire)

```
__pycache__/
*.pyc
.env
.env.*
*.log
venv/
```

### 1.4 Commit initial

```bash
git add .
git commit -m "init: boiler bridge"
```

---

## 2. GitHub — Dépôt privé

Créer un dépôt privé nommé **`boiler-bridge`**, puis :

```bash
git remote add origin git@github.com:antoinevalentinHA/boiler-bridge.git
git branch -M main
git push -u origin main
```

> **Prérequis :** clé SSH configurée (voir section 9).

---

## 3. Pi — Installation initiale

Connexion SSH classique.

### 3.1 Cloner le dépôt (SSH obligatoire)

```bash
cd /home/pi
git clone git@github.com:antoinevalentinHA/boiler-bridge.git
cd boiler-bridge
```

### 3.2 Déployer

```bash
/home/pi/boiler-bridge/deploy.sh
```

Le script déploie les unités systemd depuis le dépôt, recharge systemd et redémarre les services.

### 3.3 Activer le timer guard si nécessaire

```bash
sudo systemctl enable boiler-guard.timer
sudo systemctl restart boiler-guard.timer
```

### 3.4 Vérifier

```bash
systemctl status boiler_bridge.service --no-pager
systemctl status boiler-guard.timer --no-pager
journalctl -t boiler-guard -n 20 --no-pager
```

---

## 4. Workflow quotidien

### Sur le PC — modifier et publier

```bash
python -m py_compile boiler_mqtt.py   # Windows : python ; Pi : python3
git add .
git commit -m "fix: gestion ACK timeout"
git push
```

### Sur le Pi — déployer

```bash
/home/pi/boiler-bridge/deploy.sh
```

Le script deploy.sh :

- vérifie l’absence de modifications locales (garde-fou Git) ;
- synchronise le dépôt (`git fetch` + `reset --hard origin/main`) ;
- vérifie l’intégrité du code (Python + Bash) ;
- déploie les unités systemd depuis le dépôt vers `/etc/systemd/system/` ;
- recharge systemd (`daemon-reload`) ;
- redémarre les services.

👉 Le résultat est un runtime strictement aligné sur `origin/main`
(sans merge, sans état intermédiaire).

Le script refuse le déploiement si :

- un override systemd (*.service.d/) est présent ;
- une référence /etc/arsenal est détectée.

👉 deploy.sh est le seul mécanisme autorisé de déploiement.
👉 Toute modification manuelle du runtime est interdite.

---

## 5. Rollback

```bash
cd /home/pi/boiler-bridge
git log --oneline
git reset --hard <commit_id>
/home/pi/boiler-bridge/deploy.sh
```

Pour revenir ensuite sur la dernière version de `main` :

```bash
/home/pi/boiler-bridge/deploy.sh
```

`deploy.sh` applique `fetch` + `reset --hard origin/main`, vérifie le code, redéploie les unités systemd et redémarre les services.

---

## 6. Discipline — règles non négociables

| Règle | Détail |
|-------|--------|
| **Jamais modifier sur le Pi** | Le Pi est un environnement d'exécution, pas de développement. Toute modification directe casse le modèle. |
| **Toujours committer avant de déployer** | Le Pi n'exécute que du code versionné. |
| **Un commit = une intention claire** | Pas de commits "test", "wip" ou "misc". |

Configuration git recommandée sur le Pi (à faire une fois) :

```bash
git config --global pull.ff only
git config --global advice.detachedHead false
```

---

## 7. Secrets — ne jamais versionner

Ne jamais mettre dans git :

- identifiant MQTT
- mot de passe MQTT
- tokens / clés API

**Emplacement obligatoire :**

```
/home/pi/boiler_bridge.env
```

Créer le fichier :

```ini
MQTT_USER=monuser
MQTT_PASSWORD=monpassword
```

Verrouiller les droits (obligatoire) :

```bash
chmod 600 /home/pi/boiler_bridge.env
chown pi:pi /home/pi/boiler_bridge.env
```

Référencer dans le service :

```ini
EnvironmentFile=/home/pi/boiler_bridge.env
```

> Le fichier `/home/pi/boiler_bridge.env` est hors du dépôt git et hors de `/home/pi/boiler-bridge/`. Il n'est jamais versionné.

---

## 8. README du dépôt

Le dépôt contient un `README.md` décrivant :

- l'architecture locale ;
- le rôle du bridge et du guard ;
- le déploiement via `deploy.sh` ;
- l'observabilité ;
- la sauvegarde ;
- la restauration ;
- les invariants de production.

Le README ne doit pas documenter de procédure parallèle à `deploy.sh`.

---

## 9. Authentification SSH vers GitHub (obligatoire)

```bash
ssh-keygen -t ed25519 -C "arsenal-boiler-bridge"
cat ~/.ssh/id_ed25519.pub   # coller dans GitHub → Settings → SSH keys
```

Vérifier que le remote utilise SSH :

```bash
git remote set-url origin git@github.com:antoinevalentinHA/boiler-bridge.git
```

---

## 10. Script de déploiement en une commande

Script canonique :

```bash
/home/pi/boiler-bridge/deploy.sh
```

Le script est versionné dans le dépôt et constitue le seul point d'entrée autorisé pour déployer sur le Pi.

Il assure :

* garde-fou Git local ;
* synchronisation `origin/main` ;
* vérification Python/Bash ;
* déploiement explicite des unités systemd ;
* `daemon-reload` ;
* redémarrage des services ;
* affichage des statuts et logs ;
* refus des overrides systemd ;
* refus des références legacy `/etc/arsenal`.

---

## 11. Backup (obligatoire)

Script local :

```
/home/pi/boiler-bridge/backup_boiler_bridge.sh
```

Le script sauvegarde :

```text
/home/pi/boiler-bridge/
/home/pi/boiler_bridge.env
/etc/systemd/system/boiler_bridge.service*
/etc/systemd/system/boiler-guard.service*
/etc/systemd/system/boiler-guard.timer
```

Le backup inclut à la fois la source (repo) et l'état runtime systemd.

Le script échoue si `/mnt/backups_boiler_pi` n'est pas monté et conserve les 7 dernières sauvegardes.

Destination :

```
/mnt/backups_boiler_pi/
```

> ⚠️ **Invariant** : si le NAS n'est pas monté, le script échoue immédiatement. Aucun backup silencieux en local.

---

## Résumé

| Élément | Choix |
|---------|-------|
| Versioning | Git (local + GitHub privé) |
| Déploiement | `/home/pi/boiler-bridge/deploy.sh` |
| Rollback | `git reset --hard <commit_id>` + `deploy.sh` |
| Secrets | `/home/pi/boiler_bridge.env`, hors git |
| Remote GitHub | SSH obligatoire |

**Invariants de production :**

```
service bridge  = boiler_bridge.service
service guard   = boiler-guard.service
timer guard     = boiler-guard.timer
scripts         = /home/pi/boiler-bridge/
config          = /home/pi/boiler_bridge.env
systemd source  = /home/pi/boiler-bridge/systemd/
overrides       = interdits en régime nominal
legacy          = /etc/arsenal interdit
```
