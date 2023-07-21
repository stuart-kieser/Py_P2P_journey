import random


def test_tx():
    amount = random.randint(10, 100)
    accounts = ["abc", "def", "ghi", "qwd", "gtr"]
    first_account = random.choice(accounts)
    remaining_accounts = [account for account in accounts if account != first_account]
    second_account = random.choice(remaining_accounts)
    tx = str(first_account), str(amount), str(second_account)
    return tx
