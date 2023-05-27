# import random
# import re
# import string
# import time
#
# from data_utils import Data_utils
#
# POPULATION_SIZE = 100
# WORDS_WEIGHT = 0.3
# SELECTED_SIZE = 15
# MUTATION_RATE = 0.1
# GENERATIONS = 300
# LOCAL_MAXIMUM = 10
# STOP_NO_CHANGE = 25
# STARTERS = 5
#
#
# class GeneticAlgorithm:
#     def __init__(self):
#         self.data_util = Data_utils()
#         self.population = self.generate_population()
#         self.encrypted_text = self.data_util.get_encrypted_text()
#         self.one_letters = self.data_util.get_letters_freq()
#         self.two_letters = self.data_util.get_letters2_freq()
#         self.words = set(self.data_util.get_words())
#         self.alphabet = [c for c in string.ascii_lowercase]
#         self.best_dict = None
#         self.best_fitness = float('-inf')
#         self.best_generation = 1
#         self.count_iters = 0
#         self.local_maximum = 0
#         self.stop = 0
#
#     def generate_population(self):
#         dicts_list = []
#         lower_case_chars = [c for c in string.ascii_lowercase]
#         upper_case_chars = [c for c in string.ascii_uppercase]
#         while len(dicts_list) < POPULATION_SIZE:
#             random.shuffle(upper_case_chars)
#             element = {lower_case_chars[i]: upper_case_chars[i] for i in range(len(lower_case_chars))}
#             dicts_list.append(element)
#         return dicts_list
#
#     def text_decoder(self, dictionary):
#         decoded_text = ""
#         for letter in self.encrypted_text:
#             decoded_text += dictionary.get(letter, letter)
#         return decoded_text
#
#     def one_letter_fitness(self, text):
#         chars = [c for c in string.ascii_lowercase]
#         one_letter_freq = {char: text.count(char) / len(text) for char in chars}
#         sum_one_letter = sum([pow(self.one_letters[char] - one_letter_freq.get(char, 0), 2) for char in chars])
#         return sum_one_letter
#
#     def two_letter_fitness(self, text):
#         chars = [c for c in string.ascii_lowercase]
#         len_text = len(text) - 1
#         two_letter_freq = {}
#         for i in range(len_text):
#             two_letter = text[i: (i + 2)]
#             if two_letter in self.two_letters:
#                 temp = int(two_letter_freq.get(two_letter, 0))
#                 two_letter_freq[two_letter] = temp + 1
#         sum_all_two_letters = sum(two_letter_freq.values())
#         two_letter_new_freq = {two_letters: val / sum_all_two_letters for two_letters, val in two_letter_freq.items()}
#         sum_two_letters = sum(
#             [pow(self.two_letters[char] - two_letter_new_freq.get(char, 0), 2) for char in self.two_letters])
#         return sum_two_letters
#
#     def words_fitness(self, text):
#         count_words = 0
#         for line in text.split("/n"):
#             for word in line.split(" "):
#                 clean_word = word.lower().rstrip(",.").rstrip()
#                 if clean_word in self.words:
#                     count_words += 1
#         return pow(count_words * WORDS_WEIGHT, 2)
#
#     def fitness(self, dictionary):
#         # text = self.text_decoder(dictionary)
#         # return self.one_letter_fitness(text) + self.two_letter_fitness(text) + self.words_fitness(text)
#         decoded_text = self.text_decoder(dictionary)
#
#         # Calculate letter frequencies for the decoded text
#         letter_frequencies = {letter: decoded_text.count(letter) / len(decoded_text) for letter in self.alphabet}
#
#         # Calculate bigram frequencies for the decoded text
#         bigram_frequencies = {}
#         for i in range(len(decoded_text) - 1):
#             bigram = decoded_text[i:i + 2]
#             if bigram in self.two_letters:
#                 bigram_frequencies[bigram] = bigram_frequencies.get(bigram, 0) + 1
#         total_bigrams = sum(bigram_frequencies.values())
#         bigram_frequencies = {bigram: count / total_bigrams for bigram, count in bigram_frequencies.items()}
#
#         # Calculate fitness as the sum of the squared differences between the observed and expected frequencies
#         letter_fitness = sum(
#             [(self.one_letters[letter] - letter_frequencies.get(letter, 0)) ** 2 for letter in self.alphabet])
#         bigram_fitness = sum([(self.two_letters[bigram] - bigram_frequencies.get(bigram, 0)) ** 2 for bigram in
#                               self.two_letters])
#
#         # Calculate fitness contribution of common words
#         decoded_words = re.findall(r'''\b\w+\b''', decoded_text, re.DOTALL | re.IGNORECASE)
#         common_words_count = sum([1 for word in decoded_words if word.lower() in self.words])
#         common_words_fitness = (common_words_count * WORDS_WEIGHT) ** 2
#
#         fitness_value = letter_fitness + bigram_fitness + common_words_fitness
#
#         return fitness_value
#
#     def selection(self, best_fitness):
#         samples = random.sample(best_fitness, SELECTED_SIZE)
#         sorted_samples = sorted(samples, key=lambda x: x[1], reverse=True)
#         index, fitness = sorted_samples[0]
#         return self.population[index]
#
#     def correct_dict(self, dictionary):
#         chars = [c for c in string.ascii_lowercase]
#         letters_in_dict = set(dictionary.values())
#         not_in_dict = list(set(chars) - set(letters_in_dict))
#         values_in_use = set()
#         for letter in dictionary:
#             if dictionary[letter] in values_in_use:
#                 for i in range(len(not_in_dict)):
#                     if not_in_dict[i] not in values_in_use:
#                         dictionary[letter] = not_in_dict[i]
#                         values_in_use.add(not_in_dict[i])
#                         break
#             else:
#                 values_in_use.add(dictionary[letter])
#         return dictionary
#
#     def crossover(self, first_parent, second_parent):
#         cutoff = random.choice(list(first_parent.keys()))
#         first_child = {key: first_parent[key] if key <= cutoff else second_parent[key] for key in first_parent}
#         second_child = {key: second_parent[key] if key <= cutoff else first_parent[key] for key in second_parent}
#         return self.correct_dict(first_child), self.correct_dict(second_child)
#
#     def mutation(self, dictionary):
#         len_dict = len(dictionary)
#         chars = [c for c in string.ascii_lowercase]
#         len_chars = len(chars)
#         for _ in range(len_dict):
#             rand_value = random.random()
#             if rand_value < MUTATION_RATE:
#                 key1, key2 = random.sample(range(len_chars), 2)
#                 val1, val2 = chars[key1], chars[key1]
#                 dictionary[val1], dictionary[val2] = dictionary[val2], dictionary[val1]
#         return dictionary
#
#     def next_generations_loop(self):
#         for generation in range(GENERATIONS):
#             fitness_values = sorted([(i, int(self.fitness(dictionary))) for i, dictionary in
#                                      enumerate(self.population)], key=lambda x: -x[1])
#             index, fitness = fitness_values[0]
#             if fitness > self.best_fitness:
#                 self.best_dict = self.population[index]
#                 self.best_generation = generation
#                 self.local_maximum = 0
#                 self.stop = 0
#             self.count_iters += len(self.population)
#             offsprings = []
#             parents = [self.selection(fitness_values) for _ in range(POPULATION_SIZE)]
#             for i in range(0, POPULATION_SIZE, 2):
#                 first = parents[i % POPULATION_SIZE]
#                 second = parents[(i+1) % POPULATION_SIZE]
#                 child_first, child_second = self.crossover(first, second)
#                 offsprings.append(self.mutation(child_first))
#                 offsprings.append(self.mutation(child_second))
#             if self.best_dict not in offsprings:
#                 offsprings[0] = self.best_dict
#
#             if self.local_maximum == LOCAL_MAXIMUM:
#                 print("In local maximum, number of steps" + str(self.count_iters))
#                 return self.best_dict, self.best_generation, self.best_fitness
#
#             self.population = offsprings
#             self.stop += 1
#             self.local_maximum += 1
#             if self.stop == STOP_NO_CHANGE:
#                 print("No change - iteration " + str(STOP_NO_CHANGE))
#                 print("No change, number of steps " + str(self.count_iters))
#                 break
#         return self.best_dict, self.best_generation, self.best_fitness
#
#
# if __name__ == '__main__':
#     time_start = time.time()
#     outputs = []
#     number_of_iterations = STARTERS
#     algorithm = None
#     while number_of_iterations > 0:
#         number_of_iterations -= 1
#         algorithm = GeneticAlgorithm()
#         outputs.append(algorithm.next_generations_loop())
#
#     best_fitness = float('-inf')
#     best_dict_all = None
#     best_generation = 0
#     for best_dict, generation, fitness in outputs:
#         if fitness > best_fitness:
#             best_fitness = fitness
#             best_dict_all = best_dict
#             best_generation = generation
#
#     chars = [c for c in string.ascii_lowercase]
#     values_list = list(best_dict_all.values())
#     with open("perm.txt", "w") as file:
#         for i, symbol in enumerate(chars.alphabet):
#             file.write(f"{symbol}: {values_list[i]}\n")
#     file.close()
#     with open("plain.txt", "w") as file:
#         file.write(algorithm.text_decoder(best_dict_all))
#     file.close()
#
#     time_end = time.time()
#     all_time = (time_end - time_start) / 60
#     print("Time for algorithm: ", all_time)
#
#
#
#
#

