from setuptools import setup, find_packages

setup(
    name="gemini_data_processor",
    version="1.0.1",
    author="Yukendiran",
    author_email="yukendiranjayachandiran@gmail.com",
    description="A Python module to process data using Google's generative AI (Gemini).",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Yukendiran2002/GeminiDataProcessor",  # Replace with your repository URL
    packages=find_packages(),
    install_requires=[
        "pandas",
        "tqdm",
        "google-generativeai",
        "nest-asyncio",
        "pytz"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "gemini-process = GeminiDataProcessor.__main__:main",  # Replace with your main function path
        ],
    },
)
