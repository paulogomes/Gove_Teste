
# Solução do desafio para a vaga da empresa Gove

Foi criado as soluções em Python e também no Pentaho PDI

## Desafio:

### Tarefa 1 - limpar/normalizar:
 - Separar o endereço criando novos campos: TIPO_LOGRADOURO, NOME_LOGRADOURO, NUMERO e COMPLEMENTO

**OBS:** No campo NUMERO deverá conter apenas dados de tipo numéricos, outras informações deverão ser colocadas no campo COMPLEMENTO.

### Tarefa 2 - juntar endereços utilizando o DocId
- Identificar os Clientes com mesmo Codigo e DocId colocar na mesma linha os endereços encontrados

**OBS:** Podem ser criados novos campos: (TIPO_LOGRADOURO_1, NOME_LOGRADOURO_1, NUMERO_1, COMPLEMENTO_1; TIPO_LOGRADOURO_2, NOME_LOGRADOURO_2, NUMERO_2, COMPLEMENTO_2; ... ;TIPO_LOGRADOURO_N, NOME_LOGRADOURO_N, NUMERO_N, COMPLEMENTO_N;)

### Tarefa 3 - achar/tratar DocId vazios/zerados  
- Identificar nome e código de clientes com DocId vazios/zerados utilizando as chaves que julgar ser suficiente para tal (Identificar DocId em novo campo DOCId_SUGERIDO)

**OBS:** Não esquecer de voltar na tarefa 2 e adicionar os endereços referentes ao docs sugeridos.


## Como Para rodar o código do python:

 - é necessário utilizar a versão Python 3.9

 - e instalar o pandas e suas dependências rodando o comando:

``` bash
    pip install -r requirements.txt
```

e depois rodar o comando:

``` bash
    python Gove.py
```

vai ser gerado os arquivos .xlsx na mesma pasta

## Como rodar a transformação do Pentaho:

- É necessário utilizar a versão 9.3
- Abrir o arquivo Gove.ktr e utilizar a opção "Run".

vai ser gerado os arquivos .xlsx na mesma pasta do ktr.