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
                    variavel_str = f"{t}_P_{l}_{c}_{v}"
                    mapeamento[variavel_str] = contador_var
                    contador_var += 1

    #t_A_M
    for t in range(1, max_passos): #até o estado 9, pois do estado 10 simboliza que passou para o estado 11
        for m in ['C', 'B', 'E', 'D']:
            variavel_str = f"{t}_A_{m}"
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
                    variavel_str = f"{t}_P_{l}_{c}_{v}"
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
                            variavel_str = f"{t}_P_{l}_{c}_{v1}"
                            numero_v1 = meu_mapeamento[variavel_str]
                            variavel_str = f"{t}_P_{l}_{c}_{v2}"
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
                    variavel_str = f"{t}_A_{m1}"
                    mov_m1 = meu_mapeamento[variavel_str]
                    variavel_str = f"{t}_A_{m2}"
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
            variavel_str = f"{t}_A_{acao}"
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
                        variavel_str = f"{t}_P_{l}_{c}_0"
                        pre_cond1 = meu_mapeamento[variavel_str]    #partida
                        variavel_str = f"{t}_P_{l-1}_{c}_{v}"
                        pre_cond2 = meu_mapeamento[variavel_str]    #destino
                        variavel_str = f"{t}_A_C"                   #acao
                        acao1 = meu_mapeamento[variavel_str] 
                        variavel_str = f"{t+1}_P_{l-1}_{c}_0"
                        pos_cond1 = meu_mapeamento[variavel_str]    #efeito da troca
                        variavel_str = f"{t+1}_P_{l}_{c}_{v}"
                        pos_cond2 = meu_mapeamento[variavel_str]    #efeito da troca                                                                                 
                        clausula1 = [-pre_cond1, -pre_cond2, -acao1, pos_cond1]   #(pre_cond1 & pre_cond2 & acao1) -> (pos_cond1 & pos_cond2) traduzido para:    
                        clausula2 = [-pre_cond1, -pre_cond2, -acao1, pos_cond2]
                        lista_clausula_mov.append(clausula1)
                        lista_clausula_mov.append(clausula2)
                if l < 3: #mover para baixo
                    for v in range(1, 9):
                        variavel_str = f"{t}_P_{l}_{c}_0"
                        pre_cond1 = meu_mapeamento[variavel_str]
                        variavel_str = f"{t}_P_{l+1}_{c}_{v}"
                        pre_cond2 = meu_mapeamento[variavel_str]
                        variavel_str = f"{t}_A_B"
                        acao1 = meu_mapeamento[variavel_str]
                        variavel_str = f"{t+1}_P_{l+1}_{c}_0"
                        pos_cond1 = meu_mapeamento[variavel_str]
                        variavel_str = f"{t+1}_P_{l}_{c}_{v}"
                        pos_cond2 = meu_mapeamento[variavel_str]
                        clausula1 = [-pre_cond1, -pre_cond2, -acao1, pos_cond1]
                        clausula2 = [-pre_cond1, -pre_cond2, -acao1, pos_cond2]
                        lista_clausula_mov.append(clausula1)
                        lista_clausula_mov.append(clausula2)
                if c > 1: #mover para a esquerda]
                    for v in range(1, 9):
                        variavel_str = f"{t}_P_{l}_{c}_0"
                        pre_cond1 = meu_mapeamento[variavel_str]
                        variavel_str = f"{t}_P_{l}_{c-1}_{v}"
                        pre_cond2 = meu_mapeamento[variavel_str]
                        variavel_str = f"{t}_A_E"
                        acao1 = meu_mapeamento[variavel_str]
                        variavel_str = f"{t+1}_P_{l}_{c-1}_0" 
                        pos_cond1 = meu_mapeamento[variavel_str]
                        variavel_str = f"{t+1}_P_{l}_{c}_{v}"
                        pos_cond2 = meu_mapeamento[variavel_str]
                        clausula1 = [-pre_cond1, -pre_cond2, -acao1, pos_cond1]
                        clausula2 = [-pre_cond1, -pre_cond2, -acao1, pos_cond2]
                        lista_clausula_mov.append(clausula1)
                        lista_clausula_mov.append(clausula2)
                if c < 3: #mover para a direita
                    for v in range(1, 9):
                        variavel_str = f"{t}_P_{l}_{c}_0"
                        pre_cond1 = meu_mapeamento[variavel_str]
                        variavel_str = f"{t}_P_{l}_{c+1}_{v}"
                        pre_cond2 = meu_mapeamento[variavel_str]
                        variavel_str = f"{t}_A_D"
                        acao1 = meu_mapeamento[variavel_str]
                        variavel_str = f"{t+1}_P_{l}_{c+1}_0"
                        pos_cond1 = meu_mapeamento[variavel_str]
                        variavel_str = f"{t+1}_P_{l}_{c}_{v}"
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
                    zero_pos_var = meu_mapeamento[f"{t}_P_{l_zero}_{c_zero}_0"]
                    # Células afetadas: onde o '0' está e a casa acima dele
                    celulas_afetadas = {(l_zero, c_zero), (l_zero - 1, c_zero)}

                    # Agora, para todas as outras células que NÃO são afetadas
                    for l_inercia in range(1, 4):
                        for c_inercia in range(1, 4):
                            if (l_inercia, c_inercia) not in celulas_afetadas:
                                # Para cada peça possível (v) nesta célula de inércia
                                for v in range(0, 9):
                                    peca_t = meu_mapeamento[f"{t}_P_{l_inercia}_{c_inercia}_{v}"]
                                    peca_t1 = meu_mapeamento[f"{t+1}_P_{l_inercia}_{c_inercia}_{v}"]
                                    lista_clausulas_inercia.append([-acao_var, -zero_pos_var, -peca_t, peca_t1]) #SE (acao_var E zero_pos_var E peca_t) ENTÃO (peca_t1)
                                    lista_clausulas_inercia.append([-acao_var, -zero_pos_var, peca_t, -peca_t1]) #SE (acao_var E zero_pos_var E NÃO peca_t) ENTÃO (NÃO peca_t1)

                # inercia quando  move para baixo
                if l_zero < 3:
                    acao_var = meu_mapeamento[f"{t}_A_B"]
                    zero_pos_var = meu_mapeamento[f"{t}_P_{l_zero}_{c_zero}_0"]
                    celulas_afetadas = {(l_zero, c_zero), (l_zero + 1, c_zero)}

                    for l_inercia in range(1, 4):
                        for c_inercia in range(1, 4):
                            if (l_inercia, c_inercia) not in celulas_afetadas:
                                for v in range(0, 9):
                                    peca_t = meu_mapeamento[f"{t}_P_{l_inercia}_{c_inercia}_{v}"]
                                    peca_t1 = meu_mapeamento[f"{t+1}_P_{l_inercia}_{c_inercia}_{v}"]
                                    lista_clausulas_inercia.append([-acao_var, -zero_pos_var, -peca_t, peca_t1])
                                    lista_clausulas_inercia.append([-acao_var, -zero_pos_var, peca_t, -peca_t1])

                # inercia quando move para esquerda
                if c_zero > 1:
                    acao_var = meu_mapeamento[f"{t}_A_E"]
                    zero_pos_var = meu_mapeamento[f"{t}_P_{l_zero}_{c_zero}_0"]
                    celulas_afetadas = {(l_zero, c_zero), (l_zero, c_zero - 1)}
                    
                    for l_inercia in range(1, 4):
                        for c_inercia in range(1, 4):
                            if (l_inercia, c_inercia) not in celulas_afetadas:
                                for v in range(0, 9):
                                    peca_t = meu_mapeamento[f"{t}_P_{l_inercia}_{c_inercia}_{v}"]
                                    peca_t1 = meu_mapeamento[f"{t+1}_P_{l_inercia}_{c_inercia}_{v}"]
                                    lista_clausulas_inercia.append([-acao_var, -zero_pos_var, -peca_t, peca_t1]) 
                                    lista_clausulas_inercia.append([-acao_var, -zero_pos_var, peca_t, -peca_t1])

                #inercia quando move para a direita
                if c_zero < 3:
                    acao_var = meu_mapeamento[f"{t}_A_D"]
                    zero_pos_var = meu_mapeamento[f"{t}_P_{l_zero}_{c_zero}_0"]
                    celulas_afetadas = {(l_zero, c_zero), (l_zero, c_zero + 1)}

                    for l_inercia in range(1, 4):
                        for c_inercia in range(1, 4):
                            if (l_inercia, c_inercia) not in celulas_afetadas:
                                for v in range(0, 9):
                                    peca_t = meu_mapeamento[f"{t}_P_{l_inercia}_{c_inercia}_{v}"]
                                    peca_t1 = meu_mapeamento[f"{t+1}_P_{l_inercia}_{c_inercia}_{v}"]
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
            variavel_str = f"1_P_{l+1}_{c+1}_{peca}"
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
            string_pos_invalida = f"{t}_P_1_{c}_0"
            num_pos_invalida = mapeamento[string_pos_invalida]
            clausula = [-num_acao_C, -num_pos_invalida]
            lista_proibicoes.append(clausula)

        string_acao_B = f"{t}_A_B"
        num_acao_B = mapeamento[string_acao_B]
        for c in range(1,4):
            string_pos_invalida = f"{t}_P_3_{c}_0"
            num_pos_invalida = mapeamento[string_pos_invalida]
            clausula = [-num_acao_B, -num_pos_invalida]
            lista_proibicoes.append(clausula)

        string_acao_E = f"{t}_A_E"
        num_acao_E = mapeamento[string_acao_E]
        for l in range(1,4):
            string_pos_invalida = f"{t}_P_{l}_1_0"
            num_pos_invalida = mapeamento[string_pos_invalida]
            clausula = [-num_acao_E, -num_pos_invalida]
            lista_proibicoes.append(clausula)

        string_acao_D = f"{t}_A_D"
        num_acao_D = mapeamento[string_acao_D]
        for l in range(1,4):
            string_pos_invalida = f"{t}_P_{l}_3_0"
            num_pos_invalida = mapeamento[string_pos_invalida]
            clausula = [-num_acao_D, -num_pos_invalida]
            lista_proibicoes.append(clausula)

    return lista_proibicoes


