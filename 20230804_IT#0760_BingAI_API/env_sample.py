def get_env_variable(key):

    env_variable_dict = {

        "BING_AI_API_KEY" : "xxxx",
    }
    ret_val = env_variable_dict.get(key, None)
    return ret_val