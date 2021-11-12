def scopeExists(db, scope):
    scopes = db.secret.list_scopes()

    scopes = scopes.get("scopes")

    if scopes:
        for _scope in scopes:
            if _scope["name"] == scope:
                return True
    return False

def createScope(db, scope):
    if scopeExists(db, scope):
        print(f"Scope {scope} already exists, skipping creation.")
    else:
        print(f"Scope {scope} doesn't exist, creating...")
        db.secret.create_scope(scope)
        if scopeExists(db, scope):
            print(f"\t...Scope {scope} created.")
        else:
            raise Exception(f'Scope {scope} could not be created')

def deleteScope(db, scope):
    if scopeExists(db, scope):
        print(f"Deleting Secret Scope {scope}...")
        db.secret.delete_scope(scope)
        print(f"\t...deleted")
    else:
        print(f"Couldn't delete Scope {scope} as it doesn't exist.")
            
def secretExists(db, scope, secret):
    secrets = db.secret.list_secrets(scope)

    secrets = secrets.get("secrets")

    if secrets:
        for _secret in secrets:
            if _secret["key"] == secret:
                return True
    return False

def createSecret(db, scope, secret, value):
    if secretExists(db, scope, secret):
        print(f"Secret {secret} already exists in {scope}, updating...")
    else:
        print(f"Secret {secret} already exists in {scope}, creating...")

    db.secret.put_secret(scope=scope,
                         key=secret,
                         string_value=value)

    if secretExists(db, scope, secret):
        print(f"\t...Secret {secret} in {scope} created.")
    else:
        raise Exception(f'Scope {secret} in {scope} could not be created')    

def createMLSecrets(db, scope, prefix, host, token, workspace_id):
    createSecret(db, scope, f"{prefix}-host", host)
    createSecret(db, scope, f"{prefix}-token", token)
    createSecret(db, scope, f"{prefix}-workspace-id", workspace_id)