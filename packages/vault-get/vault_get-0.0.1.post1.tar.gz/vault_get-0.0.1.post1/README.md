# vault-get
Python hvac cli wrapper: get kv from hashicorp vault by auth token or jwt. 

# Why
This tool helps when you don't have access to vanilla hashicorp **vault** binary and need only to retrieve kv from vault.

# Usage

vault-get can be used to print kv secrets via token or jwt auth to stdout.

## vault auth token

```bash
export VAULT_TOKEN=xxx
export VAULT_ADDRESS=https://vault.local

vault-get -a $VAULT_ADDRESS -m MyMountPoint -p my_secret_path -k my_secret_key
topsecret
```

## jwt gitlab-ci
Check your vault authentication method to know auth path.

```bash
vault read auth/jwt-1
```

```yaml
varables:
  CI_JWT_ROLE: role_gitlab_ci
  VAULT_JWT_PATH: jwt-1

job01:
  stage: test
  id_tokens:
    VAULT_ID_TOKEN:
      aud: $VAULT_ADDR
  before_script:
    - export MY_VALUE="$(vault-get -a $VAULT_ADDR -j $VAULT_ID_TOKEN -ap $VAULT_JWT_PATH -r $CI_JWT_ROLE -m MyMountPoint -p my_secret_path -k my_secret_key)"
  script:
    - echo $MY_VALUE

```


## cli help

```bash
vault-get --help
usage: vault-get [-h] [-v] [-a VAULT_ADDRESS] [-ap AUTH_PATH] [-r JWT_AUTH_ROLE] [-j JWT] -m MOUNT_POINT -p SECRET_PATH -k SECRET_KEY

Vault get secret. Simple hvac wrapper used to pull from hvault. Print kv-secret from vault to stdout.

options:
  -h, --help            show this help message and exit
  -v, --verbose         Set logging level to DEBUG. Warning: secrets will be revealed.

Vault:
  If jwt-auth-role and jwt are not set uses $VAULT_TOKEN env variable for auth.

  -a VAULT_ADDRESS, --vault-address VAULT_ADDRESS
                        Vault address. Example "https://vault.local". Default="https://127.0.0.1"
  -ap AUTH_PATH, --auth-path AUTH_PATH
                        Vault auth method auth path. Example "jwt-test". Default="jwt"
  -r JWT_AUTH_ROLE, --jwt-auth-role JWT_AUTH_ROLE
                        Auth role for jwt auth. Used in pair with --jwt.
  -j JWT, --jwt JWT     JWT for jwt auth. Used in pair with --jwt-auth-role.

Get secret by path and key:
  Printout secret value by mount-point, secret-path and secret-key.

  -m MOUNT_POINT, --mount-point MOUNT_POINT
                        Vault mount point. Example "MyMountPoint".
  -p SECRET_PATH, --secret-path SECRET_PATH
                        Vault secret path. Example "my_super_secret"
  -k SECRET_KEY, --secret-key SECRET_KEY
                        Vault secret key. Example "access_token"

Usage 
vault-get -m MyMountPoint -p my_secret_path -k my_secret_key

Examples:
    Use $VAULT_ADDR and $VAULT_TOKEN to access vault and auth:
        vault-get -m MyMountPoint -p my_secret_path -k my_secret_key
    Use JWT auth method in gitlab-ci job:
        vault-get -a https://vault.local -j $CI_JOB_JWT -r role_gitlab_ci -m MyMountPoint -p my_secret_path -k my_secret_key
```

