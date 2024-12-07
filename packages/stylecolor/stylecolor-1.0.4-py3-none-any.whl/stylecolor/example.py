import stylecolor as sc


# functions
print(sc.blue('blue text'))
print(sc.lblue('light blue text'))
print(sc.bblue('background blue text'))
print(sc.blblue('background light blue text'))
print(sc.underline('underline text'))
print(sc.strikethrough('strikethrough text'))

# constants
print()
print(sc.YELLOW, 'constant yellow text', sc.RESET, sep='')
print(sc.YELLOW, sc.UNDERLINE, 'constant yellow underline text', sc.RUNDERLINE, ' | only yellow text', sep='')

# combinations
print()
print(sc.blue(sc.bold('blue bold text')))
print(sc.underline(sc.bold("underline bold text")))
print(sc.underline(sc.CYAN, sc.BLBLACK, 'underline cyan text, with light black background', sep=''), sc.blue('additionally, simple blue text', sep=''))
print(sc.GREEN, 'green text ', sc.UNDERLINE, sc.ITALIC, 'italic underline green text', sc.RUNDERLINE, sc.RCOLOR, ' just italic text', sc.RESET, sep='')

# apply one or many custom style at once
print()
print(sc.style('here,', 'different', 'text values with', 'unique style', style='red'))
print(sc.styles('here, unique text, with different styles', 'red', 'byellow', 'bold', 'underline'))
print(sc.rgb('different values', 'colored with custom rgb value', r=100, g=150, b=100))
print(sc.rgb('differents values', 'colored with custom rgb', 'tuple', rgb=(100, 150, 100)))
print(sc.brgb('background', 'custom colored text', rgb=(0, 50, 50)))
print(sc.hexa('colored text', 'with hexadecimal color', hexa='#148ADF'))
print(sc.hexa('colored text', 'with hexadecimal color', "without '#'", hexa='#148ADF'))
print(sc.bhexa('background colored text', 'with custom hexadecimal color', hexa='259BEF'))

# deactivate() and reactivate()
print()
print(sc.blue('styled text'))
sc.deactivate()
print(sc.blue('unstyled text'))
print(sc.BOLD + 'unstyled text' + sc.RESET)
sc.reactivate()
print(sc.lblue('restyled text'))

# debug / Advanced functions
styled = sc.styles('styled text', 'lred', 'bblue', 'underline')

raw = sc.raw(styled) # return raw string
print(raw)
sc.rprint(styled) # directly print raw string