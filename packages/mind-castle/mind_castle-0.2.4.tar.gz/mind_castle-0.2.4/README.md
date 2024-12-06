# Mind-Castle - Build a wall around your secrets

A universal secret store for sqlalchemy.

Currently supports:
- HashiCorp Vault
- AWS Secrets Manager
- In-memory and JSON stores that should only be used for testing

## Install

`pip install mind-castle`


## Configure

You can configure mind-castle by setting environment variables for your chosen secret store. To see what configuration options are required for each store:

```bash
$ python -m mind_castle

Mind-Castle - Shhhhh
====================
Available secret stores:

memory            - Required env vars: []
awssecretsmanager - Required env vars: ['MIND_CASTLE_AWS_REGION', 'MIND_CASTLE_AWS_ACCESS_KEY_ID', 'MIND_CASTLE_AWS_SECRET_ACCESS_KEY']
hashicorpvault    - Required env vars: ['MIND_CASTLE_VAULT_HOST', 'MIND_CASTLE_VAULT_PORT', 'MIND_CASTLE_VAULT_TOKEN']
json              - Required env vars: []
```

## Use

In your model file:

```python
from mind_castle.sqlalchemy import SecretData

class MyDBModel(Base):
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    secret_data = Column(SecretData("hashicorpvault"))
```

Your secrets are now safely stored in Vault (or AWS, or anywhere else)!


## TODO

- Create migration script (must work for json and non-json columns)
- Add precommit
- Support deleting secrets when row is deleted
- Delete secrets after test and/or mock cloud clients for unit tests
- Implement prefixes/folders for secrets
- Explain how secrets are stored in the readme