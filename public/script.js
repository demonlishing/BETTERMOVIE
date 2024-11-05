async function register() {
    const username = document.getElementById("register-username").value;
    const email = document.getElementById("register-email").value;
    const password = document.getElementById("register-password").value;

    const response = await fetch('/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password })
    });

    const result = await response.json();
    alert(result.message);

    // Limpa os campos de cadastro após o envio
    document.getElementById("register-username").value = '';
    document.getElementById("register-email").value = '';
    document.getElementById("register-password").value = '';
}

async function login() {
    const username = document.getElementById("login-username").value;
    const password = document.getElementById("login-password").value;

    const response = await fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });

    const result = await response.json();
    alert(result.message);

    if (response.ok) {
        // Aqui você pode redirecionar para a página de cadastro de filmes
        window.location.href = 'filmes.html'; // Altere para a URL correta da página de filmes
    } else {
        // Limpa os campos de login se falhar
        document.getElementById("login-username").value = '';
        document.getElementById("login-password").value = '';
    }
}
