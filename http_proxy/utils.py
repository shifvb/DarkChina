import getopt
import sys


def usage(is_local):
    if is_local:
        print()
        print('DarkChina client_side help document')
        print('Usage: python3 ./server.py [option [value]]...')
        print('Options:')
        print('\t-h                         show this help document')
        print('\t-l local_addr              local binding address, default: 127.0.0.1')
        print('\t-b local_port              local binding port, default: 12306')
        print('\t-s server_addr             server address')
        print('\t-p server_port             server port, default: 2333')
        print('\t-V                         show current version')
    else:
        print('\nUsage: python3 ./server.py [option [value]]...\n')
        print('DarkChina server_side help document\n')
        print('Options:')
        print('\t-h                          show this help document')
        print('\t-s server_addr              server address, default: 0.0.0.0')
        print('\t-p server_port              server port, default: 2333')
        print('\t-V                          show current version')


def parse_args(is_local: bool, version: str) -> dict:
    config_dict = {}
    if is_local:  # is_local is True, local side
        args_dict, args_left = getopt.getopt(sys.argv[1:], 'hVl:b:s:p:', [])
        # set values
        for k, v in args_dict:
            if k == '-h':
                usage(is_local)
                sys.exit(0)
            elif k == '-V':
                print(version)
                sys.exit(0)
            elif k == '-l':
                config_dict["local_addr"] = v
            elif k == '-b':
                config_dict["local_port"] = int(v)
            elif k == '-s':
                config_dict["server_addr"] = v
            elif k == '-p':
                config_dict["server_port"] = int(v)

        # set default values
        config_dict.setdefault("local_addr", '127.0.0.1')
        config_dict.setdefault("local_port", 12306)
        if not config_dict.get("server_addr", None):
            print('\nServer address required!')
            usage(is_local)
            sys.exit(1)
        config_dict.setdefault("server_port", 2333)

    else:  # is_local is False, server side
        args_dict, args_left = getopt.getopt(sys.argv[1:], 'hVs:p:', [])
        # set values
        for k, v in args_dict:
            if k == '-h':
                usage(is_local)
                sys.exit(0)
            elif k == '-V':
                print(version)
                sys.exit(0)
            elif k == '-s':
                config_dict["server_addr"] = v
            elif k == '-p':
                config_dict["server_port"] = int(v)

        # set default values
        config_dict.setdefault("server_addr", '0.0.0.0')
        config_dict.setdefault("server_port", 2333)
    return config_dict


if __name__ == '__main__':
    result = parse_args(False, 'test version')
    print(result)