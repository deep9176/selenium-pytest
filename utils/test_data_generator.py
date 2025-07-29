import random
import string
import time
import datetime
import json
import os
from faker import Faker
import gender_guesser.detector as gender

class UserDataGenerator:
    def __init__(self, data_file="testdata/login_data.json"):
        self.fake = Faker()
        self.gender_detector = gender.Detector()
        
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.data_file = os.path.join(project_root, data_file)
        self.user_data = {}
    
    def generate_name(self):
        first_name = self.fake.first_name()
        last_name = self.fake.last_name()
        full_name = f"{first_name} {last_name}"
        return first_name, last_name, full_name

    def generate_email(self, first_name, last_name):
        timestamp = int(time.time())
        email = f"{first_name.lower()}.{last_name.lower()}{timestamp}@example.com"
        return email

    def generate_random_password(self, length=12):
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        special_characters = string.punctuation
        
        password = [
            random.choice(lowercase),
            random.choice(uppercase),
            random.choice(digits),
            random.choice(special_characters)
        ]
        
        all_characters = lowercase + uppercase + digits + special_characters
        password += random.choices(all_characters, k=length-4)
        
        random.shuffle(password)
        return ''.join(password)

    def generate_gender(self, first_name):
        gender_guess = self.gender_detector.get_gender(first_name)

        if gender_guess == "male":
            return "Male"
        elif gender_guess == "female":
            return "Female"
        elif gender_guess == "unknown":
            return random.choice(["Male", "Female"])
        else:
            return random.choice(["Male", "Female"])

    def generate_dob(self, min_age=18, max_age=90):
        current_date = datetime.datetime.now()
        current_year = current_date.year

        min_year = current_year - max_age
        max_year = current_year - min_age

        year = random.randint(min_year, max_year)

        month = random.randint(1, 12)

        if month in [1, 3, 5, 7, 8, 10, 12]:
            day = random.randint(1, 31)
        elif month in [4, 6, 9, 11]:
            day = random.randint(1, 30)
        else:
            day = random.randint(1, 28)
        
        return day, month, year

    def generate_address(self):
        address1 = self.fake.address().splitlines()[0]
        address2 = self.fake.address().splitlines()[1] if random.choice([True, False]) else ""
        company = self.fake.company()
        country = self.fake.country()
        state = self.fake.state()
        city = self.fake.city()
        zipcode = self.fake.zipcode()
        phone_number = self.fake.phone_number()
        
        return address1, address2, company, country, state, city, zipcode, phone_number

    def generate_user_data(self):
        first_name, last_name, full_name = self.generate_name()
        email = self.generate_email(first_name, last_name)
        password = self.generate_random_password()
        gender = self.generate_gender(first_name)
        day, month, year = self.generate_dob()
        address1, address2, company, country, state, city, zipcode, mobile_number = self.generate_address()

        self.user_data = {
            "first_name": first_name,
            "last_name": last_name,
            "full_name": full_name,
            "email": email,
            "password": password,
            "gender": gender,
            "dob_day": day,
            "dob_month": month,
            "dob_year": year,
            "company": company,
            "address1": address1,
            "address2": address2,
            "country": country,
            "state": state,
            "city": city,
            "zipcode": zipcode,
            "mobile_number": mobile_number
        }

    def save_user_data_with_id(self):
        user_id = f"user_{int(time.time())}"

        try:
            with open(self.data_file, 'r') as file:
                all_user_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            all_user_data = {}

        all_user_data[user_id] = self.user_data

        with open(self.data_file, 'w') as file:
            json.dump(all_user_data, file, indent=4)

        print(f"User data saved with ID: {user_id} to {self.data_file}")
        return user_id

    def get_user_data_by_id(self, user_id):
        try:
            with open(self.data_file, 'r') as file:
                all_user_data = json.load(file)

            return all_user_data.get(user_id, None)

        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Error: Could not find data file '{self.data_file}'.")
            return None
        
    def delete_user_by_email(self, email):
        try:
            with open(self.data_file, 'r') as file:
                all_user_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Error: Data file {self.data_file} not found or invalid.")
            return False

        user_id_to_delete = None
        for user_id, user_data in all_user_data.items():
            if user_data.get("email") == email:
                user_id_to_delete = user_id
                break

        if user_id_to_delete:
            del all_user_data[user_id_to_delete]
            with open(self.data_file, 'w') as file:
                json.dump(all_user_data, file, indent=4)
            print(f"Deleted user {email} from {self.data_file}")
            return True
        else:
            print(f"User with email {email} not found in data file.")
            return False