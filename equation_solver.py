class Groups:
 def __init__(self):
    self.equations = []
    
    def organize_information(information):
        all_patterns = [
            "([*][*]|[*]|[/][/]|[/]|[+]|[-])([a-z]+)",
            "([a-z]+)([*][*]|[*]|[/][/]|[/]|[+]|[-])",
            "(\d+)([*][*]|[*]|[/][/]|[/]|[+]|[-])",
            "([*][*]|[*]|[/][/]|[/]|[+]|[-])(\d+)",
            "(\d+)([a-z]+)"
        ]
        for selected_pattern in all_patterns:
            patterns_found = re.findall(selected_pattern, information)
            for tuple_pattern_found in patterns_found:
                list_pattern_altered = [''.join(x) for x in tuple_pattern_found]
                pattern_found = ''.join(list_pattern_altered)
                if selected_pattern == "(\d+)([a-z]+)":
                    pattern_altered = ' * '.join(list_pattern_altered)
                else:
                    pattern_altered = ' '.join(list_pattern_altered)
                information = information.replace(pattern_found, pattern_altered)
        information = information.replace("(", " ( ").replace(")", " ) ")
        
        return information
        
 def add_information(self, information):
    information = re.sub("[=]", " = ", information)
    information = organize_information(information)
    # Transform union in intersection and make equation
    unions = re.findall('([a-z]+)(UNI)([a-z]+)', information)
    for select_union in unions:
        list_union = [''.join(x) for x in select_union]
        union = ''.join(['self.', ''.join(list_union)])
        intersection = ''.join([
            'self.', list_union[0], ' + ', 'self.', list_union[2], ' - ',
            'self.', list_union[0], 'INT', list_union[2]
        ])
        self.equations.append([union, intersection])
    # Transform intersection in union and make equation
    intersections = re.findall('([a-z]+)(INT)([a-z]+)', information)
    for selected_intersection in intersections:
        list_intersection = [''.join(x) for x in selected_intersection]
        intersection = ''.join(['self.', ''.join(list_intersection)])
        union = ''.join([
            'self.', list_intersection[0], 'UNI', list_intersection[2], ' - ',
            'self.', list_intersection[0], ' - ', 'self.', list_intersection[2]
        ])
        self.equations.append([union, intersection])
    # Transform in equation
    variables_found = []
    list_variables_found = re.findall('[a-zA-Z]+', information)
    information = ' '.join(['self.' + x if bool(re.match('[a-zA-Z]+', x)) else x for x in information.split(' ')])
    split_by_equal_sign = re.split("\s+[=]\s+", information)
    self.equations.append([split_by_equal_sign[0], split_by_equal_sign[1]])
    self.run_equations()
    
 def run_equations(self):
    symbols = []
    for equation in self.equations:
        for equation_part in equation:
            variables = [x for x in re.split(" ", equation_part) if bool(re.match('self.[a-z]+', x))]
            [symbols.append(x) for x in variables if x not in symbols]
    for symbol in set(symbols):
        setattr(self, symbol.replace("self.", ''), sympy.Symbol(symbol))
        
    list_equations = []
    for equation in self.equations:
        list_equations.append(sympy.Eq(eval(equation[0]), eval(equation[1])))
    
    self.solution = sympy.solve(list_equations, dict=True)
