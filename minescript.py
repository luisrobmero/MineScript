import sys
import re
import random

# ─── Object Storage ────────────────────────────────────────────────────────
objects = {}     # stores all defined objects
variables = {}   # stores carry/nametag variables
return_value = None

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

# ─── Object Definitions ────────────────────────────────────────────────────
def define_object(name, args):
    """Parse and store object definitions."""
    # Steve is always the entry point: Steve(hp, attack, armor)
    if name == "Steve":
        objects["Steve"] = {
            "hp": int(args[0]),
            "max_hp": int(args[0]),  # ← add this line
            "attack": int(args[1]),
            "armor": int(args[2])
        }
        print(f"[MineScript] Steve has entered the world.")

    # Player object: PlayerName("name", level)
    elif args[0].startswith('"'):
        player_name = args[0].strip('"')
        objects[name] = {
            "name": player_name,
            "level": int(args[1])
        }

    # Mob object: MobName(hp, attack)
    else:
        objects[name] = {
            "hp": int(args[0]),
            "attack": int(args[1]),
            "armor": 0   # Mobs have no armor
        }

# ─── /chat Command ─────────────────────────────────────────────────────────
def execute_chat(arg):
    arg = arg.strip()

    # Check if arg is a function call: /functionName args
    if arg.startswith("/"):
        parts = arg[1:].strip().split()
        func_name = parts[0]
        func_args = parts[1:] if len(parts) > 1 else []
        result = execute_function(func_name, func_args)
        if result is not None:
            print(result)
        return

    # String literal
    if arg.startswith('"') and arg.endswith('"'):
        print(arg.strip('"'))
        return

    # Object attribute
    elif "." in arg:
        obj_name, attr = arg.split(".")
        if obj_name in objects:
            obj = objects[obj_name]
            if attr in obj:
                print(obj[attr])
            else:
                print(f"[Error] Unknown attribute: {arg}")
        else:
            print(f"[Error] Unknown object: {obj_name}")
        return

    # Variable
    elif arg in variables:
        print(variables[arg])
        return

    else:
        print(f"[Error] Unknown value: {arg}")

# ─── Variable Declaration ──────────────────────────────────────────────────
def execute_carry(args):
    parts = [a.strip() for a in args.split(",", 1)]
    identifier = parts[0]
    expression = parts[1].strip()

    # Check if expression is a function call: /functionName args
    func_call = re.match(r'^/([a-zA-Z]+)\s*(.*)?$', expression)
    if func_call:
        func_name = func_call.group(1)
        func_args = func_call.group(2).strip().split() if func_call.group(2).strip() else []
        result = execute_function(func_name, func_args)
        if result is not None:
            variables[identifier] = result
            if "Steve" in objects and identifier in objects["Steve"]:
                objects["Steve"][identifier] = result
        return

    # Replace variables in expression with their values
    for var, val in variables.items():
        expression = re.sub(rf'\b{var}\b', str(val), expression)

    def replace_attr(match):
        obj_name = match.group(1)
        attr = match.group(2)
        if obj_name in objects and attr in objects[obj_name]:
            return str(objects[obj_name][attr])
        return match.group(0)

    expression = re.sub(r'([A-Z][a-zA-Z]*)\.([a-z]+)', replace_attr, expression)

    try:
        value = int(eval(expression))
        variables[identifier] = value
        if "Steve" in objects and identifier in objects["Steve"]:
            objects["Steve"][identifier] = value
    except Exception as e:
        print(f"[Error] Could not evaluate expression: {expression} → {e}")

def execute_nametag(args):
    """Handle Steve.nametag(identifier, "value")"""
    parts = [a.strip() for a in args.split(",", 1)]
    identifier = parts[0]
    value = parts[1].strip().strip('"')
    variables[identifier] = value

# ─── Expression Evaluator ──────────────────────────────────────────────────
def evaluate_condition(condition):
    """Evaluate a condition like Creeper.hp > 0 or i % 3 == 0"""
    condition = condition.strip()

    # Replace object attributes e.g. Creeper.hp with their value
    def replace_attr(match):
        obj_name = match.group(1)
        attr = match.group(2)
        if obj_name in objects and attr in objects[obj_name]:
            return str(objects[obj_name][attr])
        # Check saved combat results in variables
        saved_key = f"{obj_name}_{attr}"
        if saved_key in variables:
            return str(variables[saved_key])
        return match.group(0)

    condition = re.sub(r'([A-Z][a-zA-Z]*)\.([a-z]+)', replace_attr, condition)

    # Replace variables with their values
    for var, val in variables.items():
        if not var.endswith("_hp"):
            condition = re.sub(rf'\b{var}\b', str(val), condition)

    try:
        return eval(condition)
    except Exception as e:
        print(f"[Error] Could not evaluate condition: {condition} → {e}")
        return False

