#variáveis
avg_TAT = 0
avg_WT = 0
var = 0
ct = []
tat = []
wt = []

#lê arquivo como input
input = open("input.txt").readlines()
np = int(input[0])
algo = input[1]
id_list = []
AT_list = []
BT_list = []

#Algoritmos
def FCFS(array):
    print("FCFS")
    for i in range (np):
        if array[i][2] == 0:
            var = array[i][0] + array[i][1]
            ct.append(var)
        else:
            var = var + array[i][1]
            ct.append(var)

def SJF(array):
    print("SJF")

    for i in range(np - 1):
        index = i
        for j in range(i + 1, np):
            if (array[j][1] < array[index][1]):
                index = j

        array[i], array[index] = array[index], array[i]

    for i in range (np):
        if i == 0:
            ctime = (array[i][1] + array[i][0])
            ct.append(ctime)
        else:
            ctime = (ctime) + array[i][1]
            ct.append(ctime)

def RR():
    print("RR")




#Atribui Id, AT e BT a suas respectivas listas
for i in range(np):
    id = int(input[i+(2+i)+i])
    id_list.append(id)
    at = int(input[i+(3+i)+i])
    AT_list.append(at)
    bt = int(input[i+(4+i)+i])
    BT_list.append(bt)

#cria uma lista de processos
pArray = [None] * np
for i in range(np):
    pArray[i] = [AT_list[i], BT_list[i], id_list[i]]



# Calcula o CT
if algo.strip() == "FCFS":
    FCFS(pArray)
if algo.strip() == "SJF":
    SJF(pArray)
# else:
#     RR()



# Calcula o TAT e o WT
for i in range(np):
    tat.append(ct[i] - pArray[i][0])
    wt.append(tat[i] - pArray[i][1])

#Faz output do resultado do algoritmo
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
output.write("GRÁFICO DE GANT:")
space = f"\n"
output.write(space)
output.write(space)
for i in range(np):

    if i == 0:
        gantOn = f"#" * pArray[i][1]
        gantVoid = f"." * pArray[i][0]
        output.write(f"P{pArray[i][2]}: ")
        output.write(gantVoid)
        output.write(gantOn)
        output.write(space)
    else:
        gantOn = f"#" * pArray[i][1]
        gantVoid = f"." * pArray[i][0]
        gantOff = f"-" * (ct[i-1] - pArray[i][0])
        output.write(f"P{pArray[i][2]}: ")
        output.write(gantVoid)
        output.write(gantOff)
        output.write(gantOn)
        output.write(space)
