from collections import Counter

# Frequências de letras no idioma Português (%)
FREQUENCIA_PT = {
    'A': 14.63, 'B': 1.04, 'C': 3.88, 'D': 4.99, 
    'E': 12.57, 'F': 1.02, 'G': 1.30, 'H': 1.28,
    'I': 6.18, 'J': 0.40, 'K': 0.02, 'L': 2.78,
    'M': 4.74, 'N': 5.05, 'O': 10.73, 'P': 2.52, 
    'Q': 1.20, 'R': 6.53, 'S': 7.81, 'T': 4.34,
    'U': 4.63, 'V': 1.67, 'W': 0.01, 'X': 0.21, 
    'Y': 0.01, 'Z': 0.47
}

# Frequências de letras no idioma Inglês (%)
FREQUENCIA_EN = {
    'A': 8.167, 'B': 1.492, 'C': 2.782, 'D': 4.253, 
    'E': 12.702, 'F': 2.228, 'G': 2.015, 'H': 6.094,
    'I': 6.966, 'J': 0.153, 'K': 0.772, 'L': 4.025,
    'M': 2.406, 'N': 6.749, 'O': 7.507, 'P': 1.929, 
    'Q': 0.095, 'R': 5.987, 'S': 6.327, 'T': 9.056,
    'U': 2.758, 'V': 0.978, 'W': 2.360, 'X': 0.150, 
    'Y': 1.974, 'Z': 0.074
}

def remover_nao_letras(plaintext:str) -> str:
    """
    Remove todos os caracteres que não são letras e capitaliza com code golf.

    Args:
        plaintext (str): Texto de entrada.

    Returns:
        str: Plaintext com apenas letras maiúsculas.

    """
    return "".join([char for char in plaintext if char.isalpha()]).upper()


def encontrar_repeticoes(ciphertext:str, tamanho_grupo=3) -> dict:
    """
    Encontra substrings repetidas de tamanho fixo (default=3) e registra suas posições no texto.

    Args:
        ciphertext (str): Texto cifrado original.
        tamanho_grupo (int): Tamanho das substrings a serem analisadas (default=3).

    Returns:
        dict: Dicionário onde as chaves são substrings repetidas e os valores são listas com os 
              índices de ocorrência dessas substrings no texto.
    """
    texto_limpo = remover_nao_letras(ciphertext)
    repeticoes = dict()

    for i in range(len(texto_limpo) - (tamanho_grupo+1)):
        grupo = ciphertext[i:i+tamanho_grupo] # Ex: "FWC", "OXO", "ABA"...

        if (grupo in repeticoes):
            repeticoes[grupo].append(i) # Agrega à lista de ocorrências
        else:
            repeticoes[grupo] = [i] # Guarda primeira ocorrência

    # Remove substrings que só aparecem uma vez
    repeticoes = {grupo: pos for grupo, pos in repeticoes.items() if len(pos) > 1}

    return repeticoes


def encontrar_espacamentos(repeticoes_por_grupo:dict) -> list:
    """
    Para cada grupo repetido, calcula as distâncias entre as repetições de substrings consecutivas.
    
    Args:
        repeticoes_por_grupo (dict): Dicionário onde as chaves são substrings repetidas
                                     e os valores são listas com as posições de ocorrência.

    Returns:
        List[int]: Lista de espaçamentos (diferenças entre posições consecutivas).
    """
    espacamentos = list()

    for posicoes in repeticoes_por_grupo.values():
        for i in range(len(posicoes) - 1):
            espacamentos.append(posicoes[i+1]-posicoes[i]) # Ex: [1, 3, 4] ➔ [2, 1]

    return espacamentos


def encontrar_divisores(espacamentos:list) -> list:
    """
    Encontra os divisores entre 2 e 20 que dividem exatamente cada espaçamento.
    
    Args:
        espacamentos (List[int]): Lista de espaçamentos entre repetições de substrings.

    Returns:
        List[int]: Lista de divisores possíveis do tamanho da chave.
    """
    divisores = list()

    for espacamento in espacamentos:
        for divisor in range(2, 21): # Ignora 1 e evita 0
            if (espacamento % divisor == 0):
                divisores.append(divisor)

    return divisores


def estimar_tamanho_chave(divisores:list) -> list:
    """
    Estima os tamanhos mais prováveis da chave de acordo com a frequência dos divisores.

    Args:
        divisores (List[int]): Lista de divisores que aparecem nos espaçamentos entre substrings repetidas.

    Returns:
        List[int]: Lista ordenada dos tamanhos de chave mais prováveis (do mais comum ao menos comum).
    """
    # Contador de frequência manual
    freq_divisor = dict()
    for divisor in divisores:
        if (divisor not in freq_divisor):
            freq_divisor[divisor] = 1
        else:
            freq_divisor[divisor] += 1
    
    # Ordena os divisores por frequência decrescente
    tamanhos_estimados = sorted(freq_divisor, key=lambda k: freq_divisor[k])
    return tamanhos_estimados[::-1]


