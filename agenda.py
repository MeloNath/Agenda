import sys
import string
import matplotlib.pyplot as plt
import datetime

TODO_FILE = 'todo.txt'
ARCHIVE_FILE = 'done.txt'

RED = "\033[1;31m"
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
GREEN = "\033[0;32m"
WRITE = "\033[37m"
RESET = "\033[0;0m"
BOLD = "\033[1m"
REVERSE = "\033[;7m"
YELLOW = "\033[0;33m"

ADICIONAR = 'a'
REMOVER = 'r'
FAZER = 'f'
PRIORIZAR = 'p'
LISTAR = 'l'
DESENHAR = 'g'

def soDigitos(numero):                                # Valida que a data ou a hora contém apenas dígitos, desprezando espaços extras no início e no fim.
    if type(numero) != str:
        return False
    for x in numero :
        if x < '0' or x > '9':
            return False
        return True

def horaValida(hora):
    horaValida = hora
    if len(hora) != 4 or not soDigitos(hora):
        print("\n")
        printCores("", "Hora Inválida!", REVERSE)
        return False
    else:
        horaMin = int(hora)
        horas = horaMin // 100
        minutos = horaMin % 100
        if horas > 23 or minutos > 59:
            print("\n")
            printCores("", "Hora Inválida!", REVERSE)
            return False
        else:
            return horaValida

