

from .pyReqCheck import *
import argparse

parser = argparse.ArgumentParser(
    description="Script for checking if all imports are in requirements.txt"
)
parser.add_argument(
    "-ignore",
    "--ignore-modules",
    nargs="+",
    type=str,
    required=False,
    default=[],
    action="store",
    help="name of modules to ignore",
)
args = parser.parse_args()


def main():
    imports = get_all_imports(
        ".",
        encoding=None,
        extra_ignore_dirs=["requirements_check"],
        follow_links=True,
        ignore_modules=args.ignore_modules,
    )

    requirements = []
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for f in files:
        if f.endswith(".txt"):
            requirements.extend(parse_requirements(f))
            print(f)

    package_names = [package["name"] for package in requirements]
    compare_lists(imports, package_names)

if __name__ == "__main__":
    main()



