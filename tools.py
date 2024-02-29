def fix_title(title):
    return ((title.replace('?', '').replace('?', '').replace('"', '').replace('!', '')
            .replace(':', '').replace('>', '').replace('*', '').replace('/', ''))
            .replace('\\', '').replace('<', '').replace('|', ''))
