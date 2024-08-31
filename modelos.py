class Cliente:
    def __init__(self, id_cliente, nome, telefone, data_cadastro):
        self.id_cliente = id_cliente
        self.nome = nome
        self.telefone = telefone
        self.data_cadastro = data_cadastro

class TipoProduto:
    def __init__(self, cod, descricao):
        self.cod = cod
        self.descricao = descricao

class Fornecedor:
    def __init__(self, id_fornecedor, nome_empresa, tipo_empresa):
        self.id_fornecedor = id_fornecedor
        self.nome_empresa = nome_empresa
        self.tipo_empresa = tipo_empresa


class Produto:
    def __init__(self, id_produto, nome, preco_custo, id_tipo_produto, fabricante, marca, cor, id_fornecedor, data_cadastro):
        self.id_produto = id_produto
        self.nome = nome
        self.preco_custo = preco_custo
        self.tipo_produto = id_tipo_produto
        self.fabricante = fabricante
        self.marca = marca
        self.cor = cor
        self.id_fornecedor = id_fornecedor
        self.data_cadastro = data_cadastro


class Venda:
    def __init__(self, id_venda, data_venda, id_cliente, id_produto, quantidade, preco_venda, lucro):
        self.id_venda = id_venda
        self.data_venda = data_venda
        self.id_cliente = id_cliente
        self.id_produto = id_produto
        self.quantidade = quantidade
        self.preco_venda = preco_venda
        self.lucro = lucro
