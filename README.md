# Hub

## Português

---

### O que você precisa instalar/ter

-   [Docker](https://www.docker.com/);
-   [Python](https://www.python.org/downloads/);
-   Bash ou similar(Zsh, etc.): se você tem Linux ou Mac, o Bash já vem embutido. No caso do Windows é necessário instalar o [Git Bash](https://git-scm.com/downloads).
-   É necessário ter acesso ao Gitlab da Smarthis, falar com alguém da equipe sobre isso.
-   Pedir a algum integrante da equipe os arquivos de Variáveis de ambiente tanto do Hub como do Orchestrator

### Editor recomendado

-   [VS Code](https://code.visualstudio.com/)
-   Depois de configurado, mantemos um padrão de código através da extensão "Prettier - Code".
-   Acessa o Settings do VS Code e procura por "default formatter".
-   Selecione o Prettier - Code
-   Acesse o arquivo Code/User/settings.json, e adicione:
    ```
        "[html]": {
            "editor.defaultFormatter": null
        },
        "[django-html]": {
            "editor.formatOnSave": false
        },
        "[python]": {
            "editor.defaultFormatter": null
        },
        "prettier.printWidth": 100,
        "prettier.semi": true,
        "prettier.useTabs": true,
        "prettier.tabWidth": 4,
        "prettier.singleQuote": true,
        "prettier.htmlWhitespaceSensitivity": "ignore",
        "editor.formatOnSave": true,
    ```
-   Instale a extensão Python da microsoft.
-   Salve algum arquivo py, vai aparecer no canto direito uma sugestão pra instalar o autopep8, por favor clique sim

## Configuração

**A primeira coisa que você deve fazer é realizar um fork do repositório do HUB Smarthis para a SUA conta do Github e depois clonar o SEU repositório na sua máquina.**

### Docker

---

Um grande problema que as equipes de software enfrentam é a configuração do seu ambiente. Você pode usar um sistema operacional diferente, às vezes você tem uma biblioteca instalada em uma versão e o seu colega em outra (_exemplo: python2 e python3_), e no final tem aquela frase: _roda na minha máquina_, o que só aumenta sua raiva.

Para tentar solucionar esses problemas, nós usamos o Docker, uma tecnologia que utiliza containers. Cada container simula um ambiente com os recursos e dependências necessários pra rodar em qualquer sistema operacional, indepente da sua configuração individual de ambiente.

**No nosso caso**, como necessitamos diversos ambientes (um para o Django, outro pra Base de Dados, entre outros do backend) para o funcionamento do Hub, nós usamos o [Docker Compose](https://docs.docker.com/compose/), para que possamos gerar mais de um Container, um para cada parte importante do sistema:

-   Para o site do HUB, temos o _hub_app_1_;
-   Para a base de dados, temos o _hub_database_1_;
-   Para a fila (voltado para o back end), _temos o hub_rabitmq_1_;
-   Para o trabalhador que vai consumir as filas temos o _hub_worker_1_.

#### Passo a passo da configuração do fork do HUB

1.  Forke o [repositório do HUB](https://github.com/SmarthisHub/Hub) para a sua conta do Github;

#### Passo a passo da configuração dos arquivos do HUB

1.  Criar pasta chamada smarthis;
2.  Dentro da pasta clone o repositório que você forkou (o da sua conta)

    ```sh
    git clone <LINK DO SEU FORK DO REPOSITÓRIO DO HUB>
    ```

3.  Dentro da mesma pasta (smarthis) clone o [repositório do Orchestrator](https://github.com/SmarthisHub/Orchestrator)

    3.1 No caso do repositório do Orchestrator, como vamos apenas consumir ele, você pode clonar diretamente do das Smarthis

#### Passo a passo da configuração do Docker

---

1.  Abrir o docker;

2.  Acessar via terminal a pasta clonada do github:

    ```sh
    cd pastas-antes/Hub
    ```

3.  Inicie o build do docker com:

    ```sh
    docker-compose up
    ```

    **Não feche o terminal que você realizar o docker-compose up**

4.  Estando os containers iniciados, é necessário descobrir o ID de cada um pra poder atualizar o banco de dados de um dos containers, para isso:

    ```sh
    docker ps
    ```

    **CONTAINER ID está na primeira coluna do output deste comando**

5.  Tendo o CONTAINER ID, é necessário copiar o [dump](https://pt.wikipedia.org/wiki/Dump_de_banco_de_dados) realizado do banco de dados dentro do volume criado pelo docker-compose.yml . Para isso, são necessários 2 passos:

    5.1. Descobrir em que pasta do container esse volume está localizado, através do comando no terminal:

        docker inspect -f '{{ json .Mounts }}' CONTAINER_ID | python -m json.tool

    **Obs: Caso você tenha instalado o Python3 na sua máquina, talvez tenha que rodar python3 ao invés de python**

    5.2. Pegar o caminho do arquivo de dump (src/dump/nome-do-arquivo.sql), além do _DESTINATION_ dele e o _NOME do CONTAINER_ (também encontrado no _docker ps_), digitar:

        docker cp caminho-do-arquivo-de-dump.sql CONTAINER_NAME:DESTINATION

    Exemplo:

        docker cp src/dump/hubdump.sql hub_database_1:/var/lib/postgresql/data

6.  Obter os 3 primeiros digitos do CONTAINER ID postgres e acessá-lo através do comando:

    ```sh
    docker exec -it CONTAINER_ID bash
    ```

7.  Estando no container, está na hora de acessar o postgres mesmo, através do comando:

    ```sh
    psql -U postgres
    ```

8.  Criar a base de nome manager e em seguida sair do container:

    ```sh
    create database manager;
    exit
    ```

9.  Como você está dentro do container database, execute o arquivo dump que foi copiado nele, através do comando:

    ```sh
    cat dump_file_name;sql | psql -U postgres -d database_name
    ```

    No meu caso ficou:

        cat hubdump_21-06-2022.sql | psql -U postgres -d manager

    Esse comando vai resultar em várias linhas do postgres.

10. Agora, a estrutura da sua base de dados necessita ser atualizada. Acesse o container app e realize os comandos:

    ```sh
    docker exec -it hub_app_1 sh
    python manage.py migrate
    ```

**Obs: Mesmo se você tiver usado python3 anteriormente, agora é necessário usar só python, pois você estará dentro do container**

11. Agora como o banco está ativo, as migrações foram feitas, é necessário parar os containers e rodar novamente:

    ```sh
    docker-compose stop
    ```

    E reiniciando:

    ```sh
    docker-compose up -d
    ```

12. Suba o docker do Orchestrator:

    ```sh
    cd smarthis/Orchestrator
    docker-compose -f docker-compose-contas.yml up -d
    ```

13. Visite o http://localhost:8000/ para checar se está funcionando.

-   Se quiser ver os logs:

    ```sh
    docker logs -f hub_app_1
    ```

#### Criando um usuário

---

1.  ```
    docker exec -it hub_app_1 sh
    ```

2.  ```
    python manage.py createsuperuser
    ```

3.  Coloque o seu e-mail da Smarthis e crie uma senha;
    3.1. Além disso, é necessário associar esse usuário a um cliente, através dos comandos

    ```
        python manage.py shell
        from subscriptions.models import User, Client, Profile
        user = User.objects.get(email='gz@testereadme.com')
        client = Client.objects.get(name='Smarthis')
        user_profile = Profile.objects.get(user=user)
        user_profile.client = client
        user_profile.save()
    ```

    OBS: como email utilizei o exemplo acima(gz@testereadme.com) utilize o seu email de exemplo

4.  Visite http://localhost:8000/ e faça login com o seu email e senha;

5.  Em seguida, visite http://localhost:8000/admin ;

6.  Vá na seção de Subscriptions e clique em Users;

7.  Encontre seu e-mail e clique NELE (não no checkbox);

8.  Vá até o final da página, escolha um cliente (consulte alguém da equipe) e coloque como role: _admin_.

9.  Aperte SAVE.

#### Configuração do Git Remote

---

Depois de forkado o repositorio pro seu perfil, e clonado para sua máquina a partir desse fork, é necessário diferenciar os repositórios internamente, com o objetivo de não confundir o desenvolvimento do que é do repositório original e do que é do seu fork.

Você pode configurar o seu remote da forma que for mais conveniente e natural para você, alguns preferem deixar o origin como o repositório original e outros deixam o upstream como o original e o origin como o seu fork.

**Obs: Em relação à forma de clonar (https ou ssh), recomendamos o SSH por questões de segurança, mas não é obrigatório.**

Quando você clona um repositório, automaticamente o git define o repositorio de onde você clonou (no nosso caso, o reposirório forkado na sua conta do github) como _origin_, você pode checar isso com o seguinte comando:

        git remote -v

Caso você queira alterar os seus repositorios remotos (origin, upstream, ou qualquer outro que você criar), use o seguinte comando:

        git remote add <nome do remoto> <url do repositório>

Exemplos:

        git remote add origin git@github.com:SmarthisHub/Hub.git ;

        git remote add upstream https://github.com/SmarthisHub/Hub.git ;

        git remote add qualquerNome git@github.com:SmarthisHub/Hub.git ;

**Sugestão: ficar atento ao development da origin através do comando:**

    git pull <nome que você deu ao repositório original> development

#### Configurando Edição automática do código

Como cada pc tem sua configuração pessoal, ao longo do desenvolvimento, percebemos mudanças que impactavam na organização do código quando modificado. Sendo assim, optamos por utilizar o editorconfig. Pra manter funcionando enquanto você desenvolve, você precisa:

1. Instalar a extensão "EditorConfig for VS Code" no vs code

---

## English

---

### What you need to install/have

-   [Docker](https://www.docker.com/);
-   [Python](https://www.python.org/downloads/);
-   Bash or similar (Zsh, etc.): if you have Linux or Mac, Bash is already built-in. In the case of Windows, it is necessary to install [Git Bash](https://git-scm.com/downloads).
-   It is necessary to have access to Gitlab from Smarthis, talk to someone on the team about it.
-   Ask a team member for the Environment Variables files from both the Hub and Orchestrator

### Recommended editor

-   [VS Code](https://code.visualstudio.com/)
-   After setup, we keep the code pattern through the extension "Prettier - Code".
-   Now, access your Settings on VS Code and look for "default formatter".
-   Select Prettier - Code
-   Access file Code/User/settings.json , and add:
    ```
        "[html]": {
            "editor.defaultFormatter": null
        },
        "[django-html]": {
            "editor.formatOnSave": false
        },
        "[python]": {
            "editor.defaultFormatter": null
        },
        "prettier.printWidth": 100,
        "prettier.semi": true,
        "prettier.useTabs": true,
        "prettier.tabWidth": 4,
        "prettier.singleQuote": true,
        "prettier.htmlWhitespaceSensitivity": "ignore",
        "editor.formatOnSave": true,
    ```
-   Install the extension Python from microsoft.
-   Save any py file, in your right corner will appear a suggestion to install autopep8, please click yes

## Configuration

**The first thing you should do is fork the HUB Smarthis repository to YOUR Github account and then clone YOUR repository on your machine.**

#### HUB fork configuration walkthrough

1.  Fork the [HUB repository](https://github.com/SmarthisHub/Hub) to your Github account;

#### HUB files configuration step by step

1. Create folder called smarthis;
2. Inside the clone folder the repository you forked (your account)

    ```sh
    git clone <LINK TO YOUR HUB REPOSITORY FORK>
    ```

3. Inside the same folder (smarthis) clone the [Orchestrator repository](https://github.com/SmarthisHub/Orchestrator)

    3.1 In the case of the Orchestrator repository, as we are only going to consume it, you can clone directly from das Smarthis

### Docker

---

A major problem that software teams face is the configuration of their environment. You can use a different operating system, sometimes you have a library installed in one version and your colleague in another (_example: python2 and python3_), and at the end, there is that sentence: _works on my machine_, which only increases your anger.

To try to solve these problems, we use Docker, a technology that uses containers. Each container simulates an environment with the necessary resources and dependencies to run on any operating system, regardless of its individual environment configuration.

**In our case**, as we need several environments (one for Django, another for the Database, among others for the backend) for the Hub to work, we use [Docker Compose](https://docs.docker.com/compose/), so that we can generate more than one Container, one for each important part of the system:

-   For the HUB website, we have _hub_app_1_;
-   For the database, we have _hub_database_1_;
-   For the queue (facing the back end), _we have hub_rabitmq_1_;
-   For the worker who is going to consume the queues we have _hub_worker_1_.

#### Docker setup step by step

---

1.  Open Docker;

2.  Access the cloned github folder via terminal:

        sh cd folders-before/Hub

3.  Start the docker build with:

        docker-compose up

    **Do not close the terminal that you perform the docker-compose up**

4.  Once the containers are started, it is necessary to find out the ID of each one in order to be able to update the database of one of the containers, for this:

        docker ps

    **CONTAINER ID is in the first column of the output of this command**

5.  Having the CONTAINER ID, it is necessary to copy the [dump](https://pt.wikipedia.org/wiki/Dump_de_banco_de_dados) made from the database within the volume created by docker-compose.yml. For this, 2 steps are necessary:

    5.1. Find out in which folder of the container this volume is located, running this command in the terminal:

        docker inspect -f '{{json .Mounts}}' CONTAINER_ID | python -m json.tool

    **Note: If you have installed Python3 on your machine, you may have to run python3 instead of python**

    5.2. Get the dump file path (src/dump/FILENAME.sql), in addition to his _DESTINATION_ and the CONTAINER_NAME (also found in the docker ps), type:

        docker cp dump-file-path.sql CONTAINER_NAME:DESTINATION

    Example:

        docker cp src/dump/hubdump.sql hub_database_1:/var/lib/postgresql/data

6.  Obtain the first 3 digits of the CONTAINER ID postgres and access it through the command:

        docker exec -it CONTAINER_ID bash

7.  Being inside the container, it's time to access postgres, running the command:

        psql -U postgres

8.  Create the base name manager and then exit the container:

        create database manager;
        exit;

9.  As you are inside database container, run the dump file that was copied into it, using the command:
    `sh cat dump_file_name;sql | psql -U postgres -d database_name `
    In my case it was:

        cat hubdump_21-06-2022.sql | psql -U postgres -d manager

    This command will result in lots of database lines.

10. Now, your database estructure must be updated. Access the app container and perform the command:

        docker exec -it hub_app_1 sh
        python manage.py migrate

    **Note: Even if you have used python3 previously, it is now necessary to use only python, as you will be inside the container**

11. Now with the active database, the migrations have been made, it is necessary to stop the containers and run them again:

        docker-compose stop

    And restarting:

        docker-compose up -d

12. Upload Orchestrator docker:

    ```sh
    cd smarthis/Orchestrator
    docker-compose -f docker-compose-contas.yml up -d
    ```

13. Visit http://localhost:8000/ to check if it is working.

-   If you want to see the logs:

          docker logs -f hub_app_1

#### Creating a user

---

1. docker exec -it hub_app_1 sh

2. python manage.py createsuperuser

3. Enter your Smarthis email and create a password;

    3.1. Other than that, it is necessary to associate this user with a client, through the commands:

    ```
        python manage.py shell
        from subscriptions.models import User, Client, Profile
        user = User.objects.get(email='gz@testereadme.com')
        client = Client.objects.get(name='Smarthis')
        user_profile = Profile.objects.get(user=user)
        user_profile.client = client
        user_profile.save()
    ```

    OBS: as email I used the example above (gz@testereadme.com) use your email as an example

4. Visit http://localhost:8000/ and log in with your email and password;

5. Next, visit http://localhost:8000/admin;

6. Go to the Subscriptions section and click Users;

7. Find your email and click on it (not in the checkbox);

8. Scroll to the bottom of the page, choose a customer (ask someone of the team), and put as role: _admin_.

9. Press SAVE.

#### Git Remote configuration

---

After you fork the repository into your profile, clone into your machine from that fork, it is necessary to differentiate the repositories internally, in order not to confuse the development of what is from the original repository and what is from your fork.

You can configure your remote in the way that is most convenient and natural for you, some prefer to leave origin as the original repository and others leave upstream as the original and origin as their fork.

**Note: Regarding how to clone (https or ssh), we recommend SSH for security reasons, but it is not mandatory.**

When you clone a repository, git automatically defines the repository you cloned from (in our case, the repository forked into your github account) as _origin_, you can check this with the following command:

         git remote -v

If you want to change your remote repositories (origin, upstream, or whatever you create), use the following command:

         git remote add <remote name> <repository url>

Examples:

         git remote add origin git@github.com:SmarthisHub/Hub.git;

         git remote add upstream https://github.com/SmarthisHub/Hub.git;

         git remote add anyName git@github.com:SmarthisHub/Hub.git;

**Suggestion: be aware of the development of origin through the command:**

     git pull <NAME YOU GAVE TO THE ORIGINAL REPOSITORY> development

#### Setting up automatic code editing

As every personal computer has its own configuration, over development, we realized some changes that impacted on code set up when modified. Therefore, we chose to use editorconfig. To keep it working as you develop, you need to:

1. Install extension "EditorConfig for VS Code" on vs code
