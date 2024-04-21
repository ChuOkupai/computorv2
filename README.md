# 🖥️ Computor v2

This project is the direct continuation of [computorv1](https://github.com/ChuOkupai/computorv1).

Computor v2 is a program that works like an advanced calculator. It can evaluate complex expressions, solve equations, store variables and functions...
It has been written as part of the 42 school curriculum.

My motivation was drastically reduced during the project due to the few experience points gained for the time invested.
42, my programming school, considers that a simple network project completed in a few hours yields 22450 XP compared to 9450 XP for Computor v2. This project took me hundreds of hours... I learned what I wanted. This is why I did not want to finish all the features on the [optimizer](doc/optimizer.md). However, I left the document that I had written on the rules to apply if necessary. GLHF 🙂

## ✨ Features
### 📚 Core features

- ⌨️ A CLI that allows the user to interact with the program
- 🧮 An evaluator with support for:
	- 📊 Complex numbers
	- 📐 Matrices
	- 📏 Arithmetic operations
	- 💾 Functions and variables assignment
	- 📈 Equations solving of degree up to 2

### 🎁 Bonus features

- 📜 Auto-completion for functions and variables names
- 💽 Commands history
- 🧱 Built-in constants:
	- `e` - Euler's number
	- `i` - Imaginary unit
	- `inf` - Infinity
	- `pi` - Pi
	- `tau` - Tau
- 🧱 Built-in functions:
	- `abs` - Absolute value
	- `cos` - Cosine
	- `exp` - Exponential
	- `identity` - Identity matrix
	- `inv` - Inverse matrix
	- `log` - Natural logarithm
	- `ones` - Matrix of ones
	- `sin` - Sine
	- `sqrt` - Square root
	- `tan` - Tangent
	- `transpose` - Transpose matrix
	- `zeros` - Matrix of zeros
- ⌨️ Built-in commands with prefix `%`:
	- `clear` - 🧹 Clear the screen
	- `delete` - 🗑️ Delete a variable or a function
	- `help` - 📚 Display the list of available commands or the help of a specific command
	- `show` - 📜 Display all stored functions and/or variables
- 📈 Functions with multiple arguments

### 🚀 Improvements

- Expressions evaluation can be done without using `= ?` at the end of the line.
- Support for digits and underscores in function and variable names
- Matrix exponentiation use the exponentiation by squaring algorithm for better performance
- The commands history is saved in a file to be persistent between sessions
- The program can be run in a non-interactive mode by providing a file as a shell redirection like this:
	```sh
	./computorv2 < file.txt
	```

## 📦 Prerequisites

Python 3.9.2 or higher is recommended to run the program.
An additional package named [PLY](https://www.dabeaz.com/ply) is also required.
You can install it by running the following command:
```
pip3 install -r requirements.txt
```

## 🛠️ Usage

To use the program, run the following command:
```sh
make run
```
Then, you can enter your expressions in the prompt that appears.

### 💡 Tips

- 🔬 Some examples are available in the [example](example) directory.
- ⚠️ Implicit multiplication has a higher priority than every other operation, so:
	- `2x ^ 3` is evaluated as `(2 * x) ^ 3`
	- `2 * x ^ 3` is evaluated as `2 * (x ^ 3)`
- 💡 You can use the `%help` command to display the list of available commands.
- 💡 You can use the `up` and `down` arrow keys to navigate through the commands history.
- 💡 You can exit the program by pressing `Ctrl + D`.

## 🧪 Testing

The source code is covered by unit tests written using the [unittest](https://docs.python.org/3/library/unittest.html) framework provided by Python.
There are located in the [test](test) directory.
The CLI is the only part of the program that is not covered by tests.

To run the unit tests, you can use the following command:

```sh
make test
```

## ⚖️ License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
