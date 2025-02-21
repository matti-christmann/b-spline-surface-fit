def replace_spaces_with_semicolon(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    updated_content = content.replace(' ', ';')
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)

# Usage example
file_path = '/home/mattichristmann/Dokumente/03 Code/05 scripts/test_env/examples/random_point_cloud.csv'  # Change this to your actual file path
replace_spaces_with_semicolon(file_path)
