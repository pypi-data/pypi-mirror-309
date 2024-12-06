# jkpackager/__main__.py
import argparse
from jkpackager import JkPackager


def main():
    parser = argparse.ArgumentParser(description="Package Python scripts into .exe, .pkg, .deb, and .rpm formats.")
    parser.add_argument("-i", "--icon", help="Path to the icon file (for .exe)", required=False)
    parser.add_argument("script", help="Path to the Python script to package")
    args = parser.parse_args()

    packager = JkPackager(args.script, icon_path=args.icon)
    packager.run()


if __name__ == "__main__":
    main()
