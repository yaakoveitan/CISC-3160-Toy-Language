import re
from typing import List

def tokenize(expression: str) -> List[str]:
    # Add spaces around +, -, =, and * characters so that they are treated as separate tokens
    expression = expression.replace('+', ' + ')
    expression = expression.replace('-', ' - ')
    expression = expression.replace('=', ' = ')
    expression = expression.replace('*', ' * ')
    expression = expression.replace('(', ' ( ')
    expression = expression.replace(')', ' ) ')
    expression = expression.replace(';', ' ; ')

    # Split the expression on spaces to get a list of tokens
    tokens = expression.split(' ')

    # Remove empty tokens from the list
    tokens = [token for token in tokens if token]

    return tokens



class RDParser:
    def __init__(self, tokens: List[str]):
        self.tokens = tokens
        print(tokens)
        self.current_token = 0
        self.variables = {}
    #Program: Assignment*
    def parse_program(self) -> None:
        while self.current_token < len(self.tokens):
          while self.accept(';'):
            self.current_token += 1
          self.parse_assignment()

    #Assignment: Identifier = Exp
    def parse_assignment(self) -> None:
        identifier = self.parse_identifier()
        self.expect('=')
        exp = self.parse_exp()
        self.expect(';')
        self.variables[identifier] = exp
    #Exp: Term Exp'
    def parse_exp(self) -> int:
        term = self.parse_term()
        return self.parse_exp_prime(term)
    #Exp': + Term Exp' | - Term Exp' | e
    def parse_exp_prime(self, term: int) -> int:
        if self.accept('+'):
            term2 = self.parse_term()
            return self.parse_exp_prime(term + term2)
        elif self.accept('-'):
            term2 = self.parse_term()
            return self.parse_exp_prime(term - term2)
        else:
            return term
    #Term: Fact Term'
    def parse_term(self) -> int:
        fact = self.parse_fact()
        return self.parse_term_prime(fact)
    #Term': * Fact Term' | e
    def parse_term_prime(self, fact: int) -> int:
        if self.accept('*'):
            fact2 = self.parse_fact()
            return self.parse_term_prime(fact * fact2)
        else:
            return fact
    #Fact: - Fact | + Fact | ( Exp ) | Literal | Identifier
    def parse_fact(self) -> int:
        if self.accept('-'):
            fact = self.parse_fact()
            return -fact
        elif self.accept('+'):
            fact = self.parse_fact()
            return fact
        elif self.accept('('):
            exp = self.parse_exp()
            self.expect(')')
            return exp
        elif self.current_token < len(self.tokens) and re.fullmatch(r'\d+', self.tokens[self.current_token]):
            return self.parse_literal()
        else:
            return self.parse_identifier()
    #Identifier: Letter [Letter | Digit]*
    def parse_identifier(self) -> int:
      identifier = self.tokens[self.current_token]
      self.current_token += 1
      if identifier in self.variables:
          return self.variables[identifier]
      else:
          return identifier  
    #Literal: 0 | NonZeroDigit Digit*
    def parse_literal(self) -> int:
      literal = self.tokens[self.current_token]
  
      # Check if the literal starts with a zero, and if so, raise a ValueError
      if literal[0] == '0' and literal[1] is not null:
          raise ValueError(f"Number cannot have leading zero: {literal}")
  
      self.current_token += 1
      return int(literal)

    def accept(self, token: str) -> bool:
        if self.current_token < len(self.tokens) and self.tokens[self.current_token] == token:
            self.current_token += 1
            return True
        else:
            return False

    def expect(self, token: str) -> None:
      if self.current_token < len(self.tokens) and self.tokens[self.current_token] == token:
          self.current_token += 1
      else:
          raise ValueError(f"Expected token {token}, but found {self.tokens[self.current_token]}")

test='a=5; b=6; c = -a*(a +b -3); d=7+c;'
print(test)
test_tokenized = tokenize(test)
parser = RDParser(test_tokenized)
parser.parse_program()


# Print the values of the variables after the program has been parsed

for i in parser.variables:
  print(str(i) + " = " + str(parser.variables[i]))

#output: 
#a = 5
#b = 6
#c = -40
#d = -33
