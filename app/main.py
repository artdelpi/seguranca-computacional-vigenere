from flask import Flask, render_template, request
from src.cifrador_decifrador import criptografar_vigenere, descriptografar_vigenere
from src.ataque_recuperador_chave import descobrir_chave_por_frequencia

app = Flask(__name__)
seletor_global = {'valor': 0}

@app.route("/", methods=["GET", "POST"])
def index():
    resultado_cript = ""
    resultado_descript = ""
    msg_cript = ""
    chave_cript = ""
    msg_descript = ""
    chave_descript = ""

    if request.method == "POST":
        modo = request.form.get("modo")

        if modo == "criptografar":
            msg_cript = request.form["msg_criptografar"]
            chave_cript = request.form["chave_cript"]
            resultado_cript = criptografar_vigenere(msg_cript, chave_cript)

        elif modo == "descriptografar":
            msg_descript = request.form["msg_descriptografar"]
            chave_descript = request.form["chave_descript"]
            resultado_descript = descriptografar_vigenere(msg_descript, chave_descript)

    return render_template("index.html",
                           resultado_cript=resultado_cript,
                           resultado_descript=resultado_descript,
                           msg_cript=msg_cript,
                           chave_cript=chave_cript,
                           msg_descript=msg_descript,
                           chave_descript=chave_descript)


@app.route("/ataque", methods=["GET", "POST"])
def ataque():
    resultado = ""
    chave_estimada = ""
    idioma = request.form.get("idioma", "Inglês")
    msg = ""
    fim_de_tentativas = False

    if request.method == "POST":
        msg = request.form["msg_ataque"]
        modo = request.form["modo"]

        if modo == "ataque":
            seletor_global["valor"] = 0
        elif modo == "proxima_chave":
            seletor_global["valor"] += 1

        seletor = seletor_global["valor"]
        chave_estimada, _ = descobrir_chave_por_frequencia(msg, idioma, seletor)

        if chave_estimada is None:
            fim_de_tentativas = True
            seletor_global["valor"] -= 1
            resultado = "Não há mais chaves possíveis com base na análise de frequência."
        else:
            resultado = descriptografar_vigenere(msg, chave_estimada)

    return render_template("ataque.html",
                           resultado=resultado,
                           chave_estimada=chave_estimada,
                           idioma=idioma,
                           fim=fim_de_tentativas,
                           msg=msg)


if __name__ == "__main__":
    app.run(debug=True)
