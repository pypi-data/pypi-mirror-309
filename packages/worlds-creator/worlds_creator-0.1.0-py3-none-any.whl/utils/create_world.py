import os
import subprocess
from datetime import datetime


def create_world():
    while True:
        world_name = input("Name your world: ").strip()
        if world_name:
            break
        print("World name cannot be empty. Please enter a valid name.")

    file_name = f"{world_name}.yaml"
    file_path = os.path.join(os.getcwd(), "data", file_name)

    os.makedirs("data", exist_ok=True)

    if os.path.exists(file_path):
        while True:
            overwrite = (
                input(f"'{file_name}' already exists. Overwrite? (Y/N) : ")
                .strip()
                .lower()
            )
            if overwrite == "y":
                break
            elif overwrite == "n":
                os.system("clear")
                return
            else:
                print("Please enter 'Y' to overwrite or 'N' to cancel.")

    world_data = f"""---
world: {world_name}
date_created: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
---

T1. 
T2. 
T3. 
T4. 
T5. 
"""

    # Write the data to the YAML file
    with open(file_path, "w") as file:
        file.write(world_data)

    print(f"'./data/{file_name}' created.")

    # Attempt to open the file in Vim (or any other editor)
    try:
        subprocess.run(["vim", file_path])
    except Exception as e:
        print(f"Could not open the file automatically: {e}")
