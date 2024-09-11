# Learning Path (frontend)

Este repositório foi gerado usando a interface
[Angular CLI](https://github.com/angular/angular-cli), v18.2.3.

## Configurações do abiente de desenvolvimento

1. Instalação do [node](https://nodejs.org) v20.17.0:

```bash
# instalação do nvm (Node Version Manager)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash

# download e instalação do Node.js
nvm install 20

# verificações das versões
node -v # should print `v20.17.0`
npm -v # should print `10.8.2`
```

2. Instalação do [Angular](https://angular.dev) v18.2.3:

```bash
npm install -g @angular/cli

# verificação da versão
ng --version
```

## Build e execução do projeto

Use `ng build`, (IMPORTANTE) dentro do diretório frontend, para buildar o
projeto. Todos os artefatos resultantes da build estarão no diretório `dist/`.

Se estiver usando o VS Code, abra o frontend como projeto e você poderá usar as
instruções de build do projeto pela interface do editor! Se estiver com
problemas para executar, no arquivo `launch.json`, dentro do diretório
`.vscode`, altere "firefox" para o nome do seu navegador padrão!

Para rodar o projeto, use `ng serve` e abra o navegador no endereço
`http://localhost:4200/`. Cada nova alteração nos arquivos fonte serão
automaticamente espelhadas nessa instância rodando.

## Criando novos componentes

Para criar novos componentes, use `ng generate component component-name`. Há 
uma infinitude de outras diretivas que podem ser usadas com o generate, como:
`ng generate directive|pipe|service|class|guard|interface|enum|module`.

## Dúvidas sobre a CLI do Angular

Qualquer dúvida, use `ng help` ou acesse [Angular CLI Overview and Command Reference](https://angular.dev/tools/cli).
