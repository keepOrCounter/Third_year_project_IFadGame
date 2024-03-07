import json

def convert_to_jsonl(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    with open(output_file, 'w') as f:
        for item in range(0, len(data), 2):
            # system_role = item.get('system_role', '')
            system_role = "You are writting the description about 'description_target' for a survival text-based adventure game based on game information given"
            user_role = data[item]
            assistant_role = data[item + 1]
            
            # Creating the JSONL format
            json_line = {
                "messages": [
                    {"role": "system", "content": system_role},
                    {"role": "user", "content": str(user_role)},
                    {"role": "assistant", "content": str(assistant_role)}
                ]
            }
            
            # Writing each JSONL line to the file
            f.write(json.dumps(json_line) + '\n')

# Replace 'input.json' and 'output.jsonl' with your file names
convert_to_jsonl('backup.json', 'output.jsonl')
