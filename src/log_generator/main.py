from formatters.multiline_formatter import MultilineFormatter
from generators.graphql import GraphQLGenerator

# Create a generator with multiline formatting
formatter = MultilineFormatter(indent=2)
generator = GraphQLGenerator(formatter)

# Generate logs
generator.generate_log()