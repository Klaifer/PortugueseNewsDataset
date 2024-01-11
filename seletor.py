# Filter news from a set of specific categories

import argparse
import logging
import json

logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S %p',
                    level=logging.INFO)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str,
                        default='content/json/wikinoticias_full.json',
                        help='Wikipedia json content')

    parser.add_argument('--output', type=str,
                        default='content/json/wikinoticias_categories.json',
                        help='Selected content')

    parser.add_argument('--categories', nargs='+',
                        default=['Desporto', 'Crime, Direito e Justiça', 'Saúde', 'Economia e negócios', 'Política'],
                        help='Selected categories')

    args = parser.parse_args()
    logging.info(args)

    with open(args.input, "r") as f:
        data = json.load(f)

    content = []
    for d in data:
        matches = 0
        for c in args.categories:
            if c in d['categories']:
                matches += 1
                catfound = c

        if matches == 1:
            d['category'] = catfound
            del(d['categories'])
            content.append(d)

    with open(args.output, 'w') as f:
        json.dump(content, f, indent=4)

    logging.info("Filtered {} articles".format(len(content)))
