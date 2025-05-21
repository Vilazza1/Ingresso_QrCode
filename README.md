🎟️ Ingresso_QrCode

        Esse projeto foi desenvolvido para ajudar a empresa StrelaPet na organização do seu evento de 30 anos, que será realizado no dia 27/05/2025.
        O objetivo principal do sistema é permitir o cadastro de convidados e o controle de acesso por meio de QR Codes únicos, tanto para o titular quanto para o acompanhante.

📌 Funcionalidades

        ✅ Cadastro de convidados com ou sem acompanhante

        ✅ Geração de QR Code para cada ingresso (titular e acompanhante)

        ✅ Validação dos ingressos via leitura de QR Code

        ✅ Controle de uso do ingresso (impede reutilização)

        ✅ Visualização e download do QR Code gerado

🧰 Tecnologias Utilizadas
        
        🔙 Backend
                Python 3

                Flask – Microframework para construção da API REST

                Flask-CORS – Permite requisições entre domínios (CORS)

                Flask-SQLAlchemy – ORM que simplifica a manipulação do banco SQLite

                qrcode – Biblioteca para geração de QR Codes

                SQLite – Banco de dados leve e local

        🔜 Frontend
                Vue.js 3 – Framework reativo para construção da interface

                Vite – Ferramenta moderna para build e hot reload

                Axios – Biblioteca para fazer requisições HTTP com facilidade

🧠 Lógica de Funcionamento

        Cadastro e Geração dos Códigos
        Ao cadastrar um novo convidado, o sistema gera dois códigos únicos:

        Um para o titular (ING00001T)

        Um para o acompanhante, se existir (ING00001A)

        Esses códigos são salvos no banco de dados e usados para gerar QR Codes individuais.

        Os QR Codes são imagens salvas temporariamente no servidor e disponibilizadas via link.

        Validação de Ingressos
        Quando o QR Code é escaneado, o sistema acessa a rota /validar/<codigo>.

        A API verifica:

        Se o código existe

        Se já foi utilizado anteriormente
        
        Se for um código válido e ainda não utilizado, o ingresso é marcado como usado e a entrada é autorizada.

        Caso o código já tenha sido usado, o sistema exibe uma mensagem de erro, impedindo o acesso duplicado.

🚀 Como Executar o Projeto

🔧 Requisitos
Python 3 instalado

Node.js e npm instalados

▶️ Backend (API Flask)
bash
Copiar
Editar
cd backend
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
pip install -r requirements.txt
python app.py
A API será executada em:
👉 http://127.0.0.1:10000

🖥️ Frontend (Vue.js)
bash
Copiar
Editar
cd frontend
npm install
npm run dev
A interface será acessível em:
👉 http://localhost:5173

✅ Validação de Ingressos
Cada QR Code gerado aponta para uma URL como:
http://SEU_DOMINIO/validar/<codigo>

A leitura do QR Code valida o ingresso no sistema e o marca como "usado".

Tentativas de reutilização mostram uma mensagem de erro.
