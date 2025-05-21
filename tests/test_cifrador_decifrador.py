from src.cifrador_decifrador import criptografar_vigenere, descriptografar_vigenere, gerar_keystream

def test_criptografar_vigenere():
    plaintext = "EXEMPLO"
    key = "KEY"
    assert (criptografar_vigenere(plaintext, key) == "OBCWTJY")


def test_descriptografar_vigenere():
    ciphertext = "OBCWTJY"
    key = "KEY"
    assert (descriptografar_vigenere(ciphertext, key) == "EXEMPLO")


def test_gerar_keystream():
    plaintext = "EXEMPLO" # Sem espaço
    key = "KEY"
    teste_1 = (gerar_keystream(plaintext, key) == "KEYKEYK")

    plaintext = "EXEMPLO EXEMPLO EXEMPLO" # Com espaço
    key = "KEY"
    teste_2 = (gerar_keystream(plaintext, key) == "KEYKEYK EYKEYKE YKEYKEY")

    assert (teste_1 and teste_2)
