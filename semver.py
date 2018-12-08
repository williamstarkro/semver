from pathlib import Path
import sys
import re
from itertools import zip_longest as izip_longest

# Use regex to compare and separate a full version string into pieces
_re = re.compile('^'
                 '(\d+)\.(\d+)\.(\d+)'  # minor, major, patch
                 '(-[0-9A-Za-z-\.]+)?'  # pre-release
                 '(\+[0-9A-Za-z-\.]+)?'  # build
                 '$')


# Basic func to convert str to int
def _try_int(s):
    assert type(s) is str
    try:
        return int(s)
    except ValueError:
        return s

# Func to split the first 3 sections (major, minor, patch) into array
def _make_group(g):
    return [] if g is None else list(map(_try_int, g[1:].split('.')))

# return mmp (major, minor, patch) from version
def mmp(d):
    return [d['major'], d['minor'], d['patch']]

'''
Compare two pre-release values and return True if first is less than second
Basically just iterates through both strings until a difference is caught
Rules for pre-release:
    - Char > Num
    - ASCII Char rules for comparing Char to Char
    - Basic Num > Num rules
'''
def seq(first, second):
    # izip lets us use a for over the longest string
    # important so we can compare None to a val (val > None)
    for s, o in izip_longest(first, second):
        assert not (s is None and o is None)
        if s is None or o is None:
            return bool(s is None)
        if type(s) is int and type(o) is int:
            if s < o:
                return True
        elif type(s) is int or type(o) is int:
            return type(s) is int
        elif s != o:
            return s < o

class Version:
    # Create a txt file with a list line-separated comparison versions
    # This will be the problem file, which you will unput into the init as 'problemFileName.txt'
    # The actualFile var is where you want the end outputs of the program to be saved in
    # The expectedFile is the txt file that has the expected list of outputs
    def __init__(self, _problemFile, _actualFile, _expectedFile):
        self.problemFile = _problemFile
        self.actualFile = _actualFile
        self.expectedFile = _expectedFile
        self.versionComparison = []
        self.solutionList = []
        self.verList = []
        self.count = -1
        problemFile = Path(_problemFile)
        if problemFile.is_file():
            self._problemSnapshot()
        with open(self.actualFile, 'w') as f:
            for x in range(0,len( self.solutionList)):
                f.write("%s" % self.solutionList[x])
                if x < len(self.solutionList)-1:
                    f.write("\n")

    # Separate and and do sanity checks on base invalid cases
    def _problemSnapshot(self):
        with open(self.problemFile, "r") as ins:
            for line in ins:
                versionList = line.split()
                self.versionComparison.append(versionList)
                if len(versionList) != 2:
                    self.solutionList.append("invalid")
                    continue
                else:
                    matchList = []
                    for version in versionList:
                        match = _re.match(version)
                        if not match:
                            self.solutionList.append("invalid")
                            break
                        matchList.append(match)
                    if len(matchList) == 2:
                        for match in matchList:
                            _major, _minor, _patch = map(int, match.groups()[:3])
                            _pre_release = _make_group(match.group(4))
                            _build = _make_group(match.group(5))
                            d = {'major': _major, 'minor': _minor, 'patch': _patch, 'pre_release': _pre_release, 'build': _build}
                            self.verList.append(d.copy())
                            self.count += 1
                        self.solutionList.append(self._compare())

    # Comparison following rules of semver.org
    def _compare(self):
        first = self.verList[self.count-1]
        second = self.verList[self.count]
        if mmp(first) == mmp(second):
            if first['pre_release'] and not second['pre_release']:
                return "before"
            elif not first['pre_release'] and second['pre_release']:
                return "after"
            if first['pre_release'] == second['pre_release']:
                return "equal"
            elif first['pre_release'] and second['pre_release']:
                val = seq(first['pre_release'], second['pre_release'])
                if val:
                    return "before"
                else:
                    return "after"
        elif mmp(first) > mmp(second):
            return "after"
        elif mmp(first) < mmp(second):
            return "before"

    # True/False assertion on how accurate the actual results are compared to expected
    def assertEqual(self):
        expectedFile = Path(self.expectedFile)
        if expectedFile.is_file():
            with open(self.expectedFile, "r") as ins:
                x = 0
                for line in ins: 
                    l = ' '.join((self.versionComparison[x]))
                    if line.split()[0] == self.solutionList[x]:
                        print('%s: `%s` actual is correct.' % (l, self.solutionList[x]))
                    else:
                        print('%s: `%s` actual is incorrect.' % (l, self.solutionList[x]))
                    x += 1