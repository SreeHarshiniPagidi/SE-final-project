import pygame
import pygame_gui
import os
import random
import itertools
import json


class Tile(pygame.sprite.Sprite):
    """Implementation of the tile sprite class"""

    def __init__(self, x, y, game):
        """Init the tile image"""
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("sprites", "Grass_Tile.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (
            game.tile_size * x + game.tile_size / 2, game.tile_size * y + game.tile_size / 2 + game.menu_height)


class Bush(pygame.sprite.Sprite):
    """Implementation of the bush sprite class"""

    def __init__(self, x, y, game):
        """Init the bush image according to the map"""
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("sprites", f"Bush_0{game.map[y][x]}.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (
            game.tile_size * x + game.tile_size / 2, game.tile_size * y + game.tile_size / 2 + game.menu_height)


class Player(pygame.sprite.Sprite):
    """Implementation of the player sprite class"""

    def __init__(self, x, y, idx, game):
        """Init the player sprite"""
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("sprites", f"{idx}.png"))
        self.rect = self.image.get_rect()
        self.idx = idx
        self.game = game
        self.rect.center = (self.game.tile_size * x + self.game.tile_size / 2,
                            self.game.tile_size * y + self.game.tile_size / 2 + self.game.menu_height)
        self.move_count = 0

    def update(self):
        """Random move player on every update"""
        old_x = self.rect.x
        old_y = self.rect.y
        self.rect.x += (self.game.tile_size * random.randint(-1, 1))
        self.rect.y += (self.game.tile_size * random.randint(-1, 1))
        self.rect.x = 0 if self.rect.x < 0 else (self.game.width - self.game.tile_size) if self.rect.x > (
                self.game.width - self.game.tile_size) else self.rect.x
        self.rect.y = self.game.menu_height if self.rect.y < self.game.menu_height else (
                self.game.height - self.game.tile_size) if self.rect.y > (
                self.game.height - self.game.tile_size) else self.rect.y

        if self.rect.x != old_x or self.rect.y != old_y:
            self.move_count += 1


