class Restaurante:
    def __init__(self, nome, categoria, ativo = False):
        self.nome = nome
        self.categoria = categoria
        self.ativo = ativo
        pass
    def __str__(self):
        return self.nome
restaurantes = []
restaurantes.append(Restaurante("Pipocaria", 'pipoca', True))


nomes = ['Caue', 'Valeria', 'Gabriel']
categorias = ['Hamburgueria', 'Coxinharia', 'Pizzaria']

for i in range(3):
    restaurantes.append(Restaurante(nomes[i], categorias[i]))

for j in restaurantes:
    print(j)