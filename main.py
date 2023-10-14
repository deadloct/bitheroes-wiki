import argparse
import csv
import json
from jinja2 import Environment, FileSystemLoader
from models import familiar 

class Commands:
    CMD_FAMILIARS = 'familiars'
    CMD_OUTPUT_JSON = 'json'

def cmd_familiars(args):
    print('Processing CSV file {}'.format(args.tsv))
    with open(args.tsv, mode='r', newline='', encoding='utf-8') as csv_file, open(args.out, mode='w', encoding='utf-8') as wiki_file:
        csv_reader = csv.DictReader(csv_file, dialect="excel-tab")

        environment = Environment(loader=FileSystemLoader('templates/'))
        template = environment.get_template('familiars.j2')
        
        familiars = []
        for row in csv_reader:
            familiars.append(familiar.Familiar(row))
        
        content = template.render(familiars=familiars, rarity=args.rarity.capitalize())
        wiki_file.write(content)

    print('Finished writing wikitext to {}'.format(args.out))

def cmd_json(args):
    print("Converting familiar tsv to json")
    with open(args.tsv, mode='r', newline='', encoding='utf-8') as csv_file, open(args.out, mode='w', encoding='utf-8') as json_file:
        csv_reader = csv.DictReader(csv_file, dialect="excel-tab") 
        arr = []
        for row in csv_reader:
            arr.append(familiar.Familiar(row).toJSON())
        json_file.write('[{}]'.format(",".join(arr)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='convert csv file to wikitext for the Bit Heroes wiki')
    subparsers = parser.add_subparsers(dest='subcommand')
    
    parser_familiars = subparsers.add_parser(Commands.CMD_FAMILIARS, help='convert fam csv file into a wiki familiar table')
    parser_familiars.add_argument('-t', '--tsv', required=True, help='input tsv file')
    parser_familiars.add_argument('-o', '--out', required=True, help='wikitext output file')
    parser_familiars.add_argument('-r', '--rarity', required=True, help='one of these: common|rare|epic|legendary|mythic')

    output_json = subparsers.add_parser(Commands.CMD_OUTPUT_JSON, help='convert a tsv file to json')
    output_json.add_argument('-t', '--tsv', required=True, help='input tsv file')
    output_json.add_argument('-o', '--out', required=True, help='wikitext output file')

    args = parser.parse_args()

    match args.subcommand:
        case Commands.CMD_FAMILIARS:
            cmd_familiars(args) 

        case Commands.CMD_OUTPUT_JSON:
            cmd_json(args)

        case _:
            print("At least one subcommand is required. Usage info:\n")
            parser.print_help()
