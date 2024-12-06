import pathlib
import setuptools

if __name__ == "__main__":
    name = "e_commerce_scraper"
    version = "0.1.0"  # Specify a valid version number
    license = "MIT"
    description = "A bot which scrapes products from Tunisian e-commerce websites"

    pkg_name = name.replace("-", "_")
    pkg_path = pathlib.Path(__file__).parent

    # Read the install_requires and extras_require (ensure correct file paths)
    with open(pkg_path / "requirements" / "prod") as fp:
        install_requires = fp.read().splitlines()

    with open(pkg_path / "requirements" / "dev") as fd:
        extra_requires_dev = fd.read().splitlines()

    setuptools.setup(
        name=name,
        version=version,  # Added version field
        description=description,
        license=license,
        packages=setuptools.find_packages(exclude=["tests"]),
        install_requires=install_requires,
        extras_require={"dev": extra_requires_dev},
        package_data={"": ["*.exe", "*.txt"]},
        include_package_data=True,
        zip_safe=False,
        python_requires=">=3.6",
    )
