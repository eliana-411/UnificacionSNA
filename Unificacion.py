import json
import os
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import community

#! Integrantes del equipo
#? Lina María Nieto Alarcon
#? María José Castañeda Grajales
#? Eliana Gallego Rivera


def leer_tweets(folder_path, palabra_clave):
    archivos_json = []
    user_tweets = {}
    tweets_encontrados = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".json"):
                archivos_json.append(os.path.join(root, file))

    for archivo in archivos_json:
        with open(archivo, "r", encoding="utf-8") as archivo_json:
            for linea in archivo_json:
                tweet = json.loads(linea)
                if "text" in tweet and palabra_clave in tweet["text"].lower():
                    if "lang" in tweet and tweet["lang"].lower() == "en":
                        if "user" in tweet and "screen_name" in tweet["user"]:
                            username = tweet["user"]["screen_name"].lower()

                            if username not in user_tweets:
                                user_tweets[username] = []

                            if tweet not in user_tweets[username]:
                                user_tweets[username].append(tweet)

    for username, tweets in user_tweets.items():
        tweets_encontrados.extend(tweets)

    return tweets_encontrados

def crear_grafo(tweets_encontrados):
    G = nx.DiGraph()

    for tweet in tweets_encontrados:
        user = tweet["user"]["screen_name"]

        if not G.has_node(user):
            G.add_node(user)

        if "retweeted_status" in tweet:
            retweeted_user = tweet["retweeted_status"]["user"]["screen_name"]

            if not G.has_node(retweeted_user):
                G.add_node(retweeted_user)

            G.add_edge(user, retweeted_user, retweet=True)

        if "user_mentions" in tweet:
            for mention in tweet["user_mentions"]:
                mentioned_user = mention["screen_name"]

                if not G.has_node(mentioned_user):
                    G.add_node(mentioned_user)

                G.add_edge(user, mentioned_user, mention=True)

    return G

def visualizar_grafo(G):
    print("Visualización 1")
    # pos = nx.kamada_kawai_layout(G)
    pos = nx.spring_layout(G)
    labels = {node: node for node in G.nodes}
    nx.draw(G, pos, labels=labels, with_labels=False, node_size=10, node_color="lightblue")
    plt.show()

def visualizar_grafo2(G):
    print("Visualización 2")
    pos = nx.shell_layout(G)
    labels = {node: node for node in G.nodes}
    nx.draw(G, pos, labels=labels, with_labels=False, node_size=10, node_color="lightblue")
    plt.show()

def visualizar_grafo4(G):
    print("Visualización 3")
    pos = nx.circular_layout(G)
    labels = {node: node for node in G.nodes}
    nx.draw(G, pos, labels=labels, with_labels=False, node_size=10, node_color="lightblue")
    plt.show()

def visualizar_grafo5(G):
    print("Visualización 4")
    pos = nx.random_layout(G)
    labels = {node: node for node in G.nodes}
    nx.draw(G, pos, labels=labels, with_labels=False, node_size=10, node_color="lightblue")
    plt.show()

def encontrar_componentes_fuertemente_conectados(grafo):
     # Encontrar los componentes fuertemente conectados
    componentes_fuertemente_conectados = list(nx.strongly_connected_components(grafo))

    print("Componentes Fuertemente Conectados:", componentes_fuertemente_conectados)
    print(f"Componentes: {len(componentes_fuertemente_conectados)}")

    # Imprimir los componentes fuertemente conectados y su tamaño
    for i, componente in enumerate(componentes_fuertemente_conectados, 1):
        print(f"Componente {i}: {componente}, Cantidad de Nodos: {len(componente)}")
    
    
def calcular_centralidad_de_grado(grafo):
    # Calcular la centralidad de grado
    centralidad_grado = nx.degree_centrality(grafo)

    # Encontrar la cuenta con el mayor número de menciones y retweets
    cuenta_mas_influyente = max(centralidad_grado, key=centralidad_grado.get)

    # Imprimir la cuenta más influyente y su valor de centralidad de grado
    print(f"Cuenta más influyente: {cuenta_mas_influyente}, Centralidad de Grado: {centralidad_grado[cuenta_mas_influyente]}")

