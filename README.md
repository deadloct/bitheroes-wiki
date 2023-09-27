# Bit Heroes CSV to Wikitext Generator

Usage:

> Convert a very specifically formatted CSV file to the BH wiki familiar format. Will hopefully get more generic in the future if we find other uses for this script.
>
> positional arguments:
>
> * input_file: input file
> * output_file: wikitext output file
> * rarity: One of these: Common|Rare|Epic|Legendary|Mythic
>
> options:
> -h, --help: show this help message and exit

For example:

```bash
$ python3 main.py samples/epic.csv samples/epic.wiki Epic
Finished writing wikitext to samples/epic.wiki
```
