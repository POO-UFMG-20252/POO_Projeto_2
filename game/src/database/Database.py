import sqlite3
from datetime import datetime
import os

class Database:
    def __init__(self, db_name="tower_defense.db"):
        # Garante que o banco fica na pasta database
        db_path = os.path.join(os.path.dirname(__file__), db_name)
        self.db_name = db_path
        self.criar_tabelas()
    
    def criar_tabelas(self):
        """Cria a tabela leaderboard se não existir"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS leaderboard (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_player TEXT NOT NULL,
                pontuacao INTEGER NOT NULL,
                wave_alcancada INTEGER NOT NULL,
                dinheiro_final INTEGER NOT NULL,
                torres_construidas INTEGER NOT NULL,
                inimigos_eliminados INTEGER NOT NULL,
                data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f" Banco de dados inicializado: {self.db_name}")
    
    def salvar_pontuacao(self, nome_player, pontuacao, wave_alcancada, 
                         dinheiro_final, torres_construidas, inimigos_eliminados):
        """Salva a pontuação completa do jogador no leaderboard"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO leaderboard 
                (nome_player, pontuacao, wave_alcancada, dinheiro_final, 
                 torres_construidas, inimigos_eliminados)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (nome_player, pontuacao, wave_alcancada, dinheiro_final, 
                  torres_construidas, inimigos_eliminados))
            
            conn.commit()
            conn.close()
            print(f" Pontuação salva: {nome_player} - {pontuacao} pontos")
            return True
        except Exception as e:
            print(f" Erro ao salvar pontuação: {e}")
            return False
    
    def obter_top_10(self):
        """Retorna os 10 melhores jogadores"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT nome_player, pontuacao, wave_alcancada, 
                       inimigos_eliminados, data_hora
                FROM leaderboard
                ORDER BY pontuacao DESC, wave_alcancada DESC
                LIMIT 10
            ''')
            
            resultados = cursor.fetchall()
            conn.close()
            
            return resultados
        except Exception as e:
            print(f" Erro ao obter top 10: {e}")
            return []
    
    def obter_melhor_pontuacao_player(self, nome_player):
        """Retorna a melhor pontuação de um jogador específico"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT MAX(pontuacao), wave_alcancada, inimigos_eliminados
                FROM leaderboard
                WHERE nome_player = ?
            ''', (nome_player,))
            
            resultado = cursor.fetchone()
            conn.close()
            
            if resultado and resultado[0]:
                return {
                    'pontuacao': resultado[0],
                    'wave': resultado[1],
                    'inimigos': resultado[2]
                }
            return None
        except Exception as e:
            print(f" Erro ao obter melhor pontuação: {e}")
            return None
    
    def obter_estatisticas_player(self, nome_player):
        """Retorna estatísticas gerais do jogador"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_partidas,
                    MAX(pontuacao) as melhor_pontuacao,
                    AVG(pontuacao) as pontuacao_media,
                    MAX(wave_alcancada) as melhor_wave,
                    SUM(inimigos_eliminados) as total_inimigos
                FROM leaderboard
                WHERE nome_player = ?
            ''', (nome_player,))
            
            resultado = cursor.fetchone()
            conn.close()
            
            if resultado:
                return {
                    'total_partidas': resultado[0],
                    'melhor_pontuacao': resultado[1] or 0,
                    'pontuacao_media': int(resultado[2]) if resultado[2] else 0,
                    'melhor_wave': resultado[3] or 0,
                    'total_inimigos': resultado[4] or 0
                }
            return None
        except Exception as e:
            print(f" Erro ao obter estatísticas: {e}")
            return None