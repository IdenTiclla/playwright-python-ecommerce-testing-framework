from faker import Faker

def generate_random_email():
    faker = Faker() 
    return faker.email()

def generate_random_password():
    faker = Faker()
    return faker.password()