import argparse
import os
import sys

from ._loader import Loader


def _set_sys_path(
    project_dir: str | None = ".", manifest_path: str | None = None
):
    project_folder = "."
    if project_dir is not None:
        project_folder = project_dir
    elif manifest_path is not None:
        project_folder = os.path.dirname(manifest_path)

    abs_project_folder = os.path.abspath(project_folder)
    if abs_project_folder not in sys.path:
        sys.path.append(abs_project_folder)


def run(
    dir: str | None = ".",
    manifest_path: str | None = None,
    root: str | None = None,
):
    """
    Verse Deploy
    """
    _set_sys_path(dir, manifest_path)
    loader = Loader(dir=dir, manifest_path=manifest_path, root=root)
    root_component = loader.load_root()
    root_component.run()


def main():
    parser = argparse.ArgumentParser(description="Verse ")
    parser.add_argument(
        "--dir",
        type=str,
        default=".",
        help="Project directory",
    )
    parser.add_argument(
        "--manifest_path",
        type=str,
        default=None,
        help="Path to the manifest file",
    )
    parser.add_argument(
        "--root",
        type=str,
        default=None,
        help="Root handle",
    )

    args = parser.parse_args()
    run(
        dir=args.dir,
        manifest_path=args.manifest_path,
        root=args.root,
    )


if __name__ == "__main__":
    main()
