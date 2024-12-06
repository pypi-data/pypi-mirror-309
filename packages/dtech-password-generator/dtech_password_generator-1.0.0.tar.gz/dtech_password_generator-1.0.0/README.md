Password Generator
==================

Overview
--------

The **Password Generator** is a Python package designed to create strong, random passwords that meet modern security requirements. It supports generating passwords of customizable lengths with a mix of uppercase, lowercase, digits, and special characters. The package is easy to use and ensures flexibility while maintaining safety standards for password creation.

Features
--------

*   Generates random, secure passwords.
    
*   Password length customization between 7 and 35 characters.
    
*   Includes uppercase, lowercase, numbers, and special characters for enhanced security.
    
*   Easy-to-integrate functionality for other projects.
    

Installation
------------

Install the package using pip:
```python
pip install dtech-password-generator
```
Usage
-----

Here are some examples to demonstrate how to use the package:

### Basic Usage
```python
from dtech_password_generator import password

# Generate a default password
print(password())  # Example: '2?QF7WX#[k'

# Generate a password of specific length
print(password(20))  # Example: '#UI7HN31d+0\"n|wq9rh'
```

### Handling Invalid Lengths
```python
# Requesting a password below the minimum length
print(password(5))  # Output: 'Length must be within 7 and 40'

# Requesting a password above the maximum length
print(password(60))  # Output: 'Length must be within 7 and 40'
```
### Assigning Passwords to Variables
```python
# Assigning a generated password to a variable
x = password(7)
print(x)  # Example: 'BN3bz7+'
```

### Tests
Snippet of tests
```python
Python 3.8.10 (default, Sep 11 2024, 16:02:53) 
[GCC 9.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from password_generator import password
>>> password()
'qCcM#071H3'
>>> password(5)
'Length must be within 7 and 40'
>>> password(6)
'Length must be within 7 and 40'
>>> password(7)
'<Ku/0+7'
>>> password(7)
'/1*Nxl2'
>>> x = password(7)
>>> x
'BN3bz7+'
>>> print(x)
BN3bz7+
>>> print(password())
2?QF7WX#[k
>>> print(password(20))
#UI7HN31d+0\"n|wq9rh
>>> password(60)
'Length must be within 7 and 40'
>>> 
```
### License
This package is licensed under the MIT License.

### Contribution
Contributions are welcome! If you'd like to add features or improve the package, feel free to open a pull request or submit an issue on GitHub.