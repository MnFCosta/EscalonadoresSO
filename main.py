#variáveis e listas
avg_TAT = 0
avg_WT = 0
var = 0
ct = []
tat = []
wt = []
gant = []
id_list = []
AT_list = []
BT_list = []

#lê arquivo como input
input = open("input.txt").readlines()
np = int(input[0])
algo = input[1]
output = open("output.txt", 'w')

#Algoritmos
def FCFS(array):
    print("FCFS")
    time = 0
    ap = 0
    fila = []
    pronto = 0
    while (pronto < np):
        #coloca todos os processos em uma fila de espera
        for i in range(np):
            if time == array[i][0]:
                fila.append(array[i])
                ap += 1
        time += 1

        if time == np+1:
            #executa o primeiro processo
            for i in range(np):
                if i == 0:
                    #calcula o CT do processo
                    var = fila[i][1] + fila[i][0]
                    #adiciona o CT a lista de CTs
                    ct.append(var)
                    #Adiciona o processo ao gráfico de gant
                    for j in range(fila[i][1]):
                        gant.append(fila[i][2])
                    #Incrementa a variável pronto
                    pronto += 1
            #executa os próximos processos e faz os mesmos passos
                else:
                    var = var + fila[i][1]
                    ct.append(var)
                    pronto += 1
                    for j in range(fila[i][1]):
                        gant.append(fila[i][2])
    return fila

def remover_prontos(a, b):
    for i in a[:]:
        if i in b:
            a.remove(i)
def SJF(array):
    print("SJF")
    time = 0
    ap = 0
    fila = []
    pronto = 0
    filaP = []
    while(pronto<np):
        #percorra os elementos de array e cheque se o AT de algum deles é igual ou menor que tempo
        #caso sejam adicione o elemento a fila de processos que já chegaram
        for i in array:
            if time >= i[0]:
                fila.append(i)
                ap+=1
        print(f"Fila após sair do loop: {fila} tempo {time}")
        #CASO UM PROCESSO JÁ EXECUTADO TENHA SIDO ADICIONADO A FILA, RETIRE-O
        remover_prontos(fila,filaP)
        print(f"Fila após prontos terem sido retirados: {fila} tempo {time}")
        if len(fila) > 0:
            fila.sort(key=lambda  x : (x[1]))
            print(f"Fila após terem sido organizados: {fila} tempo {time}")
            for index, item in enumerate(fila):
                if not index:
                    for _ in range (item[1]):
                        gant.append(item[2])
                    time+=item[1]
                    ct.append(time)
                    pronto+=1
                    #ADICIONAR ESTADO PRONTO AO PROCESSO
                    filaP.append(item)
                    fila.pop(fila.index(item))
                    #RETIRA O PROCESSO DA FILA DE EXECUÇÃO
            fila = []
        print(gant)
    print(filaP)
    return filaP

#Função que muda posições dos elementos da lista baseado em quanto tempo estão esperando
#Organiza a fila de modo que o processo que está esperando a mais tempo tenha prioridade
def shiftFila(alist):
    temp = alist[0]
    for i in range(len(alist)-1):
        alist[i]=alist[i+1]
    alist[len(alist)-1]=temp
    return alist
def RR(array):
    print("RR")
    quantum = int(algo.split()[1])
    fila = []
    time = 0
    ap = 0  # processos que chegaram
    rp = 0  # processos prontos para executar
    pronto = 0  # processo finalizados
    trocafila = 0

    while (pronto < np):
        # adiciona processos a fila caso o atual tempo seja maior ou igual ao AT do processo
        for i in range(ap, np):
            if time >= array[i][0]:
                fila.append(array[i])
                print(f"TEMPO {time} FILA {fila}")
                ap += 1
                rp += 1

        # caso o numero de processos prontos para executar seja menor do que 1 incremente o tempo e continue
        if rp < 1:
            time += 1
            continue

        #caso a primeira execução tenha sido feita, comece a ordenar processos por quanto os mesmos estão esperando
        if trocafila:
            fila = shiftFila(fila)

        #se o BT do primeiro elemento da fila for maior que 0 (não terminou ainda de ser executado)
        if fila[0][1] > 0:
            #E for maior do que o quantum (pode ainda ser executado por quantum)
            if fila[0][1] > quantum:
                #execute-o por quantum e subtraia seu BT e incremente tempo por quantum
                for g in range(time, time + quantum):
                    gant.append(fila[0][2])
                time += quantum
                fila[0][1] -= quantum
            #caso for maior do que 0 porém menor do que quantum
            else:
                #execute o pelo resto de tempo que falta (atual valor de BT), incremente o tempo pelo BT restante
                #seu BT agora é igual a 0 (não precisa mais ser executado), o processo está pronto
                for g in range(time, time + fila[0][1]):
                    gant.append(fila[0][2])
                time += fila[0][1]
                fila[0][1] = 0
                pronto += 1
                rp -= 1
            trocafila = 1

#Atribui Id, AT e BT a suas respectivas listas
for i in range(np):
    id = (input[i+2].strip()).split()
    id_list.append(int(id[0]))
    at = (input[i+2].strip()).split()
    AT_list.append(int(at[1]))
    bt = (input[i+2].strip()).split()
    BT_list.append(int(bt[2]))

# cria uma lista de processos
pArray = [None] * np
for i in range(np):
    pArray[i] = [AT_list[i], BT_list[i], id_list[i]]

# Identifica qual algoritmo deve ser usado
if algo.strip() == "FCFS":
    pArray = FCFS(pArray)
elif algo.strip() == "SJF":
    pArray = SJF(pArray)
else:
    RR(pArray)

#Reatribui valores originais a suas listas (RR altera o valor de BT)
if algo.split()[0] == "RR":
    for i in range(np):
        bt = (input[i+2].strip()).split()
        BT_list.append(int(bt[2]))

    for i in range(np):
        pArray[i] = [AT_list[i], BT_list[i], id_list[i]]

    # Adiciona os completion times a lista ct
    for i in range(np):
        ct.append(len(gant) - gant[::-1].index(i))

# Calcula o TAT e o WT

for i in range(np):
    tat.append(ct[i] - pArray[i][0])
    wt.append(tat[i] - pArray[i][1])

#Output do resultado do algoritmo
output = open("output.txt", 'w')

#TABELA DE PROCESSOS
for i in range(np):
    text = f"Processo {pArray[i][2]}: AT = {pArray[i][0]} BT = {pArray[i][1]} CT = {ct[i]} TAT = {tat[i]} WT = {wt[i]}\n"
    avg_TAT = avg_TAT + tat[i]
    avg_WT = avg_WT + wt[i]
    output.write(text)

#TAT E WT MÉDIO
avg_TAT = avg_TAT/np
avg_WT = avg_WT/np
tat = f"\nTempo médio no sistema: {avg_TAT}\n"
wt = f"Tempo médio de espera: {avg_WT}\n\n"
output.write(tat)
output.write(wt)


#GRÁFICO DE GANT

output.write(str(gant))
