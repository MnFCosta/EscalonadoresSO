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
    rp = 0
    fila = []
    pronto = 0
    while(pronto<np):
        for i in range (np):
            if time==array[i][0]:
                fila.append(array[i])
                ap+=1
                rp+=1
        time+=1
        if time == np+1:
            for i in range (np):
                if i == 0:
                    var = fila[i][1] + fila[i][0]
                    print(f"PROCESS0 {i} CT = {var}")
                    pronto+=1
                    ct.append(var)
                    for j in range (fila[i][1]):
                        gant.append(fila[i][2])
                else:
                    var = var + fila[i][1]
                    print(f"PROCESS0 {i} CT = {var}")
                    ct.append(var)
                    pronto += 1
                    for j in range (fila[i][1]):
                        gant.append(fila[i][2])
    return fila
def SJF(array):
    print("SJF")
    time = 0
    ap = 0
    rp = 0
    fila = []
    pronto = 0
    var = 0

    while(pronto<np):
        for i in range (np):
            if time==array[i][0]:
                fila.append(array[i])
                ap+=1
                rp+=1
        time+=1
        if ap == np:
            print(fila)
            fila.sort(key=lambda x: (x[1], x[0]))
            print(fila)
            pronto = np
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
    time= 0
    ap = 0 #processos que chegaram
    rp = 0 #processos prontos para executar
    pronto = 0#processo finalizados
    trocafila= 0
    global gant

    while(pronto<np):

        #adiciona processos a fila caso o atual tempo seja maior ou igual ao AT do processo
        for i in range(ap,np):
            if time>=array[i][0]:
                fila.append(array[i])
                print(f"TEMPO {time} FILA {fila}")
                ap+=1
                rp+=1

        #caso o numero de processos seja menor do que 1
        if rp<1:
            gant.append("sus")
            time+=1
            continue

        if trocafila:
            fila = shiftFila(fila)


        if fila[0][1]>0:
            if fila[0][1] > quantum:
                for g in range(time, time + quantum):
                    gant.append(fila[0][2])
                time+=quantum
                fila[0][1]-=quantum
            else:
                for g in range(time, time + fila[0][1]):
                    gant.append(fila[0][2])
                time+=fila[0][1]
                fila[0][1]=0
                pronto+=1
                rp-=1
            trocafila=1

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
    SJF(pArray)
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
print(pArray)
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
# output.write("GRÁFICO DE GANT:")
# space = f"\n"
# output.write(space)
# output.write(space)
# for i in range(np):
#     if i == 0:
#         gantOn = f"#" * 2
#         gantVoid = f"." * pArray[i][0]
#         output.write(f"P{pArray[i][2]}: ")
#         output.write(gantVoid)
#         output.write(gantOn)
#         output.write(space)
#     else:
#         gantOn = f"#" * 2
#         gantVoid = f"." * pArray[i][0]
#         gantOff = f"-" * (ct[i-1] - pArray[i][0])
#         output.write(f"P{pArray[i][2]}: ")
#         output.write(gantVoid)
#         output.write(gantOff)
#         output.write(gantOn)
#         output.write(space)
