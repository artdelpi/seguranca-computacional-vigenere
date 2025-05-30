"""
from src.ataque_recuperador_senha import remover_nao_letras, encontrar_repeticoes, agrupar_letras_igualmente_deslocadas, estimar_tamanho_chave, encontrar_espacamentos, encontrar_divisores, descobrir_chave_por_frequencia
from src.cifrador_decifrador import descriptografar_vigenere, criptografar_vigenere, gerar_keystream

def remover_nao_letras():
    pass


def encontrar_repeticoes():
    pass


def test_encontrar_espacamentos():
    pass


def test_encontrar_divisores():
    pass


def test_estimar_tamanho_chave():
    pass


def test_agrupar_letras_igualmente_deslocadas():
    # Monta grupos de letras com o mesmo deslocamento no ciphertext
    ciphertext = "ABCDEFGHIJKLMNOPQRSTUV"
    tamanho_chave = 3
    agrupamento_esperado = [['A', 'D', 'G', 'J', 'M', 'P', 'S', 'V'], 
                            ['B', 'E', 'H', 'K', 'N', 'Q', 'T'], 
                            ['C', 'F', 'I', 'L', 'O', 'R', 'U']]
    teste_1 = (test_agrupar_letras_igualmente_deslocadas(ciphertext, tamanho_chave) == agrupamento_esperado)

    assert(teste_1)


def test_descobrir_melhor_deslocamento():
    pass


def test_descobrir_chave_por_frequencia():
    plaintext = (
        "The House of Representatives shall be composed of Members "
        "chosen every second Year by the People of the several States, and the Electors "
        "in each State shall have the Qualifications requisite for "
        "Electors of the most numerous Branch of the State Legislature."

        "No Person shall be a Representative who shall not have attained to the "
        "Age of twenty five Years, and been seven Years a Citizen of the United States, "
        "and who shall not, when elected, be an Inhabitant of that State in which he shall be chosen."

        "Representatives and direct Taxes shall be apportioned among the several States "
        "which may be included within this Union, according to their "
        "respective Numbers, which shall be determined by adding to the whole Number "
        "of free Persons, including those bound to Service for a Term of Years, "
        "and excluding Indians not taxed, three fifths of all other Persons. "
        "The actual Enumeration shall be made within three Years after the first "
        "Meeting of the Congress of the United States, and within every subsequent "
        "Term of ten Years, in such Manner as they shall by Law direct.The Number of Representatives "
        "shall not exceed one for every thirty Thousand, but each State shall have at Least one Representative; "
        "and until such enumeration shall be made, the State of New Hampshire shall "
        "be entitled to chuse three, Massachusetts eight, Rhode-Island and Providence Plantations one, "
        "Connecticut five, New-York six, New Jersey four, Pennsylvania eight, "
        "Delaware one, Maryland six, Virginia ten, North Carolina five, South Carolina five, and Georgia three."

        "When vacancies happen in the Representation from any State, "
        "the Executive Authority thereof shall issue Writs of Election to fill such Vacancies."

        "The House of Representatives shall chuse their Speaker and other Officers;"
        "and shall have the sole Power of Impeachment."
    ) # String extensa, sem acentos
    ciphertext = criptografar_vigenere(plaintext, "CRYPTOGRAPHY")
    chave_descoberta = descobrir_chave_por_frequencia(ciphertext, "Inglês") # Considera frequência de letras do Inglês
    chave_esperada = "CRYPTOGRAPHY"
    teste_1 = (chave_esperada == chave_descoberta)

    assert(teste_1)
"""