def dataValida(data):
    dataValida = data
    if len(data) != 8 or not soDigitos(data) or data[2] == "/":
        printCores("", "Data Inválida!", REVERSE)
        return False
    else:
        data = int(data)
        dia = data // 10**6
        mes = (data // 10**4) - (dia*10**2)
        if dia < 1 or dia > 31 or mes < 1 or mes > 12:
            print("\n")
            printCores("", "Data Inválida!", REVERSE)
            return False
        else:
            if (mes == 2 and dia > 29) or (mes == 4 and dia > 30) or (mes == 6 and dia > 30) or (mes == 9 and dia > 30) or (mes == 11 and dia > 30):
                print("\n")
                printCores("", "Data Inválida!", REVERSE)
                return False
            else:
                return dataValida

def projetoValido(proj):
    if len(proj) < 2:
        print("\n")
        printCores("", "Projeto Inválido!", REVERSE)
        return False
    else:
        if proj[0] == "+":
            return proj
        else:
            print("\n")
            printCores("", "Projeto Inválido!", REVERSE)
            return False

def contextoValido(contexto):
    if len(contexto) < 2:
        print("\n")
        printCores("", "Contexto Inválido!", REVERSE)
        return False
    else:
        if contexto[0] == "@":
            return contexto
        else:
            print("\n")
            printCores("", "Contexto Inválido!", REVERSE)
            return False

def prioridadeValida(pri):
    if len(pri) != 3:
        printCores("", "Prioridade Inválida!", REVERSE)
        return False
    else:
        prioridade = pri.upper()
        if prioridade[0] == "(" and prioridade[1] >= "A" and prioridade[1] <= "Z" and prioridade[2] == ")":
            return prioridade
        else:
            printCores("", "Prioridade Inválida!", REVERSE)
            return False

class Compromisso:
    def __init__(self, data, hora, pri, descricao, contexto, proj):
        self.data = data
        self.hora = hora
        self.pri = pri
        self.descricao = descricao
        self.contexto = contexto
        self.proj = proj

    def imprimir(self):
        return self.data, self.hora, self.pri, self.descricao, self.contexto, self.proj

    def __str__(self):
        return str(self.imprimir())

def organizar(linhas):
    linhas = linhas.strip()                             # Remove espaços em branco e quebras de linha do começo e do fim
    itens = ""
    data = ""
    hora = ""
    pri = ""
    contexto = ""
    projeto = ""
    desc = ""

    for l in linhas:
        if l != " ":
            itens = itens + l
        else:
            if itens == "":
                itens = ""
            elif (itens.isnumeric() == True and len(itens) > 4) or (len(itens) >= 8 and (((itens[0]+itens[1]).isnumeric() and (itens[3]+itens[4]).isnumeric() and (itens[6]+itens[7]).isnumeric()) == True)):
                data = itens
                itens = ""
            elif (itens.isnumeric() == True and len(itens) <= 4) or (len(itens) >= 5 and (itens[0]+itens[1]).isnumeric() and (itens[3]+itens[4]).isnumeric()) == True:
                hora = itens
                itens = ""
            elif itens[0] == "(":
                pri = itens
                itens = ""
            elif itens[0] == "@":
                contexto = itens
                itens = ""
            elif itens[0] == "+":
                projeto = itens
                itens = ""
            else:
                desc = desc + itens + " "
                itens = ""
    if itens.isnumeric() == True and len(itens) > 4:
        data = itens
    elif itens.isnumeric() == True and len(itens) <= 4:
        hora = itens
    elif itens[0] == "(":
        pri = itens
    elif itens[0] == "@":
        contexto = itens
    elif itens[0] == "+":
        projeto = itens
    else:
        desc = desc + itens + " "

    #VALIDAÇÃO
    if data != "":
        data = dataValida(data)
        if data != False:
            data = str(data)
    if hora != "":
        hora = horaValida(hora)
        if hora != False:
            hora = str(hora)
    if pri != "":
        pri = prioridadeValida(pri)
    if contexto != "":
        contexto = contextoValido(contexto)
    if projeto != "":
        projeto = projetoValido(projeto)
    if desc == "":
        printCores("", "Digite uma descrição!", REVERSE)
        return False

    #COMPROMISSO
    organizada = Compromisso(data, hora, pri, desc, contexto, projeto)
    return [organizada.data, organizada.hora, organizada.pri, organizada.descricao, organizada.contexto, organizada.proj]

def adicionar(descricao, novaAtividade):
    atividade = ""
    for i in range(0, len(novaAtividade)):
        if novaAtividade[i] != "":
            atividade = atividade.strip() + " " + novaAtividade[i].strip()
    atividade = atividade.strip()
    arq = open('todo.txt', 'a')
    arq.write("\n")
    arq.write(atividade)
    arq.close()
    print("Compromisso adicionado com sucesso!")

def ordenarPorDataHora(itens):     # Recebe lista de listas
    listaOrganizadaPri = itens
    listaParaOrganizarData = []
    listaOrganizadaMes = []
    listaOrganizadaDia = []
    listaOrganizada = []
    semData = []

    for k in range(0, len(listaOrganizadaPri)):
        if listaOrganizadaPri[k][0] != "":
            listaParaOrganizarData.append(listaOrganizadaPri[k])
        else:
            semData.append(listaOrganizadaPri[k])

    anos = [x for x in range(1, 9999 + 1)]
    meses = [y for y in range(1, 12 + 1)]
    dias = [z for z in range(1, 31 + 1)]
    for l in dias:
        for m in range(0, len(listaParaOrganizarData)):
            dia = int(listaParaOrganizarData[m][0][0] + listaParaOrganizarData[m][0][1])
            if l == dia:
                listaOrganizadaDia.append(listaParaOrganizarData[m])
    for n in meses:
        for o in range(0, len(listaOrganizadaDia)):
            mes = int(listaOrganizadaDia[o][0][2] + listaOrganizadaDia[o][0][3])
            if n == mes:
                listaOrganizadaMes.append(listaOrganizadaDia[o])
    for p in anos:
        for q in range(0, len(listaOrganizadaMes)):
            ano = int(listaOrganizadaMes[q][0][4] + listaOrganizadaMes[q][0][5] + listaOrganizadaMes[q][0][6] + listaOrganizadaMes[q][0][7])
            if p == ano:
                listaOrganizada.append(listaOrganizadaMes[q])
    for r in range(0, len(listaOrganizada)-1):
        if listaOrganizada[r][0] == listaOrganizada[r+1][0]:
            guarda = listaOrganizada[r]
            if listaOrganizada[r+1][1] < listaOrganizada[r][1]:
                listaOrganizada[r] = listaOrganizada[r+1]
                listaOrganizada[r + 1] = guarda
    for a in semData:
        listaOrganizada.append(a)

    return listaOrganizada

def ordenarPorPrioridade(itens):
    listaParaOrganizar = itens
    listaParaOrganizarPri = []
    listaOrganizadaPri = []
    listaOrganizadaFinal = []
    semPrioridade = []

    for i in range(0, len(listaParaOrganizar)):
        if listaParaOrganizar[i][2] != "":
            listaParaOrganizarPri.append(listaParaOrganizar[i])
        else:
            semPrioridade.append(listaParaOrganizar[i])

    prioridades = list(string.ascii_uppercase)
    for i in prioridades:
        for j in range(0, len(listaParaOrganizarPri)):
            if i == listaParaOrganizarPri[j][2][1]:
                listaOrganizadaPri.append(listaParaOrganizarPri[j])
        if listaOrganizadaPri != []:
            listaOrdenadaDataHora = ordenarPorDataHora(listaOrganizadaPri)
            for b in listaOrdenadaDataHora:
                listaOrganizadaFinal.append(b)
        listaOrganizadaPri = []
    semPrioridade = ordenarPorDataHora(semPrioridade)
    for c in semPrioridade:
        listaOrganizadaFinal.append(c)

    return listaOrganizadaFinal

def printCores(posicao, texto, cor):
    print(posicao, cor + texto + RESET)

def listar():
    arq = open('todo.txt', 'r')
    ler = arq.readlines()
    arq.close()

    listaParaOrganizar = []
    for i in range(0, len(ler)):
        listaParaOrganizar.append(organizar(ler[i]))
    listaOrganizadaFinal = ordenarPorPrioridade(listaParaOrganizar)

    texto = ""
    contador = 0
    biblioteca = {}
    atividades = []
    atividade = ""
    listaFinal = listaOrganizadaFinal[:]

    for i in range(0, len(listaFinal)):
        for j in range(0, len(listaFinal[i])):
            if j == 3:
                atividade = atividade + listaFinal[i][j]
            elif listaFinal[i][j] != "":
                atividade = atividade + listaFinal[i][j] + " "
        atividades.append(atividade.strip()+"\n")
        atividade = ""
    for i in range(0, len(listaOrganizadaFinal)):
        if listaOrganizadaFinal[i][0] != "":
            listaOrganizadaFinal[i][0] = (str(listaOrganizadaFinal[i][0][0])+str(listaOrganizadaFinal[i][0][1])+"/"+str(listaOrganizadaFinal[i][0][2])+str(listaOrganizadaFinal[i][0][3])+"/"+str(listaOrganizadaFinal[i][0][4])+str(listaOrganizadaFinal[i][0][5])+str(listaOrganizadaFinal[i][0][6])+str(listaOrganizadaFinal[i][0][7]) + " ")
        if listaOrganizadaFinal[i][1] != "":
            listaOrganizadaFinal[i][1] = (str(listaOrganizadaFinal[i][1][0])+str(listaOrganizadaFinal[i][1][1])+"h"+str(listaOrganizadaFinal[i][1][2])+str(listaOrganizadaFinal[i][1][3])+"m"+" ")
        if (listaOrganizadaFinal[i][2] != "") and (listaOrganizadaFinal[i][3] != ""):
            listaOrganizadaFinal[i][3] = " " + listaOrganizadaFinal[i][3]
        if (listaOrganizadaFinal[i][4] != "") and (listaOrganizadaFinal[i][5] != ""):
            listaOrganizadaFinal[i][5] = " " + listaOrganizadaFinal[i][5]
    for j in range(0, len(listaOrganizadaFinal)):
        contador = contador + 1
        if listaOrganizadaFinal[j][2] == "(A)":
            for k in listaOrganizadaFinal[j]:
                texto = texto + k
                biblioteca[contador] = texto
            printCores(contador, texto, BOLD + RED)
            texto = ""
        elif listaOrganizadaFinal[j][2] == "(B)":
            for k in listaOrganizadaFinal[j]:
                texto = texto + k
                biblioteca[contador] = texto
            printCores(contador, texto, YELLOW)
            texto = ""
        elif listaOrganizadaFinal[j][2] == "(C)":
            for k in listaOrganizadaFinal[j]:
                texto = texto + k
                biblioteca[contador] = texto
            printCores(contador, texto, BLUE)
            texto = ""
        elif listaOrganizadaFinal[j][2] == "(D)":
            for k in listaOrganizadaFinal[j]:
                texto = texto + k
                biblioteca[contador] = texto
            printCores(contador, texto, GREEN)
            texto = ""
        else:
            for k in listaOrganizadaFinal[j]:
                texto = texto + k
                biblioteca[contador] = texto
            printCores(contador, texto, WRITE)
            texto = ""

    return atividades

def remover(itemRemover):
    if itemRemover.isnumeric() == False:
        print("\n")
        printCores("", "Digite o índice em formato numérico!", REVERSE)
        printCores("", "Não foi possível remover o compromisso do arquivo " + TODO_FILE, REVERSE)
    else:
        itemRemover = int(itemRemover)
        atividades = listar()
        if itemRemover > len(atividades) or itemRemover <= 0:
            print("\n")
            printCores("", "Digite um índice válido!", REVERSE)
            printCores("", "Não foi possível remover o compromisso do arquivo " + TODO_FILE, REVERSE)
        else:
            itemRemovido = atividades[itemRemover-1]
            atividades.pop(itemRemover-1)
            atividadesAtualizado = ""
            for i in atividades:
                atividadesAtualizado = atividadesAtualizado + i
            arq = open('todo.txt', 'w')
            arq.write(atividadesAtualizado)
            arq.close()

def priorizar(num, prioridade):
    if num.isnumeric() == False:
        print("\n")
        printCores("", "Digite o índice em formato numérico!", REVERSE)
        printCores("", "Não foi possível priorizar o compromisso do arquivo " + TODO_FILE, REVERSE)
    elif len(prioridade) > 1 or not(prioridade.upper() >= "A" and prioridade.upper()  <= "Z"):
        print("\n")
        printCores("", "Digite um prioridade válida!", REVERSE)
        printCores("", "Não foi possível priorizar o compromisso do arquivo " + TODO_FILE, REVERSE)
    else:
        num = int(num)
        prioridade = prioridade.upper()
        atividades = listar()
        if num > len(atividades):
            print("\n")
            printCores("", "Digite um número válido!", REVERSE)
            printCores("", "Não foi possível priorizar o compromisso do arquivo " + TODO_FILE, REVERSE)
        else:
            listaPriorizar = []
            for i in range(0, len(atividades)):
                listaPriorizar.append(organizar(atividades[i]))

            if listaPriorizar[num-1][2] == "":
                listaPriorizar[num-1][2] = "(" + prioridade + ")"
            else:
                listaPriorizar[num - 1][2] = "(" + prioridade + ")"

            atividades = []
            atividade = ""
            for i in range(0, len(listaPriorizar)):
                for j in range(0, len(listaPriorizar[i])):
                    if j == 3:
                        atividade = atividade + listaPriorizar[i][j]
                    elif listaPriorizar[i][j] != "":
                        atividade = atividade + listaPriorizar[i][j] + " "
                atividades.append(atividade.strip() + "\n")
                atividade = ""
            atividadesAtualizado = ""
            for j in atividades:
                atividadesAtualizado = atividadesAtualizado + j
            arq = open('todo.txt', 'w')
            arq.write(atividadesAtualizado)
            arq.close()

def fazer(num):
    if num.isnumeric() == False:
        print("Digite um número!")
    else:
        num = int(num)
        atividades = listar()
        if num > len(atividades):
            print("Digite um número válido!")
        else:
            itemRemovido = atividades[num - 1]
            atividades.pop(num - 1)
            atividadesAtualizado = ""
            for i in atividades:
                atividadesAtualizado = atividadesAtualizado + i
            arq = open('todo.txt', 'w')
            arq.write(atividadesAtualizado)
            arq.close()

            arqSaida = open('done.txt', 'a')
            arqSaida.write(itemRemovido)
            arqSaida.close()

def desenhar(dias):
    if dias.isnumeric() == False:
        print("\n")
        printCores("", "Digite um número válido!", REVERSE)
    elif int(dias) <= 0:
        print("\n")
        printCores("", "Digite um número válido!", REVERSE)
    else:
        arq = open('done.txt', 'r')
        ler = arq.readlines()
        arq.close()

        listaParaDesenhar = []
        for i in range(0, len(ler)):
            listaParaDesenhar.append(organizar(ler[i]))

        datas = []
        for j in range(0, len(listaParaDesenhar)):
            data = str(listaParaDesenhar[j][0])
            if data.isnumeric() == True and len(listaParaDesenhar[j][0]) == 8:
                datas.append(listaParaDesenhar[j][0])
        y = []
        x = []
        ocorrencia = 1
        for l in range(0, len(datas)):
            for k in range(1, len(datas)):
                if datas[l] != "":
                    if datas[l] == datas[k] and l != k:
                        ocorrencia = ocorrencia + 1
                        datas[k] = ""
            if datas[l] != "":
                x.append(datas[l])
                y.append(ocorrencia)
            ocorrencia = 1

        dataAtual = datetime.date.today()
        eixoX = []
        eixoY = []

        for i in range (0, len(x)):
            dia = int(x[i][0]+x[i][1])
            mes = int(x[i][2]+x[i][3])
            ano = int(x[i][4]+x[i][5]+x[i][6]+x[i][7])

            dataComparar = datetime.date(day=dia, month=mes, year=ano)

            if abs((dataAtual - dataComparar).days) <= int(dias):
                eixoX.append(x[i])
                eixoY.append(y[i])


        plt.plot(eixoX, eixoY)
        plt.show()

def processarComandos(comandos):      #recebe lista de strings
    if comandos[1] == ADICIONAR:
        comandos.pop(0)                                                             #remove 'agenda.py'
        comandos.pop(0)                                                             #remove 'adicionar'
        try:
            itemParaAdicionar = organizar([' '.join(comandos)][0])
            adicionar(itemParaAdicionar[3], itemParaAdicionar)                      #novos itens não têm prioridade
        except (IndexError, TypeError, AttributeError) as err:
            if str(err) == "string index out of range":
                print("\n")
                printCores("", "Não foi possível adicionar o compromisso no arquivo " + TODO_FILE, REVERSE)
                printCores("", "Adicione pelo menos uma descrição!", REVERSE)
            else:
                printCores("", "Não foi possível adicionar para o arquivo " + TODO_FILE, REVERSE)

    elif comandos[1] == LISTAR:
        try:
            listar()
        except TypeError as err:
            print("\n")
            printCores("", "Não foi possível listar o arquivo " + TODO_FILE, REVERSE)
            printCores("", "Rever o arquivo " + TODO_FILE + "!", REVERSE)

    elif comandos[1] == REMOVER:
        try:
            remover(comandos[2])
        except IndexError as err:
            print("\n")
            printCores("", "Não foi possível remover o compromisso do arquivo " + TODO_FILE, REVERSE)
            printCores("", "Adicione um índice!", REVERSE)

    elif comandos[1] == FAZER:
        try:
            fazer(comandos[2])
        except IndexError as err:
            print("\n")
            printCores("", "Não foi possível fazer o compromisso do arquivo " + TODO_FILE, REVERSE)
            printCores("", "Adicione um índice!", REVERSE)

    elif comandos[1] == PRIORIZAR:
        try:
            comandos[2] = comandos[2].upper()
            priorizar(comandos[2], comandos[3])
        except IndexError as err:
            print("\n")
            printCores("", "Não foi possível priorizar o compromisso no arquivo " + TODO_FILE, REVERSE)
            printCores("", "Adicionar comandos válidos!", REVERSE)

    elif comandos[1] == DESENHAR:
        try:
            desenhar(comandos[2])
        except IndexError as err:
            print("\n")
            printCores("", "Não foi possível mostrar gráfico! ", REVERSE)
            printCores("", "Adicionar comandos válidos!", REVERSE)
    else:
        print("Comando inválido.")

processarComandos(sys.argv)

# sys.argv é uma lista de strings
# python3 agenda.py a Mudar de nome.
# sys.argv terá como conteúdo ['agenda.py', 'a', 'Mudar', 'de', 'nome']