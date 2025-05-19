import requests
import os
import json
import pygame
import time
from io import BytesIO
from conf import Conf
class PokemonAPI:
    def __init__(self):
        self.base_url = "https://pokeapi.co/api/v2/"
        self.pokemon_cache = {}
        self.sprites_cache = {}
        self.pokemon_dir = os.path.join(Conf.BASE_DIR, "assets", "pokemon")
        
        # Create pokemon directory if it doesn't exist
        if not os.path.exists(self.pokemon_dir):
            os.makedirs(self.pokemon_dir)
    
    def get_pokemon_list(self, limit=20):
        """Get a list of Pokemon from the PokeAPI with increased limit to 20"""
        # Check if we have cached data first
        cache_file = os.path.join(self.pokemon_dir, "pokemon_list.json")
        
        # Check if we need to update the cache
        needs_new_data = False
        
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    cached_data = json.load(f)
                    if len(cached_data) < limit:
                        needs_new_data = True
                        # Jangan menghapus file, kita akan menimpa nantinya
            except Exception as e:
                print(f"Error saat membuka cache: {e}")
                needs_new_data = True
        else:
            needs_new_data = True
        
        # Jika cache valid dan tidak perlu diupdate, gunakan cache
        if os.path.exists(cache_file) and not needs_new_data:
            try:
                with open(cache_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error membaca cache: {e}")
                needs_new_data = True
        
        # Jika perlu data baru, ambil dari API
        if needs_new_data:
            pokemon_list = self._fetch_pokemon_data_from_api(limit)
            
            # Simpan cache dengan aman
            try:
                # Buat file temporary dulu
                temp_cache_file = os.path.join(self.pokemon_dir, f"pokemon_list_temp_{int(time.time())}.json")
                with open(temp_cache_file, 'w') as f:
                    json.dump(pokemon_list, f)
                
                # Jika berhasil, coba rename ke file asli
                try:
                    # Di Windows kita perlu menghapus file lama dulu jika ada
                    if os.path.exists(cache_file):
                        try:
                            os.remove(cache_file)
                        except Exception as e:
                            print(f"Tidak bisa menghapus cache lama: {e}")
                    
                    os.rename(temp_cache_file, cache_file)
                except Exception as e:
                    print(f"Tidak bisa rename file cache: {e}")
                    # Tetap gunakan data yang sudah diambil meskipun caching gagal
            except Exception as e:
                print(f"Error menyimpan cache: {e}")
            
            return pokemon_list
    
    def _fetch_pokemon_data_from_api(self, limit):
        """Fetch fresh Pokemon data from the API"""
        url = f"{self.base_url}pokemon?limit={limit}"
        try:
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                
                # Process data to include only what we need
                pokemon_list = []
                for pokemon in data['results']:
                    # Fetch more details about each Pokemon
                    pokemon_url = pokemon['url']
                    pokemon_details = self.fetch_pokemon_details(pokemon_url)
                    
                    pokemon_id = pokemon['url'].split('/')[-2]
                    pokemon_data = {
                        'id': pokemon_id,
                        'name': pokemon['name'].capitalize(),
                        'sprite_url': f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_id}.png",
                        'type': pokemon_details.get('type', 'Unknown'),
                        'height': pokemon_details.get('height', 0),
                        'weight': pokemon_details.get('weight', 0)
                    }
                    pokemon_list.append(pokemon_data)
                
                return pokemon_list
            else:
                print(f"Error API: status code {response.status_code}")
                return []
        except Exception as e:
            print(f"Error mengambil data Pokémon: {e}")
            return []
    
    def fetch_pokemon_details(self, url):
        """Fetch additional details about a Pokemon"""
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                types = [t['type']['name'] for t in data['types']]
                
                return {
                    'type': '/'.join(types),
                    'height': data['height'] / 10,  # Convert to meters
                    'weight': data['weight'] / 10   # Convert to kg
                }
        except Exception as e:
            print(f"Error fetching Pokemon details: {e}")
        
        return {'type': 'Unknown', 'height': 0, 'weight': 0}
    
    def get_pokemon_sprite(self, pokemon_id):
        """Get a sprite for a specific Pokemon"""
        # Check if the sprite is already cached in memory
        if pokemon_id in self.sprites_cache:
            return self.sprites_cache[pokemon_id]
        
        # Check if we have the sprite file locally
        sprite_path = os.path.join(self.pokemon_dir, f"{pokemon_id}.png")
        if os.path.exists(sprite_path):
            try:
                sprite = pygame.image.load(sprite_path)
                # Scale the sprite to match the bird size (adjust as needed)
                bird_img = pygame.image.load(os.path.join(Conf.BASE_DIR, "assets", "bird.png"))
                sprite = pygame.transform.scale(sprite, bird_img.get_size())
                self.sprites_cache[pokemon_id] = sprite
                return sprite
            except Exception as e:
                print(f"Error loading cached sprite: {e}")
        
        # If not cached, fetch from the API
        sprite_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_id}.png"
        
        try:
            response = requests.get(sprite_url)
            if response.status_code == 200:
                # Coba simpan sprite secara lokal
                try:
                    with open(sprite_path, 'wb') as f:
                        f.write(response.content)
                except Exception as e:
                    print(f"Tidak bisa menyimpan sprite: {e}")
                
                # Load the sprite into pygame
                sprite = pygame.image.load(BytesIO(response.content))
                # Scale the sprite to match the bird size
                bird_img = pygame.image.load(os.path.join(Conf.BASE_DIR, "assets", "bird.png"))
                sprite = pygame.transform.scale(sprite, bird_img.get_size())
                
                # Cache it
                self.sprites_cache[pokemon_id] = sprite
                return sprite
        except Exception as e:
            print(f"Error fetching Pokemon sprite: {e}")
            
        # If all else fails, return the default bird sprite
        return pygame.image.load(os.path.join(Conf.BASE_DIR, "assets", "bird.png")) 