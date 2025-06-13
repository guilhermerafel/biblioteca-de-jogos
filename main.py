from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'minha-chave-secreta-unica'

jogos = [
    {"id": 1, "nome": "The Witcher 3", "genero": "RPG", "ano": 2015},
    {"id": 2, "nome": "Red Dead Redemption 2", "genero": "Ação-Aventura", "ano": 2018},
    {"id": 3, "nome": "Stardew Valley", "genero": "Simulação", "ano": 2016}
]


def novo_id():
    return max(jogo['id'] for jogo in jogos) + 1 if jogos else 1


@app.route('/')
def index():
    contagem_generos = {}
    for jogo in jogos:
        if jogo['genero'] in contagem_generos:
            contagem_generos[jogo['genero']] += 1
        else:
            contagem_generos[jogo['genero']] = 1
    return render_template('index.html', jogos=jogos, contagem=contagem_generos)


@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if request.method == 'POST':
        novo_jogo = {
            'id': novo_id(),
            'nome': request.form['nome'],
            'genero': request.form['genero'],
            'ano': int(request.form['ano'])
        }
        jogos.append(novo_jogo)
        flash('Jogo adicionado com sucesso!', 'success')
        return redirect(url_for('index'))
    return render_template('adicionar.html')


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    jogo = next((j for j in jogos if j['id'] == id), None)

    if not jogo:
        flash('Jogo não encontrado!', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        try:
            jogo['nome'] = request.form['nome']
            jogo['genero'] = request.form['genero']
            jogo['ano'] = int(request.form['ano'])
            flash('Jogo atualizado com sucesso!', 'success')
            return redirect(url_for('index'))
        except ValueError:
            flash('Ano deve ser um número válido!', 'danger')

    return render_template('editar.html', jogo=jogo)


@app.route('/excluir/<int:id>')
def excluir(id):
    global jogos
    jogos = [j for j in jogos if j['id'] != id]
    flash('Jogo excluído com sucesso!', 'info')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)