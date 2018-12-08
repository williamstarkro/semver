from pathlib import Path
from semver import Version


def test():
    """Global test on all types
    """

    v = Version('test.txt', 'actual.txt', 'expected.txt')

    expectedFile = Path(v.expectedFile)
    if expectedFile.is_file():
        with open(v.expectedFile, "r") as ins:
            x = 0
            for line in ins:
                assert line.split()[0] == v.solutionList[x]
                x += 1

