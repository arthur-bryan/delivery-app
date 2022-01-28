# Demonstracao SSO com OAuth2 - Google
Aplicacao para demonstracao pratica do funcionamento do OAuth utilizando o Google como servidor.

## Instalacao:

- Descompactar o arquivo
- Entrar na pasta "entregas"
- Rodar o comando: python3 -m pip install -r requirements.txt

## Para desktop:

- Entrar na pasta "entregas"
- Rodar o comando:
    ```sh
    python3 -m pip install -r requirements.txt
    ```
#### Apesar de as bibliotecas utilizadas serem multiplataforma, foi testado apenas no Linux

## Para android:

- Entrar na pasta "entregas"
- Instalar o auxiliar de compilacao [buildozer]("https://buildozer.readthedocs.io/en/latest/installation.html")
- Conectar o celular via USB e permitir a depuracao e transferencia de arquivos via USB
- Rodar o comando:
    ```sh
    buildozer android debug deploy run
    ```
#### Na execucao da instalacao para android, sera necessaria a compilacao do codigo. Isso levara em media 5 minutos e caso tudo ocorra bem, o aplicativo ira iniciar automaticamente.
#### Na instalacao para android, nao desconectar o celular do USB ou desativar a depuracao ate que a aplicacao inicialize. Depois, pode remover.

## Codigo da implementacao do Oauth pode ser encontrado nos arquivos:

- main.py : Onde sao setados o CLIENT_ID e o CLIENT_SECRET
- google_auth.py : Logica do browser, redirecionamentos, uso da oauthlib, tratamentos e login em si (o local do arquivo varia de cada instalacao. Aqui esta em "~/venvs/entregas/lib/python3.9/site-packages/kivyauth/desktop/google_auth.py".
No caso de instalacao fora de ambiente virtual, pode ser que se encontre em "/lib/python<versao>/site-packages/kivyauth/desktop/google_auth.py"
- classes/screens/login_screen.py: Onde a logica do login se inicia. A funcao "do_google_login()" inicia chamadas de funcoes subsequentes.
