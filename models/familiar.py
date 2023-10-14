import json
import re

ZONE_NAMES = [
    "Bit Valley",
    "Wintermarsh",
    "Lakehaven",
    "Ashvale",
    "Aramore",
    "Morgoroth",
    "Cambora",
    "Galaran",
    "Eshlyn",
    "Uamor",
    "Melvin's Genesis",
    "Zord Attacks!",
    "Ancient Odyssey",
    "Southpeak",
    "Fenrir's Omen",
    "Steamfunk City",
    "Olympian Secret Party",
    "Sruxon Attack!",
    "Galactic Trials",
    "Big Claw"
]

class Familiar:
    def __init__(self, csv_row):
        self.name = csv_row['Name']
        self.rarity = csv_row['Rarity'].capitalize()
        self.zone = csv_row['Zone']
        self.flavor = csv_row['Flavor Text']
        self.bonuses = csv_row['Bonuses'].splitlines()
        self.power, self.stamina, self.agility = [stat + '%' for stat in csv_row['Stat Spread'].split(" / ")]
        self.dungeons = self._get_dungeon_links(self.zone, csv_row['Dungeon'])
        self.skill_names, self.skill_descs, self.skill_ranges = self._get_skills(csv_row['Skills'])

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        
    def _get_skills(self, skills_csv):
        skills = skills_csv.splitlines()
        skill_names = []
        skill_descs = []
        for skill in skills:
            skill_name, skill_desc = skill.split(": ", 1)
            skill_names.append(skill_name)
            skill_descs.append(skill_desc)
        skill_ranges = ["TBC"] * len(skills) # TBC is temporary until we have values
        return skill_names, skill_descs, skill_ranges

    def _get_dungeon_links(self, zone, dungeon_csv):
        dungeon_strings = []
        for dungeon in dungeon_csv.split(", "):
            dungeon_strings.append("{}{}".format(zone, dungeon))

        dungeon_links = []
        for dungeon in dungeon_strings:
            pattern = r'Z(\d+)D\d+'
            match = re.search(pattern, dungeon)
            if match:
                zone_num = int(match.group(1))
                dungeon_links.append(
                    "[[Zones/{}|{}]]".format(ZONE_NAMES[zone_num-1], dungeon)
                )
            else:
                dungeon_links.append(dungeon)

        return dungeon_links