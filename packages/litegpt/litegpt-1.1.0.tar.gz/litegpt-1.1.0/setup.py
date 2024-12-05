from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    README = f.read()
setup(
    name="litegpt",
    version="1.1.0",
    author_email="Redpiar.official@gmail.com",
    description="LiteGPT provides free access to the ChatGPT and image generator",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/RedPiarOfficial/LiteGPT",
    author="RedPiar",
    license="MIT",
    keywords=[
        "artificial-intelligence",
        "ai",
        "lite",
        "gpt",
        "assistant",
        "chatbot",
        "image-generator"
    ],
    python_requires=">=3.8",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "httpx",
        "httpx[http2]"
    ],
    project_urls={
        "Source": "https://github.com/RedPiarOfficial/LiteGPT",
    },
)
