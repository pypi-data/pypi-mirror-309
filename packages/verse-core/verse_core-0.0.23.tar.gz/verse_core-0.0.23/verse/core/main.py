import argparse

from ._loader import Loader


def run(
    dir: str,
    manifest: str,
    root: str | None,
):
    """
    Verse Deploy
    """
    loader = Loader(dir=dir, manifest=manifest, root=root)
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
        "--manifest",
        type=str,
        default=Loader.MANIFEST_FILE,
        help="Manifest filename",
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
        manifest=args.manifest,
        root=args.root,
    )


if __name__ == "__main__":
    main()
