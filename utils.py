class Element:
    def __init__(self, occurrence):
        self.__occurrence = occurrence

    def get_occurrence(self):
        return self.__occurrence

    def set_occurrence(self, occurrence):
        self.__occurrence = occurrence

    def __eq__(self, other):
        return self.get_occurrence() == other.get_occurrence()

    def __lt__(self, other):
        return self.get_occurrence() < other.get_occurrence()


class Feuille(Element):
    def __init__(self, occurrence, character):
        super().__init__(occurrence)
        self.__character = character

    def get_character(self):
        return self.__character

    def __str__(self):
        return f"Feuille: {self.get_occurrence()} - {self.get_character()}"


class Noeud(Element):
    def __init__(self, occurrence, left=None, right=None):
        super().__init__(occurrence)
        self.__left = left
        self.__right = right

    def get_left(self):
        return self.__left

    def get_right(self):
        return self.__right

    def __str__(self):
        return f"Noeud: {self.get_occurrence()}"


class Huffman:
    def __init__(self, file_path):
        self.__file_path = file_path
        self.__huffman_list = []
        self.__huffman_dict = {}

    def read_file(self):
        with open(self.__file_path, "r") as f:
            return f.read()

    def generate_huffman_list(self):
        text = self.read_file()
        for char in text:
            found = False
            for i, element in enumerate(self.__huffman_list):
                if isinstance(element, Feuille) and element.get_character() == char:
                    element.set_occurrence(element.get_occurrence() + 1)
                    found = True
                    while i > 0 and self.__huffman_list[i - 1] < self.__huffman_list[i]:
                        self.__huffman_list[i - 1], self.__huffman_list[i] = self.__huffman_list[i], self.__huffman_list[i - 1]
                        i -= 1
                    break
            if not found:
                self.__huffman_list.insert(0, Feuille(1, char))

    def generate_huffman_tree(self):
        while len(self.__huffman_list) > 1:
            left, right = self.__huffman_list.pop(), self.__huffman_list.pop()
            occurrence = left.get_occurrence() + right.get_occurrence()
            node = Noeud(occurrence, left, right)
            self.__huffman_list.append(node)
            self.__huffman_list.sort(reverse=True)

    def creerCode(self, element, code=""):
        if isinstance(element, Feuille):
            self.__huffman_dict[element.get_character()] = code
        else:
            self.creerCode(element.get_left(), code + "1")
            self.creerCode(element.get_right(), code + "0")

    def coder(self):
        root = self.__huffman_list[0]
        self.creerCode(root)

    def afficherCode(self):
        for character, code in self.__huffman_dict.items():
            print(f"{character}: {code}")

    @staticmethod
    def coder_huffman(text, code):
        text_code = ""
        for character in text:
            text_code += code[character]
        return text_code

    @staticmethod
    def decoder_huffman(text_code, tree):
        content = ""
        decoded_content = ""

        # inversion de l'arbre
        decoding_tree = {}

        for key in tree:
            decoding_tree[tree[key]] = key

        for character in text_code:
            content += character

            if content in decoding_tree:
                decoded_content += decoding_tree[content]
                content = ""

        return decoded_content

