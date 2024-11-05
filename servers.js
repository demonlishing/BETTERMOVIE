const http = require('http');
const fs = require('fs');
const path = require('path');

const porta = 3000;
const USERS_FILE = 'users.json';
const MOVIES_FILE = 'movies.json';

// Função para carregar os dados de um arquivo JSON
function loadJSON(filePath) {
    if (fs.existsSync(filePath)) {
        return JSON.parse(fs.readFileSync(filePath, 'utf8'));
    }
    return {};
}

// Função para salvar dados em um arquivo JSON
function saveJSON(filePath, data) {
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
}

// Servidor HTTP
const server = http.createServer((req, res) => {
    // Serve o arquivo index.html e outros arquivos estáticos
    if (req.url === '/' && req.method === 'GET') {
        fs.readFile(path.join(__dirname, 'public', 'index.html'), (err, content) => {
            if (err) throw err;
            res.writeHead(200, { 'Content-Type': 'text/html' });
            res.end(content);
        });
    } else if (req.url === '/style.css' && req.method === 'GET') {
        fs.readFile(path.join(__dirname, 'public', 'style.css'), (err, content) => {
            if (err) throw err;
            res.writeHead(200, { 'Content-Type': 'text/css' });
            res.end(content);
        });
    } else if (req.url === '/script.js' && req.method === 'GET') {
        fs.readFile(path.join(__dirname, 'public', 'script.js'), (err, content) => {
            if (err) throw err;
            res.writeHead(200, { 'Content-Type': 'application/javascript' });
            res.end(content);
        });
    }

    // Endpoint de cadastro
    else if (req.url === '/register' && req.method === 'POST') {
        let body = '';
        req.on('data', chunk => {
            body += chunk.toString();
        });
        req.on('end', () => {
            const { username, email, password } = JSON.parse(body);
            const users = loadJSON(USERS_FILE);
            
            if (users[username]) {
                res.writeHead(400, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ message: 'Usuário já existe' }));
            } else {
                users[username] = { email, password };
                saveJSON(USERS_FILE, users);
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ message: 'Usuário cadastrado com sucesso!' }));
            }
        });
    }

    // Endpoint de login
    else if (req.url === '/login' && req.method === 'POST') {
        let body = '';
        req.on('data', chunk => {
            body += chunk.toString();
        });
        req.on('end', () => {
            const { username, password } = JSON.parse(body);
            const users = loadJSON(USERS_FILE);

            if (users[username] && users[username].password === password) {
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ message: 'Login bem-sucedido!', username }));
            } else {
                res.writeHead(401, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ message: 'Nome de usuário ou senha inválidos.' }));
            }
        });
    }

    // Endpoint para adicionar filme
    else if (req.url === '/add-movie' && req.method === 'POST') {
        let body = '';
        req.on('data', chunk => {
            body += chunk.toString();
        });
        req.on('end', () => {
            const { username, movieName, rating } = JSON.parse(body);
            const movies = loadJSON(MOVIES_FILE);

            if (!movies[username]) {
                movies[username] = [];
            }
            movies[username].push({ name: movieName, rating });
            saveJSON(MOVIES_FILE, movies);

            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ message: 'Filme cadastrado com sucesso!' }));
        });
    }

    else {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('404 Not Found');
    }
});

server.listen(porta, () => {
    console.log(`Servidor rodando em http://localhost:${porta}/`);
});
