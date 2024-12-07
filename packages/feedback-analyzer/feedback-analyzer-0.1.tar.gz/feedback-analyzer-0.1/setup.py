from setuptools import setup, find_packages

setup(
    name="feedback-analyzer",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "nltk",
        "pymystem3",
        "wordcloud",
        "matplotlib"
    ],
    description="Лibrary for feedback analysis with NLP tools",
    author="Your Name",
)
