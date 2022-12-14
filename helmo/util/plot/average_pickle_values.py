import argparse
import pickle

import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument(
    'files',
    help="A list of pickle files from which lines are loaded. "
         "All files have to contain similar amounts of objects "
         "which have to have similar shapes.",
    nargs='+',
    type=argparse.FileType('rb'),
    default=None
)
parser.add_argument(
    '--stddev',
    help="Path to file where stddev corrected estimation will be placed. "
         "By default standard deviation is put into stddev.pickle",
    default="stddev.pickle"
)
parser.add_argument(
    '--stderr_of_mean',
    help="Path to file where standard error of mean will be placed. "
         "By default standard error of mean is put into stderr_of_mean.pickle",
    default="stderr_of_mean.pickle"
)
parser.add_argument(
    '--mean',
    help="Path to file where mean line will be placed. "
         "By default it is put into mean.pickle",
    default="mean.pickle"
)
parser.add_argument(
    '--preprocess',
    help="Function applied to values before averaging. Possible "
         "options: (1)sqrt. Default is None",
    default=None,
)

args = parser.parse_args()


def load_pickle_file(file):
    l = []
    while True:
        try:
            l.append(pickle.load(file))
        except EOFError:
            break
    return l


for_averaging = []
for file in args.files:
    for_averaging.append(np.stack(load_pickle_file(file)))
    file.close()

for_averaging = np.stack(for_averaging)

if args.preprocess == 'sqrt':
    f = np.sqrt
else:
    f = lambda x: x

for_averaging = f(for_averaging)

N = for_averaging.shape[0]
m = np.mean(for_averaging, axis=0, keepdims=False)
s = np.std(for_averaging, axis=0, keepdims=False, ddof=1)
sm = s / N**0.5

with open(args.mean, 'wb') as f:
    pickle.dump(m, f)

with open(args.stddev, 'wb') as f:
    pickle.dump(s, f)

with open(args.stderr_of_mean, 'wb') as f:
    pickle.dump(sm, f)
