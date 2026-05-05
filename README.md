# MineScript

A Minecraft-themed programming language that makes coding more fun and engaging by replacing traditional syntax with familiar game mechanics, objects, and commands from Minecraft.

---

## Overview

MineScript is an object-oriented, interpreted programming language with a middle-ground syntax — familiar enough for programmers, themed enough to feel like an adventure. Programs are written as Minecraft-style encounters, and execution produces a text-based terminal narration of the story.

The language is interpreted by a Python-based interpreter (`minescript.py`) and programs are saved with the `.ms` file extension.

---

## Getting Started

### Requirements
- Python 3

### Running a Program
```
python3 minescript.py <file.ms>
```

### Example
```
python3 minescript.py fizzbuzz.ms
```

---

## Syntax Rules

### Rule 1: Integer Variable Declaration
```
Steve.carry(identifier, value)
```
- Handles both declaration and reassignment
- Integers only
- Expressions are supported: `Steve.carry(count, count + 1)`

### Rule 2: String Variable Declaration
```
Steve.nametag(identifier, "value")
```
- Handles both declaration and reassignment of strings
- String values are wrapped in double quotes

### Rule 3: If / Else
```
Steve.encounter(condition) {
    ...
} otherwise {
    ...
}
```
- `encounter` replaces `if`
- `otherwise` replaces `else`
- The `otherwise` block is optional

### Rule 4: While Loop
```
Steve.mine(condition) {
    ...
}
```
- `mine` replaces `while`
- In combat contexts, the loop automatically terminates when either participant's HP reaches 0

### Rule 5: For Loop
```
Steve.loot(init, condition, increment) {
    ...
}
```
- `loot` replaces `for`
- Follows standard three-part structure: `Steve.loot(i = 1, i <= 10, i++)`

### Rule 6: Output
```
/chat value
/chat "string value"
```
- Global command, not tied to any object
- Works with integers, strings, and variables

### Rule 7: Functions
```
/functionName param1 param2 {
    ...
}

/functionName arg1 arg2
```
- No parentheses — arguments are space separated
- Entity argument is required when the function involves a specific object

### Rule 8: Object Definition

**Program Entry Point:**
```
Steve(HP, Attack, Armor)
```
- Defining Steve starts the program
- Attributes assigned in order: HP, Attack, Armor

**Optional Player Characters:**
```
PlayerName("Name", Level)
```
- Attributes assigned in order: Name, Level
- Access via dot notation: `PlayerName.name`, `PlayerName.level`

**Mob Objects:**
```
MobName(HP, Attack)
```
- Any capitalized name is treated as a Mob
- Attributes assigned in order: HP, Attack
- Access via dot notation: `MobName.hp`, `MobName.attack`

### Rule 9: Break Statement
```
/run
```
- Exits the current loop immediately
- Prints: `Steve ran away!`

### Rule 10: Health Restoration
```
/sleep
/eat amount
```
- `/sleep` fully restores Steve's HP
- `/eat amount` restores a specific amount of HP

### Rule 11: Random Number
```
/random identifier
```
- Generates a random integer between 1 and 10
- Stores the result in the given identifier

---

## Semantic Rules

### Semantic Rule 1: Implicit HP Constraint
Any `Steve.mine` loop involving a Mob automatically terminates when either Steve's HP or the Mob's HP reaches 0. This is enforced by the interpreter — the programmer does not need to write this condition explicitly.

### Semantic Rule 2: Damage Calculation
```
Damage = Attacker.attack - Defender.armor
```
- Mobs have no armor, so their armor value is always 0
- Damage cannot be negative
- Handled automatically by `/attack`

### Semantic Rule 3: Operators
All standard mathematical and comparison operators are preserved:
- Mathematical: `+`, `-`, `*`, `/`, `%`
- Comparison: `>`, `<`, `==`, `!=`, `>=`, `<=`

---

## Sample Programs

