#!/usr/bin/env python3
"""Transform all 87 Ninja Luxe Cafe recipes - v4: full array rebuild approach."""

import re
import sys
import shutil

def load_file(path):
    with open(path, 'r') as f:
        return f.read()

def save_file(path, content):
    with open(path, 'w') as f:
        f.write(content)

# ── Machine detail indicators (skip if already present) ──
MACHINE_INDICATORS = [
    'luxe basket', 'double basket', 'barista assist', 'auto-grinds',
    'ninja milk jug', 'press brew', 'cold-pressed on the dial',
    'brew over ice', 'quad on the dial', 'classic on the dial',
    'rich on the dial', 'cold brew on the control panel',
    'drip coffee filter basket', 'size button', 'group head',
    'place the whisk in the lid',
]

def has_machine_detail(text):
    return any(ind in text.lower() for ind in MACHINE_INDICATORS)

def transform_step(step, recipe_type, recipe_name, recipe_id, all_steps_str):
    text = step.strip()
    lower = text.lower()
    
    if has_machine_detail(text):
        return text
    
    # "Pull [a/your] [X] espresso/ristretto shot" — flexible matching
    # Handles: "Pull a double shot", "Pull your espresso shot", "Pull a double ristretto (or espresso) shot"
    if re.search(r'pull\s+(?:a\s+|your\s+)?(?:single|double|quad(?:ruple)?)?\s*(?:espresso|ristretto)\b', lower):
        if 'quad' in lower:
            return "Select ESPRESSO mode, then QUAD on the dial. The machine pulls four shots automatically using the Luxe basket (18-20g)."
        elif 'single' in lower:
            return "Select ESPRESSO mode. Use the Double basket (10-12g). Let Barista Assist recommend the grind size. The machine auto-grinds, doses, and tamps. Place your cup under the group head and press BREW."
        else:
            return "Select ESPRESSO mode. Use the Luxe basket (18-20g). Let Barista Assist recommend the grind size. The machine auto-grinds, doses, and tamps. Place your cup under the group head and press BREW."
    
    # "Pull espresso shot" (no article, frappe-style: "Pull espresso shot and cool")
    if re.search(r'pull\s+espresso\s+shot', lower):
        return "Select ESPRESSO mode. Use the Luxe basket (18-20g). Let Barista Assist recommend the grind size. The machine auto-grinds, doses, and tamps. Place your cup under the group head and press BREW."
    
    # Vague "Select ESPRESSO mode"
    if re.search(r'^select\s+espresso\s+mode', lower) and 'basket' not in lower and 'brew' not in lower:
        return "Select ESPRESSO mode. Use the Luxe basket (18-20g). Let Barista Assist recommend the grind size. The machine auto-grinds, doses, and tamps. Press BREW."
    
    # "Select COLD PRESSED ESPRESSO mode"
    if re.search(r'select\s+cold.?pressed\s+espresso\s+mode', lower):
        return "Select ESPRESSO mode, then COLD-PRESSED on the dial. This uses cold water at high pressure. Use the Luxe basket (18-20g). Press BREW."
    
    # "Select COLD BREW"
    if re.search(r'select\s+cold\s+brew', lower):
        return "Press COLD BREW on the control panel. The machine recommends a coarse grind (23-25). Insert the drip filter basket. Select your size with the SIZE button and press BREW."
    
    # "Select BREW OVER ICE"
    if re.search(r'select\s+brew\s+over\s+ice', lower):
        return "Select ESPRESSO mode, then rotate the dial to BREW OVER ICE. Fill your cup with ice first. The machine adjusts extraction for ice dilution. Press BREW."
    
    # "Brew cold brew using the machine" or similar vague cold brew references
    if re.search(r'brew\s+cold\s+brew', lower):
        return "Press COLD BREW on the control panel. The machine recommends a coarse grind (23-25). Insert the drip filter basket. Select your size with the SIZE button and press BREW."
    
    # "Brew a cup of drip coffee" or "Select COFFEE mode and brew"
    if re.search(r'(?:brew\s+(?:a\s+cup\s+of\s+)?drip\s+coffee|select\s+coffee\s+mode)', lower):
        return "Select COFFEE mode, then CLASSIC on the dial. Remove the portafilter and insert the drip coffee filter basket. Select your size with the SIZE button. Press BREW."
    
    # "Froth milk on [SETTING]" - generic
    froth_setting = re.search(r'(?:froth|select)\s+(?:milk\s+)?(?:on\s+)?(?:the\s+)?(?:milk\s+)?(?:frother|jug)?\s*(?:with\s+|on\s+|to\s+)?(STEAMED MILK|THICK FROTH|THIN FROTH|COLD FOAM)', text, re.IGNORECASE)
    if froth_setting:
        s = froth_setting.group(1).upper()
        if s == 'STEAMED MILK':
            return "Fill the Ninja milk jug to the LATTE line. Place the whisk in the lid, select STEAMED MILK on the frother, and press start. The machine froths hands-free."
        elif s == 'THICK FROTH':
            return "Fill the Ninja milk jug to the CAPPUCCINO line. Place the whisk in the lid, select THICK FROTH on the frother, and press start. The machine froths hands-free."
        elif s == 'THIN FROTH':
            return "Fill the Ninja milk jug to the LATTE line. Place the whisk in the lid, select THIN FROTH on the frother, and press start."
        elif s == 'COLD FOAM':
            return "Fill the Ninja milk jug to the minimum line. Place the whisk in the lid, select COLD FOAM on the frother, and press start. The machine froths hands-free."
    
    # "Fill the milk jug to [X] line" without whisk
    if re.search(r'fill\s+(?:the\s+)?(?:ninja\s+)?milk\s+jug\s+to\s+the\s+(LATTE|CAPPUCCINO|minimum)\s+line', lower) and 'whisk' not in lower:
        return text + ". Place the whisk in the lid, select the frother setting, and press start."
    
    # "Fill milk jug with X oz milk" → replace with machine-specific
    if re.search(r'fill\s+(?:the\s+)?milk\s+jug\s+with', lower):
        return "Fill the Ninja milk jug to the LATTE line. Place the whisk in the lid, select STEAMED MILK on the frother, and press start."
    
    # "Add hot water" / "Heat water separately"
    if re.search(r'(?:heat|add)\s+hot\s+water(?:\s+separately)?', lower) and 'blank' not in lower and 'kettle' not in lower:
        return "Use a separate kettle or run a blank espresso shot for hot water"
    
    # "Pour over ice" for iced/cocktail
    if re.search(r'(?:fill|pour).*?(?:glass|cup).*?(?:with\s+)?ice', lower):
        if recipe_type in ('iced', 'cocktail') and 'brew over ice' not in all_steps_str.lower() and 'brew over ice' not in lower:
            return text + ". For best results, use the Brew Over Ice setting: select ESPRESSO mode, rotate dial to BREW OVER ICE."
    
    # "Sweeten to taste"
    if re.search(r'sweeten\s+to\s+taste', lower):
        return "Add your preferred syrup or sweetener to taste"
    
    # Generic "Froth" or "Steam" standalone
    if re.match(r'^(?:Froth|Steam)\s', text):
        if 'thick' in lower or 'cappuccino' in lower:
            return "Fill the Ninja milk jug to the CAPPUCCINO line. Place the whisk in the lid, select THICK FROTH on the frother, and press start."
        elif 'cold' in lower:
            return "Fill the Ninja milk jug to the minimum line. Place the whisk in the lid, select COLD FOAM on the frother, and press start."
        else:
            return "Fill the Ninja milk jug to the LATTE line. Place the whisk in the lid, select STEAMED MILK on the frother, and press start."
    
    # "Steam about X oz milk" / "Froth a small amount of milk"
    if re.search(r'(?:steam|froth)\s+(?:about\s+\d+.?oz|a\s+small\s+amount)', lower):
        return "Fill the Ninja milk jug to the minimum line. Place the whisk in the lid, select STEAMED MILK on the frother, and press start."
    
    return text


