import enum
import re
from typing import List

class TokenType(enum.Enum):
    KEYWORD = 1
    IDENTIFIER = 2
    INT_LITERAL = 3
    FLOAT_LITERAL = 4
    STRING_LITERAL = 5
    BOOL_LITERAL = 6
    OPERATOR = 7
    PUNCTUATION = 8
    EOF = 9

class LexerError(Exception):
    def __init__(self, position, message="Unexpected token structure"):
        self.position = position
        self.message = message
        super().__init__(f"LexerError at line {position[0]} column {position[1]}: {message}")

class Token:
    def __init__(self, type: TokenType, value: str, line: int, column: int):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

# ========================================================
# [[LLM_MUTATION_ZONE]]
# ========================================================
# If the mutation zone is blank or dropped, initialize clean, rigid defaults
if 'MUTATION_MAP' not in locals():
    MUTATION_MAP = {
        'KEYWORDS': ['let', 'fn', 'if', 'else', 'while', 'return'],
        'BOOLEANS': ['true', 'false'],
        'OPERATORS': ['==', '!=', '<=', '>=', '&&', '||', '=', '+', '-', '*', '/', '%', '!'],
        'PUNCTUATION': ['{', '}', '(', ')', '[', ']', ',', ';', ':'],
        'PREFERENCE_LEVELS': {
            '==': 10, '!=': 10, '<=': 10, '>=': 10, '&&': 9, '||': 9,
            '=': 5, '+': 5, '-': 5, '*': 6, '/': 6, '%': 6, '!': 8
        },
        'CUSTOM_ERROR_MAPS': {
            '@': "Unexpected '@' — Aero does not support decorators",
            '#': "Unexpected '#' — Aero does not use preprocessor directives",
            '$': "Unexpected '$' — variable names do not require sigils in Aero",
            '~': "Unexpected '~' — bitwise NOT is not supported in Aero",
            '`': "Unexpected backtick — template literals are not supported in Aero"
        }
    }

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.length = len(source)

    def tokenize(self) -> List[Token]:
        tokens = []
        
        # Pull matching specifications safely out of the structural map configuration
        keywords_set = set(MUTATION_MAP.get('KEYWORDS', []))
        bools_set = set(MUTATION_MAP.get('BOOLEANS', []))
        
        # Sort operators: longest first, then by preference level (higher = earlier)
        pref_levels = MUTATION_MAP.get('PREFERENCE_LEVELS', {})
        operators_list = sorted(
            MUTATION_MAP.get('OPERATORS', []),
            key=lambda op: (-len(op), -pref_levels.get(op, 0)),
        )
        punctuation_set = set(MUTATION_MAP.get('PUNCTUATION', []))
        custom_errors = MUTATION_MAP.get('CUSTOM_ERROR_MAPS', {})

        while self.position < self.length:
            char = self.source[self.position]
            
            # 1. Whitespace Handler
            if char == '\n':
                self.line += 1
                self.column = 1
                self.position += 1
                continue
            if char.isspace():
                self.column += 1
                self.position += 1
                continue
                
            # 2. Line Comment Handler (//)
            if char == '/' and self.position + 1 < self.length and self.source[self.position + 1] == '/':
                while self.position < self.length and self.source[self.position] != '\n':
                    self.position += 1
                continue
                
            # 3. Block Comment Handler (/* */)
            if char == '/' and self.position + 1 < self.length and self.source[self.position + 1] == '*':
                self.position += 2
                self.column += 2
                while self.position + 1 < self.length and not (self.source[self.position] == '*' and self.source[self.position+1] == '/'):
                    if self.source[self.position] == '\n':
                        self.line += 1
                        self.column = 1
                    else:
                        self.column += 1
                    self.position += 1
                self.position += 2
                self.column += 2
                continue

            # 4. String Literal Processing
            if char in ('"', "'"):
                quote_type = char
                start_line, start_col = self.line, self.column
                value_chars = []
                self.position += 1
                self.column += 1
                
                while self.position < self.length and self.source[self.position] != quote_type:
                    curr_ch = self.source[self.position]
                    if curr_ch == '\n':
                        self.line += 1
                        self.column = 1
                    else:
                        self.column += 1
                    value_chars.append(curr_ch)
                    self.position += 1
                    
                if self.position >= self.length:
                    raise LexerError((start_line, start_col), "Unterminated string literal pattern")
                    
                self.position += 1  # consume closing quote
                self.column += 1
                tokens.append(Token(TokenType.STRING_LITERAL, "".join(value_chars), start_line, start_col))
                continue

            # 5. Numeric Float and Integer Literals
            if char.isdigit() or (char == '.' and self.position + 1 < self.length and self.source[self.position + 1].isdigit()):
                start_col = self.column
                num_chars = []
                has_dot = False
                
                if char == '.':
                    has_dot = True
                    num_chars.append('.')
                    self.position += 1
                    self.column += 1
                    
                while self.position < self.length and (self.source[self.position].isdigit() or self.source[self.position] == '.'):
                    curr_ch = self.source[self.position]
                    if curr_ch == '.':
                        if has_dot: break # second dot stops literal read
                        has_dot = True
                    num_chars.append(curr_ch)
                    self.position += 1
                    self.column += 1
                    
                num_str = "".join(num_chars)
                token_type = TokenType.FLOAT_LITERAL if has_dot else TokenType.INT_LITERAL
                tokens.append(Token(token_type, num_str, self.line, start_col))
                continue

            # 6. Compound Operator Matrix Splicer
            op_matched = False
            for op in operators_list:
                op_len = len(op)
                if self.position + op_len <= self.length and self.source[self.position:self.position + op_len] == op:
                    tokens.append(Token(TokenType.OPERATOR, op, self.line, self.column))
                    self.position += op_len
                    self.column += op_len
                    op_matched = True
                    break
            if op_matched:
                continue

            # 7. Structural Punctuation Matcher
            if char in punctuation_set:
                tokens.append(Token(TokenType.PUNCTUATION, char, self.line, self.column))
                self.position += 1
                self.column += 1
                continue

            # 8. Word Tokens: Identifiers, Keywords, and Booleans
            if char.isalpha() or char == '_':
                start_col = self.column
                word_chars = [char]
                self.position += 1
                self.column += 1
                
                while self.position < self.length and (self.source[self.position].isalnum() or self.source[self.position] == '_'):
                    word_chars.append(self.source[self.position])
                    self.position += 1
                    self.column += 1
                    
                word_str = "".join(word_chars)
                if word_str in keywords_set:
                    tokens.append(Token(TokenType.KEYWORD, word_str, self.line, start_col))
                elif word_str in bools_set:
                    tokens.append(Token(TokenType.BOOL_LITERAL, word_str, self.line, start_col))
                else:
                    tokens.append(Token(TokenType.IDENTIFIER, word_str, self.line, start_col))
                continue

            if char in custom_errors:
                raise LexerError((self.line, self.column), custom_errors[char])
            raise LexerError((self.line, self.column), f"Unexpected character encountered: {char}")
                
        tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return tokens

def tokenize(source: str) -> List[Token]:
    return Lexer(source).tokenize()
