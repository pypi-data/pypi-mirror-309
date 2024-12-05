import os
from setuptools import setup


# INSTALL_PACKAGES = open(path.join(DIR, 'requirements.txt')).read().splitlines()
def read(rel_path: str) -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with open(os.path.join(here, rel_path), 'r', encoding='UTF-8') as fp:
        return fp.read()


long_description = read("README.rst")


setup(
    name='NLPX',
    packages=['nlpx', 'nlpx.model', 'nlpx.llm', 'nlpx.text_token', 'nlpx.dataset', 'nlpx.training'],
    description="A tool set for NLP. Text classification. Training. Tokenizer",
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='1.7.1',
    url='https://gitee.com/summry/nlpx',
    author='summy',
    author_email='xiazhongbiao@126.com',
    keywords=['NLP', 'nlp', 'AI', 'llm', 'GPT', 'Machine learning', 'Deep learning', 'tokenize', 'torch'],
    package_data={
        # include json and txt files
        '': ['*.rst', '*.dtd', '*.tpl'],
    },
    include_package_data=True,
    python_requires='>=3.6',
    zip_safe=False
)

