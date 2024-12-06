# Overview

`argpi` revolutionizes argument parsing in python by introducing a registration based system. This allows users to implement argument parsing in one line of code. Any type of argument can be defined other than the conventional `--` and `-` prefix type arguments. For example, arguments can be of the type `argument1` or `_argument1` or any keyword you set. There is not restrictions on the short form of the argument. You can have `--argument1` as the long form while `_arg1` as the shorter form. This brings a lot of flexibility and customization to the users.

> ### For full documentation, visit [argpi.hashnode.space](https://argpi.hashnode.space)

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage and Examples](#usage-and-examples)
- [Contributing](#contributing)
- [License](#license)

## Features

* `argpi`'s one line implementation and fault finding system helps users maintain readability and reliability in their code.
* Flexibility and customization while defining arguments.
* Automatic help text generation.
* Prep and Exec based argument parsing helps users to create complex argument structures.

## Installation

```bash
pip install argpi
```

## Usage and Examples

Using `argpi` is pretty simple. `argpi` was made keeping in mind the concepts of Object Oriented Programming and therefore, it is recommended to create a class for your argument preparations and executions separately.

What the above statement means is that suppose you have an argument, say, `--install` which is the base argument for installing something. Now, there are different flag type arguments (meaning, let's say, `--install-with-pip` or `--install-with-conda` or `--install-with-git`, which are used to determine some boolean or case based code execution), or some arguments which take some value (like `--install-path` which takes a path as an argument). These are termed as `prep` arguments while `--install` is the `exec` argument. Before `--install`'s backend code execution, all `prep`s will be performed. Let us see how we can do this in code.

To begin, we need to import `Definition` and `Pathways` classes from `argpi` module.

```python
from argpi import Definition, Pathways
```

All the argument definitions are stored in the `Definition` class. Let us add the definitions from our example above.

```python
def_obj = Definition([
    {
        'name': 'Installation Argument',
        'value': '--install',
        'short': '_i',
        'description': 'Install something\nSyntax: <script_name> --install'
    },
    {
        'name': 'Install with pip',
        'value': '--install-with-pip',
        'short': '_ip',
        'description': 'Install with pip\nSyntax: <script_name> --install-with-pip'
    },
    {
        'name': 'Install with conda',
        'value': '--install-with-conda',
        'short': '_ic',
        'description': 'Install with conda\nSyntax: <script_name> --install-with-conda'
    },
    {
        'name': 'Install path',
        'value': '--install-path',
        'short': '_ip',
        'description': 'Install path\nSyntax: <script_name> --install-path <path>'
    },
])
```

Once we have our definitions ready, we can use the `Pathways` class to auto-capture the arguments and register preps and execs.

Now, for our example, `--install` is the exec argument and the rest are prep arguments. We will create a class for our preparations and executions.

For preparations, we will create a class `Configurations` and for executions, we will create a class `Drivers`.

> **Note:** You can name the classes anything you want. `Configurations` class basically contains information on how a particular method (let's say, for `--install`) will be executed.  
Understand it this way, the method we will define for `--install` can go several ways. The user may want to use `pip` or `conda` or `git` to install something. This is where the `Configurations` class will be used.  
`Configurations` class will have methods and attributes which will store our conditional variables such as which installer to use: `pip`, `conda`, `git` etc and the path to install the software.

```python
from typing import Union

class Configurations:
    def __init__(self) -> None:
        # Define your conditionals or variables here
        self.pip: bool = False
        self.conda: bool = False
        self.git: bool = False
        self.path: Union[str, None] = None
    
    def set_pip(self) -> None:
        self.pip = True
    
    def set_conda(self) -> None:
        self.conda = True
    
    def set_git(self) -> None:
        self.git = True
    
    def set_path(self, path: str) -> None:
        self.path = path
```

```python
class Drivers:
    @staticmethod
    def install(configurations: Configurations) -> None:
        if configurations.pip:
            print(f"Installing with pip to {configurations.path}")
        elif configurations.conda:
            print(f"Installing with conda to {configurations.path}")
        elif configurations.git:
            print(f"Installing with git to {configurations.path}")
        
        # or add your own logic here.
```

Once we have our classes ready, we can use the `Pathways` class to auto-capture the arguments and register preps and execs.

```python
# lets create our configurations object
configurations = Configurations()

pathways = PathWays(definition=def_obj)
# Check docstring for more info on the parameters,
# apart from `definition`, there is one other parameter, `skip` which is set to 1 by default.
# This parameter is used to skip the first `n` arguments from sys.argv.

```

Once we have our `Pathways` object ready, we can register our preps and execs. All arguments except `--install` are prep arguments.

While registering, we can provide a function which will be called if the argument is present. The important point to note here is that the arguments that are passed to your provided functions can either be defined by you or can be captured from the command line. This is what makes `argpi` better than other argument parsing libraries.

The `pathways.register` function has 2 signatures, where the first one is where you give your own function and own arguments. The second one is where you provide your own function but let `argpi` capture the values provided to the argument by the user and pass it to the function.

There are 3 ways you can choose to capture values from the command line:

- `Single`: This is used when you know that the argument will take only one value and whatever it is, you want to pass it to the function.
- `Till Next`: This is used when you know that the argument will take multiple values but you want to stop capturing when the next argument is encountered.
- `Till Last`: This is used when you know that the argument will take multiple values and you know for sure this argument will be the last argument passed by the user.

Do not worry, If you are unsure about `Till Next` and `Till Last`, just use `Till Next` and it will automatically detect if the argument is the last argument or not and act accordingly.

```python

pathways.register(
    argument='--install-with-pip',
    function=configurations.set_pip,
    type='PREP',
    arguments=(True,), # we are passing our own arguments to the function
)

pathways.register(
    argument='--install-with-conda',
    function=configurations.set_conda,
    type='PREP',
    arguments=(True,),
)

pathways.register(
    argument='--install-with-git',
    function=configurations.set_git,
    type='PREP',
    arguments=(True,), 
)

pathways.register(
    argument='--install-path',
    function=configurations.set_path,
    type='PREP',
    what_value_expected='Single', # we want one value from the command line
)
```

Now, let us define the `--install` argument.

```python
pathways.register(
    argument='--install',
    function=Drivers.install,
    type='EXEC',
    arguments=(configurations,),
)
```

Once all definitions and registrations are done, we can now orchestrate the pathway preps and executions.

```python
pathways.orchestrate
```

This will first perform all preps which will set the variables in the `Configurations` class and then it will perform the execution which will use these variables to execute the code.

Note that the executions will only be performed if the registered argument is present in the command line, else nothing will happen.

Also, the `pathways.orchestrate` method automatically validates all preparations and executions. It will raise an error if anything fails.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have any suggestions or improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.