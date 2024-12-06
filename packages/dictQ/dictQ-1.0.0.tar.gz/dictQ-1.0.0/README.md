# dictQ


[![PyPI version](https://badge.fury.io/py/dictQ.svg)](https://badge.fury.io/py/dictQ)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


This library was created to simplify searching algorithms by visually displaying them in the form of a horizontal table, using colors to illustrate the searching steps, giving the ability to control the searching speed and manually switching between items, all this is especially for beginners in searching algorithms.


## Installation


You can install `dictQ` via pip:


```bash
pip install dictQ
```


## Usage 


### For linear search algorithm 


```python
from dictQ import searchVisualizer


x = [26, 45, 84, 84, 88, 94, 14, 92, 6, 81]
y = searchVisualizer(x, item=92)
y.linear_search()
```


#### Output


https://drive.google.com/file/d/1U_1TuI3hqXPwG5kOIXD_TbXuRc3vrPhm/view?usp=sharing


### For binary search algorithm 


```python
from dictQ import searchVisualizer


x = [6, 14, 26, 45, 81, 84, 84, 88, 92, 94]
y = searchVisualizer(x, item=92)
y.binary_search()
```


#### Output


https://drive.google.com/file/d/1GBij5QkGtfHRGDMKpp5vlN9z3l_qrEFz/view?usp=sharing


#### You can reduce the searching speed


```python
from dictQ import searchVisualizer


x = [6, 14, 26, 45, 81, 84, 84, 88, 92, 94]
y = searchVisualizer(x, item=92, speed=7)
```


#### You can control the searching steps by pressing Enter


```python
from dictQ import searchVisualizer


x = [6, 14, 26, 45, 81, 84, 84, 88, 92, 94]
y = searchVisualizer(x, item=92, control=True)
```


## License


This project is licensed under the MIT LICENSE - see the [LICENSE](https://opensource.org/licenses/MIT) for more details.