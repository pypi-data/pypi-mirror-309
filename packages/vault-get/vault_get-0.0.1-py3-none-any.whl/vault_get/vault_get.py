import argparse
import hvac
import logging
import os

DEFAULT_VAULT_ADDRESS = "https://127.0.0.1"
DEFAULT_VAULT_AUTH_PATH = "jwt"

VAR_NAME_VAULT_ADDR = "VAULT_ADDR"
VAR_NAME_VAULT_TOKEN = "VAULT_TOKEN"
VAR_NAME_VAULT_AUTH_PATH = "VAULT_AUTH_PATH"


log = logging.getLogger(__name__)
log_handler = logging.StreamHandler()
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_handler.setFormatter(log_formatter)
log.addHandler(log_handler)


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        prog='vault-get',
        description=f"Vault get secret. Simple hvac wrapper used to pull from hvault. Print kv-secret from vault to stdout.",
        epilog=f"""\n
Usage 
vault-get -m MyMountPoint -p my_secret_path -k my_secret_key\n\n
Examples:
    Use ${VAR_NAME_VAULT_ADDR} and ${VAR_NAME_VAULT_TOKEN} to access vault and auth:
        vault-get -m MyMountPoint -p my_secret_path -k my_secret_key
    Use JWT auth method in gitlab-ci job:
        vault-get -a https://vault.local -j $CI_JOB_JWT -r role_gitlab_ci -m MyMountPoint -p my_secret_path -k my_secret_key
""",
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        required=False,
        default=False,
        help=f"Set logging level to DEBUG. Warning: secrets will be revealed.",
    )
    group_auth = parser.add_argument_group(
        'Vault', f"If jwt-auth-role and jwt are not set uses ${VAR_NAME_VAULT_TOKEN} env variable for auth."
    )
    group_auth.add_argument(
        '-a',
        '--vault-address',
        type=str,
        required=False,
        default=os.getenv(VAR_NAME_VAULT_ADDR, DEFAULT_VAULT_ADDRESS),
        help=f"Vault address. Example \"https://vault.local\". Default=\"{DEFAULT_VAULT_ADDRESS}\"",
    )
    group_auth.add_argument(
        '-ap',
        '--auth-path',
        type=str,
        required=False,
        default=os.getenv(VAR_NAME_VAULT_AUTH_PATH, DEFAULT_VAULT_AUTH_PATH),
        help=f"Vault auth method auth path. Example \"jwt-test\". Default=\"{DEFAULT_VAULT_AUTH_PATH}\"",
    )
    group_auth.add_argument(
        '-r', '--jwt-auth-role', type=str, required=False, help="Auth role for jwt auth. Used in pair with --jwt."
    )
    group_auth.add_argument(
        '-j', '--jwt', type=str, required=False, help="JWT for jwt auth. Used in pair with --jwt-auth-role."
    )
    group_get_secret = parser.add_argument_group(
        'Get secret by path and key', f"Printout secret value by mount-point, secret-path and secret-key."
    )
    group_get_secret.add_argument(
        '-m', '--mount-point', type=str, required=True, help="Vault mount point. Example \"MyMountPoint\"."
    )
    group_get_secret.add_argument(
        '-p', '--secret-path', type=str, required=True, help="Vault secret path. Example \"my_super_secret\""
    )
    group_get_secret.add_argument(
        '-k', '--secret-key', type=str, required=True, help="Vault secret key. Example \"access_token\""
    )
    args = parser.parse_args()

    if args.verbose:
        log.setLevel(logging.DEBUG)

    log.debug(args)

    if args.jwt and args.jwt_auth_role:
        client = hvac.Client(url=args.vault_address)
        response = client.auth.jwt.jwt_login(role=args.jwt_auth_role, jwt=args.jwt, path=args.auth_path)
        log.debug(response)
        client.token = response['auth']['client_token']
    elif not args.jwt and not args.jwt_auth_role:
        client = hvac.Client(url=args.vault_address, token=os.getenv(VAR_NAME_VAULT_TOKEN))
    else:
        raise ValueError("--jwt and --jwt-auth-role should be used together.")

    log.debug(f"Is authenticated: {client.is_authenticated()}")

    if not client.is_authenticated():
        log.error(f"Could not authenticate on vault {args.vault_address}")
        exit(1)

    response = client.secrets.kv.v2.read_secret_version(path=args.secret_path, mount_point=args.mount_point)
    log.debug(response)
    secret = response['data']['data'][args.secret_key]

    print(secret)


if __name__ == "__main__":
    main()
