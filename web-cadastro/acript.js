document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('registerForm');
    const successArea = document.getElementById('successArea');

    if (!form) {
        console.error("ERRO: O formulário 'registerForm' não foi encontrado!");
        return;
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Feedback visual no botão
        const btn = form.querySelector('button');
        btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Processando...';
        btn.disabled = true;

        const payload = {
            full_name: document.getElementById('full_name').value,
            email: document.getElementById('email').value,
            password: document.getElementById('password').value,
            phone: document.getElementById('phone').value || "", 
            birth_date: document.getElementById('birth_date').value || null
        };

        try {
            const response = await fetch('http://localhost:9999/users', { 
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                // A MÁGICA AQUI: Remove a classe que esconde e adiciona a que mostra
                form.classList.add('hidden'); 
                successArea.classList.remove('hidden');
                // Garante que o display não bloqueie
                successArea.style.display = 'block'; 
            } else {
                const errorData = await response.json();
                alert('Erro na API: ' + JSON.stringify(errorData.detail));
                btn.innerHTML = 'Finalizar Cadastro <i class="fa-solid fa-arrow-right"></i>';
                btn.disabled = false;
            }
        } catch (error) {
            console.error('Erro de conexão:', error);
            alert('Erro: A API na porta 9999 não respondeu. O Docker subiu?');
            btn.innerHTML = 'Finalizar Cadastro <i class="fa-solid fa-arrow-right"></i>';
            btn.disabled = false;
        }
    });
});