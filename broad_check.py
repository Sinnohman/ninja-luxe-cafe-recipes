"""Quick broad check - spot-check ~30 recipes across all types."""
import re

with open('/root/ninja-luxe-cafe/index_new.html') as f:
    content = f.read()

def get_steps(content, recipe_id):
    m = re.search(r"\{id:'" + recipe_id + r"',name:'([^']+)'", content)
    if not m: return None, []
    ridx = m.start()
    sm = re.search(r'steps:', content[ridx:ridx+800])
    if not sm: return m.group(1), []
    skw = ridx + sm.start()
    bpos = content.find('[', skw)
    if bpos < 0: return m.group(1), []
    depth = 0; instring = False; esc = False; cpos = -1
    for i in range(bpos, len(content)):
        c = content[i]
        if esc: esc = False; continue
        if c == '\\': esc = True; continue
        if c == "'" and not instring: instring = True; continue
        if c == "'" and instring: instring = False; continue
        if instring: continue
        if c == '[': depth += 1
        elif c == ']':
            depth -= 1
            if depth == 0: cpos = i; break
    if cpos < 0: return m.group(1), []
    raw = content[bpos+1:cpos]
    steps = []
    cur = ''; ins = False; es = False; i = 0
    while i < len(raw):
        c = raw[i]
        if es: cur += c; es = False; i += 1; continue
        if c == '\\': es = True; i += 1; continue
        if c == "'" and not ins: ins = True; i += 1; continue
        if c == "'" and ins:
            ins = False; steps.append(cur); cur = ''
            j = i + 1
            while j < len(raw) and raw[j] in ' \t\n\r,': j += 1
            i = j; continue
        if ins: cur += c
        i += 1
    return m.group(1), steps

# Check across all types
checks = [
    # espresso
    'espresso', 'espresso-double', 'americano', 'ristretto', 'lungo', 'long-black', 'red-eye',
    # milk
    'latte', 'cappuccino', 'flat-white', 'cortado', 'macchiato', 'latte-macchiato', 'mocha', 'white-mocha',
    'caramel-macchiato', 'dirty-chai', 'cafe-au-lait', 'breve-latte', 'hazelnut-mocha', 'nutella-latte',
    # iced
    'iced-latte', 'iced-mocha', 'iced-cappuccino', 'iced-americano', 'cold-brew',
    'iced-shaken-espresso', 'brown-sugar-shaken', 'espresso-tonic', 'vietnamese-iced-coffee',
    # specialty
    'pumpkin-spice-latte', 'peppermint-mocha', 'honey-lavender-latte', 'tiramisu-latte',
    # blended
    'coffee-frappe', 'mocha-frappe',
    # cocktails
    'espresso-martini', 'white-russian', 'affogato', 'irish-coffee',
    # tea
    'london-fog', 'hot-chocolate', 'matcha-latte', 'chai-latte', 'vanilla-steamer',
    # sugar-free
    'sf-vanilla-latte', 'skinny-mocha',
    # cold foam
    'cold-foam-vanilla', 'cold-foam-caramel',
]

issues = 0
for rid in checks:
    name, steps = get_steps(content, rid)
    if name is None:
        print(f"MISSING: {rid}")
        issues += 1
        continue
    
    # Check for machine detail in at least one step
    has_detail = any(
        any(ind in s.lower() for ind in [
            'luxe basket', 'double basket', 'ninja milk jug', 'press brew', 
            'group head', 'cold-pressed on the dial', 'brew over ice',
            'cold brew on the control panel', 'coffee mode', 'classic on the dial',
            'froth', 'whisk in the lid', 'barista assist', 'auto-grinds',
            'drip coffee filter', 'size button'
        ])
        for s in steps
    )
    
    status = '✓' if has_detail else '✗'
    if not has_detail:
        issues += 1
    print(f"{status} {name} ({rid}): {len(steps)} steps")

print(f"\nTotal issues: {issues}")
