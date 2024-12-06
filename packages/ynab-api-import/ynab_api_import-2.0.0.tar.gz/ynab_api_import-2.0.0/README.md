# ynab-api-import

[![GitHub Release](https://img.shields.io/github/release/dnbasta/ynab-api-import?style=flat)]() 
[![Github Release](https://img.shields.io/maintenance/yes/2100)]()
[![Monthly downloads](https://img.shields.io/pypi/dm/ynab-api-import)]()

[!["Buy Me A Coffee"](https://img.shields.io/badge/Buy_Me_A_Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://www.buymeacoffee.com/dnbasta)

This library enables importing YNAB transactions via the 
[Gocardless Bank Account Data API (formerly Nordigen)](https://gocardless.com/bank-account-data/). 
It is pretty helpful for cases in which your bank is not covered by YNABs native import functionality.

## Preparations
### Gocardless Bank Account API (formerly Nordigen)
1. [Check](https://gocardless.com/bank-account-data/coverage/) if your bank is supported by the API.
2. Create an account with Gocardless for the Bank Account Data API (They have a separate Login for it which you can 
   get to by clicking on 'Get API Keys' or clicking the link at the bottom of their standard login page)
3. Go to Developers -> User Secrets and create a new pair of secret_id and secret_key
### YNAB
1. Create a personal access token for YNAB as described [here](https://api.ynab.com/)

## Basic Usage
### 1. Install library from PyPI

```bash
pip install ynab-api-import
```
### 2. Initiate Library
Provide a unique reference (e.g. `'mycheckingaccount'`)  per bank connection to identify the grant later on. 
You can find the IDs of your budget and the account if you go to https://app.ynab.com/ and open the target account 
by clicking on the name on the left hand side menu. The URL does now contain both IDs `https://app.ynab.
com/<budget_id>/accounts/<account_id>`
```py
from ynabapiimport import YnabApiImport
ynab_api_import = YnabApiImport(secret_id='<secret_id>', 
                                secret_key='<secret_key>',
                                reference='<reference>',
                                token='<ynab_token>',
                                budget_id='<budget_id>',
                                account_id='<account_id>')
```
Optionally you can initiate an object from a `config.yaml` file. To do that create a YAML file with the following 
content:
```yaml
secret_id: <secret_id>
secret_key: <secret_key>
reference: <reference>
token: <ynab_token>
budget_id: <budget_id>
account_id: <account_id>
```
Save the file and provide the path to the library when initializing
```py
ynab_api_import = YnabApiImport.from_yaml('path/to/config.yaml')
```
### 2. Find the institution_id of your bank
Countrycode is ISO 3166 two-character country code. 
```py

ynab_api_import.fetch_institutions(countrycode='<countrycode>')
```
You get back a dictionary with all available banks in that country, their institution_ids and the maximum days of 
transaction history provided by the bank. Find and save the institution_id of your bank.
```py
[{'name': '<name>', 'institution_id': '<institution_id>', 'max_history_days': 'ddd'}]
```

### 3. Create Auth Link and authenticate with your bank
Provide the institution_id. You get back a link which you need to copy to your browser and go through authentication 
flow with your bank. By default, the authorization will allow you to fetch 90 days of your transaction history. You can 
set the option `use_max_historical_days` to `True` in order to fetch longer transaction history. This is known to cause 
issues sometimes, so in case you get an 500 error from the Gocardless API try an authorization with default 90 days.
```py
ynab_api_import.create_auth_link(institution_id='<institution_id>')
```

### 4. Run import with your reference and YNAB identifiers
Optionally you can provide a `startdate` argument in form of a `datetime.date` object to only import transactions 
from a specific date onwards. Equally optionally you can provide a `memo_regex` argument in from of a regex string 
to the call to clean the memo string before importing into YNAB. A good helper to write your regex is  
https://regex101.com  
```py
ynab_api_import.import_transactions()
```
## Advanced Usage
### Handling of multiple accounts in your bank connection (`MultipleAccountsError`)
The library assumes that you have one active account in your bank connection. It will raise an error if there are no 
accounts in your connection or more than one. In the latter case you need to provide the correct `resource_id` when 
initializing the library. You can find the `resource_id` by looking into the available options in the error message.
```py
from ynabapiimport import YnabApiImport
ynab_api_import = YnabApiImport(resource_id='<resource_id>',
                                secret_id='<secret_id>', 
                                secret_key='<secret_key>',
                                reference='<reference>',
                                token='<ynab_token>',
                                budget_id='<budget_id>',
                                account_id='<account_id>')
```
### Compare balances
This method will fetch the available [balance variants](https://developer.gocardless.com/bank-account-data/balance) for your account from the API and compare them to the balance in YNAB. It compares the plain balance values as well as the balances minus the sum of still pending transactions. If none of them match it raises a `BalancesDontMatchError`
```py
ynab_api_import.compare_balances()
```
### Delete current bank authorization
By default you can create only one bank authorization per reference. If you need to replace the authorization under 
your current reference you can explicitly do that by setting the `delete_current_auth` option when creating an auth 
link.
```py
ynab_api_import.create_auth_link(institution_id='<institution_id>', delete_current_auth=True)
```
### Show Logs
The library logs information about the result of the methods on the 'INFO' level. If you want to see these logs 
import the logging module and set it to the level `INFO`. You can also access the logger for advanced configuration 
via the `logger` attribute of your `YnabApiImport`instance.
```py
import logging

logging.basicConfig(level='INFO')
```
### Testing your `memo_regex`
You can test your `memo_regex` with a call to `test_memo_regex()`. The function will fetch transactions from your 
bank account, apply the regex and output the old and new memo strings in a dictionary for inspection.
```py
ynab_api_import.test_memo_regex(memo_regex=r'<memo_regex')
```
returns a list of `dict` with following content
```
[{original_memo: cleaned_memo}]
```


