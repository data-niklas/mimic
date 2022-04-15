# mimic
Mimics mouse and keyboard input

## Goals
- Cross platform
- Use `pynput`


## Installation
- Clone the repository: `git clone https://github.com/data-niklas/mimic.git`
- `cd mimic`
- Start with `python src/mimic.py`
- Or create an alias in your `.bashrc`: `alias mimic="python path/to/mimic.py"`

### Record
- Records the user input
- Records either mouse, keyboard or both
- Saves the input in a `.mimic` file
- Variables is a `play` only feature and can not be recorded
- Recorded files may be modified afterwards to include variables
- Records mouse movement either relative or absolute

### (Re)play
- (Re)play `.mimic` files
- Optional initial delay
- Optional looping `n` times
- Allow variables (find and replace macro-like functionality)
- Check file before playing and throw errors before

### `.mimic` file type
- Easily customizable and human readable file format
- No explicit sleep
- Relative timestamps
- Allow execution of other files with passed variables
- No inline comments, only full line comments
- Loops: repeat block `n` times
- Line end acts as a separator
- If: Runs block if exit code is 0
- Else: Runs block if exit is not 0
- Grammar:
```
FILE ::=    HEADER NEWLINES BODY
HEADER ::=  NEWLINES ((COMMENT | VARIABLE_DECLARATION) NEWLINES )*  HEADER_END
HEADER_END ::= -+
VARIABLE_DECLARATION ::= LITERAL

BODY ::= ((PART | COMMENT) NEWLINES )*
PART ::= ACTION | BLOCK
BLOCK ::= IF | LOOP
ACTION ::= TIME_DELTA (KEY | MOVE | CLICK | TYPE | COMMAND | MIMIC)

IF ::= if COMMAND NEWLINES BLOCK end
LOOP ::= loop INTEGER NEWLINES BLOCK end

MIMIC ::= mimic FILENAME (VARIABLE_DECLARATION=LITERAL)*
KEY ::= key LITERAL (down | up)
TYPE ::= type LITERAL

MOVE ::= move X Y RELATIVE
X ::= INTEGER
Y ::= INTEGER
RELATIVE ::= (true | false)?        True is the default value

CLICK ::= click MOUSE_BUTTON TIMES
MOUSE_BUTTON ::= INTEGER
TIMES ::= INTEGER?                  Defaults to 1

COMMAND ::= run LITERAL


LITERAL ::= [^ \n#:.]+               No reserved keywords like `end`
TIME_DELTA ::= INTEGER                Time relative to last action in milliseconds
COMMENT ::= #[^\n]*
NEWLINES ::= \n+
```
- Variables start with a `$`
- Extra whitespace is ignored, just like extra newlines or comments


## Scope / Time
- No major new goals will be added, only small tweaks will be made
- This is a short time project and GitHub issues might be ignored
