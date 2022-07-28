from spam.surbl import SurblChecker
checker = SurblChecker()

# google.com is a good domain
print(checker.check_domain("https://google.com"))
