; --------------------------------------------------------------------------
; W8 = Syscall ID | W9 = Retorno do Syscall
; W0 = Acumulador do filho | W1 = Incremento / Reg auxiliar / Exit status
; W2 = Limite (10000)      | W3 = Zero (usado para comparações e cópias)
; --------------------------------------------------------------------------

_start:
    ; Configura um registrador com o valor 0 para uso geral
    MV W3 #-2
    MV W8 #0x40        

    ; 1. Chamada de FORK
    SYSCALL #0         ; Dispara a interrupção de sistema. Retorno vem no W9

    ; 2. Verifica se é Pai ou Filho
    CMP W9, W3         ; Compara o retorno do fork (W9) com 0 (W3)
    BEQ child_start   ; Se for igual a 0 (Z flag = 1), desvia para o fluxo do filho

parent_start:
    ; 3. Fluxo do PAI: Executa o WAIT
    SYSCALL #1         ; Pai entra em espera. O OS retomará aqui quando o filho der exit.
    LOAD W7 W8                   ; O resultado final do filho (10000) estará disponível em W9.

parent_end:
    JUMP parent_end    ; Loop infinito de segurança para finalizar a execução do pai


child_start:
    ; 4. Fluxo do FILHO: Inicialização das variáveis do loop
    MV W0 #0           ; W0 é o acumulador, inicia em 0
    MV W1 #1           ; W1 é o valor de incremento (1)
    MV W2 #67      ; W2 é o limite do loop (10000 cabe nos 16-bits da inst. MV)

child_loop:
    ; 5. Loop de soma
    ADD W0, W0, W1     ; Acumula: W0 = W0 + W1 (W0++)
    CMP W0, W2         ; Compara o acumulador (W0) com 10000 (W2)
    BLT child_loop     ; Se W0 for menor que 10000 (L flag = 1), repete o loop

child_exit:
    ; 6. Filho terminou o loop e retorna o valor (10000)
    
    MV W7 #0
    ADD W8 W0 W7
    
    SYSCALL #2         ; Dispara o exit. O OS passará o valor de W1 para o pai.