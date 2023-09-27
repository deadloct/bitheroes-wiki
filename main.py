import csv
import argparse
from jinja2 import Environment, FileSystemLoader
from models import familiar 

class Commands:
    CMD_FAMILIARS = 'familiars'

def cmd_familiars(args):
    print('Processing CSV file {}'.format(args.csv))
    with open(args.csv, mode='r', newline='', encoding='utf-8') as csv_file, open(args.out, mode='w', encoding='utf-8') as wiki_file:
        csv_reader = csv.DictReader(csv_file)

        environment = Environment(loader=FileSystemLoader('templates/'))
        template = environment.get_template('familiars.j2')
        
        familiars = []
        for row in csv_reader:
            familiars.append(familiar.Familiar(row))
        
        content = template.render(familiars=familiars, rarity=args.rarity.capitalize())
        wiki_file.write(content)

    print('Finished writing wikitext to {}'.format(args.out))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='convert csv file to wikitext for the Bit Heroes wiki')
    subparsers = parser.add_subparsers(dest='subcommand')
    
    parser_familiars = subparsers.add_parser(Commands.CMD_FAMILIARS, help='convert fam csv file into a wiki familiar table')
    parser_familiars.add_argument('-c', '--csv', required=True, help='input csv file')
    parser_familiars.add_argument('-o', '--out', required=True, help='wikitext output file')
    parser_familiars.add_argument('-r', '--rarity', required=True, help='one of these: common|rare|epic|legendary|mythic')

    args = parser.parse_args()

    match args.subcommand:
        case Commands.CMD_FAMILIARS:
            cmd_familiars(args) 

        case _:
            print("At least one subcommand is required. Usage info:\n")
            parser.print_help()
