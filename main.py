from winged_edge import Objeto, Vertice, Face, Aresta, ConstrutorObj

class Query:
    def __init__(self, objName: str):
        # abre obj e o divide em classes
        self.objeto = Objeto(objName)
        self.objeto.abrir()
        self.objeto = ConstrutorObj(self.objeto)
        self.objeto.constroi()

    def facesCompartilhandoVertice(self, verticeId) -> list:
        vertice = self.objeto.vertices[verticeId]
        stack = [vertice.arestaIncidente]  # começa com aresta incidente
        visited = {}    # marcar arestas visitadas
        faces = set()   # retorno
        while stack:
            e = stack.pop()
            if e in visited:
                continue
            visited[e] = True
            # adiciona faces conectadas a essa aresta
            if e.faceEsquerda: 
                faces.add(e.faceEsquerda.id)
            if e.faceDireita: 
                faces.add(e.faceDireita.id)
            # Push nas arestas adjacentes (ambas faces) se conectadas a vertice referencia
            for arestaAdj in [e.arestaFaceEsquerdaAnterior, e.arestaFaceEsquerdaPosterior,
                                e.arestaFaceDireitaAnterior, e.arestaFaceDireitaPosterior]:
                if arestaAdj and (arestaAdj.verticeInicial == vertice or 
                                    arestaAdj.verticeFinal == vertice):
                    stack.append(arestaAdj)
        return list(faces)

    def arestasCompartilhandoVertice(self, verticeId) -> list:
        vertice = self.objeto.vertices[verticeId]
        stack = [vertice.arestaIncidente]  # começa com aresta incidente
        visited = {}    # marcar arestas visitadas
        arestas = set()   # retorno
        while stack:
            e = stack.pop()
            if e in visited:
                continue
            visited[e] = True
            # adiciona aresta
            arestas.add(e.id)
            # Push nas arestas adjacentes (ambas faces) se conectadas a vertice referencia
            for arestaAdj in [e.arestaFaceEsquerdaAnterior, e.arestaFaceEsquerdaPosterior,
                                e.arestaFaceDireitaAnterior, e.arestaFaceDireitaPosterior]:
                if arestaAdj and (arestaAdj.verticeInicial == vertice or 
                                    arestaAdj.verticeFinal == vertice):
                    stack.append(arestaAdj)
        return list(arestas)

    def facesCompartilhandoAresta(self, aresta_id) -> list:
        aresta = self.objeto.arestas[aresta_id]
        return sorted([aresta.faceEsquerda.id, aresta.faceDireita.id])

    def arestasCompartilhandoFace(self, faceId) -> list:
        face = self.objeto.faces[faceId]
        arestaAtual = face.aresta
        arestas = [arestaAtual.id]
        if face == arestaAtual.faceEsquerda:
            arestas.append(arestaAtual.arestaFaceEsquerdaAnterior.id)
            arestas.append(arestaAtual.arestaFaceEsquerdaPosterior.id)
        else:
            arestas.append(arestaAtual.arestaFaceDireitaAnterior.id)
            arestas.append(arestaAtual.arestaFaceDireitaPosterior.id)
        return sorted(arestas)

    def facesAdjacentesAFace(self, faceId) -> list:
        face = self.objeto.faces[faceId]
        arestaAtual = face.aresta
        arestas = [arestaAtual]
        if face == arestaAtual.faceEsquerda:
            arestas.append(arestaAtual.arestaFaceEsquerdaAnterior)
            arestas.append(arestaAtual.arestaFaceEsquerdaPosterior)
        else:
            arestas.append(arestaAtual.arestaFaceDireitaAnterior)
            arestas.append(arestaAtual.arestaFaceDireitaPosterior)
        faces = set()
        for aresta in arestas:
            if aresta.faceEsquerda == face:
                faces.add(aresta.faceDireita.id)
            else:
                faces.add(aresta.faceEsquerda.id)
        return sorted(list(faces))

def main():
    query = Query("cube.obj")
    while True:
        print("\nMenu de Consultas:")
        print("1. Faces que compartilham um dado vértice")
        print("2. Arestas que compartilham um dado vértice")
        print("3. Faces que compartilham uma dada aresta")
        print("4. Arestas que compartilham uma dada face")
        print("5. Faces adjacentes a uma dada face")
        print("0. Sair")
        
        opcao = input("Escolha uma opção (0-5): ")
        
        if opcao == '0':
            print("Saindo do programa.")
            break
        
        try:
            if opcao == '1':
                # mostrar numero de vertices
                verticeId = int(input(f"Digite o ID do vértice (1-{len(query.objeto.vertices)}): "))
                print("Faces compartilhadas:", query.facesCompartilhandoVertice(verticeId-1))
            
            elif opcao == '2':
                # mostrar numero de vertices
                vertice_id = int(input(f"Digite o ID do vértice (1-{len(query.objeto.vertices)}): "))
                print("Arestas compartilhadas:", query.arestasCompartilhandoVertice(vertice_id-1))
            
            elif opcao == '3':
                # mostrar numero de arestas
                aresta_id = int(input(f"Digite o ID da aresta (1-{len(query.objeto.arestas)}): "))
                print("Faces compartilhadas:", query.facesCompartilhandoAresta(aresta_id-1))
            
            elif opcao == '4':
                # mostrar numero de faces
                face_id = int(input(f"Digite o ID da face (1-{len(query.objeto.faces)}): "))
                print("Arestas compartilhadas:", query.arestasCompartilhandoFace(face_id-1))
            
            elif opcao == '5':
                # mostrar numero de vertices
                face_id = int(input(f"Digite o ID da face (1-{len(query.objeto.faces)}): "))
                print("Faces adjacentes:", query.facesAdjacentesAFace(face_id-1))
            
            else:
                print("Opção inválida. Tente novamente.")
        
        except (ValueError, IndexError) as e:
            print(f"Erro: {str(e)}. Verifique os IDs e tente novamente.")

if __name__ == "__main__":
    main()