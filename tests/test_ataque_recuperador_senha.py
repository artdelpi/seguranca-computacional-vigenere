from src.ataque_recuperador_senha import remover_nao_letras, encontrar_repeticoes, agrupar_letras_igualmente_deslocadas

#def test_remover_nao_letras():
#    pass


#def test_encontrar_repeticoes():
#    pass

def test_agrupar_letras_igualmente_deslocadas():
    # Monta grupos de letras com o mesmo deslocamento no ciphertext
    ciphertext = "ABCDEFGHIJKLMNOPQRSTUV"
    tamanho_chave = 3
    agrupamento_esperado = [['A', 'D', 'G', 'J', 'M', 'P', 'S', 'V'], 
                            ['B', 'E', 'H', 'K', 'N', 'Q', 'T'], 
                            ['C', 'F', 'I', 'L', 'O', 'R', 'U']]
    test1 = (test_agrupar_letras_igualmente_deslocadas(ciphertext, tamanho_chave) == agrupamento_esperado)

    assert(test1)