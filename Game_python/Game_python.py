# Accéder à la librairie pygame
import pygame

# Caractéristiques de l'écran
SCREEN_TITLE = 'Crossy RPG'
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

# Choix des couleurs
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)

# Horloge utilisée pour mettre à jour les événements et l'affichage du jeu
clock = pygame.time.Clock()

pygame.font.init()
font = pygame.font.SysFont('comicsans', 75)


class Game:
    
    # Fréquence de rafraîchissement (équivalent au FPS)
    TICK_RATE = 60

    def __init__(self, image_path, title, width, height):
        self.title = title
        self.width = width
        self.height = height

        # Créer une fenêtre  pour afficher le jeu
        self.game_screen = pygame.display.set_mode((width, height))
        # Colorer la fenêtre de jeu
        self.game_screen.fill(WHITE_COLOR)
        # Afficher le titre du jeu dans la barre principale de la fenêtre
        pygame.display.set_caption(title)

        background_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(background_image, (width, height))

    def run_game_loop(self, level_speed):
        '''Boucle principale de jeu, exécutée une fois'''
        is_game_over = False
        did_win = False
        direction = 0

        # Création du personnage et des ennemies
        player_character = PlayerCharacter('player.png', 375, 700, 50, 50)
        enemy_0 = NonPlayerCharacter('enemy.png', 720, 600, 50, 50)
        enemy_1 = NonPlayerCharacter('enemy.png', 200, 400, 50, 50)
        enemy_2 = NonPlayerCharacter('enemy.png', 20, 200, 50, 50)
        enemies = [enemy_0, enemy_1, enemy_2]
        
        # Augmentation de la vitesse en fonction de la difficulté
        for enemy in enemies:
            enemy.SPEED *= level_speed
        treasure = GameObject('treasure.png', 375, 50, 50, 50) 
        
        # Boucle principale du jeu, utilisée pour mettre à jour toutes les composantes du jeu en cours
        while not is_game_over:

            # Une boucle pour traiter tous les événements du jeu
            for event in pygame.event.get():
                # Le jeu est quitté si un événement "quitter" est détecté
                if event.type == pygame.QUIT:
                    is_game_over = True
                # Détecter lorsqu'une touche est pressée
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        direction = 1
                    if event.key == pygame.K_DOWN:
                        direction = -1
                # Détecter lorsque  la touche est relâchée
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        direction = 0

                print(event)

            # Redessiner l'image de fond pour éviter la "trace" des précédentes positions
            self.game_screen.fill(WHITE_COLOR)
            # Mettre l'image de fond dans la fenêtre
            self.game_screen.blit(self.image, (0, 0))

            # Représenter le trésor
            treasure.draw(self.game_screen)
            
            # Mettre à jour la position du personnage
            player_character.move(direction, self.height)
            # Représenter le personnage à la nouvelle position
            player_character.draw(self.game_screen)

            # Mettre à jour la position de l'ennemi
            enemy_0.move(self.width)
            # Représenter l'ennemi à la nouvelle position
            enemy_0.draw(self.game_screen)

            # Faire apparaitre de nouveaux ennemis en fonction du niveau
            if level_speed >=  1.6:
                enemy_1.move(self.width)
                enemy_1.draw(self.game_screen)
            if level_speed >= 2:
                enemy_2.move(self.width)
                enemy_2.draw(self.game_screen)

            # Détecter la collision entre le personnage et les ennemis, ou le trésor, pour arrêter le jeu  
            for enemy in enemies:
                if player_character.detect_collision(enemy):
                    is_game_over = True
                    did_win = False
                    text = font.render('You lose ! :(', True, BLACK_COLOR)
                    self.game_screen.blit(text, (275, 350))
                    pygame.display.update()
                    clock.tick(1)
                    break
            if player_character.detect_collision(treasure):
                is_game_over = True
                did_win = True
                text = font.render('You win ! :)', True, BLACK_COLOR)
                self.game_screen.blit(text, (275, 350))
                pygame.display.update()
                clock.tick(1)
                break

            # Mettre à jour l'affichage
            pygame.display.update()
            # Actionner l'horloge pour permettre el rafraîchissement
            clock.tick(self.TICK_RATE)

        # Rappeler la boucle si victoire sinon exit
        if did_win:
            self.run_game_loop(level_speed + 0.2)
        else:
            return

class GameObject:
    '''Classe générique pour les objets manipulés dans le jeu'''

    def __init__(self, image_path, x, y, width, height):
        # Charger l'image du joueur depuis le dossier courant
        object_image = pygame.image.load(image_path)
        # Redimensionner l'image qui est petite à l'origine
        self.image = pygame.transform.scale (object_image, (width, height))
        self.x_pos = x
        self.y_pos = y
        self.width = width
        self.height = height

    def draw(self, background):
        '''Dessiner l'objet créé par dessus l'image de fond (référencé game_screen)'''
        background.blit(self.image, (self.x_pos, self.y_pos))


class PlayerCharacter(GameObject):
    '''Classe représentant un personnage contrôlé par l'utilisateur'''

    # Nombre de case dont le personnage se déplace par seconde
    SPEED = 10

    def __init__(self, image_path, x, y , width, height):
        super().__init__(image_path, x, y, width, height)

    def move(self, direction, max_height):
        '''Le personnage se déplace vers le haut si "direction" est positif et inversement'''
        if direction > 0:
            self.y_pos -= self.SPEED
        elif direction < 0:
            self.y_pos += self.SPEED
        # Être sûr que le personnage ne sortira pas du bas de l'écran
        if self.y_pos >= max_height - 50:
            self.y_pos = max_height -50


    def detect_collision(self, other_body):
        '''Retourne Faux si pas de superposition sinon Vrai'''
        if self.y_pos > other_body.y_pos + other_body.height:
            return False
        elif self.y_pos + self.height < other_body.y_pos:
            return False
        if self.x_pos > other_body.x_pos + other_body.width:
            return False
        elif self.x_pos + self.width < other_body.x_pos:
            return False
        
        return True


class NonPlayerCharacter(GameObject):
    '''Classe représentant un ennemi '''

    # Nombre de case dont le personnage se déplace par seconde
    SPEED = 5

    def __init__(self, image_path, x, y , width, height):
        super().__init__(image_path, x, y, width, height)

    def move(self, max_width):
        '''L'ennemi se déplace de gauche à droite et inversement'''
        if self.x_pos <= 5:
            self.SPEED = abs(self.SPEED)
        elif self.x_pos >= max_width - 55:
            self.SPEED = -abs(self.SPEED)
        self.x_pos += self.SPEED

# Initialiser le module pygame
pygame.init()

# Créer une instance du jeu
new_game = Game('background.png', SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)

# Lancer le jeu
new_game.run_game_loop(1)

# Quitter pygame et le programme
pygame.quit()
quit()

