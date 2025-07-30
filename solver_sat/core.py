from pysat.solvers import Glucose4
import random

#t -> tempo
#l -> linha
#c -> coluna
#v ou p -> variavel/ peça
def criar_mapeamento(max_passos):
    #t_P_l_c_v 
    mapeamento = {}
    contador_var = 1
    
    for t in range(1, max_passos + 1):
        for l in range(1,4):
            for c in range(1,4):
                for v in range(0,9):
                    variavel_str = f"{t}P{l}{c}{v}"
                    mapeamento[variavel_str] = contador_var
                    contador_var += 1

    #t_A_M
    for t in range(1, max_passos): #até o estado 9, pois do estado 10 simboliza que passou para o estado 11
        for m in ['C', 'B', 'E', 'D']:
            variavel_str = f"{t}A{m}"
            mapeamento[variavel_str] = contador_var
            contador_var += 1

    return mapeamento

def min_um(meu_mapeamento, max_passos): #pelo menos um por casa
    lista_regras = []

    for t in range(1, max_passos + 1):
        for l in range(1,4):
            for c in range(1,4):

                regras_casa = []

                for v in range(0,9):
                    variavel_str = f"{t}P{l}{c}{v}"
                    valor_encontrado = meu_mapeamento[variavel_str]
                    regras_casa.append(valor_encontrado)
                lista_regras.append(regras_casa)

    return lista_regras
            
def max_um(meu_mapeamento, max_passos):
    lista_clausulas = []

    for t in range(1, max_passos + 1):
        for l in range(1, 4):
            for c in range(1, 4):
                for v1 in range(0,9):
                    for v2 in range(0,9):
                        if v1 < v2: #ver todos os pares de peças possíveis sem redundancia
                            variavel_str = f"{t}P{l}{c}{v1}"
                            numero_v1 = meu_mapeamento[variavel_str]
                            variavel_str = f"{t}P{l}{c}{v2}"
                            numero_v2 = meu_mapeamento[variavel_str]
                            clausula_do_par = [-numero_v1, -numero_v2]
                            lista_clausulas.append(clausula_do_par)
    return lista_clausulas

def max_uma_acao(meu_mapeamento, max_passos):
    lista_acao = []

    for t in range(1, max_passos):
        for m1 in ['C', 'B', 'E', 'D']:
            for m2 in ['C', 'B', 'E', 'D']:
                if m1 < m2:
                    variavel_str = f"{t}A{m1}"
                    mov_m1 = meu_mapeamento[variavel_str]
                    variavel_str = f"{t}A{m2}"
                    mov_m2 = meu_mapeamento[variavel_str]
                    clausula_par = [-mov_m1, -mov_m2]
                    lista_acao.append(clausula_par)
    return lista_acao

def min_uma_acao(mapeamento, max_passos):
    lista_geral_clausulas = []
    for t in range(1, max_passos):
        clausula_tempo = []
        m = ['C', 'B', 'D', 'E']
        for acao in m: 
            variavel_str = f"{t}A{acao}"
            numero_correspondente = mapeamento[variavel_str]
            clausula_tempo.append(numero_correspondente)
        lista_geral_clausulas.append(clausula_tempo)

    return lista_geral_clausulas

