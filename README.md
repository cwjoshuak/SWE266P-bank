# SWE 266P Course Project: Online Banking Application

## Project Description

A deliberately insecure web application with 4 exploitable vulnerabilities. The goal of this project is to construct a software system that implements a shared specification, identify vulnerabilities in another system that implements the same specification, and then fix vulnerabilities in your own system.

[Additional Project Information](./Project_Information.md)

## Features

A web application for online banking.

- Allow customers to:
  - Register and open an account with initial balance
  - Login to check their balance
  - Withdraw and deposit money from their account
- Maintain customer data
- Keep track of customer balances

## Develop / Run

```bash
# instantiate venv
$ python3 -m venv venv

# on macOS
$ source ./venv/bin/activate

# on Windows
$ venv\Scripts\activate

# install dependencies
$ pip install -r "requirements.txt"

$ export FLASK_APP=bank.py  # on Windows use set instead of export
$ flask run
```

If developing, enable development mode:
`$ export FLASK_ENV=development`

### Adding new dependencies

After installing new dependencies, run `pip freeze >"requirements.txt`, add/commit.

## Oracle

Here are some typical scenarios of bank. Note that these scenarios are neither thorough nor complete.

- Scenario: valid registration
```
Given the username, password, and initial balance are all valid
    When I register with the above valid input
    Then an account under the username should be opened with the initial balance
```

- Scenario: invalid registration
```
Given one or more of the username, password, and initial balance are invalid
    When I register with the above valid input
    Then "invalid_input" should be shown on screen
      And no account should be opened
```

- Scenario: failed login
```
Given the username or password are nonexistent or incorrect
    When I log in to the bank with the above invalid input
    Then the login should fail
```

- Scenario: authorized deposit
```
Given I am a registered customer
    When I successfully log in to the bank with my username and password
      And I deposit with a valid amount
    Then I should know the deposit is successful
      And I should see my current balance after the deposit
```

- Scenario: authorized and valid withdrawal
```
Given I am a registered customer
    When I successfully log in to the bank
      And I withdraw an amount smaller or equal to my current balance
    Then I should know the withdrawal is successful
      And I should see my current balance after the withdrawal
```

- Scenario: authorized and invalid withdrawal
```
Given I am a registered customer
    When I successfully log in to the bank
      And I withdraw an amount larger than my current balance
    Then I should know the withdrawal is failed
```

- Scenario: authorized balance query
```
Given I am a registered customer
    When I successfully log in to the bank
      And I check my balance
    Then I should see my current balance
```
