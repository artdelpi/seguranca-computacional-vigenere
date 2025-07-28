def gerar_keystream(plaintext: str, key: str) -> str:
    """
    Gera o keystream para a cifra de Vigenère.

    Observação: Tirar o resto pelo tamanho da chave garante que o resultado é um valor 
    entre zero e a chave-1. Isto é, valores válidos de índice pros elementos da chave.

    Args:
        plaintext (str): O texto a ser cifrado.
        key (str): A chave de Vigenère.

    Returns:
        str: O keystream com o mesmo tamanho do plaintext, mantendo os espaços.
    """
    keystream = ""
    key_index = 0 

    for i in range(len(plaintext)):
        if (plaintext[i].isalpha()):
            keystream += key[key_index % len(key)] # Mantém índice < len(key)
            key_index += 1 # "Avança" de caracter na chave
        else:
            keystream += " " # Concatena espaço se caracter for não-letra
    return keystream.upper()


def criptografar_vigenere(plaintext: str, key: str) -> str:
    """
    Cada caractere do plaintext é deslocado com base na letra correspondente do keystream,
    gerando o texto cifrado.

    Args:
        plaintext (str): O texto a ser cifrado.
        key (str): A chave de Vigenère.

    Returns:
        str: O texto cifrado.
    """
    plaintext, key = map(str.upper, [plaintext, key])
    keystream = gerar_keystream(plaintext, key)
    ciphertext = list()

    for i in range(len(plaintext)):
        char = plaintext[i]
        # Não criptografa caracteres especiais
        if char in (" ", ".", ",", ";", "-", "!", "'"):
            ciphertext.append(char)
        else:
            desloc = (ord(char) - ord('A') + ord(keystream[i]) - ord('A')) % 26
            ciphertext.append(chr(ord('A') + desloc))

    return ''.join(ciphertext)


def descriptografar_vigenere(ciphertext:str, key: str) -> str:
    """
    A descriptografia envolve aplicar o deslocamento inverso ao que foi feito na cifragem,
    com base no keystream derivado da chave.

    Args:
        ciphertext (str): O texto cifrado.
        key (str): A chave de Vigenère.

    Returns:
        str: O plaintext descriptografado.
    """
    ciphertext, key = map(str.upper, [ciphertext, key])
    keystream = gerar_keystream(ciphertext, key)
    plaintext = list()

    for i in range(len(ciphertext)): 
        char = ciphertext[i]
        # Não descriptografa caracteres especiais
        if char in (" ", ".", ",", ";", "-", "!", "'"):
            plaintext.append(char)
        else:
            desloc = (ord(char) - ord(keystream[i])) % 26
            plaintext.append(chr(ord('A') + desloc))

    return ''.join(plaintext)
