from math import gcd
from json import load, dump
from socket import gethostbyname, gethostname, socket, AF_INET, SOCK_STREAM
from threading import Lock, local, active_count, Thread
from hashlib import sha256
from secrets import token_hex, choice

# Server host ip: 192.168.178.2
# Default host ip: gethostbyname(gethostname())

HOST = "192.168.178.2"
PORT = 5050
s = socket(AF_INET, SOCK_STREAM)
userpass = load(open('userpass.json'))
userdata = load(open('userdata.json'))
userpasslock = Lock()
userdatalock = Lock()
Threadlocalvars = local()
listpunc = {32: None, 91: None, 93: None, 44: None}
datatypes = ["Calendar"]

def primes2(n):
    """ Input n>=6, Returns a list of primes, 2 <= p < n """
    n, correction = n-n%6+6, 2-(n%6>1)
    sieve = [True] * (n//3)
    for i in range(1,int(n**0.5)//3+1):
      if sieve[i]:
        k=3*i+1|1
        sieve[      k*k//3      ::2*k] = [False] * ((n//6-k*k//6-1)//k+1)
        sieve[k*(k-2*(i&1)+4)//3::2*k] = [False] * ((n//6-k*(k-2*(i&1)+4)//6-1)//k+1)
    return [2,3] + [3*i+1|1 for i in range(1,n//3-correction) if sieve[i]]

primeslist = primes2(2000)

def regenerate_encvars(saltlength = 32):
    """Set the keys for the RSA encryption algorhithm and generates a salt
    See documentation on algorithm here: https://www.geeksforgeeks.org/rsa-algorithm-cryptography/."""

    global primeslist

    prime1 = choice(primeslist)
    prime2 = choice(primeslist)
    while prime2 == prime1:
        choice(primeslist)
 
    n = prime1 * prime2
    phi = (prime1 - 1) * (prime2 - 1)
 
    public_key = 2
    while True:
        if gcd(public_key, phi) == 1:
            break
        public_key += 1
 
    # d = (k*Φ(n) + 1) / e for some integer k
 
    private_key = 2
    while True:
        if (private_key * public_key) % phi == 1:
            break
        private_key += 1

    salt = token_hex(saltlength)

    return private_key, public_key, n, salt

class RSA:
    def decrypt(keys:[int, int], encrypted_number:int|float):
        """Decrypts an encrypted integer/float using a private key and additional number."""

        decrypted = 1
        while keys[0] > 0:
            decrypted *= encrypted_number
            decrypted %= keys[1]
            keys[0] -= 1
        return decrypted
    
    def decoder(keys:[int, int], encoded_text:list):
        """Decodes a list of encrypted ascii numbers of letters using a private key and an additional number."""

        s = ''
        # Calling the decrypting function decoding function
        for num in encoded_text:
            s += chr(RSA.decrypt([keys[0], keys[1]], num))
        return s

    def encrypt(keys:[int, int], message:int|float) -> int:
        """Encrypts a number using a public key and an additional number."""

        encrypted_text = 1
        while keys[0] > 0:
            encrypted_text *= message
            encrypted_text %= keys[1]
            keys[0] -= 1
        return encrypted_text

    def encoder(keys:[int, int], message: str) -> list:
        """Encodes a string into a list of encrypted ascii numbers using a public key and an additional number."""
        encoded = []
        # Calling the encrypting function in encoding function
        for letter in message:
            encoded.append(RSA.encrypt([keys[0], keys[1]], ord(letter)))
        return encoded

class Accounts:

    def create_account(User:str, Pass:str, remembered:bool):
        """Adds a new account to userpass.json."""

        global userpass, userpasslock
        global userdata, userdatalock
        global Threadlocalvars

        userpasslock.acquire()
        try: 
            userpass[User]
            userpasslock.release()
            return False
        except KeyError:
            Accounts.__savepass(User, Pass)
            Threadlocalvars.Username = User
            userdatalock.acquire()
            userdata[User] = {}
            [userdata[User].update({i:{}}) for i in datatypes]
            dump(userdata, open('userdata.json', "w"))
            userdatalock.release()
            if remembered == True:
                reencpass = RSA.encoder(userpass[User][1:3:1], Pass)
                userpasslock.release()
                return reencpass
            userpasslock.release()
            return True

    def request_key(User:str) -> [int, int]:
        """Function to request a public key and additional number."""

        global userpass
        try: return userpass[User][1:3:1]
        except KeyError: return KeyError

    def login(User:str, encpass:list, remembered:bool=False) -> bool:
        """Attempts a login."""
        
        global userpass, userpasslock
        global Threadlocalvars
        userpasslock.acquire()
        try:
            if sha256((userpass[User][3] + f"{encpass}".translate(listpunc)).encode('UTF-8')).hexdigest() == userpass[User][4]:
                Pass = RSA.decoder(userpass[User][0:3:2], encpass)
                Accounts.__savepass(User, Pass)
                Threadlocalvars.Username = User
                if remembered == True:
                    reencpass = RSA.encoder(userpass[User][1:3:1], Pass)
                    userpasslock.release()
                    return reencpass
                else: 
                    userpasslock.release()
                    return True
            else: 
                userpasslock.release()
                return False
        except: 
            userpasslock.release()
            return False
    
    def __savepass(User:str, Pass:list):
        encvars = list(regenerate_encvars())
        encpass = sha256((encvars[3] + f"{RSA.encoder(encvars[1:3:1], Pass)}".translate(listpunc)).encode('UTF-8')).hexdigest()
        userpass[User] = encvars+[encpass]
        with open('userpass.json', "w") as file:
            dump(userpass, file)

class Data:
    def save(newdata, datatype):
        global userdata, userdatalock
        userdatalock.acquire()
        try: userdata[Threadlocalvars.Username][datatype] = newdata
        except: 
            userdatalock.release()
            return
        with open('userdata.json', "w") as file:
            dump(userdata, file)
        userdatalock.release()

    def request(datatype):
        try: return userdata[Threadlocalvars.Username][datatype]
        except: return False

def Main():
    global s
    s.bind((HOST, PORT))
    s.listen()
    print(f"Listening on ip: {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        print(f"Connected by {addr}. There are currently {active_count()} connection(s).")
        Thread(target=receive_messages, args=(conn,), daemon=True).start()
        
    

def receive_messages(conn:socket):
    while True:
        try:
            data = conn.recv(1024).decode('UTF-8')
        except Exception as e:
            if str(e) == "[WinError 10054] An existing connection was forcibly closed by the remote host":
                conn.close()
                break
        if data:
            print(data)
            datal = data.split("\n")
            if len(datal)>1:
                result = eval(datal[1])
            match datal[0]:
                case "func->Any":
                    conn.sendall((str(result)).encode("UTF-8"))
                case "func->None":
                    pass
                case "close":
                    conn.close()
                    break

if __name__ == "__main__":
    Main()