import os

msg = input("Message: ")
os.system("git add .")
os.system(f"git commit -m '{msg}'")
os.system("git push")
os.system("clear")