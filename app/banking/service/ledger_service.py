from app.banking.service.account_service import AccountService

accountService = AccountService()

class LedgerService:

    allTransactions = [
        {
            "account_id": "1",
            "transaction_id": "1",
            "transaction_type": "deposit",
            "amount": 2000
        },
        {
            "account_id": "1",
            "transaction_id": "2",
            "transaction_type": "withdrawal",
            "amount": 1000
        },
        {
            "account_id": "2",
            "transaction_id": "3",
            "transaction_type": "deposit",
            "amount": 1000
        },
        {
            "account_id": "2",
            "transaction_id": "4",
            "transaction_type": "withdrawal",
            "amount": 500
        }
    ]

    def get_all_transactions(self):
        return self.allTransactions
    
    def get_transactions_by_account_id(self, account_id):
        return [transaction for transaction in self.allTransactions if transaction["account_id"] == account_id]
    
    def get_transactions_by_type(self, transaction_type):
        return [transaction for transaction in self.allTransactions if transaction["transaction_type"] == transaction_type]
    
    def reverse_transaction(self, transaction_id):
        for transaction in self.allTransactions:
            if transaction["transaction_id"] == transaction_id:
                if transaction["transaction_type"] == "withdrawal":
                    transaction["transaction_type"] = "deposit"
                else:
                    transaction["transaction_type"] = "withdrawal"
                return transaction
        
        return None
    
    def get_transaction_summary_by_account_id(self, account_id):
        if not any(transaction["account_id"] == account_id for transaction in self.allTransactions):
            return {"error": "Account id not found"}
        
        transactions = self.get_transactions_by_account_id(account_id)
        
        totalDeposits, totalWithdrawals, numberOfDeposits, numberOfWithdrawals = 0, 0, 0, 0
        
        for transaction in transactions:
            if transaction["transaction_type"] == "deposit":
                totalDeposits += transaction["amount"]
                numberOfDeposits += 1
            else:
                totalWithdrawals += transaction["amount"]
                numberOfWithdrawals += 1
        
        return {
            "total_deposits": totalDeposits,
            "total_withdrawals": totalWithdrawals,
            "number_of_deposits": numberOfDeposits,
            "number_of_withdrawals": numberOfWithdrawals
        }
    

    def validate_account_balance(self, account_id: str):
        balance = accountService.get_balance(account_id)

        acountTransactions = self.get_transactions_by_account_id(account_id)

        balanceFromTransactions = 0
        for transaction in acountTransactions:
            if transaction["transaction_type"] == "deposit":
                balanceFromTransactions += transaction["amount"]
            else:
                balanceFromTransactions -= transaction["amount"]

        return{
            "accountId": account_id,
            "accountBalance": balance,
            "balanceFromTransactions": balanceFromTransactions,
            "isValid": balance == balanceFromTransactions
        } 