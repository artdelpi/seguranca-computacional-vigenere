from cifrador_decifrador import criptografar_vigenere, descriptografar_vigenere
from collections import Counter

"""
Método de Kasiski para estimar o tamanho da chave, seguido de ataque por análise de frequência.
Kasiki foi demonstrado no vídeo <https://www.youtube.com/watch?v=P4z3jAOzT9I> do relatório.
"""


def remover_nao_letras(plaintext:str) -> str:
    """
    Remove não-letras e capitaliza.
    """
    return "".join([char for char in plaintext if char.isalpha()]).upper()


def encontrar_repeticoes(ciphertext:str, tamanho_grupo=3) -> dict:
    """
    Encontra substrings repetidas de tamanho fixo (default=3) e registra suas posições no texto.
    Utilizado para encontrar espaçamentos que revelam possíveis tamanhos de chave.
    """
    repeticoes_por_grupo = dict() # Posições de repetições das substrings no ciphertext (Índice da primeira letra do grupo)
    ciphertext = remover_nao_letras(ciphertext)

    for i in range(len(ciphertext) - (tamanho_grupo+1)): # Decrementa tamanho_grupo+1 e evita IndexError
        grupo_selecionado = ciphertext[i:i+tamanho_grupo] # Ex: "FWC", "OXO", "ABA"...
        if (grupo_selecionado in repeticoes_por_grupo):
            repeticoes_por_grupo[grupo_selecionado].append(i) # Acrescenta posição à lista de intercorrências
        else:
            repeticoes_por_grupo[grupo_selecionado] = [i] # Salva posição da primeira intercorrência
    
    for key in list(repeticoes_por_grupo.keys()): # Itera em cada substring chave
        if (len(repeticoes_por_grupo[key]) == 1):
            del repeticoes_por_grupo[key] # Remove pares substrings sem repetição
    return repeticoes_por_grupo


def encontrar_espacamentos(repeticoes_por_grupo:dict) -> list:
    """
    Para cada grupo repetido, calcula as distâncias entre as repetições (espaçamentos) consecutivas.
    Esses espaçamentos são múltiplos do tamanho da chave, como consta nos vídeos de referência.
    """
    espacamentos = list()

    for posicoes in repeticoes_por_grupo.values():
        for i in range(len(posicoes) - 1):
            espacamentos.append(posicoes[i+1]-posicoes[i]) # Ex: [1, 3, 4] -> [2, 1]
    return espacamentos


def encontrar_divisores(espacamentos:list) -> list:
    """
    Encontra os divisores entre 2 e 20 que dividem exatamente cada espaçamento.
    Esses divisores são os tamanhos de chave possíveis.
    """
    divisores = list()

    for espacamento in espacamentos:
        for divisor in range(2, 21): # Verifica divisores/tamanhos de chave de tamanho 2 a 20 (Pula 0 e 1 como divisores)
            if (espacamento % divisor == 0): # Insere divisor na lista caso divida algum espaçamento específico
                divisores.append(divisor)
    return divisores


def estimar_tamanho_chave(divisores:list) -> list:
    """
    Método Kaneki propõe que o divisor mais comum dos espaçamentos das substrings de três caracteres
    é a melhor estimativa do tamanho da chave. 

    Retorna uma lista ordenada dos candidatos (tamanhos) mais prováveis.
    """
    # Encontrar divisores mais comuns (possíveis tamanhos de chave)
    freq_divisor = dict()

    # Monta hashmap com os divisores e suas respectivas frequências
    for divisor in divisores:
        if (divisor not in freq_divisor):
            freq_divisor[divisor] = 1
        else:
            freq_divisor[divisor] += 1
    
    tamanhos_estimados = list()
    # Ordena os tamanhos possíveis de chave de acordo com a frequência (Maior -> Menor)
    for _ in range(len(freq_divisor)):
        freq_maior = 0
        tamanho_chave = 0 # Tamanho de chave mais provável por iteração
        for divisor in freq_divisor:
            if (freq_divisor[divisor] > freq_maior):
                tamanho_chave = divisor # Atualiza maior valor temporário
                freq_maior = freq_divisor[divisor]
        tamanhos_estimados.append(tamanho_chave) # Divisor mais comum do laço
        del freq_divisor[tamanho_chave]
    return tamanhos_estimados


