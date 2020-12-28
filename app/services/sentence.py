def process_sentence(text_full, text_part):
    i = text_full.find(text_part)
    return text_full[:i] + '[...]' + text_full[i+len(text_part):]
