import pytest
from app.validator import ValidadorSenha

@pytest.fixture
def validador():
    return ValidadorSenha()


# Comprimento mínimo (8 caracteres)

class TestComprimentoMinimo:
    def test_senha_com_exatamente_8_caracteres_e_valida(self, validador):
        resultado = validador.validar("Ab1!xyzw")
        assert resultado["valida"] is True

    def test_senha_com_7_caracteres_e_invalida(self, validador):
        resultado = validador.validar("Ab1!xyz")
        assert resultado["valida"] is False
        assert any("8 caracteres" in e for e in resultado["erros"])

    def test_senha_vazia_e_invalida(self, validador):
        resultado = validador.validar("")
        assert resultado["valida"] is False

    def test_senha_com_mais_de_8_caracteres_passa_regra_comprimento(self, validador):
        resultado = validador.validar("Ab1!xyzwQRST")
        assert not any("ao menos 8" in e for e in resultado["erros"])



# Comprimento máximo (128 caracteres)

class TestComprimentoMaximo:
    def test_senha_com_128_caracteres_passa_regra(self, validador):
        senha = "Ab1!" + "a" * 124          # 128 chars total
        resultado = validador.validar(senha)
        assert not any("máximo" in e for e in resultado["erros"])

    def test_senha_com_129_caracteres_e_invalida(self, validador):
        senha = "Ab1!" + "a" * 125          # 129 chars
        resultado = validador.validar(senha)
        assert any("128 caracteres" in e for e in resultado["erros"])



# Letra maiúscula obrigatória

class TestLetraMaiuscula:
    def test_senha_sem_maiuscula_e_invalida(self, validador):
        resultado = validador.validar("ab1!aaaa")
        assert any("maiúscula" in e for e in resultado["erros"])

    def test_senha_com_maiuscula_passa_regra(self, validador):
        resultado = validador.validar("Ab1!xyzw")
        assert not any("maiúscula" in e for e in resultado["erros"])

    def test_maiuscula_no_meio_da_senha(self, validador):
        resultado = validador.validar("ab1!Axyz")
        assert not any("maiúscula" in e for e in resultado["erros"])


# Letra minúscula obrigatória

class TestLetraMinuscula:
    def test_senha_sem_minuscula_e_invalida(self, validador):
        resultado = validador.validar("AB1!AAAA")
        assert any("minúscula" in e for e in resultado["erros"])

    def test_senha_com_minuscula_passa_regra(self, validador):
        resultado = validador.validar("AB1!xyzw")
        assert not any("minúscula" in e for e in resultado["erros"])



# Dígito numérico obrigatório

class TestDigitoNumerico:
    def test_senha_sem_digito_e_invalida(self, validador):
        resultado = validador.validar("Abcd!efg")
        assert any("dígito" in e for e in resultado["erros"])

    def test_senha_com_digito_passa_regra(self, validador):
        resultado = validador.validar("Abcd1!fg")
        assert not any("dígito" in e for e in resultado["erros"])

    def test_multiplos_digitos_passa_regra(self, validador):
        resultado = validador.validar("Ab123!fg")
        assert not any("dígito" in e for e in resultado["erros"])



# Caractere especial obrigatório

class TestCaractereEspecial:
    def test_senha_sem_especial_e_invalida(self, validador):
        resultado = validador.validar("Abcd1234")
        assert any("especial" in e for e in resultado["erros"])

    @pytest.mark.parametrize("especial", ["!", "@", "#", "$", "%", "^", "&", "*", "-", "_"])
    def test_diversos_caracteres_especiais_sao_aceitos(self, validador, especial):
        senha = f"Abcd123{especial}"
        resultado = validador.validar(senha)
        assert not any("especial" in e for e in resultado["erros"])



#  Espaços não são permitidos

class TestEspacos:
    def test_senha_com_espaco_e_invalida(self, validador):
        resultado = validador.validar("Ab1! aaaa")
        assert any("espaço" in e for e in resultado["erros"])

    def test_senha_sem_espaco_passa_regra(self, validador):
        resultado = validador.validar("Ab1!xyzw")
        assert not any("espaço" in e for e in resultado["erros"])

    def test_senha_so_com_espacos_e_invalida(self, validador):
        resultado = validador.validar("        ")
        assert resultado["valida"] is False


# Sequência de 3+ caracteres idênticos proibida

class TestSequenciaRepetida:
    def test_tres_caracteres_iguais_consecutivos_e_invalido(self, validador):
        resultado = validador.validar("Ab1!aaab")
        assert any("consecutivos" in e for e in resultado["erros"])

    def test_dois_caracteres_iguais_consecutivos_e_permitido(self, validador):
        resultado = validador.validar("Ab1!aabb")
        assert not any("consecutivos" in e for e in resultado["erros"])

    def test_sequencia_de_numeros_repetidos_e_invalida(self, validador):
        resultado = validador.validar("Ab!11112")
        assert any("consecutivos" in e for e in resultado["erros"])


# Tipo de entrada inválido

class TestTipoEntrada:
    def test_entrada_none_levanta_type_error(self, validador):
        with pytest.raises(TypeError):
            validador.validar(None)

    def test_entrada_inteiro_levanta_type_error(self, validador):
        with pytest.raises(TypeError):
            validador.validar(12345678)

    def test_entrada_lista_levanta_type_error(self, validador):
        with pytest.raises(TypeError):
            validador.validar(["Ab1!aaaa"])



# Cenários completos (senhas válidas e inválidas reais)

class TestCenariosCompletos:
    @pytest.mark.parametrize("senha_valida", [
        "Secure@1",
        "MyP@ssw0rd",
        "Tr0ub4dor&3",
        "C0rr3ct!Horse",
        "X$9abcDE",
    ])
    def test_senhas_validas_sao_aceitas(self, validador, senha_valida):
        resultado = validador.validar(senha_valida)
        assert resultado["valida"] is True, f"Esperava válida: {senha_valida} — Erros: {resultado['erros']}"

    @pytest.mark.parametrize("senha_invalida,motivo", [
        ("short1!", "muito curta"),
        ("semdigito!", "sem dígito"),
        ("SEMMINUSCULA1!", "sem minúscula"),
        ("semmaiuscula1!", "sem maiúscula"),
        ("SemEspecial12", "sem especial"),
        ("Com Espaco1!", "com espaço"),
        ("Aaaa1!bb", "sequência repetida"),
    ])
    def test_senhas_invalidas_sao_rejeitadas(self, validador, senha_invalida, motivo):
        resultado = validador.validar(senha_invalida)
        assert resultado["valida"] is False, f"Esperava inválida ({motivo}): {senha_invalida}"
