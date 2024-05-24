from cryptography.fernet import Fernet
from dotenv import set_key

# Gerando uma chave de criptografia
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Dados a serem criptografados
user = 'postgres'
password = 'root'
host = '127.0.0.1'
port = '5432'
database = 'hospital'

# Criptografando os dados
encrypted_user = cipher_suite.encrypt(user.encode()).decode()
encrypted_password = cipher_suite.encrypt(password.encode()).decode()
encrypted_host = cipher_suite.encrypt(host.encode()).decode()
encrypted_port = cipher_suite.encrypt(port.encode()).decode()
encrypted_database = cipher_suite.encrypt(database.encode()).decode()

# Escrevendo os dados criptografados no arquivo .env
set_key(".env", "KEY", key.decode())
set_key(".env", "USER", f"b'{encrypted_user}'")
set_key(".env", "PASSWORD", f"b'{encrypted_password}'")
set_key(".env", "HOST", f"b'{encrypted_host}'")
set_key(".env", "PORT", f"b'{encrypted_port}'")
set_key(".env", "DATABASE", f"b'{encrypted_database}'")
