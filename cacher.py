import json
from mob import Mob
from radar import Radar
from skils_area import Skills_Area

class Cacher:  
    
    def save_data_to_file(self, instance1 :Mob, instance2 :Radar, skills: str, instance3 : Skills_Area, filename="cached_data.txt"):
    # Create a dictionary to store the instances
        data = {
            "Mob": instance1.__dict__,
            "Radar": instance2.__dict__,
            "skills": skills,
            "Skills_area" : instance3.__dict__,
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
        skills_area = Skills_Area(**data["Skills_area"])

        return instance1, instance2, skills, skills_area