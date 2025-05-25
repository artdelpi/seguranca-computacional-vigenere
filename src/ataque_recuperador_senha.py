from cifrador_decifrador import criptografar_vigenere


"""
Método Kasiki, demonstrado no vídeo:
https://www.youtube.com/watch?v=P4z3jAOzT9I
"""

def remover_nao_letras(plaintext:str) -> str:
    return "".join([char for char in plaintext if char.isalpha()])


def encontrar_repeticoes(ciphertext:str, tamanho_grupo=3) -> dict:
    """
    Observação: len(ciphertext)-(tamanho_grupo+1) justifica-se porque os caracteres são tomados 3 a 3
    dentro do corpo do for, e pra acessar o último grupo basta o índice da lista - (3+1).

    Exemplo: "ABCDEFGHI" vai até o índice 8 e o último grupo é "GHI", que vai do índice 6 ao 8. Assim, o valor
    de i no for só precisaria ir até 6, porque o elemento de índice 8 seria compreendido por ciphertext[6:6+3].

    Retorna: Hashmap que relaciona substring de 3 caracteres à posição que ocorre na cifra.
    Observação: A posição da substring é dada pelo índice do primeiro caractere.
    """
    repeticoes_por_grupo = dict() # Posições de repetições das substrings no ciphertext (Índice da primeira letra do grupo)
    ciphertext = remover_nao_letras(ciphertext)

    for i in range(len(ciphertext) - (tamanho_grupo+1)): # Decrementa tamanho_grupo+1 e evita IndexError
        grupo_selecionado = ciphertext[i:i+tamanho_grupo] # FWC, OXO, ABA...
        if (grupo_selecionado in repeticoes_por_grupo):
            repeticoes_por_grupo[grupo_selecionado].append(i) # Acrescenta posição à lista de intercorrências
        else:
            repeticoes_por_grupo[grupo_selecionado] = [i] # Salva posição da primeira intercorrência
    
    for key in list(repeticoes_por_grupo.keys()): # Itera em cima de uma lista de chaves
        if (len(repeticoes_por_grupo[key]) == 1):
            del repeticoes_por_grupo[key] # Remove pares chave-valor sem repetição
    return repeticoes_por_grupo


def encontrar_espacamentos(repeticoes_por_grupo:dict) -> list:
    """
    Encontrar os espaçamentos revela múltiplos do tamanho da chave. 
    Sabendo que a chave é cíclica, o espaçamento entre repetições deve ser múltiplo do tamanho da chave.

    Como as posições são encontradas à medida que o valor do índice aumenta, a disposição nas listas é crescente.
    Portanto, sem motivo de tirar módulo pra pegar a distância, basta pegar lista[índice+1] - lista[índice]

    Observação: o espaçamento no método Kaneki é a diferença dos índices dos primeiros caracteres de uma substring
    e a sua próxima repetição. Ex: "XYZABCDEFGXYZ". "XYZ" repete, e a distância é 0 - 10 (índice da primeira letra
    da substring e da primeira letra da próxima ocorrência dessa substring)

    Retorna: Todos os espaçamentos encontrados entre as substrings iguais de 3 caracteres.
    """
    espacamentos = list()

    for posicoes in repeticoes_por_grupo.values():
        for i in range(len(posicoes) - 1): # -1 porque pega 2 a 2. Nesse caso, já passou por tudo quando for (len-1)
            espacamentos.append(posicoes[i+1]-posicoes[i]) # Ex: [1, 3, 4] -> [2, 1]
    return espacamentos


def encontrar_divisores(espacamentos:list) -> list:
    """
    Encontrar os divisores dos espaçamentos mostra quais são os possíveis tamanhos da chave.
    Pra isso, basta tirar o resto dos espaçamentos com os tamanhos possíveis da chave.

    Retorna: lista com todos os divisores dos espaçamentos, todas as vezes que conseguem dividir os espaçamentos.
    """
    divisores = list()

    for espacamento in espacamentos:
        for divisor in range(2, 21): # Verifica divisores/tamanhos de chave de tamanho 2 a 20 (Pula 0 e 1 como divisores)
            if (espacamento % divisor == 0): # Insere divisor na lista caso divida algum espaçamento específico
                divisores.append(divisor)
    return divisores


def estimar_tamanho_chave(divisores:list) -> int:
    """
    Método Kaneki propõe que o divisor mais comum dos espaçamentos das substrings de três
    caracteres é a melhor estimativa do tamanho da chave. 

    Retorna: divisor mais comum das distâncias entre as substrings
    """
    # Encontrar divisores mais comuns (possíveis tamanhos de chave)
    freq_divisor = dict()

    # Monta hashmap com os divisores e suas respectivas frequências
    for divisor in divisores:
        if (divisor not in freq_divisor):
            freq_divisor[divisor] = 1
        else:
            freq_divisor[divisor] += 1
    
    freq_maior = 0
    divisor_mais_frequente = 0 # Tamanho de chave mais provável por iteração
    for divisor in freq_divisor:
        if (freq_divisor[divisor] > freq_maior):
            divisor_mais_frequente = divisor # Atualiza maior valor temporário
            freq_maior = freq_divisor[divisor]

    return divisor_mais_frequente

"""
Método Kasiki é pra estimar o tamanho da chave. Agora, segue o ataque de frequência.
"""

# Teste com mensagem e chave conhecidas
mensagem_teste = (
    "The field of cryptanalysis has grown tremendously in recent years. "
    "Modern cryptographic systems rely on complex algorithms that are resistant "
    "to traditional attacks. However, historical ciphers like the Vigenere cipher "
    "remain important for understanding cryptographic principles. "
    
    "When analyzing ciphertext, cryptanalysts look for repeating patterns that "
    "might reveal information about the encryption key. The Kasiski examination "
    "is particularly effective against polyalphabetic ciphers where the same key "
    "is reused multiple times. This method was revolutionary when published in "
    "the 19th century and remains fundamental to cryptanalysis today."
    
    "For proper testing, we need sufficient text length to allow natural language "
    "patterns to emerge through the cipher. English text contains characteristic "
    "letter frequencies that can be exploited in frequency analysis attacks. "
    "Combining statistical methods with pattern recognition often yields the best "
    "results when attempting to break classical ciphers without knowledge of the key."
)

print(mensagem_teste)
chave_teste = "KEY"  # Chave de tamanho 3
texto_cifrado = criptografar_vigenere(mensagem_teste, chave_teste)
print(texto_cifrado)

print("\n=== Teste do Método Kasiski ===")
print(f"Tamanho real da chave: {len(chave_teste)}")
print(f"Chave real: {chave_teste}")

# Executando seu pipeline
repeticoes = encontrar_repeticoes(texto_cifrado)
print(f"\nSequências repetidas encontradas: {len(repeticoes)}")

espacamentos = encontrar_espacamentos(repeticoes)
print(f"Espaçamentos encontrados: {espacamentos}")

divisores = encontrar_divisores(espacamentos)

tamanho_estimado = estimar_tamanho_chave(divisores)
print(f"\nTamanhos de chave estimados (ordem de probabilidade): {tamanho_estimado}")

# Verificando se o tamanho real está na estimativa
tamanho_real = len(chave_teste)
acerto = "SIM" if tamanho_real == tamanho_estimado else "NÃO"
print(f"\nO tamanho real ({tamanho_real}) está nas estimativas? {acerto}")