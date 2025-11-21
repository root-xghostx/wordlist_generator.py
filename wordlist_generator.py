#!/usr/bin/env python3
"""
Wordlist Generator - A command-line tool for creating custom wordlists
Creator: root@xghostx
"""

###
### ALL CREDIT TO https://t.me/joker_hx2
### 


import argparse
import itertools
import sys
from pathlib import Path

class WordlistGenerator:
    def __init__(self):
        self.args = None
    
    def parse_arguments(self):
        """Parse command line arguments"""
        parser = argparse.ArgumentParser(
            description='Generate custom wordlists for security testing, passwords, or other purposes',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Generate all 3-character combinations using lowercase letters
  python wordlist_generator.py -c abcdefghijklmnopqrstuvwxyz -l 3 -o wordlist.txt
  
  # Generate words from 2 to 4 characters using custom charset
  python wordlist_generator.py -c abc123 -m 2 -M 4 -o custom.txt
  
  # Generate words with specific pattern (use ? as wildcard)
  python wordlist_generator.py -p "pass???" -c 123 -o patterns.txt
  
  # Show progress and estimate size
  python wordlist_generator.py -c abc123 -m 1 -M 3 -o test.txt -v
            """
        )
        
        # Character set options
        char_group = parser.add_argument_group('Character Set Options')
        char_group.add_argument('-c', '--charset', 
                               help='Custom character set (e.g., "abc123")')
        char_group.add_argument('-p', '--pattern',
                               help='Pattern with ? as wildcard (e.g., "pass???")')
        
        # Predefined character sets
        char_group.add_argument('--lower', action='store_true',
                               help='Include lowercase letters (a-z)')
        char_group.add_argument('--upper', action='store_true',
                               help='Include uppercase letters (A-Z)')
        char_group.add_argument('--digits', action='store_true',
                               help='Include digits (0-9)')
        char_group.add_argument('--symbols', action='store_true',
                               help='Include common symbols (!@#$%^&* etc.)')
        
        # Length options
        length_group = parser.add_argument_group('Length Options')
        length_group.add_argument('-l', '--length', type=int,
                                 help='Fixed length for all words')
        length_group.add_argument('-m', '--min-length', type=int, default=1,
                                 help='Minimum word length (default: 1)')
        length_group.add_argument('-M', '--max-length', type=int, default=4,
                                 help='Maximum word length (default: 4)')
        
        # Output options
        output_group = parser.add_argument_group('Output Options')
        output_group.add_argument('-o', '--output', required=True,
                                 help='Output file path (.txt)')
        output_group.add_argument('-v', '--verbose', action='store_true',
                                 help='Show progress and statistics')
        
        self.args = parser.parse_args()
        self.validate_arguments()
    
    def validate_arguments(self):
        """Validate command line arguments"""
        if not self.args.charset and not self.args.pattern and not any([
            self.args.lower, self.args.upper, self.args.digits, self.args.symbols
        ]):
            print("Error: You must specify a character set or pattern")
            sys.exit(1)
        
        if self.args.length and (self.args.min_length != 1 or self.args.max_length != 4):
            print("Error: Use either --length OR --min-length/--max-length, not both")
            sys.exit(1)
        
        if self.args.length:
            self.args.min_length = self.args.length
            self.args.max_length = self.args.length
        
        if self.args.min_length > self.args.max_length:
            print("Error: min-length cannot be greater than max-length")
            sys.exit(1)
        
        if self.args.min_length < 1:
            print("Error: min-length must be at least 1")
            sys.exit(1)
    
    def build_charset(self):
        """Build the character set based on arguments"""
        charset = ""
        
        if self.args.charset:
            charset += self.args.charset
        
        # Add predefined character sets
        if self.args.lower:
            charset += 'abcdefghijklmnopqrstuvwxyz'
        if self.args.upper:
            charset += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if self.args.digits:
            charset += '0123456789'
        if self.args.symbols:
            charset += '!@#$%^&*()_+-=[]{}|;:,.<>?'
        
        # Remove duplicates and return
        return ''.join(sorted(set(charset)))
    
    def estimate_size(self, charset, min_len, max_len):
        """Estimate the number of combinations"""
        total = 0
        for length in range(min_len, max_len + 1):
            total += len(charset) ** length
        return total
    
    def generate_from_pattern(self, pattern, charset):
        """Generate words based on pattern with wildcards"""
        wildcard_count = pattern.count('?')
        if wildcard_count == 0:
            yield pattern
            return
        
        # Generate all combinations for wildcard positions
        for combination in itertools.product(charset, repeat=wildcard_count):
            result = pattern
            for char in combination:
                result = result.replace('?', char, 1)
            yield result
    
    def generate_wordlist(self):
        """Generate the wordlist based on arguments"""
        if self.args.pattern:
            charset = self.build_charset()
            yield from self.generate_from_pattern(self.args.pattern, charset)
        else:
            charset = self.build_charset()
            if not charset:
                print("Error: No characters specified for generation")
                sys.exit(1)
            
            for length in range(self.args.min_length, self.args.max_length + 1):
                for combination in itertools.product(charset, repeat=length):
                    yield ''.join(combination)
    
    def run(self):
        """Main execution function"""
        self.parse_arguments()
        
        # Build charset for estimation
        charset = self.build_charset()
        
        if self.args.verbose:
            if self.args.pattern:
                print(f"Pattern: {self.args.pattern}")
                print(f"Charset: {charset}")
                wildcards = self.args.pattern.count('?')
                combinations = len(charset) ** wildcards
                print(f"Estimated combinations: {combinations:,}")
            else:
                total_combinations = self.estimate_size(
                    charset, self.args.min_length, self.args.max_length
                )
                print(f"Charset: {charset}")
                print(f"Charset size: {len(charset)}")
                print(f"Length range: {self.args.min_length}-{self.args.max_length}")
                print(f"Estimated combinations: {total_combinations:,}")
                
                if total_combinations > 1000000:
                    print("Warning: Large wordlist generation may take time and disk space")
                    response = input("Continue? (y/N): ")
                    if response.lower() != 'y':
                        print("Generation cancelled")
                        return
        
        # Generate and save wordlist
        try:
            with open(self.args.output, 'w', encoding='utf-8') as f:
                count = 0
                for word in self.generate_wordlist():
                    f.write(word + '\n')
                    count += 1
                    
                    if self.args.verbose and count % 10000 == 0:
                        print(f"Generated {count:,} words...", end='\r')
            
            if self.args.verbose:
                print(f"\nSuccessfully generated {count:,} words")
                print(f"Saved to: {self.args.output}")
                
        except KeyboardInterrupt:
            print(f"\nGeneration interrupted. Partial wordlist saved to {self.args.output}")
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

def main():
    """Entry point"""
    generator = WordlistGenerator()
    generator.run()

if __name__ == '__main__':
    main()
