# 📋 Lista de Tarefas (To-Do List)

Aplicação desktop moderna para gerenciamento de tarefas, desenvolvida em Python com interface gráfica CustomTkinter.

## ✨ Funcionalidades

- ✅ Adicionar, editar e excluir tarefas
- 🎯 Sistema de prioridades (Baixa, Média, Alta)
- 📊 Filtros por status (Todas, Pendentes, Concluídas)
- 💾 Persistência automática em JSON
- 🎨 Interface moderna e minimalista
- 🌙 Tema escuro por padrão

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passos

1. Clone o repositório:
	git clone https://github.com/CarlosHonma/todo_app.git
	cd todo_app

2. Instale as dependências:
	pip install -r requirements.txt


## 📖 Como Usar

Recomendo criar e ativar um ambiente virtual dentro da raiz do projeto e usar o interpretador do venv:

```bash
# na raiz do repositório
python3 -m venv .venv
source .venv/bin/activate
pip install -r todo_app/requirements.txt
```

Opções para executar a aplicação:

- Executar como módulo (recomendado a partir do diretório `todo_app`):

```bash
cd todo_app
# com o venv ativado (veja acima)
python -m src.main
```

- Executar a partir da raiz do repositório com o lançador (`run_todo_app.py`):

```bash
source .venv/bin/activate
python run_todo_app.py
```

Observação: não execute `pip install tkinter` — o Tkinter é um pacote do sistema. No Ubuntu, instale o componente do sistema se necessário:

```bash
sudo apt update
sudo apt install -y python3-tk
```


### Atalhos
- **Ctrl+N**: Nova tarefa (a implementar)
- **Delete**: Excluir tarefa selecionada (a implementar)

## 🏗️ Estrutura do Projeto

todo_app/
├── src/
│ ├── models/ # Modelos de dados (Task, Priority, Status)
│ ├── utils/ # Utilitários (Database)
│ ├── gui/ # Interface gráfica (componentes, estilos)
│ ├── config/ # Configurações
│ └── main.py # Ponto de entrada
├── requirements.txt # Dependências
└── README.md # Este arquivo


## 🛠️ Tecnologias

- **Python 3.8+**: Linguagem base
- **CustomTkinter**: Framework de GUI moderna
- **JSON**: Persistência de dados

## 📝 Roadmap

- [ ] Edição de tarefas existentes
- [ ] Categorias/tags personalizadas
- [ ] Data de vencimento com alertas
- [ ] Tema claro/escuro alternável
- [ ] Exportação para CSV/PDF
- [ ] Sincronização em nuvem


