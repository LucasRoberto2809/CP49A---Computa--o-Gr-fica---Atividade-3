# Classes

class Objeto():
    def __init__(self, arquivo):
        self.arquivo = arquivo
        self.nome = ""
        self.vertices = []
        self.faces = []
        self.arestas = []
    def abrir(self):
        with open(self.arquivo, 'r') as texto:
            for linha in texto:
                linha = linha.strip()
                if not linha:
                    continue 
                linha = linha.split()
                opcao = linha[0]
                if opcao=='v':
                    self._anotaVertice(linha)
                if opcao=='f':
                    self._anotaFace(linha)

    def _anotaVertice(self, linha):
        x = float(linha[1])
        y = float(linha[2])
        z = float(linha[3])
        self.vertices.append(Vertice(x,y,z))
    
    def _anotaFace(self, linha):
        lista = [] # lista de vertices
        for v in linha[1:]:
            indice = int(v.split('/')[0])
            lista.append(indice-1) # -1 pois vertices começam em 1
        self.faces.append(Face(lista))

class Vertice:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.arestaIncidente = None

class Face():
    def __init__(self, indiceVertices):
        self.indiceVertices = indiceVertices
        self.aresta = None

class Aresta():
    def __init__(self):
        self.verticeInicial = None
        self.verticeFinal = None
        self.faceEsquerda = None
        self.faceDireita = None
        self.faceEsquerdaAnterior = None
        self.faceEsquerdaPosterior = None
        self.faceDireitaAnterior = None
        self.faceDireitaPosterior = None

class ConstrutorObj:
    def __init__(self, parser):
        self.parser = parser
        self.vertices = parser.vertices
        self.faces = parser.faces
        self.arestas = []
        self.mapaArestas = {} # usado como auxiliar em funções
    
    def constroi(self):
        for face in self.faces:
            vertices = face.indiceVertices
            n = len(vertices)
            # cria arestas para esta face
            arestasFace = []
            for i in range(n):
                v1 = vertices[i]
                v2 = vertices[(i+1)%n]
                # cria ou encontra aresta
                chaveAresta = tuple(sorted((v1, v2)))
                if chaveAresta in self.mapaArestas:
                    aresta = self.mapaArestas[chaveAresta]
                else:
                    aresta = Aresta()
                    aresta.verticeInicial = self.vertices[v1]
                    aresta.verticeFinal = self.vertices[v2]
                    self.mapaArestas[chaveAresta] = aresta
                    self.arestas.append(aresta)
                # define a face da aresta
                if aresta.verticeInicial == self.vertices[v1]:
                    aresta.faceEsquerda = face
                else:
                    aresta.faceDireita = face
                arestasFace.append(aresta)
            # conecta arestas da face atual
            for i in range(len(vertices)):
                arestaAtual = arestasFace[i]
                arestaAnterior = arestasFace[(i-1)%n]
                arestaPosterior = arestasFace[(i+1)%n]
                # confere se a face esta a esquerda ou a direita
                if arestaAtual.faceEsquerda == face:
                    arestaAtual.faceEsquerdaAnterior = arestaAnterior
                    arestaAtual.faceEsquerdaPosterior = arestaPosterior
                else:
                    arestaAtual.faceDireitaAnterior = arestaAnterior
                    arestaAtual.faceDireitaPosterior = arestaPosterior   
                # define a aresta incidente do vertice (se necessario)
                if self.vertices[vertices[i]].arestaIncidente is None:
                    self.vertices[vertices[i]].arestaIncidente = arestaAtual
            # define aresta da face
            face.aresta = arestasFace[0]