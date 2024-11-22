# Learning Path

Repositório pra o projeto da matéria MC656 - Engenharia de Software

## Integrantes

260497 - Henrique Parede de Souza

252873 - Maria Beatriz Guimarães Trombini Manhães Moreira 

260637 - Pedro Brasil Barroso

206235 - T. H. de Camargo J.

223641 - Raphael Salles Vitor de Souza

## Descrição do projeto

LearningPath é uma plataforma para criação e compartilhamento de planos de estudo e competição entre amigos seguindo um critério decidido por eles (tempo de estudo, dias estudados, número de matérias estudadas).

## Desenvolvimento

Embora front e backend estejam no mesmo repositório, no desenvolvimento eles devem ser abertos em separado. Um workspace para frontend e outro para backend.

  
## Avaliação 4 
**Parte 1: Arquitetura**   
Para a avaliação A4, escolhemos implementar uma arquitetura em camadas na nossa aplicação. Como visto no diagrama C4 há essencialmente 4 camadas:

* Frontend, as telas com que o usuário interage. Note que apesar de haver diferentes caminhos que o usuário possa percorrer vários deles consistem de páginas  meramente ilustrativas, isto é, que não requerem interação do usuário. Sendo assim, optamos por considerar todo esse escopo como uma única camada  
* Seria natural colocar a segunda camada apenas como backend, e, mesmo fazendo nisso a nível de containers, a nível de componentes notamos que havia 3 camadas distintas dentro dele:  
  * Controllers: Responsáveis por conectar os inputs do frontend com o backend como um todo  
  * Services: Responsáveis pelas operações em si feitas com os dados. Diferem a depender do contexto onde são implementados, ou seja, cada parte da aplicação necessita que o service faça algo diferente (leia mais abaixo)  
  * Models: Serializam as entidades criadas ou alteradas pelos services e salvam no BD

**Frontend \-** Escolhemos implementar o frontend utilizando Angular. Esta escolha se deve a facilidade de modularização e de escalabilidade do framework. Dividimos a nossa arquitetura em:

* Tela de apresentação (usuário externo): contextualização do usuário sobre a aplicação  
* Tela produto: explicação do funcionamento da nossa aplicação e como contribuir para o projeto  
* Tela de login: logar o usuário e redirecionar para tela principal  
* Tela principal (usuário logado): página inicial com overview dos planos de estudos criados ou seguidos pelo usuário  
* Tela equipe: apresentação dos criadores no Learning Path  
* Tela plano: plano de estudos criado ou seguido pelo usuário, com diversos tópicos a serem estudados  
* Tela logout: encerrar a sessão do usuário e direcioná-lo para tela de apresentação inicial

**Backend \-** Decidimos utilizar o framework Django devido à facilidade de integração com o banco de dados e com o frontend. Dividimos nossa arquitetura em:

* Login Controller: Inicia a autenticação e retorna a request se ela teve sucesso  
* Auth Service: Responsável por gerar e deletar tokens, a depender se é chamado pelo login ou logout controller  
* Custom User Model: Modelo do banco de dados que implementa o usuário da aplicação   
* Logout Controller: O equivalente do login controller, mas ele manda a request se o token foi deletado com sucesso.  
* Study Plan Controller: Responsável não só por receber os dados do front end, mas também especifica qual o tipo de post será feito no service (leia mais sobre isso em Padrões de Projeto)  
* Study Plan Service: Tem o CRUD do plano de estudos  
* Study Plan Model: Modelo do banco de dados que implementa o plano de estudos  
* Domain Service:  Lê o domínio da tabela  
* Domain Model: Modelo do banco de dados que implementa a tabela de domínio  
* Study Topic Controller: Pega os dados do front end e passa para o service  
* Study Topic Service: Tem o CRUD do tópico de estudos  
* Study Topic Model: Modelo do banco de dados que implementa o tópico de estudo

	Além disso temos o banco de dados, que, obviamente, guarda os dados.  
Segue o diagrama C4:
![Diagrama do Sistema](readmeAssets/C4%20-%20Avaliação%204.drawio.png)
[Baixar arquivo original](https://drive.google.com/file/d/1BJyhDH47fbebxdDqXOKrLCm6mTBW9CNz/view?usp=sharing)

