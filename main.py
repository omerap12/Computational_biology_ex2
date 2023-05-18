import random
import string


def generate_dict():
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


def initialize_population(K):
    # initialize a population of size K - every dict is unique
    dicts_set = set()
    while len(dicts_set) < K:
        d = generate_dict()  # Generate a new dictionary until it's unique
        if len(set(d.values())) < len(d):  # Check that the values are unique
            continue
        dicts_set.add(frozenset(d.items()))


def decode_sentence(sentence, decoding_dict):
    decoded_sentence = ""
    for c in sentence:
        if c == " ":
            decoded_sentence += " "
        if c in decoding_dict:
            decoded_sentence += decoding_dict[c].lower()
        else:
            decoded_sentence += c.lower()
    return decoded_sentence


if __name__ == '__main__':
    print("Omer Aplatony")

