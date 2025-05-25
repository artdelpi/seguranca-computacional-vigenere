from tkinter import ttk, scrolledtext
import tkinter as tk
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.cifrador_decifrador import criptografar_vigenere, descriptografar_vigenere
from src.ataque_recuperador_senha import descobrir_chave_por_frequencia

# Indica índice da lista com os tamanhos de chave mais prováveis.
seletor = 0

def execucao_UI():
    def criptografar():
        msg = entrada_criptografar.get("1.0", "end").strip() # Obtém todo o texto inserido no ScrolledText
        chave = chave_cript.get().upper() # Obtém chave inserida
        resultado = criptografar_vigenere(msg, chave) # Gera ciphertext
        saida_criptografada.config(state="normal") # Permite escrita
        saida_criptografada.delete("1.0", "end") # Limpa ScrolledText antes de escrever novo resultado
        saida_criptografada.insert("end", resultado) # Escreve resultado no ScrolledText


    def descriptografar():
        msg = entrada_descriptografar.get("1.0", "end").strip()
        chave = chave_descript.get().upper() 
        resultado = descriptografar_vigenere(msg, chave)
        saida_descriptografado.config(state="normal")
        saida_descriptografado.delete("1.0", "end")
        saida_descriptografado.insert("end", resultado)


    def ataque_com_seletor():
        global seletor
        msg = entrada_ataque.get("1.0", "end").strip() # Obtém todo o texto inserido no ScrolledText
        idioma = idioma_combo.get() # Obtém idioma selecionado
        chave = descobrir_chave_por_frequencia(msg, idioma, seletor) # Encontra chave de tamanho mais provável
        resultado = descriptografar_vigenere(msg, chave) # Obtém plaintext
        chave_label.config(text=f"Chave estimada: {chave}")
        saida_ataque.config(state="normal")
        saida_ataque.delete("1.0", "end")
        saida_ataque.insert("end", resultado)
        saida_ataque.config(state="disabled")


    def tentar_proxima_chave():
        global seletor
        seletor += 1 # Incrementa seletor para próxima tentativa
        ataque_com_seletor()


    # Interface
    janela = tk.Tk()
    janela.title("Vigenère - Segurança Computacional")
    janela.geometry("800x735")

    # Área para Criptografar
    tk.Label(janela, text="Mensagem para criptografar:").pack()
    entrada_criptografar = scrolledtext.ScrolledText(janela, height=4)
    entrada_criptografar.pack()
    tk.Label(janela, text="Chave:").pack()
    chave_cript = tk.Entry(janela)
    chave_cript.pack()
    tk.Button(janela, text="Criptografar", command=criptografar).pack()
    saida_criptografada = scrolledtext.ScrolledText(janela, height=4, state="disabled")
    saida_criptografada.pack()

    # Área para Descriptografar
    tk.Label(janela, text="Mensagem cifrada para descriptografar:").pack()
    entrada_descriptografar = scrolledtext.ScrolledText(janela, height=4)
    entrada_descriptografar.pack()
    tk.Label(janela, text="Chave:").pack()
    chave_descript = tk.Entry(janela)
    chave_descript.pack()
    tk.Button(janela, text="Descriptografar", command=descriptografar).pack()
    saida_descriptografado = scrolledtext.ScrolledText(janela, height=4, state="disabled")
    saida_descriptografado.pack()

    # Área do Ataque de Frequência
    tk.Label(janela, text="Mensagem cifrada para ataque:").pack()
    entrada_ataque = scrolledtext.ScrolledText(janela, height=4)
    entrada_ataque.pack()
    tk.Label(janela, text="Idioma:").pack()
    idioma_combo = ttk.Combobox(janela, values=["Português", "Inglês"])
    idioma_combo.current(1)
    idioma_combo.pack()

    # Frame para botões lado a lado
    botoes_frame = tk.Frame(janela)
    botoes_frame.pack(pady=5)

    btn_melhor_chave = tk.Button(botoes_frame, text="Usar tamanho mais provável", command=ataque_com_seletor)
    btn_melhor_chave.pack(side="left", padx=5)

    btn_proxima_chave = tk.Button(botoes_frame, text="Tentar próxima chave", command=tentar_proxima_chave)
    btn_proxima_chave.pack(side="left", padx=5)

    chave_label = tk.Label(janela, text="Chave estimada: (nenhuma ainda)")
    chave_label.pack()
    saida_ataque = scrolledtext.ScrolledText(janela, height=5, state="disabled")
    saida_ataque.pack()

    janela.mainloop() # Roda interface gráfica


def execucao_terminal():
    print("=== Cifra de Vigenère - Execução via Terminal ===")
    print("Escolha uma opção:")
    print("1 - Criptografar")
    print("2 - Descriptografar")
    print("3 - Ataque por frequência")
    opcao = input("Opção: ").strip()

    if (opcao == "1"):
        plaintext = input("Mensagem para criptografar:\n")
        chave = input("Chave:\n").upper()
        resultado = criptografar_vigenere(plaintext, chave)
        print("\nTexto cifrado:")
        print(resultado)

    elif (opcao == "2"):
        ciphertext = input("Mensagem cifrada:\n")
        chave = input("Chave:\n").upper()
        resultado = descriptografar_vigenere(ciphertext, chave)
        print("\nTexto decifrado:")
        print(resultado)

    elif (opcao == "3"):
        ciphertext = input("Mensagem cifrada:\n")
        idioma = input("Idioma (Português ou Inglês):\n").capitalize()
        seletor = 0
        while True:
            chave = descobrir_chave_por_frequencia(ciphertext, idioma, seletor)
            resultado = descriptografar_vigenere(ciphertext, chave)
            print(f"\nTentativa {seletor + 1}")
            print(f"Chave estimada: {chave}")
            print(f"Texto decifrado:\n{resultado}")
            continuar = input("\nTentar próxima chave? (s/n): ").lower()
            if continuar != "s":
                break
            seletor += 1
    else:
        print("Opção inválida.")

if __name__ == "__main__":
    print("=== Cifra de Vigenère - Escolha uma das Opções ===")
    print("1 - Com UI - Tkinter")
    print("2 - Via Terminal")
    opcao = input("Digite o número: ").strip()

    if (opcao == "1"):
        execucao_UI()
    elif (opcao == "2"):
        execucao_terminal()
    else:
        print("Escolha uma opção válida: 1 ou 2")
