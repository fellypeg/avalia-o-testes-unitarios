import re

class SenhaInvalidaError(Exception):
    pass


class ValidadorSenha:
    COMPRIMENTO_MINIMO = 8
    COMPRIMENTO_MAXIMO = 128

    def validar(self, senha: str) -> dict:
        """
        Valida uma senha conforme todas as regras de negócio.
        Retorna um dicionário com resultado e erros encontrados.
        """
        if not isinstance(senha, str):
            raise TypeError("A senha deve ser uma string.")

        erros = []

        if not self._tem_comprimento_minimo(senha):
            erros.append(f"Senha deve ter ao menos {self.COMPRIMENTO_MINIMO} caracteres.")

        if not self._respeita_comprimento_maximo(senha):
            erros.append(f"Senha deve ter no máximo {self.COMPRIMENTO_MAXIMO} caracteres.")

        if not self._tem_letra_maiuscula(senha):
            erros.append("Senha deve conter ao menos uma letra maiúscula.")

        if not self._tem_letra_minuscula(senha):
            erros.append("Senha deve conter ao menos uma letra minúscula.")

        if not self._tem_digito(senha):
            erros.append("Senha deve conter ao menos um dígito numérico.")

        if not self._tem_caractere_especial(senha):
            erros.append("Senha deve conter ao menos um caractere especial (!@#$%^&*...).")

        if self._tem_espacos(senha):
            erros.append("Senha não deve conter espaços.")

        if self._tem_sequencia_repetida(senha):
            erros.append("Senha não deve conter 3 ou mais caracteres idênticos consecutivos.")

        return {
            "valida": len(erros) == 0,
            "erros": erros,
        }

    def _tem_comprimento_minimo(self, senha: str) -> bool:
        return len(senha) >= self.COMPRIMENTO_MINIMO

    def _respeita_comprimento_maximo(self, senha: str) -> bool:
        return len(senha) <= self.COMPRIMENTO_MAXIMO

    def _tem_letra_maiuscula(self, senha: str) -> bool:
        return bool(re.search(r"[A-Z]", senha))

    def _tem_letra_minuscula(self, senha: str) -> bool:
        return bool(re.search(r"[a-z]", senha))

    def _tem_digito(self, senha: str) -> bool:
        return bool(re.search(r"\d", senha))

    def _tem_caractere_especial(self, senha: str) -> bool:
        return bool(re.search(r"[!@#$%^&*()\-_=+\[\]{};:'\",.<>?/\\|`~]", senha))

    def _tem_espacos(self, senha: str) -> bool:
        return " " in senha

    def _tem_sequencia_repetida(self, senha: str) -> bool:
        return bool(re.search(r"(.)\1{2,}", senha))