### combat_simulator.ms
Demonstrates object definition, while loops, conditionals, and slash commands.
```
Steve(20, 10, 5)
Creeper(15, 8)

Steve.mine(Creeper.hp > 0) {
    /attack Steve Creeper
    /attack Creeper Steve
}

Steve.encounter(Creeper.hp <= 0) {
    /chat "Steve wins!"
} otherwise {
    /chat "Creeper wins!"
}
```

### greeting.ms
Demonstrates string variables, player objects, functions, and conditionals.
```
Steve(20, 10, 5)
Alex("Alex", 5)
Jordan("Jordan", 10)

/greet greeter receiver {
    /chat greeter.name
    /chat "greets"
    /chat receiver.name
    /chat "Welcome, traveler!"
}

Steve.encounter(Alex.level > Jordan.level) {
    /greet Alex Jordan
} otherwise {
    /greet Jordan Alex
}
```

### fizzbuzz.ms
Demonstrates for loops, nested conditionals, and the modulo operator.
```
Steve(20, 10, 5)

Steve.loot(i = 1, i <= 100, i++) {
    Steve.encounter((i % 15) == 0) {
        /chat "FizzBuzz"
    } otherwise {
        Steve.encounter((i % 3) == 0) {
            /chat "Fizz"
        } otherwise {
            Steve.encounter((i % 5) == 0) {
                /chat "Buzz"
            } otherwise {
                /chat i
            }
        }
    }
}
```

### story.ms
A complex program that tells the full classic Minecraft storyline from spawning to defeating the Ender Dragon. Demonstrates all language features including multiple Mob objects, HP restoration, random encounters, functions, loops, and nested conditionals across six acts.

Run with:
```
python3 minescript.py story.ms
```

---

## Storyboard Generator

MineScript includes an AI-powered storyboard generator that transforms interpreter output into comic-style panels with a casual Minecraft Let's Play narration tone.

### How to Use
1. Run any `.ms` program and capture the output:
```
python3 minescript.py story.ms > output.txt
```
2. Copy the contents of `output.txt`
3. Open the MineScript Storyboard Generator artifact in Claude.ai
4. Paste the output into the text box
5. Click **Generate Storyboard**

The generator produces 4-8 comic panels that summarize the most meaningful story beats from the program output. Panel count scales with story length.

### How It Works
The storyboard generator is built as a React artifact that calls the Anthropic Claude API. It sends the interpreter output to Claude with a system prompt that instructs it to:
- Identify meaningful story beats
- Skip repetitive combat rounds and summarize fights
- Write in a casual, fun Let's Play tone
- Format output as structured JSON panels

---

## Ecosystem

- **Interpreter:** Python 3 based, handles all semantic rules and terminal narration
- **IDE:** Any text editor works. A VS Code extension with MineScript syntax highlighting is a potential future addition
- **Mod Packs:** Community libraries that add new functionality and slash commands
- **Texture Packs:** Cosmetic packages that reskin the terminal narration style without changing functionality
- **Standard Library:** Built-in slash commands (`/attack`, `/run`, `/sleep`, `/eat`, `/chat`, `/random`) and pre-defined object templates

---

## Known Challenges

1. **Semantic Rule Complexity** — The interpreter carries significant responsibility under the hood, tracking variable types, enforcing HP constraints, and calculating damage automatically
2. **Object Ambiguity** — Any capitalized name is treated as a Mob by default, which can conflict with Player object names if definition order is not followed
3. **Limited Data Types** — Only integers and strings are currently supported
4. **Scalability** — Designed for education and fun, not large-scale applications
5. **Learning Curve for Non-Minecraft Players** — The Minecraft theme is core to the language's identity and may be unfamiliar to some programmers

---

## File Structure

```
MineScript/
├── minescript.py           # The interpreter
├── combat_simulator.ms     # Sample program 1
├── greeting.ms             # Sample program 2
├── fizzbuzz.ms             # Sample program 3
├── story.ms                # Complex storyline program
└── README.md               # This file
```

---

## Language Design

MineScript was designed with three core principles:
- **Feasibility** — The language covers core programming constructs without over-engineering
- **Creativity** — Minecraft mechanics map naturally to programming concepts
- **Originality** — The middle-ground syntax and slash command system create a genuinely unique programming experience
