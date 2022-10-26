from algosdk import account, mnemonic


class Account:
    def __init__(self):
        self.private_key, _ = account.generate_account()

    def get_mnemonic(self):
        return mnemonic.from_private_key(self.private_key)
