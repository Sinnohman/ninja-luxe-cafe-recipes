import re, sys
sys.path.insert(0, '/root/ninja-luxe-cafe')

with open('/root/ninja-luxe-cafe/index_new.html') as f:
    content = f.read()

def find_steps(content, recipe_id):
    m = re.search(r"\{id:'" + recipe_id + r"',name:'([^']+)'", content)
    if not m: return None, []
    ridx = m.start()
    sm = re.search(r'steps:', content[ridx:ridx+800])
    if not sm: return m.group(1), []
    skw = ridx + sm.start()
    bpos = content.find('[', skw)
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
    # Parse steps
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

# Check key edge cases
for rid in ['con-panna', 'coffee-frappe', 'mocha-frappe', 'caramel-frappe',
            'vanilla-sweet-cream', 'irish-coffee', 'flat-white', 'affogato']:
    name, steps = find_steps(content, rid)
    if name is None:
        print(f"{rid}: NOT FOUND")
        continue
    print(f"\n{name} ({rid}):")
    for i, s in enumerate(steps):
        print(f"  [{i}] {s}")
