# Meteorologia Portugal

Projeto no âmbito da Unidade Curricular de Engenharia de Dados e Conhecimento (EDC)

![Meteorologia em GIF][https://raw.githubusercontent.com/andralves717/edc_tp1/master/meteo.gif]

## 1. Tecnologias usadas:
- Python/Django - Servidor Web em MVC;
- XML - Formato do dados;
- XML Schema - Validação do XML;
- XPATH - Filtragem dos dados;
- XSLT - Transformação de dados em XML para HTML;
- BaseX - Base de Dados baseada em XML;
- XQuery e XQuery Update - Pesquisa e gestão dos dados na base de dados;
- RSS - Recolha de notícias do [IPMA](http://www.ipma.pt/pt/produtoseservicos/index.jsp?page=rss.xml);
- [OpenWeather](api.openweathermap.org/) - Recolha de dados meteorológicos.

## 2. Como Executar:

### 2.1 Usando Python Virtual Environment (recomendado):
Versão de Python3: 3.8

Versão do PIP: pip 20.2.4

#### 2.1.1 Criar Virtual Environment:
`python3 -m venv venv`

#### 2.1.2 Abrir o Virtual Environment:
`source venv/bin/activate` (para desativar fazer executar "deactivate")

#### 2.1.3 Instalar os PIPs necessários:
`pip install -r requirements.txt`

#### 2.1.4 Usar o Pycharm para executar o projeto ou:
`python3 manage.py runserver`

---
### 2.2 Usando Python (sem virtual Environment):
Versão de Python3: 3.8

Versão do PIP: pip 20.2.4

#### 2.2.1 Instalar os PIPs necessários:
`pip install --user -r requirements.txt`
(É recomendado usar a opção --user para instalar localmente e não precisar de permissões de superuser)

#### 2.2.2 Usar o Pycharm para executar o projeto ou:
`python3 manage.py runserver`

## 3. Realizado por:

| Nome            | GitHub        | Mail |
| --------------- |:-------------:| -----|
| André Alves     | [Link](https://github.com/andralves717)| andr.alves@ua.pt |
| Alexandre Abreu | [Link](https://github.com/afabreu)| alexandre.abreu@ua.pt |
| André Almeida   | [Link](https://github.com/Almeida-a)| almeida.a@ua.pt |
