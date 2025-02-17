from formatters.multi_line import MultilineFormatter
from generators.graphql import GraphQLGenerator

def main():
    # Create a generator with multiline formatting
    formatter = MultilineFormatter(indent=2)
    generator = GraphQLGenerator(formatter)

    # Generate logs
    generator.generate_log()

if __name__ == "__main__":
    main()