command_list = []
command_names = []

def register_command(cmd):
    print(cmd.name) # TODO remove
    command_list.append(cmd)
    command_names.append(cmd.name.lower())

def get_command_instance_by_name(command_name, client):
    command_name = command_name.lower()
    for c in command_list:
        if command_name == c.name:
            return c(client)
    return False

def get_command_by_name(command_name):
    command_name = command_name.lower()
    for c in command_list:
        if command_name == c.name:
            return c
    return False