def mostrar_tabuleiro(tabuleiro, solucao_ordenada):

    tabuleiro_atual = [linha[:] for linha in tabuleiro] #copia do tabuleiro original

    print("\n--- Tabuleiro Inicial ---")
    for linha in tabuleiro_atual:
        print(linha)

    lin_vazio = 0
    col_vazio = 0
    for l in range(0,3):
        for c in range(0,3):
            if tabuleiro_atual[l][c] == 0:
                lin_vazio = l
                col_vazio = c

    for passo in sorted(solucao_ordenada.keys()):
        movimento = solucao_ordenada[passo]
        print(f"\n--- Passo {passo}: Mover para {movimento} ---")
        if  movimento == 'C':
            linha_vizinho = lin_vazio - 1
            coluna_vizinho = col_vazio
        elif movimento == 'B':
            linha_vizinho = lin_vazio + 1
            coluna_vizinho = col_vazio
        elif movimento == 'E':
            coluna_vizinho = col_vazio - 1
            linha_vizinho = lin_vazio
        elif movimento == 'D':
            coluna_vizinho = col_vazio + 1
            linha_vizinho = lin_vazio

        #realiza a troca
        tabuleiro_atual[lin_vazio][col_vazio], tabuleiro_atual[linha_vizinho][coluna_vizinho] = tabuleiro_atual[linha_vizinho][coluna_vizinho], tabuleiro_atual[lin_vazio][col_vazio]
        lin_vazio = linha_vizinho #atualiza a posicao do vazio na linha
        col_vazio = coluna_vizinho#atualiza a posicao do vazio na coluna
        for linha in tabuleiro_atual: 
            print(linha)
        

