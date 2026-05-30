from flask import Flask, render_template, request, jsonify
import secrets
import string

app = Flask(__name__)

def generate_password(length, use_upper, use_lower, use_numbers, use_special):
    characters = ""
    if use_upper:
        characters += string.ascii_uppercase
    if use_lower:
        characters += string.ascii_lowercase
    if use_numbers:
        characters += string.digits
    if use_special:
        characters += string.punctuation

    if not characters:
        # Default fallback
        characters = string.ascii_letters + string.digits

    # Ensure at least one character from each selected category is included
    password = []
    if use_upper:
        password.append(secrets.choice(string.ascii_uppercase))
    if use_lower:
        password.append(secrets.choice(string.ascii_lowercase))
    if use_numbers:
        password.append(secrets.choice(string.digits))
    if use_special:
        password.append(secrets.choice(string.punctuation))

    # Fill the rest of the password length
    remaining_length = length - len(password)
    for _ in range(remaining_length):
        password.append(secrets.choice(characters))

    # Shuffle the list to ensure randomness
    secrets.SystemRandom().shuffle(password)
    return ''.join(password)

def calculate_strength(password):
    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_num = any(c.isdigit() for c in password)
    has_spec = any(c in string.punctuation for c in password)

    score = 0
    if length >= 8: score += 1
    if length >= 12: score += 1
    if length >= 16: score += 1
    
    types_count = sum([has_upper, has_lower, has_num, has_spec])
    if types_count >= 2: score += 1
    if types_count >= 3: score += 1
    if types_count == 4: score += 1

    if score < 2: return "Weak"
    if score < 4: return "Medium"
    if score < 6: return "Strong"
    return "Very Strong"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    length = int(data.get('length', 16))
    use_upper = data.get('uppercase', True)
    use_lower = data.get('lowercase', True)
    use_numbers = data.get('numbers', True)
    use_special = data.get('special', True)

    pwd = generate_password(length, use_upper, use_lower, use_numbers, use_special)
    strength = calculate_strength(pwd)

    return jsonify({"password": pwd, "strength": strength})

if __name__ == '__main__':
    app.run(debug=True)
