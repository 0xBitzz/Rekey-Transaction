import json
from algosdk import mnemonic
from algosdk.v2client import algod
from algosdk.future.transaction import *
import account_generator
from account_generator import Account


def rekey_example():
    # Create algod client
    algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    algod_address = "http://localhost:4001"
    algod_client = algod.AlgodClient(algod_token, algod_address)

    # Msig mnemonics
    msig1_address = mnemonic.to_public_key(Account().get_mnemonic())
    msig2_address = mnemonic.to_public_key(Account().get_mnemonic())
    msig3_address = mnemonic.to_public_key(Account().get_mnemonic())

    msig = Multisig(version=1, threshold=2, addresses=[msig1_address, msig2_address, msig3_address])
    account2 = msig.address()

    # Create other accounts
    account1_passphrase = Account().get_mnemonic()
    account3_passphrase = Account().get_mnemonic()

    account1 = mnemonic.to_public_key(account1_passphrase)
    account3 = mnemonic.to_public_key(account3_passphrase)

    print("Account 1 Address: ", account1)
    print('Go to the below link to fund the created account using testnet faucet: \nhttps://dispenser.testnet.aws.algodev.network/?account={}'.format(account1))
    input(f"Hit any key to continue")
    print("Account 2 Address: ", account2)
    print('Go to the below link to fund the created account using testnet faucet: \nhttps://dispenser.testnet.aws.algodev.network/?account={}'.format(account2))
    input(f"Hit any key to continue")
    print("Account 3 Address: ", account3)
    print('Go to the below link to fund the created account using testnet faucet: \nhttps://dispenser.testnet.aws.algodev.network/?account={}'.format(account3)) 
    input(f"Hit any key to continue")

    # Build transaction
    params = algod_client.suggested_params()

    # Opt in
    amount = int(0)
    rekey_account = account1
    sender = account3
    receiver = account3
    unsigned_txn = PaymentTxn(sender, params, receiver, amount, None, None, None, rekey_account)
    
    # Sign transaction
    signed_txn = unsigned_txn.sign(mnemonic.to_private_key(account3_passphrase))
    txid = algod_client.send_transaction(signed_txn)
    print(f"Transaction signed with id {txid}")

    # Wait for confirmation
    confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
    print(f"Transaction with id {txid} confirmed in {confirmed_txn['confirmed-round']} rounds")

    # Read transaction
    try:
        confirmed_txn = algod_client.pending_transaction_info(txid)
        account_info = algod_client.account_info(account3)
    except Exception as err:
        print(err)
        print(f"Transaction information {json.dumps(confirmed_txn, indent=4)}")
        print(f"Account information {json.dumps(account_info, indent=4)}")

    # Send 1A from account 3 to account 2
    amount = int(1000000)
    sender = account3
    receiver = account(2)
    unsigned_txn = PaymentTxn(sender, params, receiver, amount, None, None, None, rekey_account)

    # Sign transaction
    signed_txn = unsigned_txn.sign(mnemonic.to_private_key(account1_passphrase))
    txid = algod_client.send_transaction(signed_txn)
    print(f"Transaction signed with id {txid}")

    # Confirm transaction
    confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
    print(f"Transaction with id {txid} confirmed in {confirmed_txn['confirmed-round']} rounds")
    account_info_rekey = algod_client.account_info(account3)
    print("Account 3 information (from) : {}".format(
    json.dumps(account_info_rekey, indent=4)))
    account_info_rekey = algod_client.account_info(account2)
    print("Account 2 information (to) : {}".format(
    json.dumps(account_info_rekey, indent=4)))



rekey_example()
