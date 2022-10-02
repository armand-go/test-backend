# Test Backend

L'objectif de ce test est de vous mettre en situation de travail sur un
projet autonome proche du travail à réalisé en entreprise.
L'architecture est libre.

Le rendu attendu est un fork du repository accompagné d'un écrit
expliquant au maximum les choix fait.

## Sujet

- Nous avons besoins d'un CRUD simple afin de gérer des utilisateurs (cf [entité player](#utilisateurs))
- Nous aimerions également implémenté un système de tournois avec récompense
- Afin que le système de tournois soit intéressant, il faudrait une route d'API permettant
    d'indiqué un résultat de match.
    Pour émuler le comportement des applications in app actuelle et simplifié le projet,
    les joueurs ne jouent pas en temps réel mais contre un score déjà réaliser par l'adversaire.

### Entités

#### Utilisateurs

- ID (format libre)
- Name (alphanumeric uniquement)
- Numéro de tel
- Points (unité artificielle de monaie)

#### Matchs

- ID (format libre)
- player_id (id du joueur)
- ennemy_id (id de l'ennemie)
- result (VICTORY/DEFEAT/DRAW)
- score (INT)

### Besoins produits

#### Users

##### Inscriptions

Un utilisateurs doit pouvoir s'inscrire. A l'inscription, son nom & téléphonne sont demandés.
Ceux-ci doivent être unique et une erreur doit être retournée en cas d'erreur.
Le nom doit être composé uniquement de charactère alphanuméric et comprende entre 3 et 38 charactères.

##### List

Nous devons être capable de listé les utilisateurs inscrits.
Cette liste doit être paginée et filtrable selon le nom.

##### Delete

Un utilisateur doit pouvoir demandé la suppression de son compte.
Un compte utilisateurs n'est pas complétement supprimé mais anonymisé
afin de conserver les liens potentiels.

#### Tournois

##### Setup

Il doit être possible de créer un nouveau tournois.
Celui-ci doit contenir les informations suivantes:

- Date de début
- Date de fin
- Somme de récompenses (entière, unité artificielle)
- Répartitions des récompenses par position dans le classement

##### Edit

Tant qu'un tournois n'est pas commencé, il doit pouvoir être éditer.
L'intégralité des informations de réglages doivent être modifiable.

##### Fin

A la date de fin, un tournois doit être définitevement clos et les récompenses
doivent être distribué aux joueurs.

#### Results

Un utilisateurs doit pouvoir indiqué le résultat d'un match (cf [entité matchs](#matchs)).
