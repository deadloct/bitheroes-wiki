import csv
import argparse
from jinja2 import Environment, FileSystemLoader
from models import familiar 

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a very specifically formatted CSV file to the BH wiki fam format")
    parser.add_argument("input_file", help="input file")
    parser.add_argument("output_file", help="wikitext output file")
    parser.add_argument("rarity", help="One of these: Common|Rare|Epic|Legendary|Mythic")
    args = parser.parse_args()

    with open(args.input_file, mode='r', newline='', encoding='utf-8') as csv_file, open(args.output_file, mode='w', encoding='utf-8') as wiki_file:
        csv_reader = csv.DictReader(csv_file)

        environment = Environment(loader=FileSystemLoader("templates/"))
        template = environment.get_template("familiars.j2")
        
        familiars = []
        for row in csv_reader:
            familiars.append(familiar.Familiar(row))
        
        content = template.render(familiars=familiars, rarity=args.rarity)
        wiki_file.write(content)

    print("Finished writing wikitext to {}".format(args.output_file))
