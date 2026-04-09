def log_generation(tokens):
    steps = []
    for t in tokens:
        steps.append(f"Processing: {t}")
    return steps
