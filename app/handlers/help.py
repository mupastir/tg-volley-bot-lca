def help_handler() -> str:
    with open("data/basic.data", "r") as file:
        basic_data = file.readlines()

    return "".join(basic_data).replace("|", " - ")
