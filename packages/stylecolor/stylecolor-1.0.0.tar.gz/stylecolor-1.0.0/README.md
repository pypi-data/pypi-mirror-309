# Stylecolor - 1.0.0

## Stylecolor
`stylecolor` is the simplest package for coloring and/or styling text in the terminal.  
`stylecolor` requires no other modules and is very lightweight and efficient.  

## Installation
No prerequisites are needed, only stylecolor.
```bash
pip install stylecolor
```

## Description
`stylecolor` uses [ANSI escape codes](https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797) to function. It is therefore compatible with all other libraries that use ANSI codes.

Some terminals do not support ANSI escape codes, so you can disable styling with `deactivate()`. In this case, you will still be able to use the functions, but the various styles will no longer be applied.  
Use `reactivate()` to reactivate the styling.

I recommend importing `stylecolor` as `sc` or `st`.\
Additionally, if you are debugging, I suggest importing the `rprint()` function like this: `from stylecolor import rprint()`

## Coloring
8 colors are available natively: `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, and `white`.  
For each color, there are functions (e.g. `stylecolor.red()`), as well as constants (e.g. `stylecolor.RED`).  
For other colors, use [`stylecolor.rgb()`](#custom-colors) or [`stylecolor.hexa()`](#custom-colors).

### Simple Colors

```python
import stylecolor as sc
print(sc.red('red text'))
print(sc.green('green text'))
print(sc.blue('blue text'))
# ...
# AND/OR
print(sc.RED + 'constant red text' + sc.RESET)
print(sc.GREEN + 'constant green text' + sc.RESET)
print(sc.BLUE + 'constant blue text' + sc.RESET)
# ...
```

**output:**
><span style="color: red;">red text</span>\
><span style="color: green;">green text</span>\
><span style="color: blue;">blue text</span>\
>...  
>  
><span style="color: red;">constant red text</span>\
><span style="color: green;">constant green text</span>\
><span style="color: blue;">constant blue text</span>\
> ...

### Light Colors
You can add the prefix `l` in front of the color to make it a `light` version.

````python
import stylecolor as sc
print(sc.lred('light red'))
print(sc.lgreen('light green'))
print(sc.lblue('light blue'))
# ...
# AND/OR
print(sc.LRED + 'constant red text' + sc.RESET)
print(sc.LGREEN + 'constant green text' + sc.RESET)
print(sc.LBLUE + 'constant blue text' + sc.RESET)
# ...
````

**output**
><span style="color: #FFCCCB;">light red</span>\
><span style="color: lightgreen;">light green</span>\
><span style="color: lightblue;">light blue</span>\
>...
> 
><span style="color: #FFCCCB;">constant light red</span>\
><span style="color: lightgreen;">constant light green</span>\
><span style="color: lightblue;">constant light blue</span>\
> ...

### Background Colors
You can add the prefix `b` in front of each color to set it as a background color.

```python
import stylecolor as sc
print(sc.bred('red background'))
print(sc.bgreen('green background'))
print(sc.bblue('blue background'))
# ...
# AND/OR
print(sc.BRED + 'constant red background' + sc.RESET)
print(sc.BGREEN + 'constant green background' + sc.RESET)
print(sc.BBLUE + 'constant blue background' + sc.RESET)
# ...
```

**output**
><span style="background-color: red;">red background</span>\
><span style="background-color: green;">green background</span>\
><span style="background-color: blue;">blue background</span>\
>...
> 
><span style="background-color: red;">constant red background</span>\
><span style="background-color: green;">constant green background</span>\
><span style="background-color: blue;">constant blue background</span>\
>...

>**NOTE**\
> You can also add `b` in front of the `light` colors.
> 
> ```python
> import stylecolor as sc
> print(sc.blred('light red background'))
> print(sc.blgreen('light green background'))
> print(sc.blblue('light blue background'))
> # ...
> #AND/OR"
> print(sc.LBRED + 'constant light red background' + sc.RESET)
> print(sc.LBGREEN + 'constant light green background' + sc.RESET)
> print(sc.LBBLUE + 'constant light blue background' + sc.RESET)
> # ...
> ```
> 
> **output**
>> <span style="background-color: #FFCCCB;color: black">light red background</span>\
>> <span style="background-color: lightgreen;color:black">light green background</span>\
>> <span style="background-color: lightblue;color:black">light blue background</span>\
>> ...
>>
>> <span style="background-color: #FFCCCB;color: black">constant light red background</span>\
>> <span style="background-color: lightgreen;color:black">constant light green background</span>\
>> <span style="background-color: lightblue;color:black">constant light blue background</span>\
>> ...

### Custom Colors
The `rgb()` and `hexa()` functions allow you to apply custom colors.

```python
import stylecolor as sc
print(sc.rgb('personalised rgb color', '+ other text', r=250, g=200, b=0))
print(sc.rgb('personalised tuple rgb color', '+ other text', rgb=(250, 200, 0)))
print(sc.hexa('personalised hexadecimal color', '+ other value', hexa='#FAC800'))
print(sc.hexa('personalised hexadecimal color', "without '#'", hexa='FAC800'))
``` 

**output**
><span style="color: #FAC800;">personalised rgb color + other text</span>\
><span style="color: #FAC800;">personalised tuple rgb color + other text</span>\
><span style="color: #FAC800;">personalised hexadecimal color + other value</span>\
><span style="color: #FAC800;">personalised hexadecimal color without '#'</span>

### Custom Background Colors
The `brgb()` and `bhexa()` functions allow you to apply custom background colors.

````python
import stylecolor as sc
print(sc.brgb('personalised rgb color', '(background)', r=250, g=200, b=0))
print(sc.brgb('personalised tuple rgb color', '(background)', rgb=(250, 200, 0)))
print(sc.bhexa('personalised hexadecimal color', '(background)', hexa='#FAC800'))
print(sc.bhexa('personalised background hexadecimal color', "without '#'", hexa='FAC800'))
````

**output**
><span style="color: #FAC800;">personalised rgb color (background)</span>\
><span style="color: #FAC800;">personalised tuple rgb color (background)</span>\
><span style="color: #FAC800;">personalised hexadecimal color (background)</span>\
><span style="color: #FAC800;">personalised background hexadecimal color without '#'</span>

### Reset Colors
The functions `stylecolor.rcolor()` or `stylecolor.RCOLOR` and `stylecolor.rbackground()` or `stylecolor.RBACKGROUND` respectively remove the text color and the background color.

> \>>> text = "<span style="color: green">green text</span>\"\
> \>>> stylecolor.rcolor(text)\
> \>>> "green text"
> \>>> text = "<span style="background-color: green">background green text</span>\"\
> \>>> stylecolor.rbackground(text)\
> \>>> "background green text"

## Built-in Styles

### Apply Styles
In addition to colors, many styles are available: `bold`, `dim`, `italic`, `underline`, `blinking`, `reverse`, `hidden`, and `strikethrough`.  
Just like with colors, styles are accessible via functions (e.g. `stylecolor.bold()`) or constants (e.g. `stylecolor.BOLD`).

```python
import stylecolor as sc
print(sc.bold('bold text'))
print(sc.italic('italic text'))
print(sc.underline('underline text'))
# ...
# AND/OR
print(sc.BOLD, 'constant bold text', sc.RESET, sep='')
print(sc.ITALIC, 'constant italic text', sc.RESET, sep='')
print(sc.UNDERLINE, 'constant underline text', sc.RESET, sep='')
# ...
``` 

**output**
> **bold text**\
> _italic text_\
> <u>underline text</u>\
> ...
>
> **constant bold text**\
> _constant italic text_\
> <u>underline text</u>\
> ...

### Reset Styles
You can add the prefix `r` in front of each style to cancel it (including with constants).
> \>>> text = "**bold text**"\
> \>>> stylecolor.rbold(text)\
> \>>> "bold text"\
> \>>> text = "<u>underline text</u>"\
> \>>> stylecolor.runderline(text)\
> \>>> "underline text"

## Other Styles
It is possible, using the functions `stylecolor.style()` and `stylecolor.styles()`, to apply one or more styles to text.  
You can use textual styles like `red`, `bred`, `underline`, or directly use ANSI codes like `31`, `41`, `4`, for example.

````python
import stylecolor as sc
def func():
    pass
print(sc.style('text1', func, 'other text', style='blue'))
print(sc.styles('unique object', 'white', 'bblack', 'underline'))
````

**output**
> <span style="color: blue;">text1 <function func at 0x00000XXXXXXXXXX> other text</span>\
> <u color='whiyte'><span style="color: white;background-color: black">unique object</span></u>

## Composability

Most functions and constants are composable with each other.

```python
import stylecolor as sc
print(sc.blue(sc.underline('blue underline text'), 'blue text only'), 'normal text')
print(sc.styles('blue underline text', 'blue', 'underline', 'italic'))
# fonctions with constants
print(sc.green(sc.UNDERLINE, 'combined green underline text', sc.RUNDERLINE, ' green text only', sep=''), 'normal text')
````

**output** 
><u style="color: blue"><span style="color: blue;">blue underline text</span></u> <span style="color: blue;">blue text only</span> normal text\
>_<u style="color: blue"><span style="color: blue;">blue underline italic text</span></u>_
> 
><u style="color: green"><span style="color: green;">combined green underline text</span></u> <span style="color: green;">green text only</span> normal text

>**NOTE**\
> Foreground colors are not composable with each other, just like background colors.
>
>````python
>import stylecolor as sc
>print(sc.blue(sc.green('colored text in blue and green which appears blue')))
>print(sc.bblue(sc.bgreen('background colored text in blue and green which appears blue')))
>```` 
>
>**output**
>> <span style="color: blue;">colored text in blue and green which appears blue</span>\
>> <span style="background-color: blue;">background colored text in blue and green which appears blue</span>

## Debug Functions

The functions `raw()` and `rprint()` allow you to get the raw version of a styled text.

````python
import stylecolor as sc
colored = sc.blue("raw blue text")
raw = sc.raw(colored) # return raw string
print(raw)
sc.rprint(colored)  # directly print raw result
````
> \033[0;34mraw blue text\033[0m\
> \033[0;34mraw blue text\033[0m
