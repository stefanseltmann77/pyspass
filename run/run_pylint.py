"""Script runner for pylint check

The MODULE_PATH has to be adjusted according to your project!
"""
from pylint import epylint as lint

MODULE_PATH: str = "YOUR_PATH_TO_THE_MODULE_OR_FILE"
(pylint_stdout, pylint_stderr) = lint.py_run(f'{MODULE_PATH} --rcfile={MODULE_PATH}/conf/pylintrc.cfg ',
                                             return_std=True)
linting = pylint_stdout.read()
linting_rows = linting.split("\n")
for row in linting_rows:
    print(row)
