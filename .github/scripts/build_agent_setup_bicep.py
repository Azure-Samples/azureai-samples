import os
import sys
from pathlib import Path
from azure.cli.core import get_default_cli
from typing import List, Union


def run_az_command(*args: Union[str, Path]) -> None:
    """Runs an Azure CLI command using the Azure CLI Python SDK."""
    cli = get_default_cli()
    command = list(args)
    exit_code = cli.invoke(command)

    if exit_code != 0:
        print(f"❌ Failed to execute: {' '.join(command)}")
        sys.exit(exit_code)


def get_main_bicep_files(modified_files: List[Path]) -> List[Path]:
    """Finds unique folders with modified files and ensures 'main.bicep' exists in each."""
    modified_folders = {Path(f).parent for f in modified_files}
    return [folder / "main.bicep" for folder in modified_folders if (folder / "main.bicep").exists()]


def build_bicep_file(bicep_file: Path) -> None:
    """Builds a Bicep file using Azure CLI Python SDK and ensures azuredeploy.json is created."""
    output_file = bicep_file.with_name("azuredeploy.json")

    print(f"🔹 Building Bicep: {bicep_file} -> {output_file}")
    os.environ.update({"AZURE_BICEP_USE_BINARY_FROM_PATH": "false", "AZURE_BICEP_CHECK_VERSION": "false"})

    # Pin the bicep CLI to minimize pre-commit failures due to modified metadata in files.
    run_az_command("bicep", "install", "--version", "v0.33.93")

    # Run az bicep build using Azure CLI SDK
    run_az_command("bicep", "build", "--file", str(bicep_file), "--outfile", str(output_file))

    # Verify if azuredeploy.json was created
    if not output_file.exists():
        print(f"❌ Build succeeded, but {output_file} was not created!")
        sys.exit(1)

    print(f"✅ Successfully built: {bicep_file} -> {output_file}")


def main() -> None:
    """Main script execution."""
    print("🚀 Running Bicep build using Azure CLI SDK...")

    # Get modified Bicep files from pre-commit
    modified_files = [Path(f) for f in sys.argv[1:]]

    if not modified_files:
        print("✅ No modified Bicep files detected. Skipping build.")
        sys.exit(0)

    # Run Bicep build on each modified file
    bicep_files = get_main_bicep_files(modified_files)

    for bicep_file in bicep_files:
        build_bicep_file(bicep_file)

    print("🎉 All Bicep files successfully built!")
    sys.exit(0)


if __name__ == "__main__":
    main()