def regra_transicao(meu_mapeamento, max_passos):
    lista_clausula_mov = []
        #consequencias de fazer uma jogada
    for t in range(1, max_passos): 
        for l in range(1,4):
            for c in range(1,4):
                if l > 1: #mover para cima
                    for v in range(1, 9):
                        variavel_str = f"{t}P{l}_{c}_0"
                        pre_cond1 = meu_mapeamento[variavel_str]    #partida
                        variavel_str = f"{t}P{l-1}{c}{v}"
                        pre_cond2 = meu_mapeamento[variavel_str]    #destino
                        variavel_str = f"{t}_A_C"                   #acao
                        acao1 = meu_mapeamento[variavel_str] 
                        variavel_str = f"{t+1}P{l-1}_{c}_0"
                        pos_cond1 = meu_mapeamento[variavel_str]    #efeito da troca
                        variavel_str = f"{t+1}P{l}{c}{v}"
                        pos_cond2 = meu_mapeamento[variavel_str]    #efeito da troca                                                                                 
                        clausula1 = [-pre_cond1, -pre_cond2, -acao1, pos_cond1]   #(pre_cond1 & pre_cond2 & acao1) -> (pos_cond1 & pos_cond2) traduzido para:    
                        clausula2 = [-pre_cond1, -pre_cond2, -acao1, pos_cond2]
                        lista_clausula_mov.append(clausula1)
                        lista_clausula_mov.append(clausula2)
                if l < 3: #mover para baixo
                    for v in range(1, 9):
                        variavel_str = f"{t}P{l}_{c}_0"
                        pre_cond1 = meu_mapeamento[variavel_str]
                        variavel_str = f"{t}P{l+1}{c}{v}"
                        pre_cond2 = meu_mapeamento[variavel_str]
                        variavel_str = f"{t}_A_B"
                        acao1 = meu_mapeamento[variavel_str]
                        variavel_str = f"{t+1}P{l+1}_{c}_0"
                        pos_cond1 = meu_mapeamento[variavel_str]
                        variavel_str = f"{t+1}P{l}{c}{v}"
                        pos_cond2 = meu_mapeamento[variavel_str]
                        clausula1 = [-pre_cond1, -pre_cond2, -acao1, pos_cond1]
                        clausula2 = [-pre_cond1, -pre_cond2, -acao1, pos_cond2]
                        lista_clausula_mov.append(clausula1)
                        lista_clausula_mov.append(clausula2)
                if c > 1: #mover para a esquerda]
                    for v in range(1, 9):
                        variavel_str = f"{t}P{l}_{c}_0"
                        pre_cond1 = meu_mapeamento[variavel_str]
                        variavel_str = f"{t}P{l}{c-1}{v}"
                        pre_cond2 = meu_mapeamento[variavel_str]
                        variavel_str = f"{t}_A_E"
                        acao1 = meu_mapeamento[variavel_str]
                        variavel_str = f"{t+1}P{l}_{c-1}_0" 
                        pos_cond1 = meu_mapeamento[variavel_str]
                        variavel_str = f"{t+1}P{l}{c}{v}"
                        pos_cond2 = meu_mapeamento[variavel_str]
                        clausula1 = [-pre_cond1, -pre_cond2, -acao1, pos_cond1]
                        clausula2 = [-pre_cond1, -pre_cond2, -acao1, pos_cond2]
                        lista_clausula_mov.append(clausula1)
                        lista_clausula_mov.append(clausula2)
                if c < 3: #mover para a direita
                    for v in range(1, 9):
                        variavel_str = f"{t}P{l}_{c}_0"
                        pre_cond1 = meu_mapeamento[variavel_str]
                        variavel_str = f"{t}P{l}{c+1}{v}"
                        pre_cond2 = meu_mapeamento[variavel_str]
                        variavel_str = f"{t}_A_D"
                        acao1 = meu_mapeamento[variavel_str]
                        variavel_str = f"{t+1}P{l}_{c+1}_0"
                        pos_cond1 = meu_mapeamento[variavel_str]
                        variavel_str = f"{t+1}P{l}{c}{v}"
                        pos_cond2 = meu_mapeamento[variavel_str]
                        clausula1 = [-pre_cond1, -pre_cond2, -acao1, pos_cond1]
                        clausula2 = [-pre_cond1, -pre_cond2, -acao1, pos_cond2]
                        lista_clausula_mov.append(clausula1)
                        lista_clausula_mov.append(clausula2)

    return lista_clausula_mov

