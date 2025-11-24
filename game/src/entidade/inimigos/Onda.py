import random
from entidade.inimigos.impl import InimigoNormal, InimigoRapido, InimigoForte

class Onda:
    def __init__(self, numero_onda):
        self.numero = numero_onda
        self.inimigos_restantes = self._calcular_total_inimigos()
        self.inimigos_por_lote = self._calcular_inimigos_por_lote()
        self.tempo_entre_lotes = 120  # Aumentei para 2 segundos entre lotes
        self.tempo_entre_inimigos = 30  # 0.3 segundos entre inimigos no mesmo lote
        self.timer_lote = 0
        self.timer_inimigo = 0
        self.ativa = True
        self.spawnando_lote = False
        self.inimigos_para_spawnar = []
        self.inimigos_spawnados_no_lote = 0
        
        # Definir composição da onda baseada no número
        self.composicao = self._definir_composicao()
    
    def _calcular_total_inimigos(self):
        """Calcula o total de inimigos baseado no número da onda"""
        return 5 + (self.numero * 2)  # Reduzi o crescimento
    
    def _calcular_inimigos_por_lote(self):
        """Calcula quantos inimigos spawnam por lote"""
        return min(2 + (self.numero // 3), 5)  # Reduzi o máximo por lote
    
    def _definir_composicao(self):
        """Define a composição de tipos de inimigos na onda"""
        if self.numero == 1:
            return {"Normal": 1.0}  # 100% normais
        elif self.numero <= 3:
            return {"Normal": 0.8, "Rapido": 0.2}  # 80% normais, 20% rápidos
        elif self.numero <= 5:
            return {"Normal": 0.6, "Rapido": 0.3, "Forte": 0.1}  # 60% normais, 30% rápidos, 10% fortes
        else:
            return {"Normal": 0.4, "Rapido": 0.3, "Forte": 0.3}  # Mix balanceado
    
    def update(self):
        """Atualiza a onda e retorna lista de inimigos para spawnar"""
        if not self.ativa or self.inimigos_restantes <= 0:
            return []

        inimigos_para_spawnar = []
        
        # Sistema de lotes com spawn gradual
        if not self.spawnando_lote:
            self.timer_lote += 1
            if self.timer_lote >= self.tempo_entre_lotes:
                self._preparar_novo_lote()
        
        # Spawn gradual dentro do lote
        if self.spawnando_lote:
            self.timer_inimigo += 1
            if (self.timer_inimigo >= self.tempo_entre_inimigos and 
                self.inimigos_spawnados_no_lote < len(self.inimigos_para_spawnar)):
                
                inimigo = self.inimigos_para_spawnar[self.inimigos_spawnados_no_lote]
                inimigos_para_spawnar.append(inimigo)
                self.inimigos_spawnados_no_lote += 1
                self.inimigos_restantes -= 1
                self.timer_inimigo = 0
                
                # Verificar se terminou o lote
                if self.inimigos_spawnados_no_lote >= len(self.inimigos_para_spawnar):
                    self.spawnando_lote = False
                    self.timer_lote = 0
                    
                    # Verificar se a onda terminou
                    if self.inimigos_restantes <= 0:
                        self.ativa = False
        
        return inimigos_para_spawnar
    
    def _preparar_novo_lote(self):
        """Prepara um novo lote de inimigos para spawn gradual"""
        quantidade_lote = min(self.inimigos_por_lote, self.inimigos_restantes)
        self.inimigos_para_spawnar = []
        
        for _ in range(quantidade_lote):
            tipo_inimigo = self._escolher_tipo_inimigo()
            self.inimigos_para_spawnar.append(tipo_inimigo)
        
        self.spawnando_lote = True
        self.inimigos_spawnados_no_lote = 0
        self.timer_inimigo = 0
    
    def _escolher_tipo_inimigo(self):
        """Escolhe aleatoriamente o tipo de inimigo baseado na composição"""
        rand = random.random()
        acumulado = 0
        
        for tipo, probabilidade in self.composicao.items():
            acumulado += probabilidade
            if rand <= acumulado:
                if tipo == "Normal":
                    return InimigoNormal()
                elif tipo == "Rapido":
                    return InimigoRapido()
                elif tipo == "Forte":
                    return InimigoForte()
        
        # Fallback
        return InimigoNormal()
    
    def esta_ativa(self):
        return self.ativa or self.spawnando_lote
    
    def get_info(self):
        return {
            "numero": self.numero,
            "inimigos_restantes": self.inimigos_restantes,
            "composicao": self.composicao,
            "spawnando_lote": self.spawnando_lote
        }