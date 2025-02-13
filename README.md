# L'interface utilisateur de l'Omnibot

L'interface permet à tout utilisateur de contrôler le robot [Omnibot](https://wiki.techlab-mines-nancy.fr/en/Robotique/Robots/Omnibot/Omnibot) du TechLab à distance, de récolter, afficher et enregistrer les données mesurées par les différents modules connectés.

Pour plus d'informations, voir le [Wiki du TechLab](https://wiki.techlab-mines-nancy.fr/en/Robotique/Robots/Omnibot/Informatique/Interface/interface_utilisateur).


<p align="center">
    <img src="./static/full.gif" widtj="70%">
</p>

# Sommaire

- [Installation](#installation)
    - [Frontend - Svelte](#frontend---svelte)
    - [Backend - Python](#backend---python)
- [Configurations](#configurations)
    - [Backend](#backend)
    - [Frontend](#frontend)
- [Utilisation](#utilisation)
- [Tips terminal & GitHub](#tips-github)
    - [Terminal](#se-déplacer-de-dossier-en-dossier-dans-le-terminal-command-prompt-ou-powershell)
        - [Se déplacer dans le terminal](#se-déplacer-de-dossier-en-dossier-dans-le-terminal-command-prompt-ou-powershell)
    - [Installer et configurer Git](#installer-et-configurer-git)
    - [Cloner un repository](#cloner-un-repository)
    - [S'informer sur le statut du repository](#sinformer-sur-le-statut-du-repository)
    - [Gitignore](#gitignore)
    - [Mettre à jour un repository local](#mettre-à-jour-un-repository-local)
    - [Afficher les branches locales existantes et en créer une](#afficher-les-branches-locales-existantes-et-en-créer-une)
    - [Se déplacer sur une branche](#se-déplacer-sur-une-branche)
    - [Synchroniser des changements (fichiers créés et modifiés)](#synchroniser-des-changements-fichiers-créés-et-modifiés)
    - [Fusionner des branches](#fusionner-des-branches)



# Installation

*Note : Le dossier `user_interface` contient l'ensemble de l'interface. Le frontend en [Svelte](https://svelte.dev/docs/svelte/overview) (dossier `src`) à exécuter grâce à [Node.Js](https://nodejs.org/fr) et le backend en [Python](https://docs.python.org/fr/3.13/using/index.html) (dossier `python`) à exécuter grâce à [Python](https://www.python.org/downloads/). Il n'est pas nécessaire d'exécuter ces deux parties depuis le même dossier/environnement/ordinateur. **Cependant, il faut que le front, le back et le robot soient connectés sur le même réseau wifi**. Attention à bien modifier les adresses ip des requêtes envoyées (voir [Configurations](#configurations)).*


## Frontend - Svelte

- Installer [Node.Js](https://nodejs.org/fr)
    
    - **IMPORTANT :**

    > Vérifier que la case « Ajouter Node.Js et npm au PATH » est cochée avant de procéder à l’installation. Cela permettra d’ajouter Node à la variable PATH de l'ordinateur. Ainsi lorsque l'on souhaite exécuter Node depuis un invité de commande, on peut utiliser Node depuis n'importe quel dossier sans avoir à spécifier le chemin d'accès de son exécutable. En tapant simplement `node`, la variable globale PATH permet d'interpréter le chemin d'accès à utiliser.


- Cloner localement le dossier [GitHub](https://github.com/mines-nancy/user_interface) (voir les [Tips GitHub](#tips-github))

- Ouvrir un terminal (Command Prompt ou PowerShell) à la racine du dossier `user_interface`

Pour vérifier que [Node.Js](https://nodejs.org/fr) est bien installé, entrer :

```bash
node -v
npm -v
```

Cela devrait afficher les versions installées. Si ce n'est pas le cas, vérifier dans les variables d'environnement de Windows si la variable PATH contient bien un chemin d'accès à l'exécutable de Node (compilateur qui servira à exécuter les fichiers Svelte ou JavaScripts par exemple). Si ce n'est pas le cas, l'ajouter. Il est parfois nécessaire de fermer et recharger une fenêtre VS Code pour actualiser l'utilisation des variables globales comme PATH.

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

    > Cocher la case « Ajouter Python 3.x au PATH » avant de procéder à l’installation. Cela permettra d’ajouter Python à la variable PATH de l'ordinateur, ce qui facilitera l’exécution de Python à partir de l’invite de commande de la même manière que pour Node.

    > Vérifier que l'installation inclut celle de `pip`. Si ce n'est pas le cas, choisir *Personnaliser l'installation* et cocher les options souhaitées (au moins `pip`).

- Cloner localement le dossier [GitHub](https://github.com/mines-nancy/user_interface) (voir les [Tips GitHub](#tips-github)), si ce n'est pas déjà fait

- Ouvrir un terminal (Command Prompt ou PowerShell) **dans le dossier parent** du dossier `user_interface`

Pour vérifier que [Python](https://www.python.org/downloads/) est bien installé, entrer :

```bash
python --version
```

Cela devrait afficher la version installée. De la même manière, vérifier que la variable globale PATH contient bien un chemin d'accès à l'exécutable Python (compilateur qui servira à exécuter les fichiers .py).

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

- Entrer les adresses ip et les ports à utiliser pour ***se connecter au robot*** dans les variables correspondantes dans le fichier `user_interface/python/backend_from_front.py` :

```python
# Robot ip address that the backend will communicate with
ROBOT_IP = "192.168.50.153"

# Robot port that the backend will communicate through
ROBOT_PORT = 6550
```

- Entrer les adresses ip et les ports à utiliser pour le ***backend*** dans les variables correspondantes dans le fichier `user_interface/python/backend_from_front.py` :

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


### Frontend

- Entrer les adresses ip et les ports à utiliser pour le ***front*** dans les variables correspondantes (port et host pour le server) dans le fichier `user_interface/vite.config.js` :

```js
// See https://vite.dev/config/server-options.html for more options
export default defineConfig({
	plugins: [sveltekit()],
	server: { 				// Options for npm run dev
		port: 5173,				// default = 5173
		strictPort: true,		// true = fail if port is already in use, false = run server on next available port
		host: 'localhost',		// default = 'localhost'
	},
	preview: { 				// Options for npm run preview (after npm run build)
		port: 4173,				// default = 4173
		strictPort: true,		// true = fail if port is already in use, false = run server on next available port
	}
});
```

- Entrer les adresses ip et les ports à utiliser pour le ***back*** dans les variables correspondantes dans le fichier `user_interface/src/config.js` :

```js
export const backend_host = "localhost";
export const backend_port = 8001;
```


# Utilisation

- Lancer le backend depuis le dossier ***parent*** de `user_interface` :

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

### Se déplacer de dossier en dossier dans le terminal (Command Prompt ou PowerShell)

*(universel, ces commandes ne sont pas liées à Git)*

```bash
# Afficher la liste des fichiers et dossiers enfants (dans le dossier actuel)
# Pour un bash / terminal sur Linux ou Ubuntu
ls
# Pour un Command Prompt ou PowerShell / terminal sur Windows
dir

# Pour afficher le chemin du dossier actuel
# Pour un bash / terminal sur Linux ou Ubuntu, ou pour Windows PowerShell
pwd
# Pour Windows Command Prompt
cd

# Se déplacer dans un dossier enfant
cd "<nom d'un dossier enfant>"

# Se déplacer dans le dossier parent
cd ..

# Se déplacer dans un dossier grâce à son chemin d'accès complet
cd "<chemin d'accès du dossier>"

# Créer un nouveau dossier
mkdir "<nom du nouveau dossier>"
```

## Installer et configurer Git

- Installer [Git](https://git-scm.com/)

- Se connecter en entrant dans un terminal (Command Prompt ou PowerShell) :

```bash
git config --global user.name "<Your git account user name>"
git config --global user.email "<Your git account email>"
```

## Cloner un repository

Dans un terminal (Command Prompt ou PowerShell) ouvert depuis le dossier local où le repository sera téléchargé :

```bash
git clone "<adresse http du repository>"

# Exemple pour le dossier user_interface
git clone https://github.com/mines-nancy/user_interface
```

## S'informer sur le statut du repository

Dans un terminal (Command Prompt ou PowerShell) ouvert depuis le dossier où le repository a été téléchargé :

```bash
git status
```

## Gitignore

Le fichier `.gitignore` permet de spécifier des fichiers ou dossiers locaux à ne pas synchroniser avec la version remote du repository. Il est toujours mieux d'ajouter les dossiers contenant les librairies ou packages (comme node_modules) au gitignore, car ces dossiers prennent beaucoup de place et peuvent empêcher le bon fonctionnement du repository. De plus, les librairies et packages sont regénérées à chaque `npm install` ou `pip install`, donc à chaque initialisation du projet.

## Mettre à jour un repository local

Dans un terminal (Command Prompt ou PowerShell) ouvert depuis le dossier où le repository a été téléchargé :

```bash
git pull
```

## Afficher les branches locales existantes et en créer une

Dans un terminal (Command Prompt ou PowerShell) ouvert depuis le dossier où le repository a été téléchargé :

```bash
git branch #Consulter les branches
git branch <nouvelle branche> #Créer une branche
git checkout <nouvelle branche> #Se deplacer sur une branche
```

***IMPORTANT : Penser à toujours se déplacer sur la branche créée avant de commencer à apporter des modifications au code !***

## Se déplacer sur une branche

Dans un terminal (Command Prompt ou PowerShell) ouvert depuis le dossier où le repository a été téléchargé :


```bash
git checkout <autre branche>
```

***Attention*** *si le dossier local n'est pas à jour par rapport au dossier remote sur la branche actuelle, il peut y avoir des conflits qui empechent le changement de branche.*

*Si conflits: bien vérifier qu'il n y a pas de changements latents (pending changes, staged changes, ...) et que tous les commit ont été push. Le dossier local doit être synchronisé avec le dossier remote. Si besoin, pour forcer le changement de branche, utiliser `git stash` qui met les changements latents de côté et permet de revenir à la version synchronisée avec le dossier remote avant de changer de branche.*

## Synchroniser des changements (fichiers créés et modifiés)

= Ajouter des fichiers créés ou modifiés à la liste des changements qui seront synchronisés lors du commit

Dans un terminal (Command Prompt ou PowerShell) ouvert depuis le dossier où le repository a été téléchargé :

```bash
git add <fichiers à sauvegarder>
git add * #sauvegarde tous les fichiers
git commit -m "Description des changements apportés"  
# -m permet d'indiquer que ce qui suit est le message de description accompagnant un commit. Il est obligatoire
```

*Tant que des commits n'ont pas été envoyés en remote, ils ne sont pas effectifs et il est possible de les annuler (voir la fonction Undo Last Commit proposée par VS Code).*

***Pour que des changements soient entièrement synchronisés, il ne faut pas oublier le `git push` ! Celui-ci permet d'envoyer l'ensemble des derniers commits en remote et de rendre effective la synchronisation.***

Dans un terminal (Command Prompt ou PowerShell) ouvert depuis le dossier où le repository a été téléchargé :

```bash
git push
```

Une fois la synchronisation terminée, on peut vérifier l'état des lieux avec `git status`.


## Fusionner des branches

**IMPORTANT**

Usuellement, la branche principale (`main` ou parfois `master`) est gardée la plus propre et fonctionnelle possible. Dès que l'on veut travailler sur une modification ou l'ajout d'une feature, ou simplement dès que l'on est plusieurs à travailler sur un même projet, il est très conseillé de se créer une branche depuis la branche `main`, travailler dessus jusqu'à la fin des modifications, puis de fusionner sa branche avec la branche `main`.

Il peut être utilse de d'abord incorporer la branche `main` sur sa branche de développement -- notamment dans le cas où la branche `main` aurait subi des modifications ou d'autres fusions entre temps -- afin de tester la fusion et vérifier l'état fonctionnel du projet une fois la fusion réalisée.



Dans un terminal (Command Prompt ou PowerShell) ouvert depuis le dossier où le repository a été téléchargé :

**L'opération `git merge <branche a incorporer` se fait TOUJOURS depuis la branche d'arrivée, celle qui sera le résultat de la fusion.**

```bash
git checkout <branche d arrivee>
git merge <branche a incorporer>
```

Donc pour effectuer un merge d'abord sur sa branche de développement puis envoyer le résultat sur `main` (nécessaire seulement si `main` a subi des modifications depuis la création de la branche de développement) :

- Se déplacer sur sa branche
- Effectuer la fusion en incorporant `main` dans sa branche de travail

```bash
git checkout <branche de dev>
git merge main #ou master selon le nom de la branche principale
```

- Vérifier le résultat de la fusion (parfois il est demander de gérer des conflits de fusion. Utiliser `git status` et/ou l'outil intégré dans VS Code qui permet de gérer ses conflits via le Merge Conflicts Editor)

Une fois le résultat validé :

- Se déplacer sur la branche principale
- Effectuer la fusion
- Vérifier le résultat
- Supprimer la branche de développement (optionnel)

```bash
git checkout main #ou master
git merge <branche de dev>
git branch -d <branche de dev>
```