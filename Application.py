import random

# Classe para instanciar novos Pokemons
class Pokemon:
    def __init__(self, name, health, experience, level, moves):
        self.name = name
        self.health = health
        self.experience = experience
        self.level = level
        self.moves = moves

# Classe para instanciar novos ataques para os pokemons
class Move:
    def __init__(self, name, power, accuracy, power_point):
        self.name = name
        self.power = power  # Poder do movimento
        self.accuracy = accuracy    # Taxa de acerto
        self.power_point = power_point  # Quantidade de vezes que pode ser utilizado

# Computar se o movimento é válido, caso seja, reduz
# a eficiência do mesmo, evitando uso abusivo.
def compute_move(move):
    # Não é mais um movimento válido
    if move.power_point == 0:
        return False
    
    # Reduzir power points
    move.power_point -= 1

    # Randomizar se o ataque será válido ou não tendo acurácia como peso.
    if random.randrange(100) < move.accuracy:
        move.power *= 0.90 # Reduzir o poder do ataque em 10%
        move.accuracy *= 0.80 # Reduzir a acurácia em 20%
        return True
    
    return False

# Computar o dano em determinado Pokemon a partir de um valor de dano
def compute_damage(pokemon, move_power):
    pokemon.health -= move_power
    pokemon.health = 0 if pokemon.health < 0 else pokemon.health

    print("\nName: " + pokemon.name)
    print("HP: " + str(round(pokemon.health, 2)))
    print("\nPoor " + pokemon.name + " loses health... :[\n")

# Controla a rodada atual do jogo
def turn(local_pokemon, remote_pokemon):
    print("Your turn!\n")
    print("Name: " + local_pokemon.name)
    print("HP: " + str(round(local_pokemon.health, 2)))
    print("\nMove list:\n")

    # Printar movimentos do Pokémon da rodada atual
    for move in local_pokemon.moves:
        print(move.name + " | " + str(round(move.power, 2)) + " | " + str(round(move.accuracy, 2)) + " | " + str(move.power_point))
    
    # Escolher o movimento dentro dos disponíveis
    input_move = input("\nChoose your move! ")

    for move in local_pokemon.moves:
        if move.name == input_move:
            if compute_move(move):
                compute_damage(remote_pokemon, move.power) # Aplicar dano ao oponente
            else:
                print("\nMiss!!! You'r too slow! :]\n")
            return
    
    print("You'r a terrible trainer!")

if __name__ == "__main__":
    fire_moves = [Move("Tackle", 12.0, 100.0, 10), Move("QuickAttack", 14.0, 100.0, 7), Move("Ember", 15.0, 100.0, 7)]
    eletric_moves = [Move("Thunderbolt", 15.0, 100.0, 7), Move("QuickAttack", 14.0, 100.0, 7), Move("ThunderShock", 20.0, 100.0, 3)]
    grass_moves = [Move("Absorb", 8.0, 100.0, 10), Move("LeafBlade", 20.0, 80.0, 5), Move("Tackle", 12.0, 100.0, 10)]
    water_moves = [Move("AquaTail", 12.0, 100.0, 10), Move("Bubble", 14.0, 100.0, 7), Move("QuickAttack", 14.0, 100.0, 7)]

    pikachu = Pokemon("Pikachu", 45.0, 0, 5, eletric_moves)
    charmander = Pokemon("Charmander", 45.0, 0, 5, fire_moves)

    while (charmander.health > 0 and pikachu.health > 0):
        turn(pikachu, charmander)
        turn(charmander, pikachu)
    
    defeated_pokemon = charmander if charmander.health == 0 else pikachu

    print(defeated_pokemon.name + " has been defeated!")