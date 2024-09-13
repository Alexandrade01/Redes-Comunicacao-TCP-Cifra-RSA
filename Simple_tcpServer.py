# Bibliotecas necessárias para o código:
import base64
import datetime
import json
from multiprocessing import Pool, cpu_count, Manager
import random
from socket import *

#######################
# Cifra RSA em Python #
#######################


##################################
# GRUPO                          #
# * Abrão Asterio Junior         #
# * Alexandre Bezerra de Andrade #
# * Daniel Santos de Sousa       #
# * Francisco Tommasi Silveira   #
##################################


#### FUNÇÕES AUXILIARES ####

####################################################
# Função para obter a data e hora atual
# Retorno:
#   a data e hora atual no formato "YYYY-MM-DD HH:MM:SS"
def agora():
    """
    Função para obter a data e hora atual
    Retorno:
        a data e hora atual no formato "YYYY-MM-DD HH:MM:SS"
    """

    # Retorna a data e hora atual
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
####################################################


##################################################
# Função para realizar o teste de primalidade de Miller-Rabin
# Parâmetros:
#   n (int): número a ser testado
#   k (int): número de iterações do teste
# Retorno:
#   bool: True se o número é provavelmente primo, False se é composto
def miller_rabin_test(n, k):
    """
    Realiza o teste de primalidade de Miller-Rabin em um número dado.

    Args:
        n (int): O número a ser testado.
        k (int): O número de iterações do teste.

    Returns:
        bool: True se o número é provavelmente primo, False se é composto.
    """
    
    # DEBUG
    #print(f"{agora()} - Iniciando o teste de Miller-Rabin para o número {n} com {k} iterações.")
    
    # Casos triviais
    if n == 2 or n == 3 or n == 5 or n == 7 or n == 11: # Teste de primos pequenos
        return True
    if n % 2 == 0 or n == 1: # Teste de paridade e de 1
        return False
    if sum(int(digito) for digito in str(n)) % 3 == 0: # Teste de divisibilidade por 3
        return False
    if n % 10 in [0, 2, 4, 5, 6, 8]: # Teste de divisibilidade por 2 e 5
        return False

    # Escreve n-1 como 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Realiza k iterações do teste
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True
##################################################


##################################################
# Função para gerar um candidato a número primo com um número específico de bits
# Parâmetros:
#   bits (int): número de bits do candidato
# Retorno:
#   int: número candidato a primo
def generate_candidate(bits):
    """
    Gera um candidato a número primo com um número específico de bits.

    Args:
        bits (int): O número de bits do candidato.

    Returns:
        int: Um número inteiro candidato a primo.
    """

    # DEBUG
    #print(f"{agora()} - Gerando um candidato a número primo com {bits} bits.")
    
    candidate = random.getrandbits(bits)
    candidate |= (1 << bits - 1) | 1  # Garante que o número é ímpar e tem o bit mais significativo definido
    return candidate
##################################################


##################################################
# Função para encontrar um número primo de um tamanho específico em bits
# Parâmetros:
#   bits (int): número de bits do número primo
#   k (int): número de iterações do teste de Miller-Rabin
#   result (multiprocessing.Manager.Value): valor compartilhado para armazenar o número primo encontrado
#   found (multiprocessing.Manager.Value): valor booleano compartilhado para indicar se um primo foi encontrado
# Retorno:
#   int: número primo encontrado
def find_prime(bits, k, result, found):
    """
    Encontra um número primo de um tamanho específico em bits.

    Args:
        bits (int): O número de bits do número primo.
        k (int): O número de iterações do teste de Miller-Rabin.
        result (multiprocessing.Manager.Value): Valor compartilhado para armazenar o número primo encontrado.
        found (multiprocessing.Manager.Value): Valor booleano compartilhado para indicar se um primo foi encontrado.

    Returns:
        int: O número primo encontrado.
    """
    #print(f"{agora()} - Iniciando a busca por um número primo de {bits} bits.")
    
    attempt = 0
    while not found.value:
        candidate = generate_candidate(bits)
        attempt += 1

        # DEBUG
        # Exibe uma mensagem a cada 10 tentativas
        #if attempt % 10 == 0:
        #    print(f"Tentativa {attempt}[NOK]: {candidate}")
        
        if miller_rabin_test(candidate, k):
            print(f"{agora()} - Foram realizadas {attempt} tentativas.")
            result.value = candidate
            found.value = True
            return candidate
