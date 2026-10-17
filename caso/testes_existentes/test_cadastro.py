import unittest

from miniloja import cadastro


class TestCadastro(unittest.TestCase):
    # Alterado no B1 (AV1.1): R3.4 muda a resposta de cadastro inválido de 400 para 422
    # com lista de erros, e R3.1 torna o cpf obrigatório (o caso válido passa a enviá-lo).
    def test_cadastro_sem_nome_e_rejeitado(self):
        cadastro.limpar()
        status, corpo = cadastro.cadastrar_cliente({"email": "a@b.com", "cpf": "529.982.247-25"})
        self.assertEqual(status, 422)
        self.assertEqual([e["campo"] for e in corpo["erros"]], ["nome"])

    def test_cadastro_valido(self):
        cadastro.limpar()
        status, corpo = cadastro.cadastrar_cliente(
            {"nome": "Ana", "email": "ana@exemplo.com", "cpf": "529.982.247-25"}
        )
        self.assertEqual(status, 201)
        self.assertEqual(corpo["id"], 1)
