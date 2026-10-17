"""Cadastro de clientes (contrato R3 em caso/regras.md)."""
import re

_CLIENTES = []

_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")  # R3.3: texto@texto.texto
_CPF_PERMITIDO = re.compile(r"^[\d.\-]+$")  # R3.2: com ou sem pontuação


def cpf_valido(cpf):
    """R3.2: 11 dígitos, dígitos verificadores válidos e não todos iguais."""
    if not isinstance(cpf, str) or not _CPF_PERMITIDO.match(cpf):
        return False
    d = [int(c) for c in cpf if c.isdigit()]
    if len(d) != 11 or len(set(d)) == 1:
        return False
    for n in (9, 10):
        soma = sum(d[i] * (n + 1 - i) for i in range(n))
        if (soma * 10) % 11 % 10 != d[n]:
            return False
    return True


def validar_cliente(payload):
    """Devolve a lista de TODOS os erros (R3.4), vazia se o payload é válido."""
    erros = []
    if not payload.get("nome"):
        erros.append({"campo": "nome", "erro": "obrigatório"})
    email = payload.get("email")
    if not email:
        erros.append({"campo": "email", "erro": "obrigatório"})
    elif not isinstance(email, str) or not _EMAIL.match(email):
        erros.append({"campo": "email", "erro": "formato inválido"})
    cpf = payload.get("cpf")
    if not cpf:
        erros.append({"campo": "cpf", "erro": "obrigatório"})
    elif not cpf_valido(cpf):
        erros.append({"campo": "cpf", "erro": "inválido"})
    return erros


def cadastrar_cliente(payload):
    """Cadastra um cliente: 422 com todos os erros (R3.4) ou 201 com id sequencial (R3.5)."""
    erros = validar_cliente(payload)
    if erros:
        return 422, {"erros": erros}
    cliente = dict(payload, id=len(_CLIENTES) + 1)
    _CLIENTES.append(cliente)
    return 201, cliente


def limpar():
    _CLIENTES.clear()