##################################################


##################################################
# Função para gerar um grande número primo utilizando múltiplos processos
# Parâmetros:
#   bits (int): número de bits do número primo
#   k (int): número de iterações do teste de Miller-Rabin
# Retorno:
#   int: número primo encontrado
def generate_random_prime(bits, k=60):
    """
    Gera um grande número primo utilizando múltiplos processos.

    Args:
        bits (int): O número de bits do número primo.
        k (int): O número de iterações do teste de Miller-Rabin (padrão: 60).

    Returns:
        int: O número primo encontrado.
    """
    print(f"{agora()} - Iniciando a geração de primos com {cpu_count()} processos...")
    
    with Manager() as manager:
        result = manager.Value('i', 0)
        found = manager.Value('b', False)
        with Pool(cpu_count()) as pool:
            pool.starmap(find_prime, [(bits, k, result, found)] * cpu_count())
            pool.close()
            pool.join()
            if result.value != 0:
                #print(f"Primo encontrado: {result.value}")
                return result.value
    print("Geração de primos concluída.")
##################################################


####################################################
# Função que usa o Algortimo de Euclides para calcular o GCD (Máximo Divisor Comum)
# Parâmetros:
#   a: número
#   b: número
# Retorno:
#   o MDC entre os dois números
def gcd(a, b):
    """
    Função para calcular o GCD (Máximo Divisor Comum)
    Parâmetros:
      a: número
      b: número
    Retorno:
      o MDC entre os dois números
    """

    print(f"{agora()} - Calculando o MDC entre {a} e {b}...\n")

    while b != 0:
        a, b = b, a % b
    return a
####################################################


####################################################
# Função para calcular o inverso modular usando o algoritmo estendido de Euclides
# Parâmetros:
#   e: número
#   phi: número
# Retorno:
#   o inverso modular de 'e' em relação a 'phi'
def mod_inverse(e, phi):
    """
    Função para calcular o inverso modular usando o algoritmo estendido de Euclides
    Parâmetros:
        e: número
        phi: número
    Retorno:
        o inverso modular de 'e' em relação a 'phi'
    """

    print(f"{agora()} - Calculando o inverso modular...")

    d, x1, x2, y1 = 0, 0, 1, 1
    temp_phi = phi

    while e > 0:
        temp1 = temp_phi // e
        temp2 = temp_phi - temp1 * e
        temp_phi, e = e, temp2
        x = x2 - temp1 * x1
        y = d - temp1 * y1
        x2, x1 = x1, x
        d, y1 = y1, y

    if temp_phi == 1:
        return d + phi
