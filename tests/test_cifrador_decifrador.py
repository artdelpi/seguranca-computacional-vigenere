from src.cifrador_decifrador import criptografar_vigenere, descriptografar_vigenere, gerar_keystream

def test_criptografar_vigenere():
    plaintext = "EXEMPLO" # Letra maiúscula sem espaço
    key = "KEY"
    teste_1 = (criptografar_vigenere(plaintext, key) == "OBCWTJY")

    plaintext = "EXEMPLO EXEMPLO" # Letra maiúscula com espaço
    key = "KEY"
    teste_2 = (criptografar_vigenere(plaintext, key) == "OBCWTJY IVOQNVS")

    plaintext = "exemplo" # Letra minúscula
    key = "KEY"
    teste_3 = (criptografar_vigenere(plaintext, key) == "OBCWTJY") # Cifra gerada sempre em upper case

    assert (teste_1 and teste_2 and teste_3)


def test_descriptografar_vigenere():
    ciphertext = "OBCWTJY" # Letra maiúscula sem espaço
    key = "KEY"
    teste_1 = (descriptografar_vigenere(ciphertext, key) == "EXEMPLO")

    ciphertext = "OBCWTJY IVOQNVS" # Letra maiúscula com espaço
    key = "KEY"
    teste_2 = (descriptografar_vigenere(ciphertext, key) == "EXEMPLO EXEMPLO")

    ciphertext = "obcwtjy" # Letra minúscula
    key = "KEY"
    teste_3 = (descriptografar_vigenere(ciphertext, key) == "EXEMPLO") # Plaintext gerado sempre em upper case

    assert (teste_1 and teste_2 and teste_3)


def test_gerar_keystream():
    plaintext = "EXEMPLO" # Sem espaço
    key = "KEY"
    teste_1 = (gerar_keystream(plaintext, key) == "KEYKEYK")

    plaintext = "EXEMPLO EXEMPLO EXEMPLO" # Com espaço
    key = "KEY"
    teste_2 = (gerar_keystream(plaintext, key) == "KEYKEYK EYKEYKE YKEYKEY")

    assert (teste_1 and teste_2)