# ─── Combat Commands ───────────────────────────────────────────────────────
def execute_attack(args):
    """Handle /attack attacker defender"""
    parts = args.strip().split()
    attacker_name = parts[0]
    defender_name = parts[1]

    attacker = objects.get(attacker_name)
    defender = objects.get(defender_name)

    if not attacker or not defender:
        print(f"[Error] Unknown object in /attack: {args}")
        return

    damage = attacker["attack"] - defender.get("armor", 0)
    damage = max(0, damage)
    defender["hp"] -= damage
    defender["hp"] = max(0, defender["hp"])

    # Auto narrate HP after attack
    print(f"{defender_name} HP: {defender['hp']}")

# ─── Function Storage ──────────────────────────────────────────────────────
functions = {}

def define_function(name, params, body):
    """Store a function definition."""
    functions[name] = {
        "params": params,
        "body": body
    }

def execute_function(name, args):
    if name not in functions:
        print(f"[Error] Unknown function: {name}")
        return None

    func = functions[name]
    params = func["params"]
    body = func["body"]

    # Save original state
    original_objects = objects.copy()
    original_variables = variables.copy()

    # Map parameters to arguments in both objects and variables
    for param, arg in zip(params, args):
        if arg in objects:
            objects[param] = objects[arg]
        elif arg in variables:
            variables[param] = variables[arg]
            objects[param] = {"value": variables[arg]}
        else:
            try:
                val = int(arg)
                variables[param] = val
                objects[param] = {"value": val}
            except ValueError:
                variables[param] = arg

    return_val = None
    try:
        run(body)
    except ReturnException as e:
        return_val = e.value
    finally:
        # Restore original state
        objects.clear()
        objects.update(original_objects)
        variables.clear()
        variables.update(original_variables)

    return return_val

# ─── Line Parser ───────────────────────────────────────────────────────────
def parse_line(line):
    """Parse and execute a single line."""
    line = line.strip()

    # Skip empty lines and comments
    if not line or line.startswith("//") or line.startswith("#"):
        return

    # Object definition: Name(arg1, arg2, ...)
    obj_match = re.match(r'^([A-Z][a-zA-Z]*)\((.+)\)$', line)
    if obj_match:
        name = obj_match.group(1)
        args = [a.strip() for a in obj_match.group(2).split(",")]
        define_object(name, args)
        return

    # /chat command
    if line.startswith("/chat "):
        arg = line[6:]
        execute_chat(arg)
        return
    
    # Steve.carry(identifier, value)
    carry_match = re.match(r'^Steve\.carry\((.+)\)$', line)
    if carry_match:
        execute_carry(carry_match.group(1))
        return

    # Steve.nametag(identifier, "value")
    nametag_match = re.match(r'^Steve\.nametag\((.+)\)$', line)
    if nametag_match:
        execute_nametag(nametag_match.group(1))
        return
    
    # /attack attacker defender
    if line.startswith("/attack "):
        execute_attack(line[8:])
        return

    # /sleep
    if line.strip() == "/sleep":
        objects["Steve"]["hp"] = objects["Steve"].get("max_hp", 20)
        print(f"Steve closes his eyes and sleeps...")
        print(f"Steve woke up fully restored! HP: {objects['Steve']['hp']}")
        return

    # /eat amount
    eat_match = re.match(r'^/eat\s+(\d+)$', line)
    if eat_match:
        amount = int(eat_match.group(1))
        objects["Steve"]["hp"] = min(
            objects["Steve"]["hp"] + amount,
            objects["Steve"].get("max_hp", 20)
        )
        print(f"Steve eats to restore HP...")
        print(f"Steve HP: {objects['Steve']['hp']}")
        return

    # /run
    if line.strip() == "/run":
        print("Steve ran away!")
        raise StopIteration
    
    # /random identifier
    random_match = re.match(r'^/random\s+(\w+)$', line)
    if random_match:
        identifier = random_match.group(1)
        variables[identifier] = random.randint(1, 10)
        return
    
    # /return value
    return_match = re.match(r'^/return\s+(.+)$', line)
    if return_match:
        expr = return_match.group(1).strip()
        
        # Replace variables
        for var, val in variables.items():
            expr = re.sub(rf'\b{var}\b', str(val), expr)
        
        # Replace object attributes
        def replace_attr(match):
            obj_name = match.group(1)
            attr = match.group(2)
            if obj_name in objects and attr in objects[obj_name]:
                return str(objects[obj_name][attr])
            return match.group(0)
        
        expr = re.sub(r'([A-Z][a-zA-Z]*)\.([a-z]+)', replace_attr, expr)
        
        try:
            value = eval(expr)
            raise ReturnException(value)
        except ReturnException:
            raise
        except Exception as e:
            print(f"[Error] Could not evaluate return expression: {expr} → {e}")
        return

