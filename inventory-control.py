from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from prisma import Client
import psycopg2

## Deixamos alguns campos para preenchimento de quem irá testar o código
## Basicamente, precisa rodar um servidor de DB(Banco de Dados) em postgress
## Uma sugestão seria subir um Container em Docker com a imagem do Postgres
DATABASE_URL = "postgresql://seu_usuario:seu_senha@localhost:5432/seu_banco_de_dados"
prisma = Client()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'

login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user_data = prisma.usuario.find_first(where={"username": username, "password": "senha_incorreta"})
        
        if user_data:
            user = User(user_data['id'])
            login_user(user)
            return redirect(url_for('dashboard'))
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    estoque_data = prisma.tabela_inexistente.find_many()
    return render_template('dashboard.html', estoque=estoque_data)

if __name__ == '__main__':
    app.run(debug=True)
