


class SingletableSelect():
    def __init__(self):
        """
        Initializes the Where handler for the given table model.
        """

    doctype = ""
    select_columns = []

    def build_condition(self, column, operator, value, datatype):
        """
        :param column: The column to filter on
        :param operator: The operator (e.g., '=', '>', '<', 'LIKE', etc.)
        :param value: The value to compare against
        : type
        :return: The condition
        """
        if datatype == 'str' or datatype == 'dt':
            value = "'" + value + "'"

        if operator == '=':
            return column + " = " + value
        elif operator == '!=':
            return column + " != " + str(value)
        elif operator == '>':
            return column + " > " + str(value)
        elif operator == '<':
            return column + " < " + str(value)
        elif operator == '>=':
            return column + " >= " + str(value)
        elif operator == '<=':
            return column + " <= " + str(value)
        elif operator == 'LIKE':
            return column + " like " + str(value)
        elif operator == 'NOT LIKE':
            return column + " NOT LIKE " + str(value)
        elif operator == 'IN':
            return column + " IN " + str(value)
        elif operator == 'NOT IN':
            return column + " NOT IN " + str(value)
        elif operator == 'IS NULL':
            return column + " IS NULL"
        elif operator == 'IS NOT NULL':
            return column + "IS NOT NULL"
        else:
            raise ValueError(f"Unsupported operator: {operator}")

    def apply_conditions(self, conditions, logical_operator):
        """
        Applies the conditions to the query based on the logical operator (AND/OR).

        :param conditions: List of conditions to apply.
        :param logical_operator: The logical operator ('AND' or 'OR')
        :return:
        """
        return_val = ""
        if len(conditions) == 1:
            return_val = conditions[0]
            return return_val

        if len(conditions) > 1:
            for i, val in enumerate(conditions):

                try:
                    if i == 0:
                        if logical_operator[i]  == 'AND':
                            return_val = return_val + " " + conditions[i] + " AND " + conditions[i + 1]
                        elif logical_operator[i] == 'OR':
                            return_val = return_val + " " + conditions[i] + " OR " + conditions[i + 1]
                        else:
                            return_val = return_val + " " + conditions[i] + " AND " + conditions[i + 1]
                    else:
                        if logical_operator[i] == 'AND':
                            return_val = return_val + " AND " + conditions[i + 1]
                        elif logical_operator[i] == 'OR':
                            return_val = return_val + " OR " + conditions[i + 1]
                        else:
                            return_val = return_val + " AND " + conditions[i + 1]

                    if i == len(conditions) - 2:
                        break
                except:
                    if i == 0:
                        return_val = return_val + " " + conditions[i] + " AND " + conditions[i + 1]
                    else:
                        return_val = return_val + " AND " + conditions[i + 1]

                if i == len(conditions) - 2:
                    break
                # raise ValueError("Logical operator must be 'AND' or 'OR'.")
        else:
            return_val = conditions

        return return_val

    def build_query(self, conditions_dict, logical_operator):
        """
        Builds the query with conditions based on the user's input.

        :param conditions_dict: A dictionary where key is the column name and value is a tuple (operator, value)
        :param logical_operator: The logical operator for combining conditions (AND/OR)
        :return:
        """
        conditions = []
        for column_name, (operator, value, datatype) in conditions_dict.items():
            # Get the column from the model
            condition = self.build_condition(column_name, operator, value, datatype)
            conditions.append(condition)

        # Combine all conditions using the logical operator
        final_condition = self.apply_conditions(conditions, logical_operator)

        # Create the query with the final condition
        return final_condition

    def get_results(self, conditions_dict={}, logical_operator=[]):
        """
        Retrieves the filtered results from the table based on conditions.
        :param conditions_dict: A dictionary where key is the column name and value is a tuple (operator, value)
        :param logical_operator: The logical operator for combining conditions (AND/OR)
        :return: The query results

        """
        if len(conditions_dict) == 0:
            return "select " + ','.join(self.select_columns) + ' from ' + self.doctype
        else:
            clause = self.build_query(conditions_dict , logical_operator)
            return "select " + ','.join(self.select_columns) + ' from ' + self.doctype + ' where ' + clause