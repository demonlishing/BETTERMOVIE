import json
import os

# Nome do arquivo JSON
USERS_FILE = 'users.json'
MOVIES_FILE = 'movies.json'

# Função para carregar os usuários do arquivo JSON
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as file:
            users = json.load(file)
    else:
        users = {}
    
    # Adiciona o administrador padrão, se não existir
    if "admin" not in users:
        users["admin"] = {
            'email': "admin@system.com",
            'password': "123"
        }
        save_users(users)  # Salva o usuário admin no arquivo caso ele tenha sido adicionado

    return users

# Função para salvar os usuários no arquivo JSON
def save_users(users):
    with open(USERS_FILE, 'w') as file:
        json.dump(users, file)

# Função para cadastrar um novo usuário
def register_user():
    users = load_users()
    
    username = input("Digite o nome de usuário: ").lower()  # Salva o nome de usuário em caixa baixa
    email = input("Digite o email: ")
    password = input("Digite a senha: ")

    if username in users:
        print("Usuário já existe. Tente novamente.")
    else:
        users[username] = {
            'email': email,
            'password': password
        }
        save_users(users)
        print("Usuário cadastrado com sucesso!")

# Função para fazer login
def login_user():
    users = load_users()
    
    username = input("Digite o nome de usuário: ").lower()  # Converte o nome de usuário digitado para caixa baixa
    password = input("Digite a senha: ")

    if username in users and users[username]['password'] == password:
        print("Login bem-sucedido!")
        return username
    else:
        print("Nome de usuário ou senha inválidos.")
        return None

# Função para cadastrar um filme
def register_movie(username):
    movies = load_movies()

    movie_name = input("Digite o nome do filme: ")
    
    # Solicita a nota do filme e valida para garantir que está entre 0 e 5
    while True:
        try:
            rating = float(input("Digite a nota do filme (0 a 5): "))
            if 0 <= rating <= 5:
                break
            else:
                print("Por favor, insira uma nota entre 0 e 5.")
        except ValueError:
            print("Entrada inválida. Digite um número entre 0 e 5.")

    # Se o usuário ainda não tem filmes, cria uma lista vazia para ele
    if username not in movies:
        movies[username] = []
    
    # Adiciona o filme com nome e nota
    movies[username].append({
        "name": movie_name,
        "rating": rating
    })
    
    save_movies(movies)
    print(f"Filme '{movie_name}' cadastrado com sucesso!")

# Função para visualizar filmes cadastrados pelo usuário
def view_movies(username, is_admin=False):
    movies = load_movies()
    
    # Se for admin, exibe a lista de usuários e permite escolher de quem ver os filmes
    if is_admin:
        print("Usuários cadastrados:")
        for user in movies.keys():
            print(f"- {user}")
        selected_user = input("Digite o nome do usuário para ver os filmes: ").lower()
        
        # Verifica se o usuário selecionado existe na lista de filmes
        if selected_user in movies:
            user_movies = movies[selected_user]
            print(f"Filmes cadastrados por {selected_user}:")
        else:
            print("Usuário não possui filmes cadastrados.")
            return
    else:
        # Usuário comum vê apenas seus próprios filmes
        user_movies = movies.get(username, [])
        if user_movies:
            print(f"Filmes cadastrados por {username}:")
        else:
            print("Nenhum filme cadastrado.")
            return

    # Exibe a lista de filmes e suas notas
    for movie in user_movies:
        print(f"- {movie['name']} (Nota: {movie['rating']}/5)")

# Função para visualizar todos os usuários (apenas para admin)
def view_users():
    users = load_users()
    print("Usuários cadastrados no sistema:")
    for username, details in users.items():
        print(f"- {username} (Email: {details['email']})")

# Função para carregar os filmes do arquivo JSON
def load_movies():
    if os.path.exists(MOVIES_FILE):
        with open(MOVIES_FILE, 'r') as file:
            return json.load(file)
    return {}

# Função para salvar os filmes no arquivo JSON
def save_movies(movies):
    with open(MOVIES_FILE, 'w') as file:
        json.dump(movies, file)

# Função principal para o sistema
def main():
    while True:
        print("\n1. Cadastrar usuário")
        print("2. Login")
        print("3. Sair")
        choice = input("Escolha uma opção: ")

        if choice == '1':
            register_user()
        elif choice == '2':
            username = login_user()
            if username:
                if username == "admin":
                    # Menu especial para o administrador
                    while True:
                        print("\n1. Ver todos os usuários")
                        print("2. Ver filmes cadastrados")
                        print("3. Cadastrar filme")
                        print("4. Sair")
                        admin_choice = input("Escolha uma opção: ")

                        if admin_choice == '1':
                            view_users()
                        elif admin_choice == '2':
                            view_movies(username, is_admin=True)
                        elif admin_choice == '3':
                            register_movie(username)
                        elif admin_choice == '4':
                            break
                        else:
                            print("Opção inválida.")
                else:
                    # Menu padrão para usuário comum
                    while True:
                        print("\n1. Ver filmes cadastrados")
                        print("2. Cadastrar filme")
                        print("3. Sair")
                        user_choice = input("Escolha uma opção: ")

                        if user_choice == '1':
                            view_movies(username)
                        elif user_choice == '2':
                            register_movie(username)
                        elif user_choice == '3':
                            break
                        else:
                            print("Opção inválida.")
        elif choice == '3':
            print("Saindo do sistema.")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
