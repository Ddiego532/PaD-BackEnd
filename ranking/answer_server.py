# Debe existir el archivo 'doclen.txt' preevio a su ejecucion.

from inverted_list import InvertedList
import socket

index = InvertedList()

def load_index():
    all_content= r"indexacion/reduced/all_content_reduced.txt"
    doc_len = r"ranking/data/doclen.txt"
    index.load_index(all_content)
    index.load_doclen(doc_len)
    print("Index load [OK]")

def make_query(query):
    words = query.split()
    intersection_list = index.find(words[0])
    for word in words[1:]:
        intersection_list = index.query_or(intersection_list, word)

    sorted_index = intersection_list.get_full_index_sorted()

    return str(sorted_index)

def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5000

    server_socket = socket.socket() # get instance
    server_socket.bind((host, port)) # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen (2)
    while True:
        conn, address = server_socket.accept() # accept new connection
        print("Connection from: " + str(address))
        data = conn.recv(1024).decode()
        if not data:
            break
        print("from connected user: " + str(data))

        data = make_query(str(data))
        print (f"response: {data}") 

        conn.send(str(data).encode())

    conn.close()


if __name__ == '__main__':
    load_index()
    server_program()