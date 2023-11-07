from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
import requests
from tkinter import *
import random
# Se conectar ao site


def seConectar(pokemon,path):
    driver = webdriver.Chrome()#puxando drive
    pokemon = pokemon.casefold()#padronizando em minusculo, o nome do pokemon
    driver.get(f'{path}{pokemon}')#acessando o site
    assert pokemon.capitalize() in driver.title #confirmando o titulo do site
    sleep(10)#pausa para o site carregar
    print('foi')#confirmação visual(apagar depois)
    return driver#Retorno do drive, para usarmos em outra funções dps

def buscar(driver,path):
    # Busca valores no site e tranforma em texto
    elem = driver.find_element(By.XPATH,path)
    return elem.text

def buscarGolpes(geracao):
    # Lista todos os golpes do pokemon
    todos_golpes = {}
    origem_golpes = ['Level up','Eggs move','Move tutor','TMs\HMs']#texto para possiveis origem de golpes

    for i in range(1,len(origem_golpes)+1):#usado para buscar e mostrar os golpes
        try:
            if i <4:#Exibe golpes de Level up, Eggs Move e Move tutor
                valor = buscar(driver,f'//*[@id="tab-moves-{geracao}"]/div/div[1]/div[{i}]/table/tbody')#busca os golpes
                todos_golpes[origem_golpes[i-1]] = valor
                
            elif i==4:#Exibe golpes de TM, o codigo faz o mesmo q o de cima, só muda o caminho
                valor = buscar(driver,f'//*[@id="tab-moves-{geracao}"]/div/div[2]/div/table/tbody')
                
                todos_golpes[origem_golpes[i-1]]  = valor
               
            else:
                print('Eita po, como q tu veio para aqui???')#Caso algum erro aconteça(tirar depois)
        except:
            #print('Não encontrado: ',origem_golpes[i-1])#mostra qual tabela não foi encontrada, pode ser erro de codigo ou o pokemon n tem
            pass

    return todos_golpes

def buscarGeracao():
    #Usado para buscar a geracao e colocar no padrão do site
    geracoes_busca = ('//*[@id="main"]/div[8]/div[1]/a[1]','//*[@id="main"]/div[9]/div[1]/a[1]',#Usado para saber a geração
                    '//*[@id="main"]/div[8]/div[1]/a[2]','//*[@id="main"]/div[9]/div[1]/a[2]')#o site tem diferentes tipos endereços 
    geracoes = []#Lista para definir o número da geração do pokemon na hora de buscar seus golpes, n tem a ver com a geração do pokemon

    geracao = {# Dicionario com o número que o site usa para cada geração
        'Ultra Sun/Ultra Moon':            16 ,
        'Sword/Shield':                    18 ,
        'Brilliant Diamond/Shining Pearl': 19 ,
        'Scarlet/Violet':                  21 
    }

    for i in geracoes_busca:#Define quais gerações são ser buscadas e adiciona seus valores em uma lista
        try:
            geracoes.append(buscar(driver,i))#adiciona uma lista o número usado no site de acordo com a geração
        except:
            pass
    return geracao[geracoes[0]]

def padronizandoNumeroNacional():
    #Tratamento de dados para conseguirmos o número do pokemon
    valor = buscar(driver,'//*[@id="main"]/div[2]/div[2]')#chamando função buscar para pegarmos a informação
    valor = valor.splitlines()#transformando todo texto em uma lista com seus valores

    numeronacional = []
    numeronacional.append(valor[1]) #pegando o index com o número nacional(Paldea é 3 em vez de 2 corrigir depois para eles)
    numeronacional.append(valor[2])

    for i in numeronacional:

        if i[11:].isnumeric():
            valor = i[11:]
    
    pokemon = ''#zerando a variavel pokemon
    
    valor = valor.strip()#Retirando os espaços 

    #padronizando o numero do pokemon para o estilo do site
    if int(valor[0])>0:#retirando o 0 do começo 
        pokemon = valor[0]

    for i in range(1,len(valor)-1):#checando qual número é necessario e qual deve se retirar
        if int(valor[i])>0 or int(valor[i-1])!=0:
            pokemon += valor[i]
    pokemon += valor[3]#colocando pelo menos o ultimo número
    return pokemon

# Instanciando a conecção
try:
    pokemon = 'flamigo'
    driver = seConectar(pokemon,'https://pokemondb.net/pokedex/')
except:
    print('Erro de conexão')



try:
    movepool = []
    #Tratamento das informações
    numeronacionalpokemon = padronizandoNumeroNacional()
    #Busca as habilidades passivas dos pokemons
    habilidades = buscar(driver,f'//*[@id="tab-basic-{numeronacionalpokemon}"]/div[1]/div[2]/table/tbody/tr[6]/td')#Buscando as habilidades do pokemon
    #Busca os golpes dos pokemons
    golpes = buscarGolpes(buscarGeracao())
    
    
except:
    print('Erro ao acessar número nacional do pokemon, ou ele é de Paldea')


# Golpes


assert "No results found." not in driver.page_source

driver.close()

'''Fazer a parte grafica
Uma janela com varias informações do pokemon
como Habilidades, Sexo, Peso e tamanho, um janela scroll para todos os golpes, atributos
um botão para gerar um aleatorio
'''
'''
def grafico():
    janela = Tk()
    janela.title('bozo')
    janela.mainloop()

grafico()
'''