def main(): #chama o maestro rsrs
    max__passos_teste = 25
    mapeamento = criar_mapeamento(max__passos_teste)
    tabuleiro_inicial = gerar_tabuleiro_inicial()

    print("\n--- Tabuleiro Inicial a Ser Resolvido ---")
    for linha in tabuleiro_inicial:
        print(linha)
    print("----------------------------------------\n")

    clausulas_iniciais = traduzir_tab_clausula(tabuleiro_inicial, mapeamento)
    tabuleiro_final = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]   
    mapa_reverso = {valor: chave for chave, valor in mapeamento.items()} #traduz o numero da solucao para sua frase

    for n in range(1, max__passos_teste + 1):
        print(f"\n=======Quantidade de passos: {n} =======")
        clausulas_finais = []

        for l in range(0, 3):
            for c in range(0, 3):   
                v = tabuleiro_final[l][c]
                variavel_str = f"{n}_P_{l+1}_{c+1}_{v}"
                numero_relacionado = mapeamento[variavel_str]
                clausulas_finais.append([numero_relacionado]) 

        regra_posicao = min_um(mapeamento, n)
        regra_exclusao = max_um(mapeamento, n)
        regra_acao = max_uma_acao(mapeamento, n)
        regra_transi = regra_transicao(mapeamento, n)
        regra_solver = min_uma_acao(mapeamento, n)
        regra_proibicao = regra_precondicao(mapeamento, n)
        regra_inercia = regras_inercia(mapeamento, n)

        formula_completa = clausulas_iniciais + clausulas_finais + regra_posicao + regra_exclusao + regra_acao + regra_transi + regra_solver + regra_proibicao + regra_inercia

        with Glucose4(bootstrap_with=formula_completa) as solver:
            if solver.solve() == True:
                # É importante pegar o modelo aqui, antes de usá-lo
                modelo = solver.get_model()
                
                tabuleiro_final_do_solver = [[-1,-1,-1], [-1,-1,-1], [-1,-1,-1]] #tabuleiro vazio
                for num in modelo:
                    if num > 0:
                        nome_variavel = mapa_reverso[num]
                        # Filtramos apenas as variáveis de Posição (_P_) para o estado final (tempo n)
                        if f"{n}_P_" in nome_variavel:
                            
                            partes = nome_variavel.split('_')
                            l = int(partes[2]) - 1 # Converte para índice 0
                            c = int(partes[3]) - 1 # Converte para índice 0
                            v = int(partes[4])
                            tabuleiro_final_do_solver[l][c] = v    

                print("\nTabuleiro final para resolver:")
                for linha in tabuleiro_final_do_solver:
                    print(linha)
                print("---------------------------------------------------------")
                solucao_ordenada = {}
                for num in modelo:
                    if num > 0:
                        nome_da_variavel = mapa_reverso[num] 
                        if "_A_" in nome_da_variavel: 
                            partes = nome_da_variavel.split('_')  #1_A_C -> exemplo
                            string_t = partes[0]
                            tempo = int(string_t)
                            acao = partes[2]
                            solucao_ordenada[tempo] = acao
                print("\nSOLUÇÃO ENCONTRADA!\n")
                print(f"Solução encontrada no estado {n}, com {n-1} passo(s).")
                mostrar_tabuleiro(tabuleiro_inicial, solucao_ordenada)
                break
            else:
                print("\nBusca continua...")  
    print("\n")


if __name__ == "__main__":
    main()