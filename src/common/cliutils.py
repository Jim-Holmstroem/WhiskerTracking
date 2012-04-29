class CliVariable:
    def __init__(self, name, is_list=False):
        self.name = name
        self.is_list = is_list
    def __repr__(self):
        return self.name + (self.is_list and " (list)" or "")
    
def extract_variables(argv, cli_definition):
    """Parse the list of strings argv as a command defined by cli_definition.
    
    Returns a dictionary of variables with names as specified by cli_definition.
    
    Example 1:
    argv = ["foo", "bar", "test.txt"]
    cli_definition = "OPERAND1 OPERAND2 [-n ITERATIONS] FILE"
    
    Returned dictionary:
    {
      OPERAND1:"foo",
      OPERAND2:"bar",
      FILE:test.txt
    }

    Example 2:
    argv = ["foo", "bar", "-n", "17", "test.txt", "Class1", "Class2"]
    cli_definition = "OPERAND1 OPERAND2 [-n ITERATIONS] FILE CLASSES..."
    
    Returned dictionary:
    {
      "OPERAND1":"foo",
      "OPERAND2":"bar",
      "ITERATIONS":"17"
      "FILE":test.txt,
      "CLASSES":["Class1", "Class2"]
    }
    """

    required_variables = []
    optional_variables = {}
    
    it = iter(cli_definition.split(" "))
    for definition in it:
        if definition[0] == "[":
            nextDef = it.next()[:-1]
            is_list = False
            if nextDef[-3:] == "...":
                is_list = True
                nextDef = nextDef[:-3]
            optional_variables[definition[1:]] = CliVariable(nextDef, is_list)
        else:
            is_list = False
            if definition[-3:] == "...":
                is_list = True
                definition = definition[:-3]

            required_variables.append(CliVariable(definition, is_list=is_list))

    varit = iter(required_variables)
    curVar = varit.next()

    result = {}

    it = iter(argv)
    for arg in it:
        if arg in optional_variables.keys():
            narg = it.next()
            if optional_variables[arg].is_list:
                result[optional_variables[arg].name] = [narg] + [i for i in it]
            else:
                result[optional_variables[arg].name] = narg
        else:
            if curVar.is_list:
                result[curVar.name] = [arg] + [i for i in it]
            else:
                result[curVar.name] = arg
            try:
                curVar = varit.next()
            except StopIteration:
                curVar = None

    return result

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print """Usage: python cliutils.py "CLI_DEFINITION" CLI_ARGS...

Parses CLI_ARGS using the definition CLI_DEFINITION and prints the result."""
        sys.exit(0)
    
    print extract_variables(sys.argv[2:], sys.argv[1])
