def get_env_variable(key):

    env_variable_dict = {

        "OPEN_AI_KEY" : "sk-xxxx",
    }
    ret_val = env_variable_dict.get(key, None)
    return ret_val