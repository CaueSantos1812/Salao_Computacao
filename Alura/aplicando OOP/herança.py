class Veiculo:
    def __init__(self, marca, modelo, ativo = False):
        self.marca = marca
        self.modelo = modelo
        self._ativo = ativo
        pass
    def __str__(self):
        ativo = 'ativo' if self._ativo else 'Desativado'
        return f'O modelo {self.modelo} da marca {self.marca} está {ativo}'
    
class Carro(Veiculo):
    def __init__(self, marca, modelo, portas = 4, ativo=False):
        super().__init__(marca, modelo, ativo)
        self.portas = portas

    def __str__(self):
        return super().__str__()+f' e possui {self.portas} portas'

carrao = Veiculo('Ford', 'Fiesta', True)
carito = Carro(carrao, 4)
print(carito)