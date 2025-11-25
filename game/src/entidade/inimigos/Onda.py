import random
from entidade.inimigos.impl import InimigoNormal, InimigoRapido, InimigoForte

class Onda:
    def __init__(self, numero_onda):
        self.__numero = numero_onda
        self.__inimigos_restantes = self._calcular_total_inimigos()
        self.__inimigos_por_lote = self._calcular_inimigos_por_lote()
        self.__tempo_entre_lotes = 120  
        self.__tempo_entre_inimigos = 30
        self.__timer_lote = 0
        self.__timer_inimigo = 0
        self.__ativa = True
        self.__spawnando_lote = False
        self.__inimigos_para_spawnar = []
        self.__inimigos_spawnados_no_lote = 0
        
        self.__composicao = self._definir_composicao()
    
    def _calcular_total_inimigos(self):
        return 5 + (self.__numero * 2)  
    
    def _calcular_inimigos_por_lote(self):
        return min(2 + (self.__numero // 3), 5)  
    
    def _definir_composicao(self):
        if self.__numero == 1:
            return {"Normal": 1.0} 
        elif self.__numero <= 3:
            return {"Normal": 0.8, "Rapido": 0.2} 
        elif self.__numero <= 5:
            return {"Normal": 0.6, "Rapido": 0.3, "Forte": 0.1}  
        else:
            return {"Normal": 0.4, "Rapido": 0.3, "Forte": 0.3} 
    
    def update(self):
        if not self.__ativa or self.__inimigos_restantes <= 0:
            return []

        inimigos_para_spawnar = []
        
        if not self.__spawnando_lote:
            self.__timer_lote += 1
            if self.__timer_lote >= self.__tempo_entre_lotes:
                self._preparar_novo_lote()
        
        if self.__spawnando_lote:
            self.__timer_inimigo += 1
            if (self.__timer_inimigo >= self.__tempo_entre_inimigos and 
                self.__inimigos_spawnados_no_lote < len(self.__inimigos_para_spawnar)):
                
                inimigo = self.__inimigos_para_spawnar[self.__inimigos_spawnados_no_lote]
                inimigos_para_spawnar.append(inimigo)
                self.__inimigos_spawnados_no_lote += 1
                self.__inimigos_restantes -= 1
                self.__timer_inimigo = 0
                
                if self.__inimigos_spawnados_no_lote >= len(self.__inimigos_para_spawnar):
                    self.__spawnando_lote = False
                    self.__timer_lote = 0
                    
                    if self.__inimigos_restantes <= 0:
                        self.__ativa = False
        
        return inimigos_para_spawnar
    
    def _preparar_novo_lote(self):
        quantidade_lote = min(self.__inimigos_por_lote, self.__inimigos_restantes)
        self.__inimigos_para_spawnar = []
        
        for _ in range(quantidade_lote):
            tipo_inimigo = self._escolher_tipo_inimigo()
            self.__inimigos_para_spawnar.append(tipo_inimigo)
        
        self.__spawnando_lote = True
        self.__inimigos_spawnados_no_lote = 0
        self.__timer_inimigo = 0
    
    def _escolher_tipo_inimigo(self):
        rand = random.random()
        acumulado = 0
        
        for tipo, probabilidade in self.__composicao.items():
            acumulado += probabilidade
            if rand <= acumulado:
                if tipo == "Normal":
                    return InimigoNormal()
                elif tipo == "Rapido":
                    return InimigoRapido()
                elif tipo == "Forte":
                    return InimigoForte()
        
        return InimigoNormal()
    
    def esta_ativa(self):
        return self.__ativa or self.__spawnando_lote
    
    def get_info(self):
        return {
            "numero": self.__numero,
            "inimigos_restantes": self.__inimigos_restantes,
            "composicao": self.__composicao,
            "spawnando_lote": self.__spawnando_lote
        }
    
    @property
    def numero(self):
        return self.__numero

    @numero.setter
    def numero(self, valor):
        self.__numero = valor

    @property
    def inimigos_restantes(self):
        return self.__inimigos_restantes

    @inimigos_restantes.setter
    def inimigos_restantes(self, valor):
        self.__inimigos_restantes = valor

    @property
    def inimigos_por_lote(self):
        return self.__inimigos_por_lote

    @inimigos_por_lote.setter
    def inimigos_por_lote(self, valor):
        self.__inimigos_por_lote = valor

    @property
    def tempo_entre_lotes(self):
        return self.__tempo_entre_lotes

    @tempo_entre_lotes.setter
    def tempo_entre_lotes(self, valor):
        self.__tempo_entre_lotes = valor

    @property
    def tempo_entre_inimigos(self):
        return self.__tempo_entre_inimigos

    @tempo_entre_inimigos.setter
    def tempo_entre_inimigos(self, valor):
        self.__tempo_entre_inimigos = valor

    @property
    def timer_lote(self):
        return self.__timer_lote

    @timer_lote.setter
    def timer_lote(self, valor):
        self.__timer_lote = valor

    @property
    def timer_inimigo(self):
        return self.__timer_inimigo

    @timer_inimigo.setter
    def timer_inimigo(self, valor):
        self.__timer_inimigo = valor

    @property
    def ativa(self):
        return self.__ativa

    @ativa.setter
    def ativa(self, valor):
        self.__ativa = valor

    @property
    def spawnando_lote(self):
        return self.__spawnando_lote

    @spawnando_lote.setter
    def spawnando_lote(self, valor):
        self.__spawnando_lote = valor

    @property
    def inimigos_para_spawnar(self):
        return self.__inimigos_para_spawnar

    @inimigos_para_spawnar.setter
    def inimigos_para_spawnar(self, valor):
        self.__inimigos_para_spawnar = valor

    @property
    def inimigos_spawnados_no_lote(self):
        return self.__inimigos_spawnados_no_lote

    @inimigos_spawnados_no_lote.setter
    def inimigos_spawnados_no_lote(self, valor):
        self.__inimigos_spawnados_no_lote = valor