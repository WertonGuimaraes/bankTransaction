# bankTransaction


Esse projeto consiste em uma *API* que realizar operações de crédito, debito e visualização das transações.

## Configuração
* Instale o [docker](https://tecadmin.net/install-docker-on-ubuntu/).
* Instale o [docker-compose](https://linuxize.com/post/how-to-install-and-use-docker-compose-on-ubuntu-18-04/).
* Dê poderes ao docker, caso precise: 
```
sudo chown $USER /var/run/docker.sock
```

## Rodando o projeto

#### Inicializando
Após o pull do projeto entre na pasta *bankChallenge/bankChallengeProject* e execute o seguinte código:
```
docker-compose up -d --build
```
Isso fará que o projeto seja construido e as dependências baixadas, para que o projeto seja executado depois.

#### Parando
Para parar o servidor entre na pasta *bankChallenge/bankChallengeProject* e execute o seguinte código:
```
docker-compose down
```

## Consumindo a api

###Criação de usuário

Path: /user

Method: POST

Response Status: **201 - CREATED** 

Exemplo: No endpoint http://localhost:8000/user envie um body do tipo:
``{"username": "Werton"}``

O usuário será criado eum json onde será mostrado como retorno, como, por exemplo.

Response Body:
```json
{
    "id": 1,
    "username": "Werton",
    "balance": 0
}
```
___

### Operações de débito e crédito
Path: /user/{usr_id}/action

Method: POST

Response Status: **201 - CREATED** 

Exemplo: No endpoint http://localhost:8000/user/1/action envie um body do tipo:
``{"value": 100, "description": "mesada"}``

A transação ocorrerá com sucesso, e o json abaixo é retornado: 

Response Body:
```json
{
    "id": 1,
    "username": "Werton",
    "balance": 100.0
}
```

Em outras palavras, foi creditado 100 reais na conta do usuário com 'id' igual a 1.

####IMPORTANTE:

- Para fazer debito basta passar um valor negativo, ex: `{"value": -100, "description": "Pagamento da energia"}`
- Os campos value e description são obrigatórios, se o usuário não passar receberá um BAD_REQUEST (400);
- O usuário não pode ficar com o saldo negativo, se ele tentar algo do tipo a ação não irá ocorrer e receberá um FORBIDDEN (403);
- Se tentar creditar ou debitar de um usuário que nao existe, o status code retornado é 404.

____
### Extrato
Path: /user/{usr_id}/extract

Method: GET

Response Status: **200 - OK** 

Exemplo: No endpoint http://localhost:8000/user/1/extract 

O extrato deverá ser mostrado com sucesso, e o json abaixo é retornado: 

Response Body:
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "description": "mesada",
            "current_balance": 100.0,
            "old_balance": 0.0,
            "value": 100.0,
            "created_at": "2021-03-26T09:38:27.886729Z"
        }
    ]
}
```

Note que é possível ver todas as transações feitas por aquele usuário de forma detalhada.
onde:
- o value é o valor que entrou ou saiu;
- o old_balance é o valor antes da operação;
- o current_balance é o valor após a operação;

####Filtros
Passando os parametros corretos é possível filtrar os resultados do extrato.

- Filtro por transação.
  - Filtro de debito: `?transaction_type=debit`
  - Filtro de credito: `?transaction_type=credit`

- Filtro por data
  - A partir da data: `?start_date=2021-03-11T00:00Z`
  - Até a data: `?end_date=2021-03-11T00:00Z`
  - Entre as datas: `?start_date=2021-03-11T00:00Z&?end_date=2021-03-15T00:00Z`


####IMPORTANTE:

- Se tentar visualizar o extrato de um usuário que nao existe, o status code retornado é 404.
