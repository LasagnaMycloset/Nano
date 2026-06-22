
# Started in 2nd/April/2026 -- Rewritten in 6/18/2026. (This is the rewrite)
# Inspired by Small Basic by Microsoft (C).
# Designed to make programming fun & easy!
# Called "Nano".

# For the last time I checked this line... it is NOT done and still under development

# (Tips)
# Make your magical programs be friendly and not contain bad language.
# Bored? Try making a random number guessing game,
# Or a different endings game where the user chooses they're path.

# Typing Hints Libraries.
from collections.abc import Iterable
from typing import Any, Final
# ==================

import re
import sys # If you opened a `.nano` file with Nano via terminal flags.
import os  # For pathing stuff.
import time
from tkinter import messagebox # For popup messages.

DEBUG_MODE: Final[bool] = True if "-d" in sys.argv else False # False by default. True if -d in terminal flags... You can toggle it

def debug(info: str = "N/A", level: int = 1) -> None:
  """A function to track execution"""
  if not DEBUG_MODE:
     return # If debug mode is off, return.

  info = re.sub(r"`(.*?)`", r"\033[96m\033[1m\1\033[0m\033[93m", info)
  print("\033[92m" + ("|" if level-1 else "") + ("_" * ((level - 1) * 3))  +   f"\033[95m[DEBUG] \x1b[33m{info}\x1b[0m")
  #      COLOR        PUT | IF LEVEL IS NOT 1    PUT _ FOR LEVELS != 1            COLOR           COLOR       RESET COLR



opened_with_file_contents = ... # Default value if there is no file attached.
if len(sys.argv) > 1 and os.path.exists(sys.argv[1]): # Check if the file exists.
  debug(f"Attached file detected via terminal flags called `{sys.argv[1]}`")
  try:
    with open(sys.argv[1], "r", encoding="utf-8") as file:
      opened_with_file_contents = file.read()
      debug("File opened successfully.\n", level=2)
  except Exception as e:
    debug(f"Couldn't read file. `e`\n", level=2)
    pass # Ditch, if the file cannot be opened.

