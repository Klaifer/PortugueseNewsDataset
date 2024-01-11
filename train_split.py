# Split an input file in train and test

import argparse
import logging
import json
from sklearn.model_selection import train_test_split

logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S %p',
                    level=logging.INFO)


def splitids(data, tsize=0.1, seed=None):
    category = [d['category'] for d in data]
    X_train, Xtest = train_test_split(data, test_size=tsize, random_state=seed, stratify=category)
    trainid = [int(d['pageid']) for d in X_train]
    dataid = [int(d['pageid']) for d in data]
    parts = [(d, 'train' if d in trainid else 'test') for d in dataid]
    return parts


def applysplit(data, spltfile, trainfile, testfile):
    with open(spltfile, "r") as f:
        parts = {}
        for d in f:
            did, part = d.split()
            parts[int(did)] = part

    categories = {d['category'] for d in data}
    categories = sorted(categories)

    train = []
    test = []
    for d in data:
        pname = int(d['pageid'])

        sample = {
            'pageid': pname,
            'text': ". ".join([d[k] for k in ['title', 'body']]),
            'label': categories.index(d['category'])
        }

        if parts[pname] == 'train':
            train.append(sample)
        elif parts[pname] == 'test':
            test.append(sample)
        else:
            raise ValueError()

    logging.info("train: {}, test: {}".format(*[len(s) for s in (train, test)]))

    with open(trainfile, 'w') as trfile, open(testfile, 'w') as tefile:
        json.dump({
            'part': 'train',
            'data': train,
            'labels': categories
        }, trfile, indent=4)

        json.dump({
            'part': 'test',
            'data': test,
            'labels': categories
        }, tefile, indent=4)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str,
                        default='content/json/wikinoticias_categories.json',
                        help='Wikipedia json content with categories')

    parser.add_argument('--splitfile', type=str,
                        default='content/json/split_ids.csv',
                        help='Split ids file name (output on "id" operation or input on "content" operation)')

    parser.add_argument('--operation',
                        choices=['generate', 'apply'],
                        default='apply',
                        help='Split ids on train, test and val, or use split ids to generate files')

    parser.add_argument('--train', type=str,
                        default='content/json/wikinoticias_train.json',
                        help='Output trainning data file')

    parser.add_argument('--test', type=str,
                        default='content/json/wikinoticias_test.json',
                        help='Output test test file')

    parser.add_argument('--seed', type=int,
                        default=0,
                        help='Used to initialize the random number generator')

    args = parser.parse_args()
    logging.info(args)

    with open(args.input, "r") as fullinput:
        full = json.load(fullinput)

    if args.operation == 'generate':
        splited = splitids(full, seed=args.seed)
        with open(args.splitfile, "w") as splitfile:
            for pgid, partname in splited:
                splitfile.write("{} {}\n".format(pgid, partname))

    else:  # apply
        applysplit(full, args.splitfile, args.train, args.test)
