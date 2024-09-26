class AccountService:

    # make accounts static for now
    accounts = {
        "1": {
            "account_id": "1",
            "account_name": "Savings Account",
            "balance": 1000
        },
        "2": {
            "account_id": "2",
            "account_name": "Current Account",
            "balance": 500
        }
    }


    def get_balance(self, account_id):
        return self.accounts[account_id]["balance"]
    
    def get_account(self, account_id):
        return self.accounts[account_id]
    
    def deposit(self, account_id, amount):
        self.accounts[account_id]["balance"] += amount
        return self.accounts[account_id]
    
    def withdraw(self, account_id, amount):
        if account_id not in self.accounts:
            raise Exception("Account not found")
        
        if self.get_balance(account_id) < amount:
            raise Exception("Insufficient balance")
        
        self.accounts[account_id]["balance"] -= amount

        return self.accounts[account_id]