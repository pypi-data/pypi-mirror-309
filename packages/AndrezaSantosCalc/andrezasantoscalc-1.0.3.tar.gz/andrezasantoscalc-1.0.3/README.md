```python

# AndrezaSantosCalc
AndrezaSantosCalc é uma biblioteca Python que fornece uma calculadora simples para realizar operações matemáticas básicas, como soma, subtração, multiplicação e divisão. Este pacote foi desenvolvido para ser uma ferramenta de uso fácil para cálculos rápidos, especialmente em ambientes educacionais e pequenos projetos.

## Instalação

Para usar a biblioteca AndrezaSantosCalc, você tem duas opções de instalação:

Método 1: Inclusão Manual
Baixe ou clone o repositório da biblioteca.
Copie a pasta AndrezaSantosCalc para o diretório principal do seu projeto.
    link de acesso: https://pypi.org/project/AndrezaSantosCalc/

Método 2: Instalando com pip
Se o pacote for publicado no PyPI, você pode instalá-lo executando:
    pip install AndrezaSantosCalc


## Como Usar

* Importação
Importe a classe Calculadora da biblioteca AndrezaSantosCalc:
    from AndrezaSantosCalc import Calculadora

Instanciando a Calculadora:
    calc = Calculadora()

* Operações Disponíveis
A classe Calculadora inclui quatro métodos principais para operações matemáticas. Veja os detalhes de cada método abaixo.

soma(a, b)
Realiza a soma de dois números.
Parâmetros:
a (float): Primeiro número.
b (float): Segundo número.
Retorna: float - O resultado da soma de a e b.

Exemplo:
    resultado = calc.soma(10, 5)
    print("Soma:", resultado)  # Saída: Soma: 15


subtracao(a, b)
Realiza a subtração de dois números.
Parâmetros:
a (float): Primeiro número.
b (float): Segundo número.
Retorna: float - O resultado da subtração de a e b.

Exemplo:
    resultado = calc.subtracao(10, 5)
    print("Subtração:", resultado)  # Saída: Subtração: 5


multiplicacao(a, b)
Realiza a multiplicação de dois números.
Parâmetros:
a (float): Primeiro número.
b (float): Segundo número.
Retorna: float - O resultado da multiplicação de a e b.

Exemplo:
    resultado = calc.multiplicacao(10, 5)
    print("Multiplicação:", resultado)  # Saída: Multiplicação: 50


divisao(a, b)
Realiza a divisão de dois números.

Parâmetros:

a (float): Primeiro número.
b (float): Segundo número.
Retorna: float - O resultado da divisão de a por b.

Exceção: Levanta ValueError se b for 0, pois divisão por zero não é permitida.

Exemplo:
    resultado = calc.divisao(10, 5)
    print("Divisão:", resultado)  # Saída: Divisão: 2.0


* Exemplo Completo
Este exemplo demonstra o uso de todos os métodos da biblioteca AndrezaSantosCalc:
from AndrezaSantosCalc import Calculadora

# Criando uma instância da calculadora
calc = Calculadora()

# Soma
resultado_soma = calc.soma(10, 5)
print("Soma:", resultado_soma)  # Saída: Soma: 15

# Subtração
resultado_subtracao = calc.subtracao(10, 5)
print("Subtração:", resultado_subtracao)  # Saída: Subtração: 5

# Multiplicação
resultado_multiplicacao = calc.multiplicacao(10, 5)
print("Multiplicação:", resultado_multiplicacao)  # Saída: Multiplicação: 50

# Divisão com tratamento de exceção
try:
    resultado_divisao = calc.divisao(10, 0)
    print("Divisão:", resultado_divisao)
except ValueError as e:
    print("Erro:", e)  # Saída: Erro: Divisão por zero não é permitida.


* Tratamento de Exceções
O método divisao(a, b) levanta uma exceção ValueError se o valor de b for 0, pois a divisão por zero é indefinida.

Exemplo de Tratamento de Exceção:
    try:
        resultado = calc.divisao(10, 0)
    except ValueError as e:
        print("Erro:", e)  # Saída: Erro: Divisão por zero não é permitida.

* Métodos
-------------------------------------------------------------------------------------------------------------------------------------------------------
| Método                | Descrição                                  | Parâmetros         | Retorno                 | Exceções                        |
|-----------------------|--------------------------------------------|--------------------|-------------------------|---------------------------------|
| `soma(a, b)`          | Soma de `a` e `b`.                         | `a`, `b` (float)   | `float`: `a + b`        | None                            |
| `subtracao(a, b)`     | Subtração de `a` e `b`.                    | `a`, `b` (float)   | `float`: `a - b`        | None                            |
| `multiplicacao(a, b)` | Multiplicação de `a` e `b`.                | `a`, `b` (float)   | `float`: `a * b`        | None                            |
| `divisao(a, b)`       | Divisão de `a` por `b`.                    | `a`, `b` (float)   | `float`: `a / b`        | `ValueError` se `b == 0`        |
-------------------------------------------------------------------------------------------------------------------------------------------------------

