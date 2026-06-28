# Nano
A programming language, called Nano, inspired my Small Basic™. Designed to make programming fun &amp; easy!

# Nano Documentation

> ⚠ Nano is still NOT done. ⚠

### Commands:

|Command|Description|Example|
|:------|:--------|:------|
|`say`|**Outputs** text to the screen.|`say Hello, world!`|
|`wait`|**Waits** a specific amount of **seconds**. Defaults to 0.05s|`wait 1.5`|
|`color`|Makes text **colorful**.|`color red` & `color bg green`|
|`reset_color`|Resets the text's color|`reset_color`|
|`var`|Creates a **variable** using **Python's* syntax.|`var Tau = 3.1415926 * 2`|
|`popup`|Opens a **popup window** containing text.|`popup I'm a popup.`|
|`beep`|Triggers the **BEL sound** by the OS.|`beep`|
|`cls`|**Clears** the **text output**|`cls`|
---

To comment you need to put `--` on the start of the line, for example: `-- This code is designed to help me with my homework.`

In strings, variables between `~`...`~` are going to be replaced with their value,

While making a `var` variables inside that var command are required to be lowercase.

for example:
```
var a = 5
say a is actually equal to ~a~
```  

You can put a `-d` flag for debugging in the terminal.

---

### Tips
- Make your variables Pascal_Snake_Case and descriptive like `Candies_I_Bought`



\
Example program:


```
var Pi_Constant = 3.1415926

var Radius_Of_The_Circle = 9

var Area_Of_The_Circle = pi_constant * radius_of_the_circle ** 2

-- While making a `var`, variables are always lowercase, otherwise, they are case-insensitive.

color red

say == Circle ==

say Radius  :  ~RADIUS_OF_THE_CIRCLE~

wait 0.2

say Area    :  ~area_of_the_circle~

reset_color

beep
wait 4

-- Wait 4 seconds so the user can read

popup I hope you enjoyed my program!

cls

```
