

try:
    from cryptage.crypt import echange_cle_client, decode_str, code_str, echange_cle_serveur
    print("Import successful!")
except ImportError as e:
    print(f"ImportError: {e}")