def calcular_centralidad_de_cercania(grafo):
    # Calcular la centralidad de cercanía
    centralidad_cercania = nx.closeness_centrality(grafo)

    # Encontrar la cuenta con la mayor centralidad de cercanía
    cuenta_mas_cercana = max(centralidad_cercania, key=centralidad_cercania.get)

    # Imprimir la cuenta más cercana y su valor de centralidad de cercanía
    print(f"Cuenta más cercana: {cuenta_mas_cercana}, Centralidad de Cercanía: {centralidad_cercania[cuenta_mas_cercana]}")

def calcular_centralidad_intermediacion(grafo):
    # Calcular la centralidad de intermediación
    centralidad_intermediacion = nx.betweenness_centrality(grafo)

    # Encontrar la cuenta con la mayor centralidad de intermediación
    cuenta_mas_intermediacion = max(centralidad_intermediacion, key=centralidad_intermediacion.get)

    # Imprimir la cuenta más influyente y su valor de centralidad de intermediación
    print(f"Cuenta más influyente: {cuenta_mas_intermediacion}, Centralidad de Intermediación: {centralidad_intermediacion[cuenta_mas_intermediacion]}")

def detectar_y_visualizar_comunidades(grafo):
    # Ejecutar el algoritmo de Louvain para detectar comunidades en el grafo,
    # Pasando el grafo dirigido a no dirigido con la función: G.to_undirected()
    partition = community.greedy_modularity_communities(grafo.to_undirected())

    # Calcular el número de comunidades
    num_communities = len(partition)

    print(f"Número de comunidades encontradas: {num_communities}")
    # Imprimir las comunidades
    for i, community_nodes in enumerate(partition):
        print(f"Comunidad {i + 1}: {community_nodes}")

    # Crear un diccionario que asigne un color único a cada comunidad
    community_colors = {}
    for i, community_nodes in enumerate(partition):
        color = plt.cm.viridis(i / num_communities)
        for node in community_nodes:
            community_colors[node] = color

    # Dibujar el grafo con los nodos coloreados según
    # las comunidades y las aristas también coloreadas
    plt.figure(figsize=(20, 20))
    pos = nx.kamada_kawai_layout(grafo)
    node_colors = [community_colors[node] for node in grafo.nodes()]
    edge_colors = [community_colors[src] for src, dest in grafo.edges()]
    nx.draw(grafo, pos, node_size=30, node_color=node_colors,
            edge_color=edge_colors, with_labels=False)
    plt.title('Grafo coloreado por comunidades')
    plt.show()



if __name__ == "__main__":
    # Cambia la ruta de acceso a la carpeta en tu ordenador
    folder_path = "C:/Users/Eliana/Downloads/SNA/Taller_Unificación/data"
    print("Entrar a la carpeta")

    # Leer los tweets de la carpeta
    tweets_encontrados = leer_tweets(folder_path, "war")
    print("Tweets encontrados")

    # Crear el grafo
    grafo = crear_grafo(tweets_encontrados)
    print("Creación del grafo")

    # Visualizar el grafo
    visualizar_grafo(grafo)
    print("Grafo 1")
    visualizar_grafo2(grafo)
    print("Grafo 2")
    visualizar_grafo4(grafo)
    print("Grafo 3")
    visualizar_grafo5(grafo)
    print("Grafo 4")

    print("COMPONENTES FUERTEMENTE CONECTADOS")
    encontrar_componentes_fuertemente_conectados(grafo)
    print("CENTRALIDAD DE GRADO")
    calcular_centralidad_de_grado(grafo)
    print("CENTRALIDAD DE CERCANIA ")
    calcular_centralidad_de_cercania(grafo)
    print("CENTRALIDAD DE INTERMEDIACIÓN")
    calcular_centralidad_intermediacion(grafo)
    print("COMUNIDADES")
    detectar_y_visualizar_comunidades(grafo)