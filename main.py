from data_utils import Data_utils
import random
import string


class GeneticAlgorithm:
    def __init__(self, size_initialize_population, mutation_chance, no_improvement_generations,
                 num_of_generations) -> None:
        self.size_initialize_population = size_initialize_population
        self.data_util = Data_utils()
        self.mutation_chance = mutation_chance
        self.list_of_dicts_population = None
        self.no_improvement_generations = no_improvement_generations
        self.fitness_dict_value = {}
        self.total_fitness_value = None
        self.encrypted_text = self.data_util.get_encrypted_text()
        self.num_of_generations = num_of_generations
        self.best_fitness_all_gens = 0

    def generate_dict(self) -> dict:
        # generate one dict randomly.
        # example - {'a': 'F', 'b': 'T', 's': 'Y'...}
        output_dict = {}
        available_uppercase_letters = list(string.ascii_uppercase)
        for c in string.ascii_lowercase:
            if len(available_uppercase_letters) == 0:
                return output_dict
            uppercase_letter = random.choice(available_uppercase_letters)
            output_dict[c] = uppercase_letter
            available_uppercase_letters.remove(uppercase_letter)
        return output_dict

    def initialize_population(self, K) -> None:
        # initialize a population of size K - every dict is unique
        dicts_set = set()
        while len(dicts_set) < K:
            d = self.generate_dict()  # Generate a new dictionary until it's unique
            if len(set(d.values())) < len(d):  # Check that the values are unique
                continue
            dicts_set.add(frozenset(d.items()))
        self.list_of_dicts_population = list(dicts_set)

    def decode_sentence(self, sentence, decoding_dict):
        decoded_sentence = ""
        for c in sentence:
            if c == " ":
                decoded_sentence += " "
            if c in decoding_dict:
                decoded_sentence += decoding_dict[c].lower()
            else:
                decoded_sentence += c.lower()
        return decoded_sentence

    def fitness_one_letter(self, text: str) -> float:
        grade = 0
        for line in text.split("/n"):
            for letter in line:
                if letter not in self.data_util.get_letters_freq().keys():
                    continue
                grade += self.data_util.get_letters_freq()[letter]
        return grade

    def fitness_two_letter(self, text: str) -> float:
        grade = 0
        window = []
        for line in text.split("/n"):
            for word in line.split(" "):
                for letter in word:
                    if len(window) < 2:
                        window.append(letter)
                    else:
                        window_string = "".join(window)
                        if window_string in self.data_util.get_letters2_freq().keys():
                            grade += self.data_util.dict_letters2[window_string]
                        window.pop(0)
                        window.append(letter)
                window_string = "".join(window)
                if window_string in self.data_util.get_letters2_freq().keys():
                    grade += self.data_util.dict_letters2[window_string]
                window.clear()
        return grade

    def fitness_words(self, text: str) -> float:
        count_words = 0
        for line in text.split("/n"):
            for word in line.split(" "):
                if word.lower() in self.data_util.get_words():
                    count_words += 1
        return count_words / len(self.data_util.get_words())

    def fitness(self, dictionary) -> float:
        decoded_text = self.decode_sentence(self.encrypted_text, dictionary)
        return self.fitness_one_letter(decoded_text) + self.fitness_two_letter(decoded_text) + self.fitness_words(
            decoded_text)

    def mutation(self, offspring: dict) -> dict:
        for i in range(len(offspring.keys())):
            if random.random() < self.mutation_chance:
                # Select two random keys from the dictionary
                key1, key2 = random.sample(list(offspring.keys()), 2)
                # Swap the values associated with the keys
                offspring[key1], offspring[key2] = offspring[key2], offspring[key1]
        return offspring

    def correct_dict(self, parent: dict) -> dict:
        all_letters = set(string.ascii_lowercase)
        all_letters_upper = set(x.upper() for x in all_letters)
        mapped_letters = set(parent.values())
        unmapped_letters = list(all_letters_upper - mapped_letters)
        letters_in_use = set()
        for letter in parent:
            value = parent[letter]
            if value in letters_in_use:
                for i in range(len(unmapped_letters)):
                    if unmapped_letters[i] not in letters_in_use:
                        parent[letter] = unmapped_letters[i]
                        letters_in_use.add(unmapped_letters[i])
                        break
            else:
                letters_in_use.add(value)
        return parent

    def crossover(self, first_parent, second_parent):
        cutoff = random.choice(list(first_parent.keys()))
        output_first_parent = {}
        output_second_parent = {}
        for letter in first_parent:
            if letter <= cutoff:
                output_first_parent[letter] = first_parent[letter]
                output_second_parent[letter] = second_parent[letter]
            else:
                output_first_parent[letter] = second_parent[letter]
                output_second_parent[letter] = first_parent[letter]
        return self.correct_dict(output_first_parent), self.correct_dict(output_second_parent)

    def select(self) -> dict:
        population_size = len(self.list_of_dicts_population)
        for dictionary in self.list_of_dicts_population:
            fitness_value = self.fitness(dictionary)
            self.total_fitness_value += fitness_value
        wheel_location = random.random() * self.total_fitness_value
        index = 0
        current_sum = self.fitness(self.list_of_dicts_population[index])
        while (current_sum < wheel_location) and (index < population_size):
            index += 1
            current_sum += self.fitness(self.list_of_dicts_population[index])
        return self.list_of_dicts_population[index]

    def next_generation(self) -> set:
        best_dict_index = None
        best_fitness_score = 0
        for generation in range(self.num_of_generations):
            fitness_evaluation = sorted([(i, int(self.fitness(individual))) for i, individual in
                                         enumerate(self.list_of_dicts_population)], key=lambda x: -x[1])
            best_index, best_fitness_val = fitness_evaluation[0]
            if best_fitness_val > self.best_fitness_all_gens:
                best_dict_index = best_index
                best_fitness_score = best_fitness_val

            offspring = []
            while len(offspring) < self.size_initialize_population:
                parent1 = self.select()
                parent2 = self.select()
                child1, child2 = self.crossover(parent1, parent2)
                child1 = self.mutation(child1)
                child2 = self.mutation(child2)
                offspring.append(child1)
                offspring.append(child2)




if __name__ == '__main__':
    print("Omer Aplatony")
