# Installation

*Note : Le dossier `user_interface` contient l'ensemble de l'interface. Le frontend en [Svelte](https://svelte.dev/docs/svelte/overview) (dossier `src`) à exécuter grâce à [Node.Js](https://nodejs.org/fr) et le backend en [Python](https://docs.python.org/fr/3.13/using/index.html) (dossier `python`) à exécuter grâce à [Python](https://www.python.org/downloads/). Il n'est pas nécessaire d'exécuter ces deux parties depuis le même dossier/environnement/ordinateur. **Cependant, il faut que le front, le back et le robot soient connectés sur le même réseau wifi**. Attention à bien modifier les adresses ip des requêtes envoyées (voir [Configurations](#configurations)).*


## Frontend - Svelte

- Installer [Node.Js](https://nodejs.org/fr)

- Cloner localement le dossier [GitHub](https://github.com/mines-nancy/user_interface) (voir les [Tips GitHub](#tips-github))

- Ouvrir un terminal (invité de commande, Command Prompt ou PowerShell) à la racine du dossier `user_interface`

Pour vérifier que [Node.Js](https://nodejs.org/fr) est bien installé, entrer :

```bash
node -v
npm -v
```

Cela devrait afficher les versions installées.

- Installer les packages et les dépendances nécessitées par le projet :

```bash
npm install
```

- Vérifier le bon fonctionnement, lever le serveur en entrant :

```bash
npm run dev

# ou pour lever le serveur en ouvrant directement l'application dans un onglet du moteur de recherche
npm run dev -- --open
```

## Backend - Python

- Installer [Python](https://www.python.org/downloads/)

    - **IMPORTANT :**

    > Cocher la case « Ajouter Python 3.x au PATH » avant de procéder à l’installation. Cela permettra d’ajouter Python à la variable PATH de l'ordinateur, ce qui facilitera l’exécution de Python à partir de l’invite de commande.

    > Vérifier que l'installation inclut celle de `pip`. Si ce n'est pas le cas, choisir *Personnaliser l'installation* et cocher les options souhaitées (au moins `pip`).

- Cloner localement le dossier [GitHub](https://github.com/mines-nancy/user_interface) (voir les [Tips GitHub](#tips-github)), si ce n'est pas déjà fait

- Ouvrir un terminal (invité de commande, Command Prompt ou PowerShell) **dans le dossier parent** du dossier `user_interface`

Pour vérifier que [Python](https://www.python.org/downloads/) est bien installé, entrer :

```bash
python --version
```

Cela devrait afficher la version installée.

- Installer les packages et les dépendances nécessitées par le projet :

```bash
pip install -r user_interface/requirements.txt
```

- Vérifier le bon fonctionnement, lever le serveur en exécutant le fichier `user_interface/python/backend_from_front.py` :

```bash
python ./user_interface/python/backend_from_front.py
```


# Configurations

### Backend

Entrer les adresses ip et les ports à utiliser dans les variables correspondantes dans le fichier `user_interface/python/backend_from_front.py` :

```python
# Front possible ip addresses
front_ip = [
    "localhost",
    "127.0.0.1"
]

# Front possible ports
front_ports = [
    5173
]

# Backend ip address that the front will communicate with
BACKEND_IP = "localhost"

# Backend port that the front will communicate through
BACKEND_PORT = 8001
```

# Utilisation

- Lancer le backend depuis le dossier parent de `user_interface` :

```bash
python ./user_interface/python/backend_from_front.py
```

- Devraient apparaître les lignes suivantes :

```bash
INFO:     Started server process [70677]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://localhost:8001 (Press CTRL+C to quit)
```

Avec à la place de `localhost` l'adresse ip, et à la place de `8001` le port, choisis et configurés à l'[étape précédente](#configurations).

*Note : L'application correspondant au backend tourne alors à l'adresse http indiquée. Pour ouvrir l'application dans son moteur de recherche, entrer l'adresse indiquée ou cliquer sur le lien donné en maintenant CTRL. Il est alors possible de tester les requêtes **get** prévues par le backend. Pour tester les autres requêtes, comme POST par exemple, utiliser un outil de test comme [Postman](https://www.postman.com/).*


- Lancer le frontend depuis le dossier `user_interface` :

```bash
npm run dev

# ou pour lever le serveur en ouvrant directement l'application dans un onglet du moteur de recherche
npm run dev -- --open
```

- Devraient apparaître les lignes suivantes :

```bash
> user-interface@0.0.1 dev
> vite dev


  VITE v5.4.11  ready in 26269 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

Avec à la place de `localhost` l'adresse ip, et à la place de `5173` le port, choisis et configurés à l'[étape précédente](#configurations).

- Ouvrir l'application dans son moteur de recherche, entrer l'adresse indiquée ou cliquer sur le lien donné en maintenant CTRL

L'interface peut mettre du temps à se charger. Une fois affichée, utiliser le clavier ou une manette (fonctionnalité à venir) pour manoeuvrer le robot, et la souris pour sélectionner les modules placés sur l'Omnibot et afficher leurs informations.


# Tips GitHub

- Installer [Git](https://git-scm.com/)

- Se connecter en entrant dans un terminal (invité de commande, Command Prompt ou PowerShell) :

```bash
git config --global user.name "<Your git account user name>"
git config --global user.email "<Your git account email>"
```

### Cloner un repository

Dans un terminal (invité de commande, Command Prompt ou PowerShell) ouvert depuis le dossier local où le repository sera téléchargé :

```bash
git clone "<adresse http du repository>"

# Exemple pour le dossier user_interface
git clone https://github.com/mines-nancy/user_interface
```