import json
from mob import Mob
from radar import Radar

class Cacher:  
    
    def save_data_to_file(self, instance1 :Mob, instance2 :Radar, skills: str, filename="cached_data.txt"):
    # Create a dictionary to store the instances
        data = {
            "Mob": instance1.__dict__,
            "Radar": instance2.__dict__,
            "skills": skills
        }

    # Save the dictionary to a file in JSON format
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
            
            

    def load_data_from_file(self, filename="cached_data.txt"):
        # Read the data from the file
        with open(filename, "r") as file:
            data = json.load(file)

        # Recreate the dataclass instances from the dictionary
        instance1 = Mob(**data["Mob"])
        instance2 = Radar(**data["Radar"])
        skills = data["skills"]

        return instance1, instance2, skills