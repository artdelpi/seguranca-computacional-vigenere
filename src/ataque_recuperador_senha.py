"""
Método Kasiki, demonstrado no vídeo:
https://www.youtube.com/watch?v=P4z3jAOzT9I
"""

def remover_nao_letras(plaintext:str) -> str:
    return "".join([char for char in plaintext if char.isalpha()])


def encontrar_repeticoes(ciphertext:str, tamanho_grupo=3):
    """
    Observação: len(ciphertext)-(tamanho_grupo+1) justifica-se porque os caracteres são tomados 3 a 3
    dentro do corpo do for, e pra acessar o último grupo basta o índice da lista - (3+1).

    Exemplo: "ABCDEFGHI" vai até o índice 8 e o último grupo é "GHI", que vai do índice 6 ao 8. Assim, o valor
    de i no for só precisaria ir até 6, porque o elemento de índice 8 seria compreendido por ciphertext[6:6+3].
    """
    repeticoes_por_grupo = dict() # Posições de repetições dos grupos no ciphertext (Índice da primeira letra do grupo)
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
    """
    divisores = list()

    # Pega os divisores de cada valor de espaçamento e monta uma lista
    for divisor in range(2, 21): # Verifica divisores/tamanhos de chave de tamanho 2 a 20 (Pula 0 e 1 como divisores)
        for espacamento in espacamentos:
            if (espacamento % divisor == 0): # Insere divisor na lista caso divida algum espaçamento específico
                divisores.append(divisor)
    return divisores


texto = (
    "DO YOU KNOW THE LAND WHERE THE ORANGE TREE BLOSSOMS?\n"
    "THE COUNTRY OF GOLDEN FRUITS AND MARVELOUS ROSES,\n"
    "WHERE THE BREEZE IS SOFTER AND BIRDS LIGHTER,\n"
    "WHERE BEES GATHER POLLEN IN EVERY SEASON,\n"
    "AND WHERE SHINES AND SMILES, LIKE A GIFT FROM GOD,\n"
    "AN ETERNAL SPRINGTIME UNDER AN EVER-BLUE SKY!\n"
    "ALAS! BUT I CANNOT FOLLOW YOU\n"
    "TO THAT HAPPY SHORE FROM WHICH FATE HAS EXILED ME!\n"
    "THERE! IT IS THERE THAT I SHOULD LIKE TO LIVE,\n"
    "TO LOVE, TO LOVE, AND TO DIE!\n"
    "IT IS THERE THAT I SHOULD LIKE TO LIVE, IT IS THERE, YES, THERE!"
)

#print(encontrar_repeticoes(texto))
#print(encontrar_espacamentos(encontrar_repeticoes(texto)))