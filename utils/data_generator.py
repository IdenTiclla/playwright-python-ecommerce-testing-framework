from faker import Faker

def generate_random_email():
    """Genera un email aleatorio"""
    faker = Faker() 
    return faker.email()

def generate_random_password():
    """Genera una contraseña aleatoria"""
    faker = Faker()
    return faker.password()

def generate_random_first_name():
    """Genera un nombre aleatorio"""
    faker = Faker()
    return faker.first_name()

def generate_random_last_name():
    """Genera un apellido aleatorio"""
    faker = Faker()
    return faker.last_name()

def generate_random_phone_number():
    """Genera un número de teléfono aleatorio"""
    faker = Faker()
    return faker.phone_number()