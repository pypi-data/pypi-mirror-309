from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as arq:
    readme = arq.read()

setup(
    name="wave-flow",
    version="1.0.3",
    license="MIT License",
    author="Lucas Lourenço",
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email="dev.lucaslourenco@gmail.com",
    keywords="wave build docx treatdata xlsx to word waveflow wave-flow",
    description="WAVE - Workflow Automation and Versatile Engine",
    packages=['WaveFlow'],
    install_requires=["python-docx", "openpyxl", "pandas"],
)
