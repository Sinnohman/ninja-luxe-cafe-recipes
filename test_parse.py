import re

with open('/root/ninja-luxe-cafe/index.html') as f:
    content = f.read()

def has_machine_detail(text):
    lower = text.lower()
    indicators = [
        'luxe basket', 'double basket', 'barista assist', 'auto-grinds',
        'ninja milk jug', 'press brew', 'cold-pressed on the dial',
        'brew over ice', 'quad on the dial', 'classic on the dial',
        'rich on the dial', 'cold brew on the control panel',
        'drip coffee filter basket', 'size button', 'group head',
        'place the whisk in the lid', 'select steamed milk on the frother',
        'select thick froth on the frother', 'select cold foam on the frother',
        'select thin froth on the frother',
    ]
    return any(ind in lower for ind in indicators)

def transform_step(step, recipe_type, recipe_name, recipe_id, all_steps_str):
    text = step.strip()
    lower = text.lower()
    
    if has_machine_detail(text):
        return text, False
    
    # Rule 1: "Pull a [X] espresso/ristretto shot"
    if re.search(r'pull\s+a\s+(?:single|double|quad(?:ruple)?)?\s*(?:espresso|ristretto)\s+shot', lower):
        if 'quad' in lower:
            return "Select ESPRESSO mode, then QUAD on the dial. The machine pulls four shots automatically using the Luxe basket (18-20g).", True
        elif 'single' in lower:
            return "Select ESPRESSO mode. Use the Double basket (10-12g). Let Barista Assist recommend the grind size. The machine auto-grinds, doses, and tamps. Place your cup under the group head and press BREW.", True
        else:
            return "Select ESPRESSO mode. Use the Luxe basket (18-20g). Let Barista Assist recommend the grind size. The machine auto-grinds, doses, and tamps. Place your cup under the group head and press BREW.", True
    
    # Rule 2: "Select ESPRESSO mode" that's vague
    if re.search(r'^select\s+espresso\s+mode', lower):
        if 'basket' not in lower and 'brew' not in lower:
            return "Select ESPRESSO mode. Use the Luxe basket (18-20g). Let Barista Assist recommend the grind size. The machine auto-grinds, doses, and tamps. Press BREW.", True
        return text, False
    
    # Rule 3: "Select COLD PRESSED ESPRESSO mode"
    if re.search(r'select\s+cold.?pressed\s+espresso\s+mode', lower):
        return "Select ESPRESSO mode, then COLD-PRESSED on the dial. This uses cold water at high pressure. Use the Luxe basket (18-20g). Press BREW.", True
    
    # Rule 4: "Select COLD BREW"
    if re.search(r'select\s+cold\s+brew', lower):
        return "Press COLD BREW on the control panel. The machine recommends a coarse grind (23-25). Insert the drip filter basket. Select your size with the SIZE button and press BREW.", True
    
    # Rule 5: "Select BREW OVER ICE"
    if re.search(r'select\s+brew\s+over\s+ice', lower):
        return "Select ESPRESSO mode, then rotate the dial to BREW OVER ICE. Fill your cup with ice first. The machine adjusts extraction for ice dilution. Press BREW.", True
    
    # Rule 6: "Select COFFEE mode and brew"
    if re.search(r'select\s+coffee\s+mode', lower):
        return "Select COFFEE mode, then CLASSIC on the dial. Remove the portafilter and insert the drip coffee filter basket. Select your size with the SIZE button. Press BREW.", True
    
    # Rule 7: Generic "Froth milk on [SETTING]"
    froth_setting = re.search(r'(?:froth|select)\s+(?:milk\s+)?(?:on\s+)?(?:the\s+)?(?:milk\s+)?(?:frother|jug)?\s*(?:with\s+|on\s+|to\s+)?(STEAMED MILK|THICK FROTH|THIN FROTH|COLD FOAM)', text, re.IGNORECASE)
    if froth_setting:
        setting = froth_setting.group(1).upper()
        if setting == 'STEAMED MILK':
            return "Fill the Ninja milk jug to the LATTE line. Place the whisk in the lid, select STEAMED MILK on the frother, and press start. The machine froths hands-free.", True
        elif setting == 'THICK FROTH':
            return "Fill the Ninja milk jug to the CAPPUCCINO line. Place the whisk in the lid, select THICK FROTH on the frother, and press start. The machine froths hands-free.", True
        elif setting == 'THIN FROTH':
            return "Fill the Ninja milk jug to the LATTE line. Place the whisk in the lid, select THIN FROTH on the frother, and press start.", True
        elif setting == 'COLD FOAM':
            return "Fill the Ninja milk jug to the minimum line. Place the whisk in the lid, select COLD FOAM on the frother, and press start. The machine froths hands-free.", True
    
    # Rule 8: "Fill the milk jug to the [X] line" without whisk detail
    jug_match = re.search(r'fill\s+(?:the\s+)?(?:ninja\s+)?milk\s+jug\s+to\s+the\s+(LATTE|CAPPUCCINO|minimum)\s+line', text, re.IGNORECASE)
    if jug_match and 'whisk' not in lower:
        return text + ". Place the whisk in the lid, select the frother setting, and press start.", True
    
    # Rule 9: "Add hot water" / "Heat water separately"
    if re.search(r'(?:heat|add)\s+hot\s+water(?:\s+separately)?', lower):
        if 'blank' not in lower and 'kettle' not in lower:
            return "Use a separate kettle or run a blank espresso shot for hot water", True
    
    # Rule 10: "Pour over ice" / "Fill a glass with ice"
    if re.search(r'(?:fill|pour).*?(?:glass|cup).*?(?:with\s+)?ice', lower):
        if recipe_type in ('iced', 'cocktail') and 'brew over ice' not in all_steps_str.lower():
            if 'brew over ice' not in lower:
                return text + ". For best results, use the Brew Over Ice setting: select ESPRESSO mode, rotate dial to BREW OVER ICE.", True
    
    # Rule 11: "Sweeten to taste"
    if re.search(r'sweeten\s+to\s+taste', lower):
        return "Add your preferred syrup or sweetener to taste", True
    
    # Rule 12: Generic "Froth" or "Steam" standalone
    if re.match(r'^(?:Froth|Steam)\s', text):
        if 'thick' in lower or 'cappuccino' in lower:
            return "Fill the Ninja milk jug to the CAPPUCCINO line. Place the whisk in the lid, select THICK FROTH on the frother, and press start.", True
        elif 'cold' in lower:
            return "Fill the Ninja milk jug to the minimum line. Place the whisk in the lid, select COLD FOAM on the frother, and press start.", True
        else:
            return "Fill the Ninja milk jug to the LATTE line. Place the whisk in the lid, select STEAMED MILK on the frother, and press start.", True
    
    # Rule 13: "Steam about X oz milk"
    if re.search(r'(?:steam|froth)\s+about\s+\d+.?oz', lower):
        return "Fill the Ninja milk jug to the minimum line. Place the whisk in the lid, select STEAMED MILK on the frother, and press start.", True
    
    # Rule 14: "Froth a small amount of milk"
    if re.search(r'froth\s+a\s+small\s+amount\s+of\s+milk', lower):
        return "Fill the Ninja milk jug to the minimum line. Place the whisk in the lid, select STEAMED MILK on the frother, and press start.", True
    
    return text, False

