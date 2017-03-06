### Example usage:
```bash
./run.py examples/actest.out
```

This command will run the tests stored in `in/` folder, pass them through actest.out program, and store results in prog_out/ directory. Then it will compare them to expected output stored in out/ directory, and will evaluate it.
Note that any differences in whitespace are neglected.
You may specify a different time limit (default is 2.0 seconds) by writing a number before program:
```bash
./run.py 3.5 examples/actest.out
```
will make it run for 3.5s at most.


### Example output:
```
Testing test1.in:
Time: 0.00s
Memory: 1352kB
Correct

Testing test2.in:
Time: 0.00s
Memory: 1452kB
Correct

Statistics:
========================
2 x Correct
0 x Wrong Answer
0 x Time Limit Exceeded
========================
```
### Settings
Depending on your naming convention you might want to change in run.py:
* UNIQUE_ID_PATTERN - it is assumed that input and ouput files will have a format of PREFIX +  UNIQUE_ID_PATTERN + SUFFIX  
Should you ever want input files and output files to use different regex pattern (or multiple patterns), take a look at `get_file_with_output_name` function.
* IN_FILE_PATTERN - your input files naming convention
* OUT_FILE_PATTERN - your files with expected output naming convention
* in_dir - directory where your input test files are located
* expected_out_dir - directory where your files with expected output of the program are located

Let's say your project directory looks like this:
```bash
├── A
│   ├── A.cbp
│   ├── A.depend
│   ├── A.layout
│   ├── A.out
│   ├── test_input
│   │   ├── in1.txt
│   │   ├── in2.txt
│   │   └── in3.txt
│   ├── main.cpp
│   └── test_output
│       ├── expected1.txt
│       ├── expected2.txt
│       └── expected3.txt
```
Change:
* UNIQUE_ID_PATTERN="(\d+?)" - leave this the same
* IN_FILE_PATTERN=re.compile("in" + UNIQUE_ID_PATTERN +".txt")
* OUT_FILE_PATTERN=re.compile("expected" + UNIQUE_ID_PATTERN + ".txt")
* in_dir=os.path.join(CURRENT_WORKING_DIRECTORY,"test_input/")
* expected_out_dir=os.path.join(CURRENT_WORKING_DIRECTORY,"test_output/")

Had `in*.txt` and `expected*.txt` files been in `A` directory (instead of `test_input` and `test_output` respectively), you would have needed to change:
* in_dir=CURRENT_WORKING_DIRECTORY
* expected_out_dir=CURRENT_WORKING_DIRECTORY

Now you can check correctness of your program by running:
```bash
cd A
~/bin/checker/run.py A.out #assuming you have the checker source code downloaded to ~/bin/checker
```

Also consider making `run.py`  system-wide available for example by:
```bash
sudo ln -s ~/bin/checker/run.py /usr/local/bin/checker
```

And use the checker like this:
```bash
cd A
checker A.out
```