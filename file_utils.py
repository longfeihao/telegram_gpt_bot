import yaml


def load_bot_conf():
    with open('./configs/bot.yaml', 'r') as f:
        bot_conf = yaml.safe_load(f)
    return bot_conf


def load_gpt_conf():
    with open('./configs/gpt.yaml', 'r') as f:
        gpt_conf = yaml.safe_load(f)
    return gpt_conf


if __name__ == '__main__':
    bot_conf = load_bot_conf()
    print(bot_conf)

    gpt_conf = load_gpt_conf()
    print(gpt_conf)

