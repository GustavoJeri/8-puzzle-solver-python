from pysat.solvers import Glucose4
import random

def criar_mapeamento(max_passos):
    mapeamento = {}
    contador_var = 1
    for t in range(1, max_passos + 1):
        for l in range(1,4):
            for c in range(1,4):
                for v in range(0,9):
                    mapeamento[f"{t}_P_{l}_{c}_{v}"] = contador_var
                    contador_var += 1
    for t in range(1, max_passos):
        for m in ['C', 'B', 'E', 'D']:
            mapeamento[f"{t}_A_{m}"] = contador_var
            contador_var += 1
    return mapeamento

def min_um(meu_mapeamento, max_passos):
    lista_regras = []
    for t in range(1, max_passos + 1):
        for l in range(1,4):
            for c in range(1,4):
                regras_casa = [meu_mapeamento[f"{t}_P_{l}_{c}_{v}"] for v in range(0,9)]
                lista_regras.append(regras_casa)
    return lista_regras
            
def max_um(meu_mapeamento, max_passos):
    lista_clausulas = []
    for t in range(1, max_passos + 1):
        for l in range(1, 4):
            for c in range(1, 4):
                for v1 in range(0,9):
                    for v2 in range(v1 + 1,9):
                        n1 = meu_mapeamento[f"{t}_P_{l}_{c}_{v1}"]
                        n2 = meu_mapeamento[f"{t}_P_{l}_{c}_{v2}"]
                        lista_clausulas.append([-n1, -n2])
    return lista_clausulas

def max_uma_acao(meu_mapeamento, max_passos):
    lista_acao = []
    movimentos = ['C', 'B', 'E', 'D']
    for t in range(1, max_passos):
        for i, m1 in enumerate(movimentos):
            for m2 in movimentos[i + 1:]:
                lista_acao.append([-meu_mapeamento[f"{t}_A_{m1}"], -meu_mapeamento[f"{t}_A_{m2}"]])
    return lista_acao

def min_uma_acao(mapeamento, max_passos):
    lista_geral_clausulas = []
    for t in range(1, max_passos):
        lista_geral_clausulas.append([mapeamento[f"{t}_A_{acao}"] for acao in ['C', 'B', 'D', 'E']])
    return lista_geral_clausulas

def regra_transicao(meu_mapeamento, max_passos):
    lista_clausula_mov = []
    for t in range(1, max_passos): 
        for l in range(1,4):
            for c in range(1,4):
                if l > 1: # mover para cima
                    for v in range(1, 9):
                        pc1,pc2,a,psc1,psc2 = (meu_mapeamento[f"{t}_P_{l}_{c}_0"], meu_mapeamento[f"{t}_P_{l-1}_{c}_{v}"], meu_mapeamento[f"{t}_A_C"], meu_mapeamento[f"{t+1}_P_{l-1}_{c}_0"], meu_mapeamento[f"{t+1}_P_{l}_{c}_{v}"])
                        lista_clausula_mov.extend([[-pc1, -pc2, -a, psc1], [-pc1, -pc2, -a, psc2]])
                if l < 3: # mover para baixo
                    for v in range(1, 9):
                        pc1,pc2,a,psc1,psc2 = (meu_mapeamento[f"{t}_P_{l}_{c}_0"], meu_mapeamento[f"{t}_P_{l+1}_{c}_{v}"], meu_mapeamento[f"{t}_A_B"], meu_mapeamento[f"{t+1}_P_{l+1}_{c}_0"], meu_mapeamento[f"{t+1}_P_{l}_{c}_{v}"])
                        lista_clausula_mov.extend([[-pc1, -pc2, -a, psc1], [-pc1, -pc2, -a, psc2]])
                if c > 1: # mover para a esquerda
                    for v in range(1, 9):
                        pc1,pc2,a,psc1,psc2 = (meu_mapeamento[f"{t}_P_{l}_{c}_0"], meu_mapeamento[f"{t}_P_{l}_{c-1}_{v}"], meu_mapeamento[f"{t}_A_E"], meu_mapeamento[f"{t+1}_P_{l}_{c-1}_0"], meu_mapeamento[f"{t+1}_P_{l}_{c}_{v}"])
                        lista_clausula_mov.extend([[-pc1, -pc2, -a, psc1], [-pc1, -pc2, -a, psc2]])
                if c < 3: # mover para a direita
                    for v in range(1, 9):
                        pc1,pc2,a,psc1,psc2 = (meu_mapeamento[f"{t}_P_{l}_{c}_0"], meu_mapeamento[f"{t}_P_{l}_{c+1}_{v}"], meu_mapeamento[f"{t}_A_D"], meu_mapeamento[f"{t+1}_P_{l}_{c+1}_0"], meu_mapeamento[f"{t+1}_P_{l}_{c}_{v}"])
                        lista_clausula_mov.extend([[-pc1, -pc2, -a, psc1], [-pc1, -pc2, -a, psc2]])
    return lista_clausula_mov

