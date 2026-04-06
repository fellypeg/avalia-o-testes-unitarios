# 🔐 Sistema de Validação de Senhas

Pequena aplicação Python que valida senhas com base em regras de negócio bem definidas, acompanhada de uma suíte completa de testes unitários automatizados com **Pytest**.

---

## 🚀 Como executar

### Pré-requisitos
- Python 3.8+
- pip

### Instalação
```bash
pip install -r requirements.txt
```

### Rodando a aplicação
```python
from app.validator import ValidadorSenha

v = ValidadorSenha()
resultado = v.validar("MinhaSenh@1")
print(resultado)
# {'valida': True, 'erros': []}
```

### Rodando os testes
```bash
# Testes simples
pytest

# Com relatório de cobertura
pytest --cov=app --cov-report=term-missing
```

---

## 📋 Regras de Negócio Testadas

| ID     | Regra                                                             | Método Validador                  |
|--------|-------------------------------------------------------------------|-----------------------------------|
| RN-01  | Senha deve ter **no mínimo 8 caracteres**                         | `_tem_comprimento_minimo`         |
| RN-02  | Senha deve ter **no máximo 128 caracteres**                       | `_respeita_comprimento_maximo`    |
| RN-03  | Senha deve conter **ao menos uma letra maiúscula** (A–Z)          | `_tem_letra_maiuscula`            |
| RN-04  | Senha deve conter **ao menos uma letra minúscula** (a–z)          | `_tem_letra_minuscula`            |
| RN-05  | Senha deve conter **ao menos um dígito numérico** (0–9)           | `_tem_digito`                     |
| RN-06  | Senha deve conter **ao menos um caractere especial** (!@#$ etc.)  | `_tem_caractere_especial`         |
| RN-07  | Senha **não deve conter espaços**                                 | `_tem_espacos`                    |
| RN-08  | Senha **não deve ter 3 ou mais caracteres idênticos consecutivos**| `_tem_sequencia_repetida`         |
| RN-09  | **Entrada deve ser string** — TypeError para outros tipos         | `validar` (guard clause)          |

---

## 🧪 Estrutura dos Testes

Os testes estão organizados por regra de negócio em `tests/test_validator.py`:

```
tests/
└── test_validator.py
    ├── TestComprimentoMinimo       → RN-01
    ├── TestComprimentoMaximo       → RN-02
    ├── TestLetraMaiuscula          → RN-03
    ├── TestLetraMinuscula          → RN-04
    ├── TestDigitoNumerico          → RN-05
    ├── TestCaractereEspecial       → RN-06 (parametrizado: 10 caracteres)
    ├── TestEspacos                 → RN-07
    ├── TestSequenciaRepetida       → RN-08
    ├── TestTipoEntrada             → RN-09
    └── TestCenariosCompletos       → RN-01 a RN-08 (integração)
```

---

## 📊 Relatório de Cobertura

```
---------- coverage: platform linux, python 3.11 ----------

Name                   Stmts   Miss  Cover   Missing
----------------------------------------------------
app/__init__.py            0      0   100%
app/validator.py          35      0   100%
----------------------------------------------------
TOTAL                     35      0   100%

=================== 40 passed in 0.42s ===================
```

---

## 📁 Estrutura do Projeto

```
password_validator/
├── app/
│   ├── __init__.py
│   └── validator.py          # Lógica de validação
├── tests/
│   ├── __init__.py
│   └── test_validator.py     # Testes unitários
├── pytest.ini                # Configuração do Pytest
├── requirements.txt          # Dependências
└── README.md
```

---

## 🛠 Ferramentas Utilizadas

- **Python 3.8+**
- **Pytest** — framework de testes
- **pytest-cov** — relatório de cobertura de testes

<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/007d0a8b-b434-4aa6-ab4c-889f0cb7b67f" />