# ─── Block Extractor ───────────────────────────────────────────────────────
def extract_block(lines, start):
    """Extract lines inside { } starting from start index.
    Returns (block_lines, index_after_closing_brace)"""
    block = []
    depth = 0
    i = start
    while i < len(lines):
        line = lines[i].strip()

        # Handle closing brace first
        if line.startswith("}"):
            depth -= 1
            if depth == 0:
                # Stop before consuming "} otherwise {" lines
                if "otherwise" in line:
                    return block, i
                return block, i + 1

        # Now count opening braces
        if "{" in line and not line.startswith("}"):
            if depth == 0:
                # This is the opening line, don't add to block
                depth += 1
                i += 1
                continue
            depth += 1

        if depth > 0:
            block.append(lines[i])

        i += 1
    return block, i

# ─── Main Runner ───────────────────────────────────────────────────────────
def run(lines, index=0):
    """Execute lines of MineScript code."""
    i = index
    while i < len(lines):
        line = lines[i].strip()

        # Skip empty lines and comments
        if not line or line.startswith("//") or line.startswith("#"):
            i += 1
            continue

        # Steve.encounter (if/else)
        encounter_match = re.match(r'^Steve\.encounter\((.+)\)\s*\{', line)
        if encounter_match:
            condition = encounter_match.group(1)
            if_block, i = extract_block(lines, i - 1)

            # Check for otherwise block
            otherwise_block = []
            if i < len(lines) and "otherwise" in lines[i]:
                # Create a fake opening line so extract_block works correctly
                fake_open = ["{"]
                rest = lines[i + 1:]
                otherwise_block, _ = extract_block(fake_open + rest, 0)
                # Advance i past the otherwise block
                i += len(otherwise_block) + 2

            if evaluate_condition(condition):
                run(if_block)
            else:
                run(otherwise_block)
            continue

        parse_line(line)
        i += 1
        
        # Steve.mine (while loop)
        mine_match = re.match(r'^Steve\.mine\((.+)\)\s*\{', line)
        if mine_match:
            condition = mine_match.group(1)
            loop_block, i = extract_block(lines, i - 1)

            # Check for combat context
            mob_names = [
                name for name, attrs in objects.items()
                if "attack" in attrs and name != "Steve"
                and "level" not in attrs
            ]

            def hp_broken():
                for mob in mob_names:
                    if objects[mob]["hp"] <= 0 or objects["Steve"]["hp"] <= 0:
                        return True
                return False

            while evaluate_condition(condition) and not hp_broken():
                try:
                    run(loop_block)
                except StopIteration:
                    break

            # Save mob HP values before cleanup
            combat_results = {}
            for name in mob_names:
                combat_results[name] = objects[name]["hp"]
                variables[f"{name}_hp"] = objects[name]["hp"]

            # Remove defeated Mobs from objects after combat loop
            defeated = [
                name for name in mob_names
                if objects[name]["hp"] <= 0
            ]
            for name in defeated:
                del objects[name]

            # Store results in variables for post-combat conditions
            for name, hp in combat_results.items():
                variables[f"{name}_hp"] = hp

            # Replace saved mob HP values e.g. Blaze.hp
            for var, val in variables.items():
                if "_hp" in var:
                    mob_name = var.replace("_hp", "")
                    condition = condition.replace(f"{mob_name}.hp", str(val))

        # Function definition: /functionName params... {
        func_def_match = re.match(r'^/([a-zA-Z]+)\s+([\w\s]+)\s*\{', line)
        if func_def_match:
            func_name = func_def_match.group(1)
            params = func_def_match.group(2).strip().split()
            func_body, i = extract_block(lines, i - 1)
            define_function(func_name, params, func_body)
            continue

        # Function call: /functionName args...
        func_call_match = re.match(r'^/([a-zA-Z]+)\s+([\w\s]+)$', line)
        if func_call_match:
            func_name = func_call_match.group(1)
            args = func_call_match.group(2).strip().split()
            # Only call if it's a defined function, not a built-in
            if func_name in functions:
                execute_function(func_name, args)
                continue

        # Steve.loot (for loop)
        loot_match = re.match(r'^Steve\.loot\((.+),\s*(.+),\s*(.+)\)\s*\{', line)
        if loot_match:
            init = loot_match.group(1).strip()
            condition = loot_match.group(2).strip()
            increment = loot_match.group(3).strip()

            # Parse initialization: i = 0
            init_parts = [p.strip() for p in init.split("=")]
            loop_var = init_parts[0]
            variables[loop_var] = int(eval(init_parts[1]))

            # Parse increment: i++ or i--
            if "++" in increment:
                inc_var = increment.replace("++", "").strip()
                inc_expr = f"{inc_var} + 1"
            elif "--" in increment:
                inc_var = increment.replace("--", "").strip()
                inc_expr = f"{inc_var} - 1"
            else:
                # Handle i += n or i -= n
                inc_var, inc_expr = [p.strip() for p in increment.split("=")]
                inc_expr = inc_expr.strip()

            loop_block, i = extract_block(lines, i - 1)

            while evaluate_condition(condition):
                run(loop_block)
                # Execute increment
                execute_carry(f"{inc_var}, {inc_expr}")

            continue

# ─── File Loader ───────────────────────────────────────────────────────────
def load_and_run(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    run(lines)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 minescript.py <file.ms>")
    else:
        load_and_run(sys.argv[1])