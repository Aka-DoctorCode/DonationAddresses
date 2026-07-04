import re

def kebab_to_camel(match):
    words = match.group(0).split('-')
    # Filter out empty strings from multiple hyphens
    words = [w for w in words if w]
    if not words: return match.group(0)
    return words[0] + ''.join(w.capitalize() for w in words[1:])

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Find class="..." in HTML and replace classes
    if filepath.endswith('.html'):
        def class_replacer(m):
            classes = m.group(1).split()
            new_classes = []
            for c in classes:
                if '-' in c:
                    c_clean = re.sub(r'-+', '-', c) # reduce multiple hyphens
                    parts = c_clean.split('-')
                    parts = [p for p in parts if p]
                    c_new = parts[0] + ''.join(p.capitalize() for p in parts[1:])
                    new_classes.append(c_new)
                else:
                    new_classes.append(c)
            return 'class="' + ' '.join(new_classes) + '"'
            
        content = re.sub(r'class="([^"]+)"', class_replacer, content)

    # Replace CSS variables everywhere
    def var_replacer(m):
        var_name = m.group(1)
        # remove prefix --
        var_body = var_name[2:]
        if '-' in var_body:
            parts = [p for p in var_body.split('-') if p]
            new_name = '--' + parts[0] + ''.join(p.capitalize() for p in parts[1:])
            return new_name
        return var_name

    content = re.sub(r'(--[a-zA-Z0-9-]+)', var_replacer, content)

    # In CSS, replace class selectors
    if filepath.endswith('.css'):
        def css_class_replacer(m):
            c = m.group(1)
            c_clean = re.sub(r'-+', '-', c)
            parts = c_clean.split('-')
            parts = [p for p in parts if p]
            return '.' + parts[0] + ''.join(p.capitalize() for p in parts[1:])
        
        content = re.sub(r'\.([a-zA-Z0-9-]+)(?=[ {:,])', css_class_replacer, content)

    with open(filepath, 'w') as f:
        f.write(content)

process_file('/Users/franciscomolina/Dev/DonationAddresses/index.html')
process_file('/Users/franciscomolina/Dev/DonationAddresses/index.css')
print("Done")