def agrupar_letras_igualmente_deslocadas(ciphertext: str, tamanhos_estimados: list, seletor_estimado=0) -> list:
    """
    Monta uma lista com grupos de letras igualmente deslocadas. Cada grupo funciona como uma Cifra de César.

    Args:
        ciphertext (str): Texto cifrado.
        tamanhos_estimados (list): Lista de tamanhos prováveis da chave.
        seletor_estimado (int): Índice do tamanho escolhido na lista de tamanhos.

    Returns:
        list[list[str]]: Lista de agrupamentos, onde cada agrupamento contém letras cifradas com a mesma letra da chave.
    """
    if seletor_estimado >= len(tamanhos_estimados):
        raise ValueError("Seletor de tamanho de chave fora do intervalo.")

    ciphertext = remover_nao_letras(ciphertext)
    tamanho_chave = tamanhos_estimados[seletor_estimado]
    agrupamentos = list()

    for i in range(tamanho_chave):
        grupo = [ciphertext[j] for j in range(i, len(ciphertext), tamanho_chave)]
        agrupamentos.append(grupo)

    return agrupamentos


def descobrir_melhor_deslocamento(agrupamento: str, freq_esperada: dict) -> int:
    """
    Calcula o melhor deslocamento (de 0 a 25) pro grupo, comparando a frequência observada 
    com a frequência esperada para o idioma.

    Args:
        agrupamento (str): Letras cifradas com o mesmo deslocamento.
        freq_esperada (dict[str, float]): Frequência percentual das letras do idioma.

    Retorna:
        int: Deslocamento mais provável entre 0 e 25.  
    """
    total, contagem, menor_erro, melhor_deslocamento = (
        len(agrupamento), # Total de letras no grupo
        Counter(agrupamento), # Frequência observada no agrupamento
        float('inf'),
        0
    )
    
    # Testa todos os possíveis deslocamentos (de 0 a 25)
    for desloc in range(26):
        erro = 0
        for letra, freq_esp in freq_esperada.items():
            # Criptografa letra do idioma com deslocamento
            letra_cifrada = chr((ord(letra) - ord('A') + desloc) % 26 + ord('A'))
            freq_obs = (contagem.get(letra_cifrada, 0) / total) * 100 
            erro += (freq_obs - freq_esp) ** 2

        # Atualiza o melhor deslocamento, caso haja algum com erro menor
        if (erro < menor_erro):
            menor_erro = erro
            melhor_deslocamento = desloc

    return melhor_deslocamento


def descobrir_chave_por_frequencia(ciphertext: str, idioma: str, opcao_chave=0) -> tuple:
    """
    Executa o ataque de análise de frequência na cifra de Vigenère.

    Etapas:
    1) Estima o tamanho da chave com base no método de Kasiski.
    2) Agrupa letras cifradas pela mesma posição relativa na chave.
    3) Aplica análise de frequência com base no idioma pra cada grupo.

    Parâmetros:
        ciphertext (str): Texto cifrado.
        idioma (str): Idioma esperado do texto original ('Português' ou 'Inglês').
        opcao_chave (int): Índice do tamanho estimado da chave a ser testado.

    Retorna:
        tuple[str, list[int]]: A chave mais provável e a lista ordenada dos tamanhos de chave estimados.
    """
    frequencia_idioma = FREQUENCIA_PT if idioma == "Português" else FREQUENCIA_EN

    # ============ Início Kasiski ============
    repeticoes = encontrar_repeticoes(ciphertext)
    espacamentos = encontrar_espacamentos(repeticoes)
    divisores = encontrar_divisores(espacamentos)
    tamanhos_estimados = estimar_tamanho_chave(divisores)
    # ============ Final  Kasiski ============

    if not tamanhos_estimados or opcao_chave >= len(tamanhos_estimados):
        return None, tamanhos_estimados

    agrupamentos = agrupar_letras_igualmente_deslocadas(ciphertext, tamanhos_estimados, opcao_chave)
    chave = ''
    
    for agrupamento in agrupamentos:
        desloc = descobrir_melhor_deslocamento(agrupamento, frequencia_idioma)
        letra_chave = chr(desloc + ord('A'))
        chave += letra_chave

    return chave, tamanhos_estimados
