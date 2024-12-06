import argparse
from typing import Any

from ._loader import Loader
from ._models import Operation


def run(
    dir: str,
    manifest: str,
    root: str | None,
) -> Any:
    """
    Verse Run
    """
    loader = Loader(dir=dir, manifest=manifest, root=root)
    root_component = loader.load_root()
    operation = Operation(
        name="run",
        args=dict(dir=dir, manifest=manifest, root=root),
    )
    return root_component.run(operation=operation)


def requirements(
    dir: str,
    manifest: str,
    root: str | None,
    out: str | None,
):
    """
    Verse Requirements
    """
    loader = Loader(dir=dir, manifest=manifest, root=root)
    requirements = loader.generate_requirements(out=out)
    return requirements


def main():
    parser = argparse.ArgumentParser(prog="verse", description="Verse CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)
    run_parser = subparsers.add_parser("run", help="Run the Verse application")
    requirements_parser = subparsers.add_parser(
        "requirements", help="Generate the pip requirements"
    )
    run_parser.add_argument(
        "--dir",
        type=str,
        default=".",
        help="Project directory",
    )
    run_parser.add_argument(
        "--manifest",
        type=str,
        default=Loader.MANIFEST_FILE,
        help="Manifest filename",
    )
    run_parser.add_argument(
        "--root",
        type=str,
        default=None,
        help="Root handle",
    )

    requirements_parser.add_argument(
        "--dir",
        type=str,
        default=".",
        help="Project directory",
    )
    requirements_parser.add_argument(
        "--manifest",
        type=str,
        default=Loader.MANIFEST_FILE,
        help="Manifest filename",
    )
    requirements_parser.add_argument(
        "--root",
        type=str,
        default=None,
        help="Root handle",
    )
    requirements_parser.add_argument(
        "--out",
        type=str,
        default=None,
        help="Output path",
    )

    args = parser.parse_args()
    if args.command == "run":
        run(
            dir=args.dir,
            manifest=args.manifest,
            root=args.root,
        )
    elif args.command == "requirements":
        requirements(
            dir=args.dir,
            manifest=args.manifest,
            root=args.root,
            out=args.out,
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
