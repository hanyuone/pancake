def pancake_print(form):
    if isinstance(form, list):
        items = ' '.join([str(x) for x in form])
        return f"[ {items} ]"
    else:
        return str(form)
