# AndrezaSantosCalc.py

class Calculadora:
    """
    Uma classe para realizar operações básicas de uma calculadora.
    """

    def soma(self, a, b):
        """
        Realiza a soma de dois números.
        
        Parâmetros:
        - a : Primeiro número.
        - b : Segundo número.
        
        Retorna:
        -  O resultado da soma de a e b.
        """
        return a + b

    def subtracao(self, a, b):
        """
        Realiza a subtração de dois números.
        
        Parâmetros:
        - a (float): Primeiro número.
        - b (float): Segundo número.
        
        Retorna:
        -  O resultado da subtração de a e b.
        """
        return a - b

    def multiplicacao(self, a, b):
        """
        Realiza a multiplicação de dois números.
        
        Parâmetros:
        - a : Primeiro número.
        - b : Segundo número.
        
        Retorna:
        -  O resultado da multiplicação de a e b.
        """
        return a * b

    def divisao(self, a, b):
        """
        Realiza a divisão de dois números.
        
        Parâmetros:
        - a : Primeiro número.
        - b : Segundo número.
        
        Retorna:
        -  O resultado da divisão de a por b.
        
        Exceção:
        - ValueError: Se b for 0, levanta um erro de divisão por zero.
        """
        if b == 0:
            raise ValueError("Divisão por zero não é permitida.")
        return a / b
