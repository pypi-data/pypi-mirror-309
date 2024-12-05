qformat: Quantitative Formatter
=======================

qformat is a number formatter that use numerical parameters (rather than magic string) to control the number formatting.

### API

`qformat(number: float, width: Optional[int]=None, precision: Optional[int]=None) -> str`


### Usage Example

```
from qformat import qformat
s = qformat(2., width=4, precision=1)
print(s)   # Output " 2.0"
```