class WanderGame:
    """Implementation of the game class"""

    def __init__(self):
        # Set preferences
        self.tile_size = 64
        self.width_tiles = 5
        self.height_tiles = 5
        self.menu_height = 200
        self.fps = 30
        # Calculate the window size
        self.width = self.width_tiles * self.tile_size
        self.height = self.height_tiles * self.tile_size + self.menu_height
        # Make a map for different sprites of bushes
        self.map = [[random.randint(1, 4) for _ in range(self.width_tiles)] for _ in range(self.height_tiles)]
        # Init the game and create a window
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Wandering in the woods")
        self.clock = pygame.time.Clock()
        # Init a manager for pygame_gui elements
        self.manager = pygame_gui.UIManager((self.width, self.height))
        # Make flags for the app running and for the game playing
        self.running = True
        self.game_play = False
        # Create groups of tiles
        self.tile_sprites = pygame.sprite.Group()
        self.bush_sprites = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        # Draw interface
        pygame_gui.elements.ui_label.UILabel(relative_rect=pygame.Rect(10, 10, 60, 30), text='Width:',
                                             manager=self.manager)
        self.width_input = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(
            relative_rect=pygame.Rect(70, 10, 40, 40),
            manager=self.manager)
        self.width_input.set_text(str(self.width_tiles))
        pygame_gui.elements.ui_label.UILabel(relative_rect=pygame.Rect(10, 40, 60, 30), text='Height:',
                                             manager=self.manager)
        self.height_input = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(
            relative_rect=pygame.Rect(70, 40, 40, 40),
            manager=self.manager)
        self.height_input.set_text(str(self.height_tiles))

        self.start_button = pygame_gui.elements.ui_button.UIButton(relative_rect=pygame.Rect(115, 10, 60, 60),
                                                                   text='Start',
                                                                   manager=self.manager)
        pygame_gui.elements.ui_label.UILabel(relative_rect=pygame.Rect(10, 70, 30, 30), text='P1:',
                                             manager=self.manager)
        self.x1 = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(
            relative_rect=pygame.Rect(40, 70, 40, 40),
            manager=self.manager)
        self.x1.set_text('0')
        self.y1 = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(
            relative_rect=pygame.Rect(80, 70, 40, 40),
            manager=self.manager)
        self.y1.set_text('0')
        pygame_gui.elements.ui_label.UILabel(relative_rect=pygame.Rect(10, 100, 30, 30), text='P2:',
                                             manager=self.manager)
        self.x2 = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(
            relative_rect=pygame.Rect(40, 100, 40, 40),
            manager=self.manager)
        self.x2.set_text(str(self.width_tiles - 1))
        self.y2 = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(
            relative_rect=pygame.Rect(80, 100, 40, 40),
            manager=self.manager)
        self.y2.set_text(str(self.height_tiles - 1))
        pygame_gui.elements.ui_label.UILabel(relative_rect=pygame.Rect(10, 130, 30, 30), text='P3:',
                                             manager=self.manager)
        self.x3 = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(
            relative_rect=pygame.Rect(40, 130, 40, 40),
            manager=self.manager)
        self.y3 = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(
            relative_rect=pygame.Rect(80, 130, 40, 40),
            manager=self.manager)
        pygame_gui.elements.ui_label.UILabel(relative_rect=pygame.Rect(10, 160, 30, 30), text='P4:',
                                             manager=self.manager)
        self.x4 = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(
            relative_rect=pygame.Rect(40, 160, 40, 40),
            manager=self.manager)
        self.y4 = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(
            relative_rect=pygame.Rect(80, 160, 40, 40),
            manager=self.manager)
        # Draw tiles
        self.update_tiles()
        # Set frame counter
        self.frame = 0
        # Init the statistics
        self.stat = {'avg': 0, 'num': 0, 'games': []}
        self.stattext = None

    def start_button_click(self):
        """Init a new round for a game"""
        # Don't do anything while game playing
        if self.game_play:
            return
        # Clear the stat textbox
        if self.stattext:
            self.stattext.kill()
            self.stattext = None
        self.stat = {'avg': 0, 'num': 0, 'games': []}
        # Delete players
        for p in self.players:
            p.kill()
        # Recalculate the field
        self.width_tiles = int(self.width_input.get_text())
        self.height_tiles = int(self.height_input.get_text())
        self.width = self.width_tiles * self.tile_size
        self.height = self.height_tiles * self.tile_size + self.menu_height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.update_tiles()
        # Add players
        x = self.x1.get_text()
        y = self.y1.get_text()
        if x and y:
            self.players.add(Player(int(x), int(y), 1, self))
        x = self.x2.get_text()
        y = self.y2.get_text()
        if x and y:
            self.players.add(Player(int(x), int(y), 2, self))
        x = self.x3.get_text()
        y = self.y3.get_text()
        if x and y:
            self.players.add(Player(int(x), int(y), 3, self))
        x = self.x4.get_text()
        y = self.y4.get_text()
        if x and y:
            self.players.add(Player(int(x), int(y), 4, self))
        self.game_play = True

    def update_tiles(self):
        """Readd and redraw background tiles"""
        for tile in self.tile_sprites:
            tile.kill()
        for tile in self.bush_sprites:
            tile.kill()
        self.map = [[random.randint(1, 4) for _ in range(self.width_tiles)] for _ in range(self.height_tiles)]

        for j in range(self.width_tiles):
            for i in range(self.height_tiles):
                tile = Tile(j, i, self)
                self.tile_sprites.add(tile)

        for j in range(self.width_tiles):
            for i in range(self.height_tiles):
                tile = Bush(j, i, self)
                self.bush_sprites.add(tile)

    def check_win(self):
        """Return a tuple of players have been met indexes or False if there is no such players"""
        if len(self.players) < 2:
            return False
        for p1, p2 in itertools.permutations(self.players, 2):
            if p1.rect.x == p2.rect.x and p1.rect.y == p2.rect.y:
                return p1.idx, p2.idx
        return False

    def load_stat(self):
        """Load statistics file"""
        filename = f"w{self.width_tiles}-h{self.height_tiles}-p{len(self.players)}.stat"
        if not os.path.exists(os.path.join('stat', filename)):
            return None
        try:
            with open(os.path.join('stat', filename), 'r') as f:
                return json.load(f)
        except json.decoder.JSONDecodeError:
            print(f"Incorrect statistics file {filename}!")
            return None

    def save_stat(self):
        """Save statistics"""
        filename = f"w{self.width_tiles}-h{self.height_tiles}-p{len(self.players)}.stat"
        try:
            with open(os.path.join('stat', filename), 'w+') as f:
                json.dump(self.stat, f)
        except:
            print("Can't save statistics!")

    def print_stats(self):
        """Print game statistics"""
        # Update stats
        moves = max(p.move_count for p in self.players)
        self.stat = self.load_stat() or self.stat
        self.stat['avg'] = (self.stat['num'] * self.stat['avg'] + moves) / (self.stat['num'] + 1)
        self.stat['num'] += 1
        self.stat['games'].append(moves)
        self.stat['games'] = sorted(self.stat['games'])[:5]
        self.save_stat()
        # Make text
        text = "Game statistics:<br>"
        i, j = self.check_win()
        text += f"Player {i} and player {j}<br>have met in {moves} moves!<br>"
        text += f"Average moves to meet: {round(self.stat['avg'], 1)}<br>"
        text += f"Number of games: {self.stat['num']}<br>"
        text += "Game records:<br>"
        for i, m in enumerate(self.stat['games']):
            text += f"{i + 1}. {m}<br>"
        # Create textbox
        self.stattext = pygame_gui.elements.ui_text_box.UITextBox(relative_rect=pygame.Rect(0, self.menu_height,
                                                                                            self.width_tiles * self.tile_size,
                                                                                            self.height_tiles * self.tile_size),
                                                                  html_text=text,
                                                                  manager=self.manager)

    def main_cycle(self):
        """Main game cycle"""
        self.frame += 1
        # check if the start button was clicked
        if self.start_button.check_pressed():
            self.start_button_click()
            pygame.mixer.music.load(os.path.join('audio', 'game.mp3'))
            pygame.mixer.music.play(-1, 0.0)
        time_delta = self.clock.tick(self.fps) / 1000.0
        self.clock.tick(self.fps)
        # process the events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.manager.process_events(event)
        # check if game is ended
        if self.game_play and self.check_win():
            pygame.mixer.music.load(os.path.join('audio', 'win.wav'))
            pygame.mixer.music.play()
            self.game_play = False
            self.print_stats()
        # update all the sprites
        self.manager.update(time_delta)
        self.tile_sprites.update()
        self.tile_sprites.draw(self.screen)
        self.bush_sprites.update()
        self.bush_sprites.draw(self.screen)
        self.players.draw(self.screen)
        if self.game_play and self.frame > 10:
            self.players.update()
            self.frame = 0
        self.manager.draw_ui(self.screen)
        # redraw the screen
        pygame.display.flip()


if __name__ == '__main__':
    game = WanderGame()
    while game.running:
        game.main_cycle()
