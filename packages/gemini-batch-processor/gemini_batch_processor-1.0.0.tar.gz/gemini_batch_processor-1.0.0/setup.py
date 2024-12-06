from setuptools import setup, find_packages

setup(
    name="gemini_batch_processor",
    version="1.0.0",
    author="Yukendiran",
    author_email="yukendiranjayachandiran@gmail.com",
    description="A Python module to process bulk data using Google's generative AI (Gemini).",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Yukendiran2002/GeminiDataProcessor",
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
    python_requires=">=3.8"
)
