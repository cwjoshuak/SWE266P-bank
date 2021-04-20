# Project Information: Spring 2021

In this course project, you will construct a software system that implements a shared specification, identify vulnerabilities in another system that implements the same specification, and then fix vulnerabilities in your own system. You are given a description of a software system, and you have to develop that program (the build phase). Then you inspect the code written from the other teams searching for flaws and vulnerabilities (the evaluate phase). Finally, you collect feedback about your code from other teams, and you try to fix the vulnerabilities (the fix phase).

You will take the role of a team of up to 4 developers and experience the different stages (or cycles) of secure software development.

In the evaluate phase, we will share the implementations among all teams, and you have the opportunity to find exploitable bugs in the code of all other students. In the third phase, you have the opportunity to fix any discovered bugs. While for this class project, we only pass through the life-cycle once, in practice it is repeated indefinitely due to new features being developed or deeper bugs being found in the existing code.

## Stages of Secure Software Development

### Build Phase

During the build phase, teams have to inject (size of team)+1 exploitable vulnerabilities in their code. Thus, if you have two team members, you need to inject three vulnerabilities. You may choose any Android or Web vulnerabilities.

Using source code obfuscation techniques as a protection mechanism against code auditing, are not allowed, as they are out of scope of this project. Furthermore, the style and readability of the code is part of the evaluation since this project aims to simulate a life-cycle in the development of maintainable software. Comments and variable names should be in English to ensure that everyone in the class can read them.

### Evaluate Phase

Once you have finished the build phase, the source code of all of the projects, will be given to all teams, so they can start looking for bugs in other team’s source code.

During this phase, your goal is to reverse engineer code from other teams and look for weaknesses, vulnerabilities, and exploits. Your goal here is to find and exploit as many bugs as possible for each other's project. Every team needs to find, document, and report 1 weaknesses per team member. If there are 4 team members, you must find 4 weaknesses from any app. Every team needs to find 1 vulnerability and exploit for it.

You are not allowed to exploit your own team’s vulnerabilities. 😊

### Fix Phase

In the 3rd, and final phase, each team receives a list containing all the bugs (i.e., weaknesses and vulnerabilities) that have been found during previous phases. The goal of this phase is to patch a number of discovered bugs equal to the size of your team and to release a new version. For example, if you have 4 team members, you need to patch at least 4 discovered bugs. If other teams did not report enough bugs in your bank, then you need to fix all the discovered bugs. Beyond that, the team has to fix all the original vulnerabilities that were inserted in the code during the 1st phase.

When receiving a new issue, you have to validate each exploit and determine its impact. You should write a security report for your project which provides an overview of all exploits, bugs, weaknesses, or vulnerabilities and how they are fixed.

The goal for each team is to mitigate all of the previous working exploits at the end of this phase.

## Requirements

### Valid Inputs

- Any input that is not valid according to the rules below should result in a string “invalid_input” that is shown on the screen.

- Numeric inputs are positive and provided in decimal without any leading `0`’s (should match `/(0|[1-9][0-9]\*)/`). Thus `42` is a valid input number but the octal `052` or hexadecimal `0x2a` are not. Any reference to “number” below refers to this input specification.

- Balances and currency amounts are specified as a number indicating a whole amount and a fractional input separated by a period.
  The fractional input is in decimal and is always two digits and thus can include a leading `0` (should match `/[0-9]{2}/`).
  The interpretation of the fractional amount v is that of having value equal to v/100 of a whole amount (akin to cents and dollars in US currency). Command line input amounts are bounded from `0.00` to `4294967295.99` inclusively but an account may accrue any non-negative balance over multiple transactions.

- Account names and passwords are restricted to underscores, hyphens, dots, digits, and lowercase alphabetical characters (each character should match `/[_\\-\\.0-9a-z]/`). Account names and passwords are to be between `1` and `127` characters long.

### Outputs

- Correct output based on different operations (e.g., registration, deposit) should be displayed on screen. Numbers (including potentially unbounded account balances) should be shown with full precision.
