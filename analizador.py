
import re

tokens = [
    ("PROGRAM", r"PROGRAM"),
    ("END", r"END"),
    ("INTEGER", r"INTEGER"),
    ("NUMBER", r"[0-9]+"),
    ("ID", r"[A-Z][A-Z0-9]*"),
    ("OP", r"[=+\-*/]"),
    ("COMMA", r","),
    ("NEWLINE", r"\n"),
    ("WS", r"[ \t]+"),
]

def lexer(code):
    pos = 0
    result = []
    
    while pos < len(code):
        match = None

        for token_type, pattern in tokens:
            regex = re.compile(pattern)
            match = regex.match(code, pos)

            if match:
                text = match.group(0)
                # ignorar espacios y saltos de línea

                if token_type not in ["WS", "NEWLINE"]:
                    result.append((token_type, text))
                pos = match.end(0)
                break

        if not match:
            raise SyntaxError(f"Token desconocido en posición {pos}")
    return result

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else ("EOF", None)

    def eat(self, token_type):
        if self.current()[0] == token_type:
            self.pos += 1
        else:
            raise SyntaxError(f"Se esperaba {token_type}, encontrado {self.current()}")

    def program(self):
        self.eat("PROGRAM")
        self.eat("ID")
        self.decl()
        self.sentencias()
        self.eat("END")
        print("✅ Programa válido")

    def decl(self):
        self.eat("INTEGER")
        self.lista_id()

    def lista_id(self):
        self.eat("ID")
        if self.current()[0] == "COMMA":
            self.eat("COMMA")
            self.lista_id()

    def sentencias(self):
        if self.current()[0] == "ID":
            self.sentencia()
            self.sentencias()

    def sentencia(self):
        self.eat("ID")
        self.eat("OP")  # '='
        self.expresion()

    def expresion(self):
        self.termino()
        if self.current()[0] == "OP" and self.current()[1] == "+":
            self.eat("OP")
            self.expresion()

    def termino(self):
        if self.current()[0] == "ID":
            self.eat("ID")
        elif self.current()[0] == "NUMBER":
            self.eat("NUMBER")
        else:
            raise SyntaxError("Término inválido")

code = """PROGRAM SUMA
INTEGER A, B, C
A = 3
B = 4
C = A + B
END"""

tokens_lex = lexer(code)
parser = Parser(tokens_lex)
parser.program()