# ── Recipe object parser ──
def parse_recipe_object(text, start_pos):
    """Parse one recipe object from text starting at start_pos.
    Returns (parsed_dict, end_pos) or (None, start_pos) on failure."""
    # text[start_pos] should be '{'
    depth = 0
    instring = False
    esc = False
    i = start_pos
    
    # Find the end of this object
    while i < len(text):
        c = text[i]
        if esc: esc = False; i += 1; continue
        if c == '\\': esc = True; i += 1; continue
        if c == "'" and not instring: instring = True; i += 1; continue
        if c == "'" and instring: instring = False; i += 1; continue
        if instring: i += 1; continue
        if c == '{': depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return text[start_pos:i+1], i+1
        i += 1
    
    return None, start_pos


def extract_field(text, field_name):
    """Extract a field value from a recipe object string."""
    pattern = field_name + r"\s*:\s*"
    m = re.search(pattern, text)
    if not m:
        return None
    start = m.end()
    
    if start >= len(text):
        return None
    
    c = text[start]
    if c == "'":
        # String value
        result = ""
        i = start + 1
        esc = False
        while i < len(text):
            cc = text[i]
            if esc:
                result += cc
                esc = False
                i += 1
                continue
            if cc == '\\':
                esc = True
                i += 1
                continue
            if cc == "'":
                return result
            result += cc
            i += 1
        return result
    elif c == '[':
        # Array value - find matching ]
        depth = 0
        instring = False
        esc = False
        i = start
        while i < len(text):
            cc = text[i]
            if esc: esc = False; i += 1; continue
            if cc == '\\': esc = True; i += 1; continue
            if cc == "'" and not instring: instring = True; i += 1; continue
            if cc == "'" and instring: instring = False; i += 1; continue
            if instring: i += 1; continue
            if cc == '[': depth += 1
            elif cc == ']':
                depth -= 1
                if depth == 0:
                    return text[start:i+1]
            i += 1
        return None
    else:
        # Other primitive (true/false/number)
        m2 = re.match(r'[^,\s}]+', text[start:])
        return m2.group(0) if m2 else None