def find_steps_bracket_end(content, start_pos):
    depth = 0
    in_string = False
    escape_next = False
    i = start_pos
    while i < len(content):
        c = content[i]
        if escape_next: escape_next = False; i += 1; continue
        if c == '\\': escape_next = True; i += 1; continue
        if c == "'": in_string = not in_string; i += 1; continue
        if in_string: i += 1; continue
        if c == '[': depth += 1
        elif c == ']':
            depth -= 1
            if depth == 0: return i
        i += 1
    return -1

def parse_step_strings(steps_inner):
    steps = []
    current = ''
    in_string = False
    escape_next = False
    i = 0
    while i < len(steps_inner):
        c = steps_inner[i]
        if escape_next:
            if c == "'": current += c
            else: current += '\\' + c
            escape_next = False; i += 1; continue
        if c == '\\':
            escape_next = True; i += 1; continue
        if c == "'" and not in_string:
            in_string = True; i += 1; continue
        if c == "'" and in_string:
            in_string = False
            j = i + 1
            while j < len(steps_inner) and steps_inner[j] in ' \t\n\r': j += 1
            if j < len(steps_inner) and steps_inner[j] == ',': i = j + 1
            else: i += 1
            steps.append(current); current = ''; continue
        if in_string: current += c
        i += 1
    if current.strip(): steps.append(current)
    return steps

def rebuild_steps_array(steps):
    step_strings = []
    for step in steps:
        escaped = step.replace("\\", "\\\\").replace("'", "\\'")
        step_strings.append(f"'{escaped}'")
    return "[" + ",".join(step_strings) + "]"

# Test espresso recipe
m = re.search(r"\{id:'espresso',name:'([^']+)'", content)
rstart = m.start()
print(f"Recipe: {m.group(1)} at pos {rstart}")

sm = re.search(r"steps:", content[rstart:rstart + 800])
skw = rstart + sm.start()
rest = content[skw + 6:]
bpos = rest.find('[')
bracket_abs = skw + 6 + bpos
cpos = find_steps_bracket_end(content, bracket_abs)
steps_inner = content[bracket_abs + 1:cpos]

old_steps = parse_step_strings(steps_inner)
print(f"\nOriginal {len(old_steps)} steps:")
for i, s in enumerate(old_steps):
    print(f"  [{i}]: '{s}'")

# Transform
all_steps_str = " | ".join(old_steps)
new_steps = []
for i, step in enumerate(old_steps):
    new_step, changed = transform_step(step, 'espresso', 'Espresso Single', 'espresso', all_steps_str)
    marker = " ***CHANGED" if changed else ""
    print(f"\n  Transform [{i}]: '{step[:60]}...' -> '{new_step[:60]}...'{marker}")
    new_steps.append(new_step)

print(f"\nNew steps count: {len(new_steps)}")
rebuilt = rebuild_steps_array(new_steps)
print(f"Rebuilt: {rebuilt[:200]}...")

# Check for empty
for i, s in enumerate(new_steps):
    if not s.strip():
        print(f"  EMPTY STEP at index {i}!")
