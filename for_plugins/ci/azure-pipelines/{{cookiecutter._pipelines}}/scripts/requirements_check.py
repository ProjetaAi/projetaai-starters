from os.path import exists, join

base_requirements_path = join("src", "requirements.txt")
dev_requirements_path = join("src", "requirements-dev.txt")
test_requirements_path = join("src", "requirements-test.txt")

paths = [base_requirements_path, dev_requirements_path, test_requirements_path]

for path in paths:
    check_file = exists(path)
    if not check_file:
        print('Necessary path: "', path, '" not found!')
        exit(1)
