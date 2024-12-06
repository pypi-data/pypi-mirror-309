from pygments.lexer import RegexLexer
from pygments.token import Text, Comment, String, Keyword, Name, Number, Operator, Punctuation

class TensorGradLexer(RegexLexer):
    name = 'TensorGrad'
    aliases = ['tensorgrad']
    filenames = ['*.tg']

    tokens = {
        'root': [
            # Comments
            (r'//.*', Comment.Single),
            (r'/\*.*?\*/', Comment.Multiline),
            
            # Strings
            (r'"(\\.|[^"\\])*"', String),

            # Keywords (control flow, function, loops, etc.)
            (r'\b(func|if|elif|else|return|for|break|range|cached|parallel|gpu)\b', Keyword),
            
            # Types
            (r'\b(int|double|bool|string|intVector|doubleVector|intMatrix|doubleMatrix)\b', Keyword.Type),

            # Constants
            (r'\b(true|false)\b', Keyword.Constant),

            # Identifiers
            (r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', Name),

            # Range expressions and iterables
            (r'\b(range)\b', Keyword.Reserved),
            (r'<-', Operator),  # Iterable operator in for loops

            # Numbers
            (r'\b[0-9]+\b', Number.Integer),
            (r'\b[0-9]+\.[0-9]*([eE][+\-]?[0-9]+)?\b', Number.Float),
            (r'\.[0-9]+([eE][+\-]?[0-9]+)?\b', Number.Float),

            # Operators
            (r'[=+\-*/%<>!&|]+', Operator),
            (r'\*\*', Operator),  # Power operator

            # Punctuation
            (r'[{}[\];(),.:]', Punctuation),

            # Unified Compound Literals (Vectors and Matrices)
            (r'\[', Punctuation, 'vector'),  # Enter vector mode

            # Whitespace
            (r'\s+', Text),
        ],

        'vector': [
            # Nested matrices or vectors
            (r'\[', Punctuation, 'vector'),
            (r'\]', Punctuation, '#pop'),
            
            # Numbers, identifiers, and commas inside vectors/matrices
            (r'\b[0-9]+(\.[0-9]+)?\b', Number),
            (r'[a-zA-Z_][a-zA-Z0-9_]*', Name),
            (r',', Punctuation),

            # Whitespace
            (r'\s+', Text),
        ],
    }
