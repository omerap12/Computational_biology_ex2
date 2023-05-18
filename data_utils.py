class Data_utils:
    def __init__(self) -> None:
        self.list_words = None
        self.dict_letters = None
        self.dict_letters2 = None
    
    def load_data(self) -> None:
        self.list_words = self.load_freq_words('dict.txt')
        self.dict_letters = self.load_letters_freq('Letter_Freq.txt')
        self.dict_letters2 = self.load_letters_freq('Letter2_Freq.txt')
    
    def print_data(self) -> None:
        print(self.list_words,end='\n')
        print(self.dict_letters,end='\n')
        print(self.dict_letters2,end='\n')

    def load_freq_words(self,filename) -> list:
        word_list = []
        with open(filename,'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                word_list.append(line)
        file.close()
        return word_list

    def load_letters_freq(self,filename) -> dict:
        data_dict = {}
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if line == "#REF!":
                    return data_dict
                if line:
                    parts = line.split('\t')
                    key = parts[1]
                    value = float(parts[0])
                    data_dict[key] = value
        return data_dict
    
    def get_words(self) -> list:
        return self.list_words
    
    def get_letters_freq(self) -> dict:
        return self.dict_letters
    
    def get_letters2_freq(self) -> dict:
        return self.dict_letters2

if __name__ == '__main__':
    d = Data_utils()
    d.load_data()
    d.print_data()