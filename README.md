# Cifra de Vigenère - Segurança Computacional (CIC0201)

Este projeto implementa a cifra de Vigenère com:

- Cifrador e decifrador
- Ataque de recuperação de chave por análise de frequência (Kasiski + frequência)
- Interface gráfica (Tkinter)
- Execução via terminal (modo texto)

## Pré-requisitos

O projeto requer Python 3.x e as seguintes dependências:
- pytest (para testes)

## Como executar

O arquivo principal do projeto é o `main.py`.
- Basta executar:

```bash
python main.py
```

Ao rodá-lo, pode escolher entre duas formas de execução:

### 1. Interface gráfica (Tkinter)
Digite `1` e pressione Enter para abrir a interface com botões e campos para criptografar, descriptografar e atacar mensagens.

### 2. Execução no terminal (modo texto)
Digite `2` e pressione Enter para continuar no terminal e escolher entre:
- `1` Criptografar
- `2` Descriptografar
- `3` Ataque por frequência
