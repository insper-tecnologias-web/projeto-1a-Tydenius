from urllib.parse import unquote_plus
from utils import load_data, load_template, addDB,updateDB, build_response

def index(request):

    if request.startswith('POST'):
        if 'id' in request:
            request = request.replace('\r', '')  # Remove caracteres indesejados
            # Cabeçalho e corpo estão sempre separados por duas quebras de linha
            partes = request.split('\n\n')
            corpo = partes[1]
            print("###########Este é o corpo da requisição##########\n" + corpo)
            params = {}
            dicId = "id"
            dicTit = "titulo"
            dicDesc = "detalhes"

            data = corpo.split('&')
            dataId = data[0].split('=')
            dataTit = data[1].split('=')
            dataDet = data[2].split('=')

            params[dicId] = unquote_plus(dataId[1])
            params[dicTit] = unquote_plus(dataTit[1])
            params[dicDesc] = unquote_plus(dataDet[1])

            print("############Parâmetros do Update############## \n")
            print(params)
            updateDB(params)
            
            notes = note_template()

            return build_response(code=303, reason='See Other', headers='Location: /') + load_template('index.html').format(notes=notes).encode() 
        else:
            request = request.replace('\r', '')  # Remove caracteres indesejados
            # Cabeçalho e corpo estão sempre separados por duas quebras de linha
            partes = request.split('\n\n')
            corpo = partes[1]
            print("###########Este é o corpo da requisição##########\n" + corpo)
            params = {}
            dicTit = "titulo"
            dicDesc = "detalhes"

            data = corpo.split('&')
            dataTit = data[0].split('=')
            dataDet = data[1].split('=')

            params[dicTit] = unquote_plus(dataTit[1])
            params[dicDesc] = unquote_plus(dataDet[1])
            addDB(params)
            print(params)

            notes = note_template()

            return build_response(code=303, reason='See Other', headers='Location: /') + load_template('index.html').format(notes=notes).encode() 

    elif request.startswith('GET /excluir'):
        notes = note_template()

        return build_response(code=303, reason='See Other', headers='Location: /') + load_template('index.html').format(notes=notes).encode() 
    else:

        notes = note_template()

        return build_response() + load_template('index.html').format(notes=notes).encode()


def note_template():
        note_template = load_template('components/note.html')
        notes_li = [
            note_template.format(id=dados.id, titulo=dados.titulo, detalhes=dados.detalhes)
            for dados in load_data()
        ]
        notes = '\n'.join(notes_li)
        return notes