def parse_array_strings(arr_text):
    """Parse a JS array of strings like ['a','b','c'] into a Python list."""
    if not arr_text or not arr_text.startswith('['):
        return []
    
    inner = arr_text[1:].rstrip().rstrip(']').strip()
    if not inner:
        return []
    
    strings = []
    current = ""
    instring = False
    esc = False
    i = 0
    
    while i < len(inner):
        c = inner[i]
        if esc:
            current += c
            esc = False
            i += 1
            continue
        if c == '\\':
            esc = True
            i += 1
            continue
        if c == "'" and not instring:
            instring = True
            i += 1
            continue
        if c == "'" and instring:
            instring = False
            strings.append(current)
            current = ""
            # skip past comma
            j = i + 1
            while j < len(inner) and inner[j] in ' \t\n\r':
                j += 1
            if j < len(inner) and inner[j] == ',':
                i = j + 1
            else:
                i += 1
            continue
        if instring:
            current += c
        i += 1
    
    return strings


def build_js_string(s):
    """Build a JS single-quoted string, escaping as needed."""
    return "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"


def process_file(input_path, output_path):
    content = load_file(input_path)
    
    # Find the RECIPES array bounds
    arr_start = content.find('const RECIPES = [')
    if arr_start == -1:
        print("ERROR: RECIPES array not found")
        return False
    
    # Find the opening bracket of the array
    bracket_open = content.index('[', arr_start)
    
    # Find matching closing bracket
    depth = 0
    instring = False
    esc = False
    bracket_close = -1
    for i in range(bracket_open, len(content)):
        c = content[i]
        if esc: esc = False; continue
        if c == '\\': esc = True; continue
        if c == "'" and not instring: instring = True; continue
        if c == "'" and instring: instring = False; continue
        if instring: continue
        if c == '[': depth += 1
        elif c == ']':
            depth -= 1
            if depth == 0:
                bracket_close = i
                break
    
    if bracket_close == -1:
        print("ERROR: Could not find closing bracket")
        return False
    
    # Parse all recipe objects within the array
    arr_inner = content[bracket_open + 1:bracket_close]
    
    recipes = []
    pos = 0
    while pos < len(arr_inner):
        # Skip whitespace and commas
        while pos < len(arr_inner) and arr_inner[pos] in ' \t\n\r,':
            pos += 1
        if pos >= len(arr_inner):
            break
        
        if arr_inner[pos] == '{':
            obj_text, end = parse_recipe_object(arr_inner, pos)
            if obj_text:
                recipes.append(obj_text)
                pos = end
            else:
                print(f"ERROR parsing recipe at {pos}")
                pos += 1
        else:
            pos += 1
    
    print(f"Parsed {len(recipes)} recipe objects")
    
    # Transform each recipe
    changed = 0
    new_recipes = []
    
    for recipe_text in recipes:
        # Extract fields
        rid = extract_field(recipe_text, 'id') or 'unknown'
        rname = extract_field(recipe_text, 'name') or 'Unknown'
        rtype = extract_field(recipe_text, 'type') or 'espresso'
        steps_arr_text = extract_field(recipe_text, 'steps')
        
        if not steps_arr_text:
            new_recipes.append(recipe_text)
            continue
        
        old_steps = parse_array_strings(steps_arr_text)
        if not old_steps:
            new_recipes.append(recipe_text)
            continue
        
        all_steps_str = " | ".join(old_steps)
        
        new_steps = []
        recipe_changed = False
        for step in old_steps:
            new_step = transform_step(step, rtype, rname, rid, all_steps_str)
            if new_step != step:
                recipe_changed = True
            new_steps.append(new_step)
        
        if recipe_changed:
            changed += 1
            # Rebuild the steps array
            new_steps_arr = "[" + ",".join(build_js_string(s) for s in new_steps) + "]"
            # Replace in recipe text
            old_steps_pattern = r"steps\s*:\s*\["
            m = re.search(old_steps_pattern, recipe_text)
            if m:
                prefix = recipe_text[:m.end()]
                # Find the matching closing bracket of the steps array
                depth = 0
                instring = False
                esc = False
                close_pos = -1
                for i in range(m.end() - 1, len(recipe_text)):
                    c = recipe_text[i]
                    if esc: esc = False; continue
                    if c == '\\': esc = True; continue
                    if c == "'" and not instring: instring = True; continue
                    if c == "'" and instring: instring = False; continue
                    if instring: continue
                    if c == '[': depth += 1
                    elif c == ']':
                        depth -= 1
                        if depth == 0:
                            close_pos = i
                            break
                
                if close_pos >= 0:
                    suffix = recipe_text[close_pos + 1:]
                    new_recipe = prefix[:-1] + new_steps_arr + suffix
                else:
                    new_recipe = recipe_text
            else:
                new_recipe = recipe_text
            new_recipes.append(new_recipe)
        else:
            new_recipes.append(recipe_text)
    
    print(f"Recipes changed: {changed}/{len(recipes)}")
    
    # Rebuild the file
    prefix = content[:bracket_open + 1]
    suffix = content[bracket_close:]
    new_arr_inner = ",\n".join(new_recipes)
    new_content = prefix + new_arr_inner + suffix
    
    # Verify
    orig_steps = content.count('steps:')
    new_steps = new_content.count('steps:')
    print(f"Steps count: {orig_steps} -> {new_steps}")
    
    if orig_steps != new_steps:
        print("ERROR: steps count mismatch!")
        save_file(output_path + ".debug", new_content)
        return False
    
    save_file(output_path, new_content)
    print(f"Saved to {output_path}")
    
    # Quick validation
    recipe_count = len(re.findall(r"\{id:'[^']+',name:'[^']+',type:'", new_content))
    print(f"Recipe id/name/type patterns in output: {recipe_count}")
    
    return True


if __name__ == '__main__':
    inp = sys.argv[1] if len(sys.argv) > 1 else '/root/ninja-luxe-cafe/index.html'
    out = sys.argv[2] if len(sys.argv) > 2 else '/root/ninja-luxe-cafe/index_new.html'
    
    shutil.copy2(inp, inp + '.bak2')
    print(f"Backup at {inp}.bak2")
    
    ok = process_file(inp, out)
    sys.exit(0 if ok else 1)