def regras_inercia(meu_mapeamento, max_passos):
    lista_clausulas_inercia = []

    for t in range(1, max_passos):
        for l_zero in range(1, 4):
            for c_zero in range(1, 4):
                if l_zero > 1: #inercia quando move para cima
                    acao_var = meu_mapeamento[f"{t}_A_C"]
                    zero_pos_var = meu_mapeamento[f"{t}P{l_zero}_{c_zero}_0"]
                    # Células afetadas: onde o '0' está e a casa acima dele
                    celulas_afetadas = {(l_zero, c_zero), (l_zero - 1, c_zero)}

                    # Agora, para todas as outras células que NÃO são afetadas
                    for l_inercia in range(1, 4):
                        for c_inercia in range(1, 4):
                            if (l_inercia, c_inercia) not in celulas_afetadas:
                                # Para cada peça possível (v) nesta célula de inércia
                                for v in range(0, 9):
                                    peca_t = meu_mapeamento[f"{t}P{l_inercia}{c_inercia}{v}"]
                                    peca_t1 = meu_mapeamento[f"{t+1}P{l_inercia}{c_inercia}{v}"]
                                    lista_clausulas_inercia.append([-acao_var, -zero_pos_var, -peca_t, peca_t1]) #SE (acao_var E zero_pos_var E peca_t) ENTÃO (peca_t1)
                                    lista_clausulas_inercia.append([-acao_var, -zero_pos_var, peca_t, -peca_t1]) #SE (acao_var E zero_pos_var E NÃO peca_t) ENTÃO (NÃO peca_t1)

                # inercia quando  move para baixo
                if l_zero < 3:
                    acao_var = meu_mapeamento[f"{t}_A_B"]
                    zero_pos_var = meu_mapeamento[f"{t}P{l_zero}_{c_zero}_0"]
                    celulas_afetadas = {(l_zero, c_zero), (l_zero + 1, c_zero)}

                    for l_inercia in range(1, 4):
                        for c_inercia in range(1, 4):
                            if (l_inercia, c_inercia) not in celulas_afetadas:
                                for v in range(0, 9):
                                    peca_t = meu_mapeamento[f"{t}P{l_inercia}{c_inercia}{v}"]
                                    peca_t1 = meu_mapeamento[f"{t+1}P{l_inercia}{c_inercia}{v}"]
                                    lista_clausulas_inercia.append([-acao_var, -zero_pos_var, -peca_t, peca_t1])
                                    lista_clausulas_inercia.append([-acao_var, -zero_pos_var, peca_t, -peca_t1])

                # inercia quando move para esquerda
                if c_zero > 1:
                    acao_var = meu_mapeamento[f"{t}_A_E"]
                    zero_pos_var = meu_mapeamento[f"{t}P{l_zero}_{c_zero}_0"]
                    celulas_afetadas = {(l_zero, c_zero), (l_zero, c_zero - 1)}
                    
                    for l_inercia in range(1, 4):
                        for c_inercia in range(1, 4):
                            if (l_inercia, c_inercia) not in celulas_afetadas:
                                for v in range(0, 9):
                                    peca_t = meu_mapeamento[f"{t}P{l_inercia}{c_inercia}{v}"]
                                    peca_t1 = meu_mapeamento[f"{t+1}P{l_inercia}{c_inercia}{v}"]
                                    lista_clausulas_inercia.append([-acao_var, -zero_pos_var, -peca_t, peca_t1]) 
                                    lista_clausulas_inercia.append([-acao_var, -zero_pos_var, peca_t, -peca_t1])

                #inercia quando move para a direita
                if c_zero < 3:
                    acao_var = meu_mapeamento[f"{t}_A_D"]
                    zero_pos_var = meu_mapeamento[f"{t}P{l_zero}_{c_zero}_0"]
                    celulas_afetadas = {(l_zero, c_zero), (l_zero, c_zero + 1)}

                    for l_inercia in range(1, 4):
                        for c_inercia in range(1, 4):
                            if (l_inercia, c_inercia) not in celulas_afetadas:
                                for v in range(0, 9):
                                    peca_t = meu_mapeamento[f"{t}P{l_inercia}{c_inercia}{v}"]
                                    peca_t1 = meu_mapeamento[f"{t+1}P{l_inercia}{c_inercia}{v}"]
                                    lista_clausulas_inercia.append([-acao_var, -zero_pos_var, -peca_t, peca_t1])
                                    lista_clausulas_inercia.append([-acao_var, -zero_pos_var, peca_t, -peca_t1])

    return lista_clausulas_inercia

