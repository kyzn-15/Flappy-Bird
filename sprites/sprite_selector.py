import pygame
import os
from conf import Conf
from pokemon_api import PokemonAPI
from database import Database

class SpriteSelector:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.screen_rect = game.screen_rect
        self.font = pygame.font.Font(None, 26)
        self.title_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 20)
        
        # Tambahkan penanganan error untuk loading
        self.loading_text = "Loading Pokemon data..."
        self.is_loading = True
        self.loading_error = False
        
        # Inisialisasi daftar kosong untuk sprites dan pokemon
        self.sprites = []
        self.pokemon_list = []
        
        # Variabel untuk animasi tombol
        self.blink_counter = 0
        self.blink_state = True
        
        # Setup tombol dengan ukuran yang lebih besar
        self.setup_buttons_initial()
        
        # Mulai proses loading secara bertahap
        self.load_pokemon_data()
    
    def setup_buttons_initial(self):
        """Setup initial buttons for loading/error screens"""
        # Tombol back yang lebih besar dan lebih menonjol
        button_width = 150
        button_height = 50
        
        self.back_button_rect = pygame.Rect(
            self.screen_rect.width // 2 - button_width // 2,
            self.screen_rect.height // 2 + 200,
            button_width,
            button_height
        )
    
    def load_pokemon_data(self):
        """Load Pokemon data with error handling"""
        try:
            self.pokemon_api = PokemonAPI()
            self.database = Database()
            
            # Get the Pokemon list from the API with larger limit (20)
            self.pokemon_list = self.pokemon_api.get_pokemon_list(limit=20)
            
            # Add default Flappy Bird to the list
            self.pokemon_list.insert(0, {
                'id': 'bird',
                'name': 'Flappy Bird',
                'sprite_url': 'bird.png',
                'type': 'Bird',
                'height': 0.3,
                'weight': 0.2
            })
            
            # Get current sprite selection
            self.selected_sprite_path, self.selected_sprite_name = self.database.get_selected_sprite()
            
            # Determine the selected index based on the sprite name
            self.selected_index = 0
            for i, pokemon in enumerate(self.pokemon_list):
                if pokemon['name'] == self.selected_sprite_name:
                    self.selected_index = i
                    break
            
            # Load sprites
            self.sprites = []
            for pokemon in self.pokemon_list:
                try:
                    if pokemon['id'] == 'bird':
                        # Load the default bird sprite
                        sprite = pygame.image.load(os.path.join(Conf.BASE_DIR, "assets", "bird.png"))
                    else:
                        # Load the Pokemon sprite
                        sprite = self.pokemon_api.get_pokemon_sprite(pokemon['id'])
                    
                    self.sprites.append({
                        'id': pokemon['id'],
                        'name': pokemon['name'],
                        'image': sprite,
                        'type': pokemon.get('type', 'Unknown'),
                        'height': pokemon.get('height', 0),
                        'weight': pokemon.get('weight', 0)
                    })
                except Exception as e:
                    print(f"Error loading sprite for {pokemon['name']}: {e}")
                    # Load the default bird sprite sebagai fallback
                    default_sprite = pygame.image.load(os.path.join(Conf.BASE_DIR, "assets", "bird.png"))
                    self.sprites.append({
                        'id': pokemon['id'],
                        'name': pokemon['name'] + " (error)",
                        'image': default_sprite,
                        'type': pokemon.get('type', 'Unknown'),
                        'height': pokemon.get('height', 0),
                        'weight': pokemon.get('weight', 0)
                    })
            
            # Set up navigation buttons
            self.setup_buttons()
            
            # Selesai loading
            self.is_loading = False
            
        except Exception as e:
            print(f"Terjadi kesalahan saat memuat data Pokemon: {e}")
            self.loading_error = True
            self.is_loading = False
            
            # Tambahkan default bird jika terjadi error
            try:
                default_sprite = pygame.image.load(os.path.join(Conf.BASE_DIR, "assets", "bird.png"))
                self.pokemon_list = [{
                    'id': 'bird',
                    'name': 'Flappy Bird',
                    'sprite_url': 'bird.png',
                    'type': 'Bird',
                    'height': 0.3,
                    'weight': 0.2
                }]
                self.sprites = [{
                    'id': 'bird',
                    'name': 'Flappy Bird',
                    'image': default_sprite,
                    'type': 'Bird',
                    'height': 0.3,
                    'weight': 0.2
                }]
                self.selected_index = 0
                self.setup_buttons()
            except Exception as e:
                print(f"Gagal memuat sprite default: {e}")
    
    def setup_buttons(self):
        """Setup the navigation buttons with larger, more visible sizes"""
        # Tombol Previous dan Next lebih besar dan menonjol
        nav_button_width = 150
        nav_button_height = 50
        
        # Tombol Previous dengan warna merah
        self.prev_button_rect = pygame.Rect(
            self.screen_rect.width // 4 - nav_button_width // 2,
            self.screen_rect.height // 2 + 100,
            nav_button_width,
            nav_button_height
        )
        
        # Tombol Next dengan warna hijau
        self.next_button_rect = pygame.Rect(
            3 * self.screen_rect.width // 4 - nav_button_width // 2,
            self.screen_rect.height // 2 + 100,
            nav_button_width,
            nav_button_height
        )
        
        # Tombol Select yang lebih besar dan mencolok
        select_button_width = 200
        select_button_height = 60
        
        self.select_button_rect = pygame.Rect(
            self.screen_rect.width // 2 - select_button_width // 2,
            self.screen_rect.height // 2 + 170,
            select_button_width,
            select_button_height
        )
        
        # Tombol Back yang lebih kecil
        back_button_width = 150
        back_button_height = 50
        
        self.back_button_rect = pygame.Rect(
            self.screen_rect.width // 2 - back_button_width // 2,
            self.screen_rect.height // 2 + 250,
            back_button_width,
            back_button_height
        )
    
    def show(self):
        # Aktualisasi counter untuk animasi berkedip
        self.blink_counter = (self.blink_counter + 1) % 15  # Berkedip setiap 15 frame
        if self.blink_counter == 0:
            self.blink_state = not self.blink_state
        
        # Fill the background
        self.screen.fill(Conf.SCREEN_BG_COLOR)
        
        # Show loading screen if still loading
        if self.is_loading:
            self.show_loading_screen()
            return
            
        # Show error screen if there was an error
        if self.loading_error and len(self.sprites) == 0:
            self.show_error_screen()
            return
            
        # Ensure we have sprites
        if len(self.sprites) == 0:
            self.show_error_screen("No Pokemon data available")
            return
        
        # Draw title
        title_text = "SELECT YOUR POKEMON CHARACTER"
        title_surface = self.title_font.render(title_text, True, (255, 255, 0))
        title_rect = title_surface.get_rect(center=(self.screen_rect.width // 2, 30))
        self.screen.blit(title_surface, title_rect)
        
        # Draw page info
        page_info = f"Pokemon {self.selected_index+1}/{len(self.sprites)}"
        page_surface = self.font.render(page_info, True, (200, 200, 200))
        page_rect = page_surface.get_rect(center=(self.screen_rect.width // 2, 60))
        self.screen.blit(page_surface, page_rect)
        
        # Draw the current sprite with enlarged size
        current_sprite = self.sprites[self.selected_index]['image']
        # Make sprite bigger (scale by 3x)
        scaled_sprite = pygame.transform.scale(current_sprite, 
                                            (current_sprite.get_width() * 3, 
                                            current_sprite.get_height() * 3))
        sprite_rect = scaled_sprite.get_rect(center=(self.screen_rect.width // 2, self.screen_rect.height // 2 - 60))
        
        # Draw decorative background for the sprite
        pygame.draw.circle(self.screen, (70, 30, 180), sprite_rect.center, max(sprite_rect.width, sprite_rect.height) // 1.5)
        
        # Redraw the sprite on top of the background
        self.screen.blit(scaled_sprite, sprite_rect)
        
        # Draw the sprite name with highlighting
        name_text = self.sprites[self.selected_index]['name']
        
        # Draw name with shadow effect
        shadow_surface = self.title_font.render(name_text, True, (30, 30, 30))
        shadow_rect = shadow_surface.get_rect(center=(self.screen_rect.width // 2 + 3, sprite_rect.bottom + 23))
        self.screen.blit(shadow_surface, shadow_rect)
        
        name_surface = self.title_font.render(name_text, True, (255, 255, 255))
        name_rect = name_surface.get_rect(center=(self.screen_rect.width // 2, sprite_rect.bottom + 20))
        self.screen.blit(name_surface, name_rect)
        
        # Draw additional information if it's a Pokemon
        if self.selected_index > 0:  # Not the default bird
            # Create info text
            pokemon_info = self.sprites[self.selected_index]
            type_text = f"Type: {pokemon_info['type']}"
            size_text = f"Height: {pokemon_info['height']}m  Weight: {pokemon_info['weight']}kg"
            
            # Render type with colored background based on type
            type_color = self.get_type_color(pokemon_info['type'])
            type_surface = self.font.render(type_text, True, (255, 255, 255))
            type_bg_rect = type_surface.get_rect(center=(self.screen_rect.width // 2, name_rect.bottom + 25))
            type_bg_rect.inflate_ip(30, 15)  # Make background a bit bigger than text
            
            pygame.draw.rect(self.screen, type_color, type_bg_rect, border_radius=15)
            self.screen.blit(type_surface, type_surface.get_rect(center=(self.screen_rect.width // 2, name_rect.bottom + 25)))
            
            # Render size info
            size_surface = self.font.render(size_text, True, (200, 200, 200))
            self.screen.blit(size_surface, size_surface.get_rect(center=(self.screen_rect.width // 2, name_rect.bottom + 60)))
        
        # Draw navigation buttons - Previous
        prev_color = (255, 50, 50)  # Red
        pygame.draw.rect(self.screen, prev_color, self.prev_button_rect, border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255), self.prev_button_rect, 3, border_radius=10)  # White border
        prev_text = self.font.render("PREVIOUS", True, (255, 255, 255))
        prev_text_rect = prev_text.get_rect(center=self.prev_button_rect.center)
        self.screen.blit(prev_text, prev_text_rect)
        
        # Draw navigation buttons - Next
        next_color = (50, 255, 50)  # Green
        pygame.draw.rect(self.screen, next_color, self.next_button_rect, border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255), self.next_button_rect, 3, border_radius=10)  # White border
        next_text = self.font.render("NEXT", True, (255, 255, 255))
        next_text_rect = next_text.get_rect(center=self.next_button_rect.center)
        self.screen.blit(next_text, next_text_rect)
        
        # Draw Select button with blinking effect
        select_color = (0, 150, 255) if self.blink_state else (0, 100, 200)  # Blinking blue
        pygame.draw.rect(self.screen, select_color, self.select_button_rect, border_radius=15)
        pygame.draw.rect(self.screen, (255, 255, 0), self.select_button_rect, 3, border_radius=15)  # Yellow border
        select_text = self.title_font.render("SELECT", True, (255, 255, 255))
        select_text_rect = select_text.get_rect(center=self.select_button_rect.center)
        self.screen.blit(select_text, select_text_rect)
        
        # Instruksi
        instruction = "Choose this Pokemon as your character"
        instruction_surface = self.small_font.render(instruction, True, (200, 200, 200))
        instruction_rect = instruction_surface.get_rect(center=(self.screen_rect.width // 2, self.select_button_rect.bottom + 10))
        self.screen.blit(instruction_surface, instruction_rect)
        
        # Draw Back button
        pygame.draw.rect(self.screen, (100, 100, 100), self.back_button_rect, border_radius=10)
        pygame.draw.rect(self.screen, (200, 200, 200), self.back_button_rect, 2, border_radius=10)  # Gray border
        back_text = self.font.render("BACK", True, (255, 255, 255))
        back_text_rect = back_text.get_rect(center=self.back_button_rect.center)
        self.screen.blit(back_text, back_text_rect)
    
    def show_loading_screen(self):
        """Show a loading screen while fetching Pokemon data"""
        loading_text = self.title_font.render(self.loading_text, True, (255, 255, 255))
        loading_rect = loading_text.get_rect(center=(self.screen_rect.width // 2, self.screen_rect.height // 2))
        self.screen.blit(loading_text, loading_rect)
        
        # Animation for loading indicator
        t = pygame.time.get_ticks() / 1000
        for i in range(3):
            alpha = (1 + pygame.math.sin(t * 5 + i * 1.5)) / 2
            color = (255, 255, 255)
            dot_size = int(8 + 4 * alpha)
            pos = (loading_rect.bottom + 30, loading_rect.centerx + i * 20 - 20)
            pygame.draw.circle(self.screen, color, pos, dot_size)
        
        # Draw back button during loading too
        pygame.draw.rect(self.screen, (100, 100, 100), self.back_button_rect, border_radius=10)
        pygame.draw.rect(self.screen, (200, 200, 200), self.back_button_rect, 2, border_radius=10)  # Gray border
        back_text = self.font.render("BACK", True, (255, 255, 255))
        back_text_rect = back_text.get_rect(center=self.back_button_rect.center)
        self.screen.blit(back_text, back_text_rect)
    
    def show_error_screen(self, error_message="Error loading Pokemon data"):
        """Show an error screen if Pokemon data could not be loaded"""
        error_text = self.title_font.render(error_message, True, (255, 50, 50))
        error_rect = error_text.get_rect(center=(self.screen_rect.width // 2, self.screen_rect.height // 2 - 50))
        self.screen.blit(error_text, error_rect)
        
        help_text = self.font.render("Try restarting the game", True, (255, 255, 255))
        help_rect = help_text.get_rect(center=(self.screen_rect.width // 2, self.screen_rect.height // 2 + 10))
        self.screen.blit(help_text, help_rect)
        
        # Draw back button
        pygame.draw.rect(self.screen, (100, 100, 100), self.back_button_rect, border_radius=10)
        pygame.draw.rect(self.screen, (200, 200, 200), self.back_button_rect, 2, border_radius=10)
        back_text = self.font.render("BACK", True, (255, 255, 255))
        back_text_rect = back_text.get_rect(center=self.back_button_rect.center)
        self.screen.blit(back_text, back_text_rect)
    
    def get_type_color(self, type_text):
        """Return a color based on Pokemon type"""
        type_colors = {
            'normal': (168, 168, 120),
            'fire': (240, 128, 48),
            'water': (104, 144, 240),
            'grass': (120, 200, 80),
            'electric': (248, 208, 48),
            'ice': (152, 216, 216),
            'fighting': (192, 48, 40),
            'poison': (160, 64, 160),
            'ground': (224, 192, 104),
            'flying': (168, 144, 240),
            'psychic': (248, 88, 136),
            'bug': (168, 184, 32),
            'rock': (184, 160, 56),
            'ghost': (112, 88, 152),
            'dragon': (112, 56, 248),
            'dark': (112, 88, 72),
            'steel': (184, 184, 208),
            'fairy': (238, 153, 172)
        }
        
        # If it's a dual type, use the first type
        primary_type = type_text.lower().split('/')[0].strip()
        
        return type_colors.get(primary_type, (120, 120, 120))  # Default gray if type not found
    
    def handle_event(self, event):
        # Selalu memeriksa tombol back saat loading
        if self.is_loading and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # Cek tombol back saat loading
            if hasattr(self, 'back_button_rect') and self.back_button_rect.collidepoint(mouse_pos):
                return "back_to_menu"
            return None
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # Check if back button was clicked (available on all screens)
            if hasattr(self, 'back_button_rect') and self.back_button_rect.collidepoint(mouse_pos):
                return "back_to_menu"
                
            # If there's an error or still loading, only the back button works
            if self.loading_error or self.is_loading or len(self.sprites) == 0:
                return None
            
            # Check if previous button was clicked
            if self.prev_button_rect.collidepoint(mouse_pos):
                self.selected_index = (self.selected_index - 1) % len(self.sprites)
                return None
            
            # Check if next button was clicked
            elif self.next_button_rect.collidepoint(mouse_pos):
                self.selected_index = (self.selected_index + 1) % len(self.sprites)
                return None
            
            # Check if select button was clicked
            elif self.select_button_rect.collidepoint(mouse_pos):
                # Save the selected sprite to the database
                sprite_id = self.sprites[self.selected_index]['id']
                sprite_name = self.sprites[self.selected_index]['name']
                
                # If it's the default bird
                if sprite_id == 'bird':
                    sprite_path = 'bird.png'
                else:
                    sprite_path = f"{sprite_id}.png"
                
                try:
                    self.database.save_selected_sprite(sprite_path, sprite_name)
                    print(f"Selected character: {sprite_name}")
                except Exception as e:
                    print(f"Error saving sprite selection: {e}")
                    # Masih lanjutkan meskipun gagal menyimpan
                    
                return "selection_complete"
        
        return None 