class Interpreter:
  def execute(self, code: Iterable[str]) -> None:
    """Just execute Nano code."""
    # Setup
    nano_vars: dict = {} # The dictionary that is going to store variables for Nano.

    def format_cmd(line: str) -> dict:
      """Turn each instruction (line) into a form that is easier to parse"""
      line = line.strip()

      if " " not in line: # If the command has no arguments, just return the command.
        return {"cmd": line.lower(), "args": ""}

      splitted: list[str] = line.split(" ", 1)

      command: str = splitted[0].lower()
      arguments: str = splitted[1]

      return {"cmd": command, "args": arguments}

    ansi_colors = {"black": "\033[30m","red": "\033[31m","green": "\033[32m","yellow": "\033[33m","blue": "\033[34m","magenta": "\033[35m","cyan": "\033[36m","white": "\033[37m",
                  "bright black": "\033[90m","bright red": "\033[91m","bright green": "\033[92m","bright yellow": "\033[93m","bright blue": "\033[94m","bright magenta": "\033[95m","bright cyan": "\033[96m","bright white": "\033[97m",
                  "bg black": "\033[40m","bg red": "\033[41m","bg green": "\033[42m","bg yellow": "\033[43m","bg blue": "\033[44m","bg magenta": "\033[45m","bg cyan": "\033[46m","bg white": "\033[47m",
                  "reset": "\033[0m","bold": "\033[1m"
    }

    def format_string(string: str) -> str:
      """Format strings (lookup things between ~...~ in the variable table)"""
      def replace(match):
        key = match.group(1)
        return str({key.lower() if isinstance(key, str) else key: value for key, value in nano_vars.items()}.get(key.lower(), f"Unfound variable `{key}`! :("))

      return re.sub(r"~(.*?)~", replace, string)

    def secure_eval(code: str) -> Any:
      """A secure evaluation to expressions"""
      # === NOT DONE!... ===
      try:
        return eval(code, {"__builtins__": {}}, nano_vars)
      except Exception as e:
        debug(e)
        warn("Can't evaluate expression. D:<")
        return "Couldn't evaluate expression... *~*"

    if isinstance(code, str):
      # If the code is a string, split by newlines, else, read it normally.
      formatted_script: Iterable[str] = map(format_cmd, code.split("\n"))
    else:
      formatted_script: Iterable[str] = map(format_cmd, code)

    def warn(text: str) -> None:
      """A `warn()` function to warn the user about the code."""
      text = re.sub(r"`(.*?)`", r"\033[96m\033[1m\1\033[0m\033[93m", text)
      print("\033[91m[ERROR] " + ansi_colors["bright yellow"], text, ansi_colors["reset"], sep="")

    debug("Interpreter setted up. Starting to execute.\n")

    # Start executing
    for exec_line, cmd in enumerate(formatted_script):
      if cmd["cmd"] == "say":
        """Say: Used to output text to the screen.
        Args: text: str
        Example: `say I love candy!` & `say My Favorite Candy is ~Favorite_Candy_Variable~` """
        print(format_string(cmd["args"])) # Format the string first...
        debug(f"Ran `say` command.\n")

      elif (not cmd["cmd"]) or (cmd["cmd"].startswith("--")):
        # Go to the next line, if this current line is just empty, or if it is a comment.
        # The commenting sequence is "--"
        """Comment: To comment you use `--`, and only can be on an independent line.
        Example: `-- This code calculates how much the candy cost`"""
        continue

      elif cmd["cmd"] == "var":
        """Var: Used to create a variable evaluated by a modified `eval()`
        Args: var_name: str, var_value: Any
        Example: `var Favorite_Candy = "Lollipop"` & `var Candy_Total_Price = 0.1 * 10 + fee`
        """

        if "=" not in cmd["args"]:
          warn(f">~< Unfound `=` character in `var` command! Can't create a variable.")
          continue

        splitted: list[str] = cmd["args"].split("=", 1)
        var_name: str = format_string(splitted[0].strip().lower())
        var_value: str = splitted[1].strip()

        if var_name.isidentifier(): # Check if the variable name is valid.
          try:
            final_value = secure_eval(var_value)
          except:
            warn(f"Invalid variable value. Can't create a variable.")
            continue

          nano_vars[var_name] = final_value
        else:
          warn(f"An invalid variable name *~* !... `{var_name}`. Can't create a variable.")
        
        debug(f"Ran `var` command with: `{var_name} = {final_value!r}`\n")

      elif cmd["cmd"] == "wait":
        """Wait: Used to time.sleep for a specific time in seconds
        Args: seconds: float
        Example: `wait 7.8` # Waits for 7.8 seconds """
        try:
          if cmd["args"]:
            to_wait = float(cmd["args"])
            time.sleep(to_wait)
          else:
            to_wait = 0.05
            time.sleep(to_wait) # sleep for a tiny time if no arguemnts provided
        except ValueError:
          warn(f"Uh oh >.<...  Can't wait for `{cmd['args']}`s, because it is not a valid real number! Can't wait.")
          continue
        
        debug(f"Ran `wait` command with {to_wait}s.\n")


      elif cmd["cmd"] == "beep":
        """Beep: Used to trigger a bell sound from the OS by printing the BEL(0x7) character
        Args: NONE
        Example: `beep`"""
        print("\a", end="")
        debug(f"Ran `beep` command.\n")

      elif cmd["cmd"] == "cls":
        """Cls: Used to clear the screen
        Args: NONE
        Example: `cls`"""
        os.system("cls" if os.name == "nt" else "clear")
        debug(f"Ran `cls` command.\n")

      elif cmd["cmd"] == "popup":
        """Popup: used for making an on-screen popup with text.
        Args: Text: str
        Example: `popup I love chocolate!`
        """
        messagebox.showinfo("Nano", format_string(cmd["args"]))
        debug(f"Ran `popup` command.\n")

      elif cmd["cmd"] == "color":
        """Color: Used to make text colorful on screen. (Colors are known by ansi_colors dict)
        Args: Color_Name: str
        Example: `color bg red` & `color green`
        """
        color = ansi_colors.get(cmd["args"].lower().strip()) # Get None if the color provided is unknown
        if not cmd["args"].strip():
          # If no color provided just reset the color.
          print(ansi_colors["reset"], end="")
          continue
        else:
          if color == None:
            # If the color is unknown. warn.
            warn(f"Unknown color `{cmd['args']}`. I can't color ~m~.")
            continue
          else:
            # Just do the color if everything goes correctly
            print(color, end="")

          # By the way I had to rewrite this section because I was lost and my editor is lagging.

        debug(f"Ran `color` command with color `{cmd['args']}`.\n")

      elif cmd["cmd"] == "reset_color":
        """Reset_Color: Used to make the text on the screen the default color.
        Args: NONE
        Example: `reset_color`"""
        print(ansi_colors.get("reset", ""), end="")
        debug("Ran `reset_color` command.\n")

      else:
        warn(f"Unkown command `{cmd["cmd"]}` ;-;")
        debug(f"Error unknown command.\n")




nano_inter = Interpreter()

if opened_with_file_contents != ...:
  nano_inter.execute(opened_with_file_contents.split("\n"))
  debug("Finished executing.")
  input()

# == You can test down here ==
# source_code = r"""
# color red
# say Hello, world!
# reset_color

# var Favorite_Candy = "Gummies"
# -- I love Gummies!

# say My Favorite Candy Is ~FAVORITE_CANDY~!

# wait 0.5

# beep

# cls

# popup I love chocolate!
#
# """
# nano_inter.execute(source_code) # Execute