def gerar_tabuleiro_inicial():

    #definir estado inicial 
    tabuleiro = [[0,1,2], [3,4,5], [6,7,8]]
    liv = 0
    cov = 0
    for i in range(0, 100):
        mov_possiveis = []
        if liv > 0: mov_possiveis.append('C')
        if liv < 2:mov_possiveis.append('B')
        if cov > 0: mov_possiveis.append('E')
        if cov < 2: mov_possiveis.append('D')
            
        movimento_escolhido = random.choice(mov_possiveis)

        if movimento_escolhido == 'C':
            linha_vizinho = liv - 1
            coluna_vizinho = cov
        elif movimento_escolhido == 'B':
            linha_vizinho = liv + 1
            coluna_vizinho = cov
        elif movimento_escolhido == 'E':
            coluna_vizinho = cov - 1
            linha_vizinho = liv
        elif movimento_escolhido == 'D':
            coluna_vizinho = cov + 1
            linha_vizinho = liv

        tabuleiro[liv][cov], tabuleiro[linha_vizinho][coluna_vizinho] = tabuleiro[linha_vizinho][coluna_vizinho], tabuleiro[liv][cov] #realizando a troca
        liv = linha_vizinho #atualilza a linha do zero
        cov = coluna_vizinho #atualiza a coluna do zero

    return tabuleiro

def traduzir_tab_clausula(tabuleiro,mapeamento): #traduz o tabuleiro inicial para 
    clausulas_do_estado = []
    for l in range(0,3):
        for c in range(0,3):
            peca =tabuleiro[l][c]
            variavel_str = f"1_P_{l+1}{c+1}{peca}"
            numero_variavel_clausula = mapeamento[variavel_str]
            clausula = [numero_variavel_clausula]
            clausulas_do_estado.append(clausula)

    return clausulas_do_estado

def regra_precondicao(mapeamento, max_passos):
    lista_proibicoes = []
    
    for t in range(1, max_passos):
        string_acao_C = f"{t}_A_C"
        num_acao_C = mapeamento[string_acao_C]
        for c in range(1,4):
            string_pos_invalida = f"{t}P_1{c}_0"
            num_pos_invalida = mapeamento[string_pos_invalida]
            clausula = [-num_acao_C, -num_pos_invalida]
            lista_proibicoes.append(clausula)

        string_acao_B = f"{t}_A_B"
        num_acao_B = mapeamento[string_acao_B]
        for c in range(1,4):
            string_pos_invalida = f"{t}P_3{c}_0"
            num_pos_invalida = mapeamento[string_pos_invalida]
            clausula = [-num_acao_B, -num_pos_invalida]
            lista_proibicoes.append(clausula)

        string_acao_E = f"{t}_A_E"
        num_acao_E = mapeamento[string_acao_E]
        for l in range(1,4):
            string_pos_invalida = f"{t}P{l}_1_0"
            num_pos_invalida = mapeamento[string_pos_invalida]
            clausula = [-num_acao_E, -num_pos_invalida]
            lista_proibicoes.append(clausula)

        string_acao_D = f"{t}_A_D"
        num_acao_D = mapeamento[string_acao_D]
        for l in range(1,4):
            string_pos_invalida = f"{t}P{l}_3_0"
            num_pos_invalida = mapeamento[string_pos_invalida]
            clausula = [-num_acao_D, -num_pos_invalida]
            lista_proibicoes.append(clausula)

    return lista_proibicoes

        

def resolver_com_sat(tabuleiro_inicial, max_passos_limite=25):
    """
    Função principal que encapsula a lógica do solver SAT.
    Recebe um tabuleiro e tenta resolvê-lo em até max_passos_limite.
    """
    mapeamento = criar_mapeamento(max_passos_limite)
    clausulas_iniciais = traduzir_tab_clausula(tabuleiro_inicial, mapeamento)
    
    tabuleiro_final = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

    mapa_reverso = {valor: chave for chave, valor in mapeamento.items()}

    for n in range(1, max_passos_limite + 1):
        print(f"Tentando resolver com {n} passo(s)...")

        clausulas_finais = []
        for l in range(3):
            for c in range(3):
                v = tabuleiro_final[l][c]
                clausulas_finais.append([mapeamento[f"{n}P{l+1}{c+1}{v}"]])

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
                        if "A" in nome_da_variavel:
                            partes = nome_da_variavel.split('_')
                            tempo = int(partes[0])
                            acao = partes[2]
                            solucao_ordenada[tempo] = acao
                
                print(f"Solução encontrada com {n-1} movimento(s)!")
                return solucao_ordenada, n
    
    print("Nenhuma solução encontrada no limite de passos.")
    return None, None