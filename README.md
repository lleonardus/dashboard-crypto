# 🪙 Dashboard Crypto

Projeto feito para a matéria de Big Data da Estácio. O objetivo é utilizar
Python para consumir os dados da API da Binance e fazer análises dos preços de
criptomoedas em tempo real.

![Imagem do app](./docs/images/app.png)

## 💿 Como rodar na sua máquina

### 📝 Pré-requisitos:

- [Git](https://git-scm.com/downloads)
- [Python 3.9 ou maior](https://www.python.org/downloads/)

#### 🪟 Windows

Caso não queira abrir o terminal, tem um arquivo na raiz do projeto chamado
`windows-run.bat` que permite você instalar as dependências e rodar o projeto
com apenas um clique.

```bash
# Clonando o projeto e entrando na pasta
$ git clone https://github.com/lleonardus/dashboard-crypto.git
$ cd dashboard-crypto

# Configurando virtual environment e instalando as dependências
$ python -m venv .venv
$ .venv\Scripts\activate
$ pip install -r requirements.txt

# Subindo servidor
$ streamlit run app.py
```

#### 🐧 Linux

```bash
# Clonando o projeto e entrando na pasta
$ git clone https://github.com/lleonardus/dashboard-crypto.git
$ cd dashboard-crypto

# Configurando virtual environment e instalando as dependências
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt

# Subindo servidor
$ streamlit run app.py
```

## 🧰 Ferramentas Utilizadas

- [git](https://git-scm.com/downloads)
- [python](https://www.python.org/downloads/)
- [streamlit](https://streamlit.io/#install)
- [python-binance](https://python-binance.readthedocs.io/en/latest/overview.html)
- [pandas](https://pandas.pydata.org/docs/getting_started/install.html)
- [plotly](https://plotly.com/python/getting-started/)
- [Pillow](https://pillow.readthedocs.io/en/stable/installation/basic-installation.html)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
