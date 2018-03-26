# gdcm-pypi
PyPI package for [GDCM](https://github.com/malaterre/GDCM/)

## How to make the package and submit it to PyPI

Download this repo, with all the submodules:

```
git clone --recursive
```

Now create a `$HOME/.pypirc` file, with the following content:

```
[distutils]
index-servers =
  pypi
  pypitest

[pypi]
username=your_username
password=your_password

[pypitest]
repository=https://test.pypi.org/legacy/
username=your_username
password=your_password
```

where `your_username` and `your_password` shall be replaced by your login
details. Let's start uploading the package to the testing PyPI repository:

```
python setup.py bdist_egg upload -r pypitest
python setup.py sdist upload -r pypitest
```

Now you can check if your package is working:

```
pip install --index-url https://test.pypi.org/simple/ vtkgdcm --user
```

After testing everything is OK, I recommend you to uninstall the package and
proceed with the live PyPI repository
