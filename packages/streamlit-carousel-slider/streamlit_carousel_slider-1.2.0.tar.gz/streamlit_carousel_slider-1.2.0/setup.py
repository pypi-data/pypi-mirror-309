from pathlib import Path

import setuptools

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="streamlit-carousel-slider",
    version="1.2.0",
    author="ryone9re",
    author_email="ryoichi.kurimoto@gmail.com",
    description="Carousel slider component for streamlit using React and tailwind with daisyui.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/streamlit-carousel-slider",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.12",
    install_requires=[
        "streamlit >= 1.40",
    ],
    extras_require={},
)
