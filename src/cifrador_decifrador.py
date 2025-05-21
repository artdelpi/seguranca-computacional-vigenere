def gerar_keystream(plaintext: str, key: str) -> str:
    """
    Gera o keystream para a cifra de Vigenère.

    Observação: Tirar o resto pelo tamanho da chave garante que o resultado é um valor 
    entre zero e a chave-1. Isto é, valores válidos de índice pros elementos da chave.

    Parâmetros:
        plaintext (str): O texto a ser cifrado.
        key (str): A chave de Vigenère.

    Retorna:
        str: O keystream com o mesmo tamanho do plaintext, mantendo os espaços.
    """
    keystream = ""
    key_index = 0 # Com rigor, na verdade o índice da chave é key_index % len(key)

    for i in range(len(plaintext)):
        if (plaintext[i] != " "):
            keystream += key[key_index % len(key)] # Mantém índice < len(key)
            key_index += 1 # "Avança" de caracter na chave
        else:
            keystream += " "
    return keystream.upper()


def criptografar_vigenere(plaintext: str, key: str) -> str:
    plaintext, key = map(str.upper, [plaintext, key])
    keystream = gerar_keystream(plaintext, key)
    ciphertext = ""

    # Iteração com índice pra correspondência de caracteres do keystream e plaintext
    for i in range(len(plaintext)):
        deslocamento = ord(keystream[i]) - ord('A') # Decimal de 'A' é a base de cálculo
        nova_posicao = ord(plaintext[i]) + deslocamento # Posição do char cifrado na tabela ASCII

        if (nova_posicao > 90): 
            nova_posicao -= 26 # "Recomeça" deslocamento a partir de 'A' se passar de 90 ('Z')

        char_cifrado = chr(nova_posicao)
        ciphertext += char_cifrado
    return ciphertext


def descriptografar_vigenere(ciphertext:str, key: str) -> str:
    pass
