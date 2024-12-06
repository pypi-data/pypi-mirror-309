import os, shutil

shutil.rmtree("dist")
cm1 = 'py -m build'
cm2 = 'twine upload -u "__token__" -p "pypi-AgEIcHlwaS5vcmcCJDg5MzdiZjNjLTdiOTEtNDNlMC05OTk2LWE0YjYzNmM4YTRlZQACKlszLCIzODIzY2YxYy0xMjEzLTRkZGYtOTc0NC1lNDM5YjI5NDBmYTQiXQAABiCnaKX4lhaftmjan9ZgfCBdGdh-aGnsQpaNO7ptNQYaTg" --repository-url https://upload.pypi.org/legacy/ dist/*'
os.system(cm1)
os.system(cm2)
input("Complete")
