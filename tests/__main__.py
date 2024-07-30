if __name__ == "__main__":
    from pytest import main
    from sys import path
    from os import path as os_path

    tests_dir = os_path.dirname(__file__)

    path.insert(0, tests_dir)
    path.insert(0, os_path.join(tests_dir, "..", "app"))

    exit(main())