import random
import re
import string
import time
from data_utils import Data_utils


POPULATION_SIZE = 100
WORDS_WEIGHT = 0.3
SELECTED_SIZE = 15
MUTATION_RATE = 0.05
GENERATIONS = 300
LOCAL_MAXIMUM = 10
STOP_NO_CHANGE = 30
TOO_MUCH_GENERATIONS = 100
STARTERS = 5


class GeneticAlgorithm:
    def __init__(self):
        self.data_utils = Data_utils()
        self.two_letters = self.data_utils.get_letters2_freq()
        self.one_letter = self.data_utils.get_letters_freq()
        self.common_words = set(self.data_utils.get_words())
        self.encrypted_text = self.data_utils.get_encrypted_text()
        self.chars = [char for char in string.ascii_lowercase]
        self.population = self.generate_population()
        self.best_dict = None
        self.best_generation = 0
        self.best_fitness = float('-inf')
        self.stop = 0
        self.local_maximum = 0
        self.count_iters = 0

    def generate_population(self):
        list_of_dicts = []
        while len(list_of_dicts) < POPULATION_SIZE:
            chars_copy = self.chars.copy()
            random.shuffle(chars_copy)
            dictionary = {self.chars[i]: chars_copy[i] for i in range(len(self.chars))}
            list_of_dicts.append(dictionary)
        return list_of_dicts

    def text_decoder(self, dictionary):
        decoded_text = ""
        for letter in self.encrypted_text:
            decoded_text += dictionary.get(letter, letter)
        return decoded_text

    def one_letter_fitness(self, text):
        chars = [c for c in string.ascii_lowercase]
        one_letter_freq = {char: text.count(char) / len(text) for char in chars}
        sum_one_letter = sum([pow(self.one_letter[char] - one_letter_freq.get(char, 0), 2) for char in chars])
        return sum_one_letter

    def two_letter_fitness(self, text):
        chars = [c for c in string.ascii_lowercase]
        len_text = len(text) - 1
        two_letter_freq = {}
        for i in range(len_text):
            two_letter = text[i: (i + 2)]
            if two_letter in self.two_letters:
                temp = int(two_letter_freq.get(two_letter, 0))
                two_letter_freq[two_letter] = temp + 1
        sum_all_two_letters = sum(two_letter_freq.values())
        two_letter_new_freq = {two_letters: val / sum_all_two_letters for two_letters, val in two_letter_freq.items()}
        sum_two_letters = sum(
            [pow(self.two_letters[char] - two_letter_new_freq.get(char, 0), 2) for char in self.two_letters])
        return sum_two_letters

    def words_fitness(self, text):
        count_words = 0
        for line in text.split("/n"):
            for word in line.split(" "):
                clean_word = word.lower().rstrip(",.").rstrip()
                if clean_word in self.common_words:
                    count_words += 1
        return pow(count_words * 0.3, 2)

    def fitness(self, dictionary):
        text = self.text_decoder(dictionary)
        return self.one_letter_fitness(text) + self.two_letter_fitness(text) + self.words_fitness(text)

    def selection(self, best_fitness):
        samples = random.sample(best_fitness, 15)
        sorted_samples = sorted(samples, key=lambda x: x[1], reverse=True)
        index, fitness = sorted_samples[0]
        return self.population[index]

    def correct_dict(self, dictionary):
        chars = [c for c in string.ascii_lowercase]
        letters_in_dict = set(dictionary.values())
        not_in_dict = list(set(chars) - set(letters_in_dict))
        values_in_use = set()
        for letter in dictionary:
            if dictionary[letter] in values_in_use:
                for i in range(len(not_in_dict)):
                    if not_in_dict[i] not in values_in_use:
                        dictionary[letter] = not_in_dict[i]
                        values_in_use.add(not_in_dict[i])
                        break
            else:
                values_in_use.add(dictionary[letter])
        return dictionary

    def crossover(self, first_parent, second_parent):
        cutoff = random.choice(list(first_parent.keys()))
        first_child = {key: first_parent[key] if key <= cutoff else second_parent[key] for key in first_parent}
        second_child = {key: second_parent[key] if key <= cutoff else first_parent[key] for key in second_parent}
        return self.correct_dict(first_child), self.correct_dict(second_child)

    def mutation(self, dictionary):
        for i in range(len(dictionary)):
            if random.random() < MUTATION_RATE:
                sample_first, sample_second = random.sample(range(len(self.chars)), 2)
                key_first, key_second = self.chars[sample_first], self.chars[sample_second]
                dictionary[key_first], dictionary[key_second] = dictionary[key_second], dictionary[key_first]
        return dictionary

    def write_to_files(self, individual, generation, best_fitness):
        # Write the decoded text to plain.txt
        with open("plain.txt", "w") as f:
            f.write(self.text_decoder(individual))

        # Write the permutation table to perm.txt
        values_list = list(individual.values())
        with open("perm.txt", "w") as f:
            for i, symbol in enumerate(self.chars):
                f.write(f"{symbol}: {values_list[i]}\n")

        # Print the number of steps and best fitness so far
        print(f"Generation {generation}, Best Fitness: {best_fitness}")

    def lamarckian_modification(self, individual):
        mutated_individual = individual.copy()
        max_fitness_score = int(self.fitness(mutated_individual))
        self.steps += 1

        # Lamarckian modification
        for _ in range(LAMARCKIAN_STEPS):
            # Choose two random keys from individual
            keys = random.sample(list(mutated_individual.keys()), 2)
            # Swap their values
            mutated_individual[keys[0]], mutated_individual[keys[1]] = mutated_individual[keys[1]], mutated_individual[
                keys[0]]
            # Check if the modified individual has a better fitness score than the original
            new_fitness_score = int(self.fitness(mutated_individual))
            self.steps += 1
            if new_fitness_score < max_fitness_score:
                # Swap back if the modification does not improve the fitness score
                mutated_individual[keys[1]], mutated_individual[keys[0]] = mutated_individual[keys[0]], \
                    mutated_individual[keys[1]]
            else:
                # Update max_fitness_score to reflect the latest best score
                max_fitness_score = new_fitness_score

        return mutated_individual

    def darwin_modification(self, offspring):
        mutated_individual = offspring.copy()
        individual = None
        generation = 0
        fitness_score = int(self.fitness(offspring[0]))
        self.steps += 1
        for permutaion in mutated_individual:
            current_fitness_score = int(self.fitness(permutaion))
            self.steps += 1
            for _ in range(2):
                # Choose two random keys from individual
                keys = random.sample(list(permutaion.keys()), 2)
                # Swap their values
                permutaion[keys[0]], permutaion[keys[1]] = permutaion[keys[1]], permutaion[keys[0]]
                # Check if the modified individual has a better fitness score than the original
                new_fitness_score = int(self.fitness(permutaion))
                self.steps += 1
                if new_fitness_score > fitness_score:
                    individual = permutaion
                    generation = self.generations
                    fitness_score = new_fitness_score
        return individual, generation, fitness_score

    def next_generation(self):
        for generation in range(POPULATION_SIZE):
            fitness_scores = sorted([(i, int(self.fitness(dictionary))) for i, dictionary in
                                     enumerate(self.population)], key=lambda x: x[1], reverse=True)
            index_, fitness = fitness_scores[0]
            if fitness > self.best_fitness:
                self.best_fitness = fitness
                self.best_generation = generation
                self.best_dict = self.population[index_]
                self.stop = 0
                self.local_maximum = 0

            parents = [self.selection(fitness_scores) for _ in range(POPULATION_SIZE)]
            children = []
            len_parents = len(parents)
            for x in range(0, POPULATION_SIZE):
                parent1 = parents[x % len_parents]
                parent2 = parents[(x+1) % len_parents]
                child1, child2 = self.crossover(parent1, parent2)
                children.append(self.mutation(child1))
                children.append(self.mutation(child2))
                x += 2

            if self.best_dict not in children:
                children[0] = self.best_dict

            self.count_iters += len(self.population)
            self.stop += 1
            self.population = children

            if self.local_maximum == LOCAL_MAXIMUM:
                print("In local maximum.")
                print("Best fitness is - " + str(self.best_fitness))
                print("Best generation is - " + str(self.best_generation))
                print("-----------------------------")
                return self.best_dict, self.best_generation, self.best_fitness

            self.local_maximum += 1
            if self.stop == STOP_NO_CHANGE and generation > TOO_MUCH_GENERATIONS:
                print("No change")
                print("Best fitness is - " + str(self.best_fitness))
                print("Best generation is - " + str(self.best_generation))
                print("-----------------------------")
                break

        return self.best_dict, self.best_generation, self.best_fitness


if __name__ == '__main__':
    start_time = time.time()
    outputs = []
    algorithm = None
    i = 0
    while STARTERS > 0:
        i += 1
        print("run number: " + str(i))
        # Create an instance of the GeneticAlgorithm class
        algorithm = GeneticAlgorithm()
        outputs.append(algorithm.next_generation())
        STARTERS -= 1

    best_fitness = float('-inf')
    best_dict_all = None
    best_generation = 0
    for best_dict, generation, fitness in outputs:
        if fitness > best_fitness:
            best_fitness = fitness
            best_dict_all = best_dict
            best_generation = generation

    chars = [c for c in string.ascii_lowercase]
    values_list = list(best_dict_all.values())
    with open("perm.txt", "w") as file:
        for i, symbol in enumerate(chars):
            file.write(f"{symbol}: {values_list[i]}\n")
    file.close()
    with open("plain.txt", "w") as file:
        file.write(algorithm.text_decoder(best_dict_all))
    file.close()

    time_end = time.time()
    all_time = (time_end - start_time) / 60
    print("Time for algorithm: ", all_time)

