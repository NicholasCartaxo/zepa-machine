def mapear_pc_linhas(caminho_arquivo):
    instrucoes_validas = {
        "AND", "OR", "XOR", "ADD", "SUB", "MUL", "UDIV", "SDIV", "CMP",
        "MV", "JUMP", "JMPR", "BEQ", "BLT", "BGT", "LOAD", "STORE",
        "LDD", "STRD", "LDB", "LDSB", "STRB", "MRET", "SYSCALL"
    }

    # Dois dicionários para busca bidirecional rápida O(1)
    pc_para_linha = {}
    linha_para_pc = {}
    
    linha_original = 0
    pc = 0

    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            for linha in arquivo:
                linha_original += 1
                
                linha_sem_espacos_iniciais = linha.lstrip()
                
                if not linha_sem_espacos_iniciais:
                    continue
                
                primeira_palavra = linha_sem_espacos_iniciais.split()[0]
                
                if primeira_palavra in instrucoes_validas:
                    # Registra o mapeamento nas duas direções
                    pc_para_linha[pc] = linha_original
                    linha_para_pc[linha_original] = pc
                    
                    # Avança o PC em 4 bytes (1 instrução de 32 bits, por exemplo)
                    pc += 4

    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado.")
        return None, None
    except Exception as e:
        print(f"Ocorreu um erro ao ler o arquivo: {e}")
        return None, None

    return pc_para_linha, linha_para_pc

# --- Execução do Programa ---
mapa_pc, mapa_linha = mapear_pc_linhas("kernel.asm")

if mapa_pc is not None and mapa_linha is not None:
    print("Mapeamento concluído!")
    print("-> Para buscar por PC, digite: pc <numero> (ex: pc 8)")
    print("-> Para buscar por Linha, digite: l <numero> (ex: l 15)")
    
    while True:
        entrada = input("\nBusca (pc X / l Y / q): ").strip().lower()
        
        if entrada == 'q':
            break
            
        partes = entrada.split()
        if len(partes) != 2:
            print("-> Formato inválido. Use 'pc 8' ou 'l 15'.")
            continue
            
        comando, valor_str = partes[0], partes[1]
        
        try:
            valor = int(valor_str)
        except ValueError:
            print("-> Erro: O valor deve ser um número inteiro.")
            continue
            
        if comando == 'pc':
            if valor in mapa_pc:
                print(f"-> O PC {valor} aponta para a linha {mapa_pc[valor]} no arquivo original.")
            else:
                print(f"-> Aviso: PC {valor} não encontrado. Certifique-se de usar múltiplos de 4 válidos.")
                
        elif comando == 'l':
            if valor in mapa_linha:
                print(f"-> A linha {valor} do arquivo original corresponde ao PC {mapa_linha[valor]}.")
            else:
                print(f"-> Aviso: A linha {valor} não contém uma instrução válida mapeada (pode ser vazia, label ou comentário).")
                
        else:
            print("-> Comando não reconhecido. Use o prefixo 'pc' ou 'l'.")
