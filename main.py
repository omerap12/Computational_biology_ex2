def load_freq_words(filename):
    word_list = []
    with open(filename,'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            word_list.append(line)
    file.close()
    return word_list

if __name__ == '__main__':
    filename = "dict.txt"
    words = load_freq_words(filename)
