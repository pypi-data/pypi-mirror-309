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
            # Keywords
            (r'\b(if|elif|else|return|func|break|print|cached|parallel|gpu)\b', Keyword),
            # Types
            (r'\b(int|double|bool|string|intVector|doubleVector|intMatrix|doubleMatrix)\b', Keyword.Type),
            # Boolean Literals
            (r'\b(true|false)\b', Keyword.Constant),
            # Identifiers
            (r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', Name),
            # Numeric literals
            (r'\b\d+\b', Number.Integer),
            (r'\b\d+\.\d*([eE][+-]?\d+)?\b', Number.Float),
            (r'\.\d+([eE][+-]?\d+)?\b', Number.Float),
            # Operators
            (r'[=+\-*/%<>!&|]+', Operator),
            # Punctuation
            (r'[{}[\];(),.:]', Punctuation),
            # Whitespace
            (r'\s+', Text.Whitespace),
        ],
    }