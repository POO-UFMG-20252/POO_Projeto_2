class Player:
    def _init_(self, dinheiro_inicial: int = 100, vida_inicial: int = 20):
        self.dinheiro: int = dinheiro_inicial
        self.vida: int = vida_inicial
        self.torres_possuidas: list = []   


    def comprar_torre(self, torre, custo: int) -> bool:

        if self.dinheiro >= custo:
            self.dinheiro -= custo
            self.torres_possuidas.append(torre)
            return True
        return False

    def perder_vida(self, qtd: int) -> None:

        self.vida -= qtd
        if self.vida < 0:
            self.vida = 0


    def ganhar_dinheiro(self, qtd: int) -> None:


        self.dinheiro += qtd

    def esta_vivo(self) -> bool:

        return self.vida > 0