from app.src.ataque_recuperador_chave import (
    remover_nao_letras, encontrar_repeticoes, encontrar_espacamentos, 
    encontrar_divisores, estimar_tamanho_chave, 
    agrupar_letras_igualmente_deslocadas, descobrir_melhor_deslocamento, 
    descobrir_chave_por_frequencia
)
from app.src.cifrador_decifrador import criptografar_vigenere


def test_remover_nao_letras():
    teste_1 = remover_nao_letras("Olá, mundo! 123.") == "OLÁMUNDO"
    teste_2 = remover_nao_letras("ABC def GHI!") == "ABCDEFGHI"
    assert(teste_1 and teste_2)


def test_encontrar_repeticoes():
    texto = "ABCDABCDEFABC"
    resultado = encontrar_repeticoes(texto, 3)
    teste_1 = "ABC" in resultado and resultado["ABC"] == [0, 4, 10]
    assert(teste_1)


def test_encontrar_espacamentos():
    repeticoes = {"ABC": [0, 4, 10]}
    resultado = encontrar_espacamentos(repeticoes)
    teste_1 = resultado == [4, 6]
    assert(teste_1)


def test_encontrar_divisores():
    espacamentos = [4, 6]
    resultado = encontrar_divisores(espacamentos)
    teste_1 = set([2, 4]) <= set(resultado)
    assert(teste_1)


def test_estimar_tamanho_chave():
    divisores = [2, 2, 3, 4, 4, 4, 6, 6]
    resultado = estimar_tamanho_chave(divisores)
    teste_1 = resultado[0] == 4  # mais frequente
    assert(teste_1)


def test_agrupar_letras_igualmente_deslocadas():
    ciphertext = "ABCDEFGHIJKLMNOPQRSTUV"
    tamanhos_estimados = [3]
    resultado = agrupar_letras_igualmente_deslocadas(ciphertext, tamanhos_estimados)
    esperado = [['A', 'D', 'G', 'J', 'M', 'P', 'S', 'V'],
                ['B', 'E', 'H', 'K', 'N', 'Q', 'T'],
                ['C', 'F', 'I', 'L', 'O', 'R', 'U']]
    assert(resultado == esperado)


def test_descobrir_melhor_deslocamento():
    agrupamento = "EEEEAAAAAAA"
    freq = {chr(i): 0 for i in range(ord('A'), ord('Z')+1)}
    freq['A'] = 50
    freq['E'] = 50
    resultado = descobrir_melhor_deslocamento(agrupamento, freq)
    assert(isinstance(resultado, int) and 0 <= resultado <= 25)


def test_descobrir_chave_por_frequencia():
    plaintext = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG " * 5
    key = "KEY"
    ciphertext = criptografar_vigenere(plaintext, key)
    chave_descoberta, _ = descobrir_chave_por_frequencia(ciphertext, "Inglês")
    assert chave_descoberta.startswith("KEY")
