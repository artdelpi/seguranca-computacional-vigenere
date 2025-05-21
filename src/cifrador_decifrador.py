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

        # Quando posição passa de 90, volta pra 'A' (-26 posições) e continua deslocamento
        if (nova_posicao > 90):
            nova_posicao -= 26 # Volta a mapear uma letra maiúscula

        char_cifrado = chr(nova_posicao)
        ciphertext += char_cifrado
    return ciphertext


def descriptografar_vigenere(ciphertext:str, key: str) -> str:
    # Conceito de des-deslocar
    ciphertext, key = map(str.upper, [ciphertext, key])
    keystream = gerar_keystream(ciphertext, key)
    plaintext = ""

    for i in range(len(ciphertext)):
        # Sabendo que |x-y| = |y-x|, pegar o deslocamento contrário é inverter a order das parcelas
        deslocamento = ord('A') - ord(keystream[i]) # Deslocamento no sentido contrário
        nova_posicao = ord(ciphertext[i]) + deslocamento

        # Quando posição fica abaixo de 65, precisa subir 26 posições e continua deslocamento
        if (nova_posicao < 65):
            nova_posicao += 26 # Volta a mapear uma letra maiúscula

        char_decifrado = chr(nova_posicao)
        plaintext += char_decifrado
    return plaintext

# print(gerar_keystream("TESTE", "KEY"))
# print(criptografar_vigenere("TESTE", "KEY"))
# print(descriptografar_vigenere("DIQDI", "KEY"))