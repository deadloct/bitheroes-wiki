import csv
import argparse
import re

parser = argparse.ArgumentParser(description="Convert a very specifically formatted CSV file to the BH wiki fam format")
parser.add_argument("input_file", help="input file")
parser.add_argument("output_file", help="wikitext output file")
parser.add_argument("rarity", help="One of these: Common|Rare|Epic|Legendary|Mythic")
args = parser.parse_args()

zone_names = [
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

# TODO: Replace all of this wikitext code with templates
row_divider = "\n|-\n"

def get_fam_header(name, rarity, flavor):
    fam_header = '''
|- id="{}"
| rowspan="3" |{{{{Icon{}}}}}<br>{{{{Missing}}}}
<!--| rowspan="3" |{{{{Icon{}}}}}<br>[[File:Familiar_{}.png|{}]]-->'''
    return fam_header.format(name, rarity, rarity, name, flavor)

def get_pow_row(name, power, skill_names):
    tmpl = "|'''{}'''\n|{{{{Power}}}}\n|'''{}'''".format(name, power)
    for skill_name in skill_names:
        tmpl = "{}\n|'''{}'''".format(tmpl, skill_name)
    return tmpl

def get_stam_row(bonuses, stamina, skill_descs):
    tmpl = "|{}\n|{{{{Stamina}}}}\n|'''{}'''".format(", ".join(bonuses), stamina)
    for skill_desc in skill_descs:
        tmpl = "{}\n|{}".format(tmpl, skill_desc)
    return tmpl

def get_agi_row(dungeons, agility, skill_ranges):
    links = []
    for dungeon in dungeons:
        pattern = r'Z(\d+)D\d+'
        match = re.search(pattern, dungeon)
        zone_num = int(match.group(1))
        if match:
            links.append("[[Zones/{}|{}]]".format(zone_names[zone_num-1], dungeon))

    tmpl = "|{}\n|{{{{Agility}}}}\n|'''{}'''".format(", ".join(links), agility)
    for skill_range in skill_ranges:
        tmpl = "{}\n|{}".format(tmpl, skill_range)
    return tmpl

def get_fam_table(csv_row):
    name = row['Name']
    rarity = row['Rarity'].capitalize()
    zone = row['Zone']
    flavor = row['Flavor Text']

    dungeons = ["{}{}".format(zone, dungeon) for dungeon in row['Dungeon'].split(", ")]
    power, stamina, agility = [stat + '%' for stat in row['Stat Spread'].split(" / ")]

    bonuses = row['Bonuses'].splitlines()

    skills = row['Skills'].splitlines()
    skill_names = []
    skill_descs = []
    skill_ranges = ["''TBC''" for skill in skills] # Placeholder skill power ranges
    for skill in skills:
        skill_name, skill_desc = skill.split(": ", 1)
        skill_names.append(skill_name)
        skill_descs.append(skill_desc)

    wiki_parts = [
        "\n".join([get_fam_header(name, rarity, flavor), get_pow_row(name, power, skill_names)]),
        get_stam_row(bonuses, stamina, skill_descs),
        get_agi_row(dungeons, agility, skill_ranges),
    ]
    return row_divider.join(wiki_parts)

if __name__ == "__main__":
    with open(args.input_file, mode='r', newline='', encoding='utf-8') as csv_file, open(args.output_file, mode='w', encoding='utf-8') as wiki_file:

        csv_reader = csv.DictReader(csv_file)
        
        wiki_file.write("<!-- START AUTO-GENERATED FROM CSV -->\n")
        wiki_file.write("""{| class="mw-collapsible bittable grey3" data-expandtext="Show" data-collapsetext="Hide"\n""")

        for row in csv_reader:
            wiki_file.write("{}\n".format(get_fam_table(row)))

        wiki_file.write("|}\n")
        wiki_file.write("<!-- END AUTO-GENERATED FROM CSV -->\n")

    print(f"Conversion completed. Data has been saved to {args.output_file}")
