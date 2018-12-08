Semver Test

```pip install -r requirements.txt```

To run the test txt I placed, run:
```py.test semver-test.py```

To run your own problem set:

Save the problem set in a txt file, line by line (test.txt)

Save the expected results line by line in a separate txt file (expected.txt)

Create a blank txt file for the actual results (actual.txt)

Run: 
```python3 -i semver.py```
```python

>>> v = Version('test.txt', 'actual.txt', 'expected.txt')

>>> v.assertEqual()
```

Will print out whether each one matches