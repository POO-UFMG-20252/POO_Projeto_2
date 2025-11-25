class Player:
    def __init__(self, vida, dinheiro, inimigos_eliminados):
        self.__vida = vida
        self.__dinheiro = dinheiro
        self.__pontuacao = 0
        self.__inimigos_eliminados = inimigos_eliminados
        
    def receber_dano(self, dano):
        self.__vida -= dano
        return self.__vida <= 0
    
    def adicionar_dinheiro(self, quantidade):
        self.__dinheiro += quantidade
    
    def gastar_dinheiro(self, quantidade):
        if self.__dinheiro >= quantidade:
            self.__dinheiro -= quantidade
            return True
        return False
    
    def adicionar_pontuacao(self, pontos):
        self.__pontuacao += pontos

    def adicionar_inimigo(self, inimigos_eliminados):
        self.__inimigos_eliminados += inimigos_eliminados
        
    @property
    def vida(self):
        return self.__vida

    @vida.setter
    def vida(self, valor):
        self.__vida = valor

    @property
    def dinheiro(self):
        return self.__dinheiro

    @dinheiro.setter
    def dinheiro(self, valor):
        self.__dinheiro = valor

    @property
    def pontuacao(self):
        return self.__pontuacao

    @pontuacao.setter
    def pontuacao(self, valor):
        self.__pontuacao = valor
        
    @property
    def inimigos_eliminados(self):
        return self.__inimigos_eliminados

    @inimigos_eliminados.setter
    def inimigos_eliminados(self, valor):
        self.__inimigos_eliminados = valor