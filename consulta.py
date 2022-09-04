from pickle import FALSE
import pycurl
import json

def getstr(str, ini, end): #--- COLETA A STRING ---#
    if ini in str: #--- VERIFICA SE EXISTE A STRING ---#
        str = str.split(ini)[1]
        str = str.split(end)[0]
        return str
    else:
        return "nao encontrado"  #--- SE NAO EXISTIR FALSE ---#

def consulta(razao, cnpj):      #INICIA A FUNCAO DE CAPTURA
    razao = razao.replace(',', '') #--- CLEAN STRING ---#
    razao = razao.replace('-', '') #--- CLEAN STRING ---#
    razao = razao.replace('/', '') #--- CLEAN STRING ---#
    razao = razao.replace('*', '') #--- CLEAN STRING ---#
    razao = razao.replace('!', '') #--- CLEAN STRING ---#
    razao = razao.replace('.', '') #--- CLEAN STRING ---#
    razao = razao.replace('-', '') #--- CLEAN STRING ---#
    razao = razao.replace('&', 'and') #--- CLEAN STRING ---#
    razao = razao.replace('[0-9]', '') #--- CLEAN STRING ---#
    razao = razao.strip() #--- CLEAN STRING ---#
    razao = razao.lower() #--- CLEAN STRING ---#
    razao = razao.replace('  ', '-') #--- CLEAN STRING ---#
    razao = razao.replace(' ', '-') #--- CLEAN STRING ---#
    searchString = razao + cnpj #--- RAZAO SOCIAL = CNPJ ---#

    ch = pycurl.Curl() #--- CURL PARA COLETA DE DADOS ---#
    ch.setopt(pycurl.URL, "https://casadosdados.com.br/solucao/cnpj/"+searchString)
    ch.setopt(pycurl.FOLLOWLOCATION, True)
    ch.setopt(pycurl.HTTPHEADER, ( 'Host: casadosdados.com.br', 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0','Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Accept-Language: pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3', 'Accept-Encoding: gzip, deflate, br', 'Alt-Used: casadosdados.com.br','Connection: keep-alive', 'Upgrade-Insecure-Requests: 1','Sec-Fetch-Dest: document','Sec-Fetch-Mode: navigate','Sec-Fetch-Site: same-origin','Sec-Fetch-User: ?1','TE: trailers'))
    ch.setopt(pycurl.COOKIEJAR, 'cookie.txt')
    ch.setopt(pycurl.COOKIEFILE, 'cookie.txt')
    ch.setopt(pycurl.ENCODING, 'utf-8')
    end = ch.perform_rs() #--- FIM DO CURL DA COLETA ---#

    razao_social = getstr(end, 'razao_social:"', '"') #--- CAPTURA STRING ---#
    cep = getstr(end, 'cep:"','"') #--- CAPTURA STRING ---#
    natureza_juridica = getstr(end, 'Natureza Jurídica</p> <p data-v-bd724178>','</p></div>') #--- CAPTURA STRING ---#
    telefone = getstr(end, 'Telefone</p> <p data-v-bd724178><a href="tel:', '"') #--- CAPTURA STRING ---#
    mail = getstr(end, 'E-MAIL</p> <p data-v-bd724178><a href="mailto:','"') #--- CAPTURA STRING ---#
    complemento = getstr(end, 'complemento:"', '"') #--- CAPTURA STRING ---#
    socio = getstr(end, 'quadro_societario:[{nome:"', '"') #--- CAPTURA STRING ---#

    if 'celular' in end: #--- REORGANIZA NUMERO DE TELEFONE ---#
        telefone = telefone.replace(" ", "9")
    elif 'fixo' in end: #--- REORGANIZA NUMERO DE TELEFONE ---#
        telefone = telefone.replace(" ", "")
    else: #--- REORGANIZA NUMERO DE TELEFONE ---#
        telefone = telefone.replace(" ", "9")

    #\/\/\/       RETORNA ARRAY COM OS DADOS CAPTURADOS   ####
    return {"telefone":telefone, "email":mail, "razão social": razao_social, "cep":cep, "natureza":natureza_juridica, "complemento":complemento, "socio":socio
    }




pdv = ['ALMIRANTE TAMANDARE','ARAUCARIA','CAMPO LARGO','CAMPO MAGRO', 'COLOMBO', 'CURITIBA', 'GUARATUBA', 'PARANAGUA','PINHAIS','PIRAQUARA','QUATRO BARRAS','SAO JOSE DOS PINHAIS','ANDIRA', 'APUCARANA', 'CAMBE','CASCAVEL','CIANORTE', 'CORNELIO PROCOPIO', 'FLORESTA','FOZ DO IGUACU', 'GUARAPUAVA',  'IBIPORA', 'JANDAIA DO SUL', 'LONDRINA','MARECHAL CANDIDO RONDON', 'MARINGA',  'MEDIANEIRA', 'PAICANDU',
 'SAO PEDRO DO IVAI', 'SAO SEBASTIAO DA AMOREIRA', 'TELEMACO BORBA', 'UNIAO DA VITORIA','WENCESLAU BRAZ','ALVORADA', 'CACHOEIRINHA', 'CAMAQUA', 'CANOAS', 'ELDORADO DO SUL', 'ESTEIO','GRAVATAI', 'GUAIBA','NOVO HAMBURGO','PORTO ALEGRE','SANTA CRUZ DO SUL',  'SAO LEOPOLDO', 'VIAMAO', 'ALEGRETE','CARAZINHO','CAXIAS DO SUL', 'ERECHIM', 'FARROUPILHA', 'GARIBALDI', 'IJUI', 'MARAU', 'PASSO FUNDO', 'PELOTAS', 'ROSARIO DO SUL',  'SANTA MARIA', 'SANTO ANGELO', 'SAO LOURENCO DO SUL',  'BLUMENAU', 'BRUSQUE',  'CHAPECO', 'CRICIUMA', 'FLORIANOPOLIS', 'GAROPABA', 'GUABIRUBA',  'ICARA', 'INDAIAL', 'ITAJAI', 'ITUPORANGA', 'JOINVILLE', 'LAGES', 'LAURENTINO', 'NAVEGANTES', 'RIO DO SUL', 'SAO JOSE', 'TUBARAO', 'CAMPINAS', 'GUARULHOS', 'HORTOLANDIA', 'SAO PAULO']

# print(consulta('OEDSON SILVA AMORIM EIRELI', '10811580000150'))  #TESTE



def coletaArray(cidade, pagina):
    if cidade == '':
        exit("ERROR: city not found")


    ch = pycurl.Curl()
    ch.setopt(pycurl.URL, "https://api.casadosdados.com.br/v2/public/cnpj/search")
    ch.setopt(pycurl.FOLLOWLOCATION, True)
    ch.setopt(pycurl.COOKIEJAR, 'cookie.txt')
    ch.setopt(pycurl.COOKIEFILE, 'cookie.txt')
    ch.setopt(pycurl.HTTPHEADER, ('Host: api.casadosdados.com.br', 'Accept: application/json, text/plain, */*', 'Accept-Language: pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3', 'Accept-Encoding: gzip, deflate, br', 'Content-Type: application/json', 'Origin: https://casadosdados.com.br', 'Connection: keep-alive', 'Referer: https://casadosdados.com.br/', 'Sec-Fetch-Dest: empty', 'Sec-Fetch-Mode: cors', 'Sec-Fetch-Site: same-site', 'TE: trailers'))
    ch.setopt(pycurl.USERAGENT, 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0')
    ch.setopt(pycurl.POST, True)
    ch.setopt(pycurl.ENCODING, 'utf-8')
    # gte = Data de Abertura - A partir de - ano-mes-dia
    # lte = Data de Abertura - Até
    ch.setopt(pycurl.POSTFIELDS, '{"query":{"termo":[],"atividade_principal":[],"natureza_juridica":[],"uf":["PR", "SC", "RS", "SP"],"municipio":["'+cidade+'"],"situacao_cadastral":"ATIVA","cep":[],"ddd":[]},"range_query":{"data_abertura":{"lte":"2022-08-31","gte":"2022-08-31"},"capital_social":{"lte":null,"gte":null}},"extras":{"somente_mei":false,"excluir_mei":true,"com_email":false,"incluir_atividade_secundaria":false,"com_contato_telefonico":true,"somente_fixo":false,"somente_celular":false,"somente_matriz":false,"somente_filial":false},"page":'+pagina+'}')
    return json.loads(ch.perform_rb())



for cidade in pdv:
    print("Catando em"+cidade+"...")
    total = coletaArray(cidade, "1")["data"]["count"]
    paginas = int(total/20)
    if paginas < 1:
        paginas = 1
    loopPaginas = 0
    print(cidade)
    while loopPaginas != paginas:
        dados = coletaArray(cidade, str(loopPaginas))
        if dados["data"]["count"] == 0:
            dados = False
        else:
            dados = dados["data"]["cnpj"]
        if dados != False:
            for linha in dados:
                material = open('material.csv', 'r')
                if linha["cnpj"] not in material.read():
                    cnpj = linha["cnpj"].replace(',', '')
                    razao_social = linha["razao_social"].replace(',', '')
                    data_abertura = linha["data_abertura"].replace(',', '')
                    atividade_principal = linha["atividade_principal"]["descricao"].replace(',', '')
                    logradouro = linha["logradouro"].replace(',', '')
                    numero = linha["numero"].replace(',', '')
                    bairro = linha["bairro"].replace(',', '')
                    municipio = linha["municipio"].replace(',', '')
                    uf = linha["uf"].replace(',', '')
                    print("escrevendo"+cnpj)
                    dadosConsulta = consulta(razao_social, cnpj)
                    telefone = dadosConsulta["telefone"].replace(',', '')
                    mail = dadosConsulta["email"].replace(',', '')
                    complemento = dadosConsulta["complemento"].replace(',', '')
                    cep = dadosConsulta["cep"].replace(',', '')
                    natureza = dadosConsulta["natureza"].replace(',', '')
                    socio = dadosConsulta["socio"].replace(',', '')
                    
                    escrever = cnpj+","+razao_social+","+logradouro+","+numero+","+complemento+","+bairro+","+municipio+","+uf+","+cep+","+data_abertura+","+atividade_principal+","+natureza+","+telefone+","+mail+"\n"
                    material = open('material.csv', 'a')
                    material.write(escrever)
                else:
                    print("Ja encontrado")


        loopPaginas = loopPaginas + 1


    