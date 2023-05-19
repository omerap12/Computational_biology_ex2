from data_utils import Data_utils
class Manipulation:
    def __init__(self) -> None:
        self.data_util = Data_utils()
    

    def fitness(self,text:str) -> float:
        return self.fitness_one_letter(text)+self.fitness_two_letter(text)+self.fitness_words(text)
    
    def fitness_one_letter(self,text:str) -> float:
        grade = 0
        for line in text.split("/n"):
            for letter in line:
                if letter not in self.data_util.get_letters_freq().keys():
                    continue
                grade += self.data_util.get_letters_freq()[letter]
        return grade
    
    def fitness_two_letter(self,text:str) -> float:
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
    
    def fitness_words(self,text:str) -> float:
        count_words = 0
        for line in text.split("/n"):
            for word in line.split(" "):
                if word.lower() in self.data_util.get_words():
                    count_words += 1
        return count_words/len(self.data_util.get_words())
            


if __name__ == '__main__':
    m = Manipulation()
    print(m.fitness("ABove IS access/nHI get_letters2_freq"))