def agrupar_letras_igualmente_deslocadas(ciphertext: str, tamanhos_estimados: list, seletor_estimado=0) -> list:
    """
    Monta uma lista com grupos de letras igualmente deslocadas. Cada grupo funciona como uma Cifra de César.

    Exemplo: 
    - Chave "KEY" com tamanho 3 e ciphertext "AbCdEfGhIjKl"
    - Grupos decorrentes da cifragem ("A", "d", "G", "j"), ("b", "E", "h", "K") e ("C", "f", "I", "l")
    - O primeiro grupo foi todo cifrado por "K", o segundo por "E" e o terceiro por "Y"
    *Obs: Número de agrupamentos = tamanho da chave
    """
    agrupamentos_igualmente_deslocados = list()
    agrupamento = list() # Agrupamento temporário pra iteração
    tamanho_chave = tamanhos_estimados[seletor_estimado] # Escolhe um tamanho possível de chave
    ciphertext = remover_nao_letras(ciphertext) # Remove pontuação e espaços: apenas caracteres que foram cifrados

    for i in range(tamanho_chave): # Número de agrupamentos equivale ao tamanho da chave
        # Agrupa as letras cifradas pela mesma parte (mesma letra, mesma posição) da chave
        # Exemplo de agrupamento: i=0 -> índices 0, 3, 6, 9... se tamanho_chave=3
        for j in range(i, len(ciphertext), tamanho_chave):
            agrupamento.append(ciphertext[j])
        agrupamentos_igualmente_deslocados.append(agrupamento)
        agrupamento = list() # Reinicializa o agrupamento temporário
    return agrupamentos_igualmente_deslocados


def descobrir_melhor_deslocamento(agrupamento: str, freq_esperada: dict) -> int:
    """
    Calcula o melhor deslocamento (de 0 a 25) pro grupo, comparando a frequência observada 
    com a frequência esperada para o idioma.
    """
    total = len(agrupamento) # Total de letras no grupo
    contagem = Counter(agrupamento) # Frequência observada no agrupamento
    menor_erro = float('inf') # Inicializa auxiliar
    melhor_deslocamento = 0 # Inicializa auxiliar

    # Testa todos os possíveis deslocamentos (de 0 a 25)
    for desloc in range(26):
        erro = 0
        for letra, freq_esp in freq_esperada.items(): # Pra cada letra
            # Tenta descriptografar letra cifrada do agrupamento com deslocamento reverso
            letra_original = chr((ord(letra) - ord('A') + desloc) % 26 + ord('A'))
            # Frequência observada da letra deslocada no agrupamento
            freq_obs = (contagem.get(letra_original, 0) / total) * 100
            # Soma o erro
            erro += (freq_obs - freq_esp) ** 2
        # Atualiza o melhor deslocamento, caso haja algum com erro menor
        if (erro < menor_erro):
            menor_erro = erro
            melhor_deslocamento = desloc
    return melhor_deslocamento


def descobrir_chave_por_frequencia(ciphertext: str, idioma: str, opcao_chave=0) -> str:
    """
    Executa o ataque de análise de frequência usando as etapas:
    1) estima tamanho da chave (Kasiski)
    2) agrupa letras igualmente cifradas pela mesma posição da chave
    3) pra cada grupo, aplica análise de frequência
    Por fim, retorna a chave mais provável. O parâmetro opcional permite testar os próximos tamanhos mais prováveis.
    """
    frequencia_portugues = {
        'A': 14.63, 'B': 1.04, 'C': 3.88, 'D': 4.99, 
        'E': 12.57, 'F': 1.02, 'G': 1.30, 'H': 1.28,
        'I': 6.18, 'J': 0.40, 'K': 0.02, 'L': 2.78,
        'M': 4.74, 'N': 5.05, 'O': 10.73, 'P': 2.52, 
        'Q': 1.20, 'R': 6.53, 'S': 7.81, 'T': 4.34,
        'U': 4.63, 'V': 1.67, 'W': 0.01, 'X': 0.21, 
        'Y': 0.01, 'Z': 0.47
    }

    frequencia_ingles = {
        'A': 8.167, 'B': 1.492, 'C': 2.782, 'D': 4.253, 
        'E': 12.702, 'F': 2.228, 'G': 2.015, 'H': 6.094,
        'I': 6.966, 'J': 0.153, 'K': 0.772, 'L': 4.025,
        'M': 2.406, 'N': 6.749, 'O': 7.507, 'P': 1.929, 
        'Q': 0.095, 'R': 5.987, 'S': 6.327, 'T': 9.056,
        'U': 2.758, 'V': 0.978, 'W': 2.360, 'X': 0.150, 
        'Y': 1.974, 'Z': 0.074
    }

    # Considera a frequência de letras do idioma selecionado
    frequencia_idioma = frequencia_portugues if (idioma == "Português") else frequencia_ingles

    # ============ Início Kasiki ============
    repeticoes = encontrar_repeticoes(ciphertext)
    espacamentos = encontrar_espacamentos(repeticoes)
    divisores = encontrar_divisores(espacamentos)
    tamanhos_estimados = estimar_tamanho_chave(divisores)
    # ============ Final  Kasiki ============

    agrupamentos = agrupar_letras_igualmente_deslocadas(ciphertext, tamanhos_estimados, opcao_chave)
    chave = ''
    
    for agrupamento in agrupamentos:
        desloc = descobrir_melhor_deslocamento(agrupamento, frequencia_idioma) # Toma o melhor deslocamento pro grupo
        # A letra_chave é a que foi usada para deslocar
        letra_chave = chr(desloc + ord('A')) # Obtém a letra da chave pelo deslocamento que ela causou
        chave += letra_chave # Monta a chave final
    return chave
