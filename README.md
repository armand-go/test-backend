# Test Backend Octo

Ce document a pour but d'expliquer les différents choix pris lors du développement de cette API.
Il comprend un rapide rappel des différents énoncés ainsi que les choix techniques effectué.

## Note
Parmi tous les énoncés donnés dans le [README_OLD](README_OLD.md), seul la distribution automatique des récompenses à la fin du tournoi n'a pas été implémenté.

Dans un premier temps, une tentative d'implémentation a voulu être faite avec la libraire APScheduler. Par manque de connaissance et de temps, je n'ai pu aller au développement de cette fonctionnalité asynchrone. Cependant, la function qui se charge de distribuer les récompenses a elle été implémentée et est fonctionnelle.

## Architecture
Pour développer cette API, une architecture porhce de celle utilisée chez Octo a été utilisée.
L'API a ainsi été développée avec Fast API, la BDD utilisée est PostgreSQL. La version de Python utilisée est la 3.10.4
La liste des librairies nécessaires et utilisées peut être parcouru dans le fichier [requirements.txt](requirements.txt)

## Initialisation
Pour commencer, il convient de créer un environnement avec la version de Python utilisée pour éviter les soucis de compatibilité:
`conda create -n octotest python=3.10.4`
Puis l'activer:
`conda activate octotest`

Une fois ceci fait, installer les dépendances nécessaires:
`pip install -r requirements.txt`

## Models
Trois modèles ont étés utilisés dans le développement de cette API:
- User
- Match
- Tournament

User et Match étaient donnés dans l'énoncé, mais l'implémentation est légèrement différentes :
Concernant les matchs, plutôt que de n'avori qu'une seule variable `score`, deux ont été créée, `score_one` et `score_two` qui stockeront respectivement le score du Joueur 1 et du Joueur 2. Il m'est apparu plus difficile d'implémenter des relation One-to-One entre les Matches et les Users puisque, si deux utilisateurs s'affrontent plusieurs fois,  retrouver le score final de la confrontation est plus fastidieux.
En ayant une relation One-to-Many entre les Matches et les Users, nous pouvons facielement retrouver notre objet Match avec le score des deux joueurs ainsi que le résultat final.

Quant au modèle Tournament, celui-ci a été créé afin d'interagir plus facilement entre les joueurs en fonction des résultat des matchs.
Il contient les fields suivants:
- ID
- max_player (Le nombre maximal de joueur pouvant s'inscire au tournoi)
- player_list (La liste des joueurs inscrits au tournoi)
- player_score (Le score de chacun des joueurs)
- begin (La date de début de tournoi)
- end (La date de fin de tournoi)
- rewards_sum (La somme des récompenses du tournoi)
- rewards_range (La répartition des récompenses par position dans le classement)

L'utilisation de `rewards_range` de format JSON, permet la définition rapide de récompense sur plusieurs places.
Le format de chaque paire key / value se défini ainsi: "{place_inf}-{place_sup}": reward, et les bornes supérieure et inférieure sont incluses.

Par exemple, un reward range qui distribuerait des récompenses aux 20 premiers d'un tournoi pourrait être défini de la manière suivante :
```
rewards_range = {
    "1-1": 100,
    "2-3": 50,
    "4-8": 25,
    "9-15": 10,
    "16-20": 5
    }
```
Le premier du tournoi se verrait attribuer 100 points, le 2ème et 3ème, 50 points, de la 4ème à la 8ème position 25 points etc.
`reward_sum` est calculé automatiquement en fonction de `rewards_range`.

Par ailleurs, ce modèle implémente une méthode `leaderboard` qui, quand elle est implémentée, retourne le classement du tournoi en question.

## CRUD
Pour les trois modèles définis, une application CRUD a été implémentée dans [crud.py](.crud.py).
La plupart de ces définitions sont classiques, certaines comme `get_users()` ont un comportement différent de ce qui est attendu pour respecter l'énoncé.
Par exemple, `delete_user` ne supprime pas réellement l'utilisateur mais update son nom et son numéro de téléphone pour le rendre anonyme et garder ainsi les relations qui pourraient exister.

## Routes
Un bon nombre de routes ont étés définies. 4 par modèle implémentent les fonctions CRUD et sont sensiblement les mêmes.
L'adresse `/tournaments` possède une multitude d'endpoints différents, parmi lesquels on retrouve :
- register_to_tournament() : Permet à un utilisateur de s'enregistrer à un tournoi. si l'utilisateur existe déjà dans la BDD, nous utilisons cet objet, sinon il est créé.
- initialize_match_between_users() : Initialise un match entre deux Users pour le tournoi donné.
- start_match() : Joue le match donné dans le tournoi renseigné. Le socre de chacun des joueurs est défini aléatoirement, ceci pour simplifier l'implémentation de ce test.
- result_match() : Détermine le résultat d'un match et attribue des points au gagnant dans le classement.
- end_tournament() : Clos le tournoi et distribue les recompenses aux joueurs en fonction de leur classement.
- leaderboard() : Récupère le leaderboard du tournoi passé en paramètre.
- match() : Pour le tournoi passé en paramètre, initialise, lance et calcule le resultat d'un match entre deux joueurs donnés.
