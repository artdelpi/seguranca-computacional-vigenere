from cifrador_decifrador import criptografar_vigenere, descriptografar_vigenere

"""
Método Kasiki, demonstrado no vídeo:
https://www.youtube.com/watch?v=P4z3jAOzT9I
"""

def remover_nao_letras(plaintext:str) -> str:
    return "".join([char for char in plaintext if char.isalpha()]).upper() # Remove não-letras e capitaliza


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


def estimar_tamanho_chave(divisores:list) -> list:
    """
    Método Kaneki propõe que o divisor mais comum dos espaçamentos das substrings de três
    caracteres é a melhor estimativa do tamanho da chave. 

    Retorna: 3 divisores mais comuns das distâncias entre as substrings
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
    for _ in range(3):
        freq_maior = 0
        tamanho_chave = 0 # Tamanho de chave mais provável por iteração
        for divisor in freq_divisor:
            if (freq_divisor[divisor] > freq_maior):
                tamanho_chave = divisor # Atualiza maior valor temporário
                freq_maior = freq_divisor[divisor]
        tamanhos_estimados.append(tamanho_chave) # Divisor mais comum do laço
        del freq_divisor[tamanho_chave]
    return tamanhos_estimados

"""
Método Kasiki é pra estimar o tamanho da chave. Agora, segue o ataque de frequência.
"""


def agrupar_letras_igualmente_deslocadas(ciphertext: str, tamanhos_estimados: list, seletor_estimado=0) -> list:
    """
    Retorna lista com grupos de letras igualmente deslocadas. Análise por grupo análoga à 
    Cifra de César pra encontrar a letra da chave responsável pelo shift.
    """
    agrupamentos_igualmente_deslocados = list() # Reúne os grupos de letras com mesmo shift
    agrupamento = list() # Agrupamento individual de letras com mesmo deslocamento
    tamanho_chave = tamanhos_estimados[seletor_estimado] # Seleciona tamanho de chave mais provável
    ciphertext = remover_nao_letras(ciphertext) # Só caracteres deslocados

    # AbcDefGhiJklMno; [index, index+Tamanho, index+tamanho+tamanho...]
    for i in range(tamanho_chave): # Número de agrupamentos é o tamanho da chave (3)
        # Começa do índice da primeira letra, vai até ciphertext/tamanho(até porque divide a cifra pelo tamanho(num_grupos)), incrementa de tamanho da chave em tamanho da chave
        for j in range(i, len(ciphertext), tamanho_chave): # Pra saber se uma letra pertence ao agrupamento, basta pegar o índice de partida de uma letra da chave e incrementar de tamanho em tamanho: Chave: Key. Primeiro grupo, pega primeira letra K de índice 0: (0,3,6,9...). A próxima: (1,4,7,10...)
            agrupamento.append(ciphertext[j])
        agrupamentos_igualmente_deslocados.append(agrupamento)
        agrupamento = list() # Reinicializa o agrupamento individual
    return agrupamentos_igualmente_deslocados


from collections import Counter


def descobrir_melhor_deslocamento(coluna: str, freq_esperada: dict) -> int:
    total = len(coluna)
    contagem = Counter(coluna)
    menor_erro = float('inf')
    melhor_deslocamento = 0

    for desloc in range(26):
        erro = 0
        for letra, freq_esp in freq_esperada.items():
            # CORREÇÃO: aplica deslocamento positivo
            letra_original = chr((ord(letra) - ord('A') + desloc) % 26 + ord('A'))
            freq_obs = (contagem.get(letra_original, 0) / total) * 100
            erro += (freq_obs - freq_esp) ** 2
        if erro < menor_erro:
            menor_erro = erro
            melhor_deslocamento = desloc

    return melhor_deslocamento


def descobrir_chave_por_frequencia(ciphertext: str, tamanhos_estimados: list) -> str:
    grupos = agrupar_letras_igualmente_deslocadas(ciphertext, tamanhos_estimados)
    chave = ''
    
    for grupo in grupos:
        desloc = descobrir_melhor_deslocamento(grupo, frequencia_ingles)
        # A letra da chave é a que foi usada para deslocar (não o inverso)
        letra_chave = chr(desloc + ord('A'))
        chave += letra_chave
    
    return chave

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



# Teste com mensagem e chave conhecidas
mensagem_teste = (
    "The field of cryptanalysis has grown tremendously in recent years. "
    "Modern cryptographic systems rely on complex algorithms that are resistant "
    "to traditional attacks. However, historical ciphers like the Vigenere cipher "
    "remain important for understanding cryptographic principles."
)

texto_cifrado = criptografar_vigenere(mensagem_teste, "KEY")
print("Texto cifrado:")
print(texto_cifrado)
print("\nTexto descriptografado com chave correta:")
print(descriptografar_vigenere(texto_cifrado, "KEY"))

# Análise Kasiski
repeticoes = encontrar_repeticoes(texto_cifrado)
espacamentos = encontrar_espacamentos(repeticoes)
divisores = encontrar_divisores(espacamentos)
tamanhos_estimados = estimar_tamanho_chave(divisores)

print("\nTamanhos de chave estimados (mais prováveis primeiro):")
print(tamanhos_estimados)

# Ataque de frequência
chave_descoberta = descobrir_chave_por_frequencia(texto_cifrado, tamanhos_estimados)
print(f"\n🔑 Chave descoberta: {chave_descoberta}")

print("\nTexto descriptografado com chave descoberta:")
print(descriptografar_vigenere(texto_cifrado, chave_descoberta))