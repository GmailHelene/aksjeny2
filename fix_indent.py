def fix_main_py():
    try:
        # Read the file line by line
        with open('app/routes/main.py', 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        # Find the profile route
        profile_start = None
        for i, line in enumerate(lines):
            if '@main.route(\'/profile\')' in line:
                profile_start = i
                break

        if profile_start is not None:
            # Read a few lines to understand the context
            profile_section = lines[profile_start:profile_start+10]
            print("Found profile section:")
            for line in profile_section:
                print(line.rstrip())

            # Fix the indentation issue
            lines[profile_start+4] = '\n'  # Replace the line with indent error with a blank line

            # Write the file back
            with open('app/routes/main.py', 'w', encoding='utf-8') as f:
                f.writelines(lines)

            print("\nFix applied successfully!")
        else:
            print("Profile route not found in main.py")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_main_py()
