## O que o twitter está pensando? Extraindo informações em redes sociais utilizando Python.

`por: `[@profadolfoguimaraes](http://www.instagram.com/profadolfoguimaraes)

Esse projeto foi resultado de um minicurso de coleta de dados do twitter ministrado em 2016. 
Em março de 2018, resolvi retomá-lo para ministrar novamente. Na ocasião foram coletados 
em torno de 600 tweets com as hashtags *#teambatman* e *#teamsuperman*. A proposta do minicurso é 
coletar os dados, fazer um rápido pré-processamento e exibir as informações em uma página web. 

O material completo desse minicurso pode ser encontrado no site: 
[http://www.data2learning.com/cursos](http://www.data2learning.com/cursos)


## Repositórios

O projeto está dividido em dois repositórios: 

* [d2l-minicursotwitter-notebook](http://github.com/adolfoguimaraes/d2l-minicursostwitter-notebook): possui todos os jupyter notebooks de explicação do conteúdo abordado no minicurso. 
* [d2l-minicursortwitte-web](http://github.com/adolfoguimaraes/d2l-minicursotwitter-web) `(este repositorio)`: possui a página web criada para visualizar as informações coletadas do twitter.

## Instalação das dependências

Para o projeto funcionar é necessário instalar algumas depedências que estão listadas no arquivo `requirements.txt`. Para 
instalar utilize o comando: 

```shell
pip install -r requirements.txt
```

O projeto utiliza python versão 3.x.

### API do Twitter

Para usar a API do Twitter é preciso se cadastrar em [apps.twitter.com](http://apps.twitter.com) e criar um App para obter 
as credenciais: Keys e Tokens. No código todas as credenciais estão como `None`. Esse valor deve ser substituído pelas credenciais
obtidas no site do twitter. Uma breve explicação de como obter tais credenciais
pode ser encontrada nos slides disponibilizados [neste link](http://www.data2learning.com/cursos).

### Projeto Web

O projeto web exibe as informações coletadas e processadas. Foi utilizado o **flask** como framework e um banco de dados em **sqlite**. No
entanto, por conta da política de uso da API do Twitter, os tweets devem ser coletados novamente já que não é permitido distribuir
os tweets coletados.

Para inserir os tweets na base, execute o script `updadte_database.py` no diretório `db/files/`.

Após coletar os tweets é preciso gerar os dados processados. Para isto execute o script `run.py` na pasta `scripts`.

Para executar o servidor web com a página, use: `python flask_app.py` no diretório raiz.

A página a seguir deve ser visualizada:

![screen_capture](http://adolfo.data2learning.com/screen_capture_d2l.png)


Qualquer dúvida e/ou sugestões, entre em contato:

`e-mail: `
[adolfo@data2learning.com](mailto:adolfo@data2learning.com) 

`instagram: `
[@profadolfoguimaraes](http://www.instagram.com/profadolfoguimaraes)