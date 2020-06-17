import subprocess  # -- run jar file

# -- run farsnet java library before run other functions
subprocess.call(['java', '-cp', 'farsnet.jar', 'ir.hitolid.farsnet.StackEntryPoint'])
