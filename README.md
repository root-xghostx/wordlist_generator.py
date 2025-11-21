# wordlist_generator.py
Python Program To Create Custom Wordlists

### make script executable
chmod +x wordlist_generator.py


Basic Examples:

Generate all 3-character lowercase combinations:
python wordlist_generator.py -c abcdefghijklmnopqrstuvwxyz -l 3 -o wordlist.txt

Generate words from 2 to 4 characters with custom charset:
python wordlist_generator.py -c abc123 -m 2 -M 4 -o custom.txt

Use predefined character sets:
python wordlist_generator.py --lower --digits -m 1 -M 3 -o alphanum.txt

Generate with pattern (use ? as wildcard):
python wordlist_generator.py -p "admin??" -c 123 -o patterns.txt

Verbose mode with progress:
python wordlist_generator.py --lower --digits -m 2 -M 3 -o test.txt -v

Advanced Examples:

Complex character set with symbols:
python wordlist_generator.py --lower --upper --digits --symbols -l 4 -o complex.txt -v

Generate password patterns:
python wordlist_generator.py -p "Summer202?" -c 1234567890 -o passwords.txt



Features
Flexible character sets: Custom charset or predefined sets (lowercase, uppercase, digits, symbols)
Length control: Fixed length or range of lengths
Pattern generation: Use wildcards for specific patterns
Progress tracking: Verbose mode shows generation progress
Size estimation: Warns about large wordlists before generation
Error handling: Validates inputs and handles interruptions gracefully

Installation Requirements
No external dependencies required! This tool uses only Python standard library modules.