def regras_inercia(meu_mapeamento, max_passos):
    lista_clausulas_inercia = []
    for t in range(1, max_passos):
        for l_zero in range(1, 4):
            for c_zero in range(1, 4):
                def add_inertia_for_move(acao_str, celulas_afetadas):
                    acao_var = meu_mapeamento[f"{t}_A_{acao_str}"]
                    zero_pos_var = meu_mapeamento[f"{t}_P_{l_zero}_{c_zero}_0"]
                    for l_inercia in range(1, 4):
                        for c_inercia in range(1, 4):
                            if (l_inercia, c_inercia) not in celulas_afetadas:
                                for v in range(0, 9):
                                    peca_t = meu_mapeamento[f"{t}_P_{l_inercia}_{c_inercia}_{v}"]
                                    peca_t1 = meu_mapeamento[f"{t+1}_P_{l_inercia}_{c_inercia}_{v}"]
                                    lista_clausulas_inercia.extend([[-acao_var, -zero_pos_var, -peca_t, peca_t1], [-acao_var, -zero_pos_var, peca_t, -peca_t1]])

                if l_zero > 1: add_inertia_for_move('C', {(l_zero, c_zero), (l_zero - 1, c_zero)})
                if l_zero < 3: add_inertia_for_move('B', {(l_zero, c_zero), (l_zero + 1, c_zero)})
                if c_zero > 1: add_inertia_for_move('E', {(l_zero, c_zero), (l_zero, c_zero - 1)})
                if c_zero < 3: add_inertia_for_move('D', {(l_zero, c_zero), (l_zero, c_zero + 1)})

    return lista_clausulas_inercia

def gerar_tabuleiro_inicial():
    tabuleiro = [[1,2,3], [4,5,6], [7,8,0]]
    liv, cov = 2, 2
    for _ in range(100):
        mov_possiveis = []
        if liv > 0: mov_possiveis.append('C')
        if liv < 2: mov_possiveis.append('B')
        if cov > 0: mov_possiveis.append('E')
        if cov < 2: mov_possiveis.append('D')
        movimento_escolhido = random.choice(mov_possiveis)
        if movimento_escolhido == 'C': linha_vizinho, coluna_vizinho = liv - 1, cov
        elif movimento_escolhido == 'B': linha_vizinho, coluna_vizinho = liv + 1, cov
        elif movimento_escolhido == 'E': linha_vizinho, coluna_vizinho = liv, cov - 1
        else: linha_vizinho, coluna_vizinho = liv, cov + 1
        tabuleiro[liv][cov], tabuleiro[linha_vizinho][coluna_vizinho] = tabuleiro[linha_vizinho][coluna_vizinho], tabuleiro[liv][cov]
        liv, cov = linha_vizinho, coluna_vizinho
    return tabuleiro

def traduzir_tab_clausula(tabuleiro, mapeamento):
    clausulas_do_estado = []
    for l in range(3):
        for c in range(3):
            clausulas_do_estado.append([mapeamento[f"1_P_{l+1}_{c+1}_{tabuleiro[l][c]}"]])
    return clausulas_do_estado

def regra_precondicao(mapeamento, max_passos):
    lista_proibicoes = []
    for t in range(1, max_passos):
        for c in range(1,4):
            lista_proibicoes.append([-mapeamento[f"{t}_A_C"], -mapeamento[f"{t}_P_1_{c}_0"]])
            lista_proibicoes.append([-mapeamento[f"{t}_A_B"], -mapeamento[f"{t}_P_3_{c}_0"]])
        for l in range(1,4):
            lista_proibicoes.append([-mapeamento[f"{t}_A_E"], -mapeamento[f"{t}_P_{l}_1_0"]])
            lista_proibicoes.append([-mapeamento[f"{t}_A_D"], -mapeamento[f"{t}_P_{l}_3_0"]])
    return lista_proibicoes

def resolver_com_sat(tabuleiro_inicial, max_passos_limite=25):
    mapeamento = criar_mapeamento(max_passos_limite)
    clausulas_iniciais = traduzir_tab_clausula(tabuleiro_inicial, mapeamento)
    
    tabuleiro_final = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    mapa_reverso = {valor: chave for chave, valor in mapeamento.items()}

    for n in range(1, max_passos_limite + 1):
        print(f"Tentando resolver com {n} passo(s)...")

        clausulas_finais = []
        for l in range(3):
            for c in range(3):
                v = tabuleiro_final[l][c]
                clausulas_finais.append([mapeamento[f"{n}_P_{l+1}_{c+1}_{v}"]])

        regra_posicao = min_um(mapeamento, n)
        regra_exclusao = max_um(mapeamento, n)
        regra_acao_max = max_uma_acao(mapeamento, n)
        regra_acao_min = min_uma_acao(mapeamento, n)
        regra_transi = regra_transicao(mapeamento, n)
        regra_proibicao = regra_precondicao(mapeamento, n)
        regra_iner = regras_inercia(mapeamento, n)

        formula_completa = (clausulas_iniciais + clausulas_finais + 
                            regra_posicao + regra_exclusao + 
                            regra_acao_max + regra_acao_min + 
                            regra_transi + regra_proibicao + regra_iner)
        
        with Glucose4(bootstrap_with=formula_completa) as solver:
            if solver.solve():
                modelo = solver.get_model()
                solucao_ordenada = {}
                for num in modelo:
                    if num > 0:
                        nome_da_variavel = mapa_reverso.get(num, "")
                        if "_A_" in nome_da_variavel:
                            partes = nome_da_variavel.split('_')
                            tempo = int(partes[0])
                            acao = partes[2]
                            solucao_ordenada[tempo] = acao
                
                print(f"Solução encontrada com {n-1} movimento(s)!")
                return solucao_ordenada, n
    
    print("Nenhuma solução encontrada no limite de passos.")
    return None, None