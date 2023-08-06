def extract_unique_tuples(input_list):
    unique_second_elements = set()
    result_tuples = []

    for ctr, tuple_element in enumerate(input_list):
        _, second_element = tuple_element  # Unpacking the tuple to get the second element
        if second_element not in unique_second_elements:
            unique_second_elements.add(second_element)
            tup = (ctr,tuple_element[1])
            # result_tuples.append(tuple_element)
            result_tuples.append(tup)

    return result_tuples

if __name__ == "__main__":
    l = [("blue","color"),("6", "first"), ("999", "second"), ("1", "third"), ("4", "first"), ("5", "second")]
    extracted_tuples = extract_unique_tuples(l)
    print(extracted_tuples)


"""
def extract_unique_second_elements(lst):
    second_element_count = {}
    result = []

    for tup in lst:
        _, second = tup
        print(f'{tup=} {second=}')

        if second in second_element_count:
            second_element_count[second] += 1
        else:
            second_element_count[second] = 1
    print(f'{second_element_count}')
    
    for tup in lst:
        _, second = tup
        if second_element_count[second] == 1:
            result.append(tup)

    return result


# Input list
l = [("1", "first"), ("2", "second"), ("3", "third"), ("4", "first"), ("5", "second")]

# Extracting two-element tuples with unique second element
unique_tuples = extract_unique_second_elements(l)

# Print the result

print(unique_tuples)
"""