####################################################

   
####################################################
# Função para gerar as chaves RSA
# Parâmetros:
#   bits: tamanho dos bits
# Retorno:
#   chave pública (e, n) e chave privada (d, n)
def generate_rsa_keys(bits):
    '''
    Função para gerar as chaves RSA
    Parâmetros:
        bits: tamanho dos bits
    Retorno:
        chave pública (e, n) e chave privada (d, n)
    '''

    print(f"{agora()} - Gerando as chaves RSA...")

    # Gerar dois números primos grandes
    p = generate_random_prime(bits // 2, 200)
    q = generate_random_prime(bits // 2, 200)

    # Calcular n = p * q
    n = p * q

    # Calcular a função totiente de Euler (phi) = (p-1) * (q-1)
    phi = (p - 1) * (q - 1)

    # Escolher um valor 'e' tal que 1 < e < phi e gcd(e, phi) = 1
    e = random.randrange(1, phi)
    while gcd(e, phi) != 1:
        e = random.randrange(1, phi)

    # Calcular o inverso modular de 'e', ou seja, d
    d = mod_inverse(e, phi)

    # Chave pública (e, n) e chave privada (d, n)
    return ((e, n), (d, n))
####################################################


####################################################
# Função para criptografar uma mensagem
# Parâmetros:
#   public_key: chave pública (e, n)
#   message: mensagem a ser criptografada
# Retorno:
#   a mensagem criptografada em base64
def encrypt_rsa(public_key, message):
    """
    Função para criptografar uma mensagem
    Parâmetros:
        public_key: chave pública (e, n)
        message: mensagem a ser criptografada
    Retorno:
        a mensagem criptografada em base64
    """

    print(f"{agora()} - Criptografando a mensagem...")

    # Desempacotar a chave pública
    e, n = public_key

    # Convertendo a mensagem para inteiro
    message_int = int.from_bytes(message.encode('utf-8'), byteorder='big')

    # Criptografar usando a fórmula: ciphertext = message^e % n
    ciphertext = pow(message_int, e, n)

    # Converter o número criptografado para bytes
    encrypted_bytes = ciphertext.to_bytes((ciphertext.bit_length() + 7) // 8, byteorder='big')

    # Codificar em base64 para uma representação segura em UTF-8
    encrypted_base64 = base64.b64encode(encrypted_bytes).decode('utf-8')

    # Retornar a mensagem criptografada em base64
    return encrypted_base64
####################################################


####################################################
# Função para descriptografar uma mensagem
# Parâmetros:
#   private_key: chave privada (d, n)
#   encrypted_base64: mensagem criptografada em base64
# Retorno:
#   a mensagem descriptografada
def decrypt_rsa(private_key, encrypted_base64):
    '''	
    Função para descriptografar uma mensagem
    Parâmetros:
        private_key: chave privada (d, n)
        encrypted_base64: mensagem criptografada em base64
    Retorno:
        a mensagem descriptografada
    '''

    print(f"{agora()} - Descriptografando a mensagem...")

    # Desempacotar a chave privada
    d, n = private_key

    # Decodificar a mensagem base64 para bytes
    encrypted_bytes = base64.b64decode(encrypted_base64.encode('utf-8'))

    # Converter os bytes de volta para um inteiro
    ciphertext = int.from_bytes(encrypted_bytes, byteorder='big')

    # Descriptografar usando a fórmula: message = ciphertext^d % n
    decrypted_message_int = pow(ciphertext, d, n)

    # Converter o inteiro de volta para string
    decrypted_message = decrypted_message_int.to_bytes((decrypted_message_int.bit_length() + 7) // 8, byteorder='big').decode('utf-8')

    # Retornar a mensagem descriptografada em UTF-8
    return decrypted_message
####################################################




# Função principal

if __name__ == "__main__":
    # Configurações do Server (Bob)
    serverPort = 1300
    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.bind(("",serverPort))
    serverSocket.listen(7) # o argumento “listen” diz à biblioteca de soquetes que queremos enfileirar no máximo 7 requisições de conexão (normalmente o máximo) antes de recusar começar a recusar conexões externas. Caso o resto do código esteja escrito corretamente, isso deverá ser o suficiente.
    print ("TCP Server\n")
    connectionSocket, addr = serverSocket.accept()

    # Gerar chaves RSA de 4096 bits
    bitsEncodind = 4096
    public_key, private_key = generate_rsa_keys(bitsEncodind)
    print(f"Chaves públicas (e, n):\n{public_key}\n")
    print(f"Chaves privadas (d, n):\n{private_key}\n")


    # HANDSHAKE
    # Enviando a chave pública para o Client (Alice)
    e, n = public_key
    connectionSocket.send(json.dumps(f"e:{e},n:{n}").encode('utf-8'))


    #### MENSAGEM RECEBIDA ####
    # Recebendo mensagem criptografada em base64
    receivedMessage = str(connectionSocket.recv(65000),"utf-8")

    # Descriptografar a mensagem recebida
    decrypted_message = decrypt_rsa(private_key, receivedMessage)
    print(f"Mensagem descriptografada:\n{receivedMessage}\n")


    #### MENSAGEM ENVIADA ####
    # Deixa a mensagem decifrada em caixa alta
    capitalizedSentence = decrypted_message.upper()
    connectionSocket.send(bytes(capitalizedSentence, "utf-8"))
    print ("Sent back to Client (Upper Case): ", capitalizedSentence)

    # Fecha a conexão
    connectionSocket.close()