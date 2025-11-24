class Player:
    def __init__(self, vida, dinheiro, inimigos_eliminados):
        self.vida = vida
        self.dinheiro = dinheiro
        self.pontuacao = 0
        self.inimigos_eliminados = inimigos_eliminados
    def receber_dano(self, dano):
        self.vida -= dano
        return self.vida <= 0
    
    def adicionar_dinheiro(self, quantidade):
        self.dinheiro += quantidade
    
    def gastar_dinheiro(self, quantidade):
        if self.dinheiro >= quantidade:
            self.dinheiro -= quantidade
            return True
        return False
    
    def adicionar_pontuacao(self, pontos):
        self.pontuacao += pontos

    def adicionar_inimigo(self, inimigos_eliminados):
        self.inimigos_eliminados += inimigos_eliminados