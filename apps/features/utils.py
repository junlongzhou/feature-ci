def unique_fci_id(prefix, db_id, maximum_len):
    return f'{prefix}{str(db_id).zfill(maximum_len - len(prefix))}'
