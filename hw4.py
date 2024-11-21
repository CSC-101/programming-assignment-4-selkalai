import build_data
import sys
from data import CountyDemographics

#function display will be used when current_operation == 'display'. It will print the county information for each county to the terminal
def display(counties_list): #display will print the county information for only the counties still in counties_list. Because its purpose is to print, it does not return anything
    for county in counties_list:
        print(f'{county.county}, {county.state}')

        print(f'\tPopulation: {county.population["2014 Population"]} ')

        print('\tAge:')
        for key, value in county.age.items():
            print(f'\t\t{key}: {value}%')
        print()

        print('\tEducation:')
        for key, value in county.education.items():
            print(f'\t\t{key}: {value}%')
        print()

        print('\tEthnicity Percentages:')
        for key, value in county.ethnicities.items():
            print(f'\t\t{key}: {value}%')
        print()

        print('\tIncome:')
        for key, value in county.income.items():
            if 'Income' in key:
                print(f'\t\t{key}: ${value}')
            else:
                print(f'\t\t{key}: {value}%')
        print('\n')

#function filter_state will be used when current_operation == 'filter-state'. It will take the parameters counties_list:list[CountyDemographics] and
# current_field:list[str](this is where the str of state abbreviation is). It will reduce the collection of counties to those with matching state
# abbreviation and if no county's state matches the abbreviation, then the resulting collection will be empty. It will print
# "Filter: state == <state abbreviation> (xyz entries)" (where xyz is the number of remaining entries) to the terminal and return the new
# filtered counties_list:list[str]

def filter_state(counties_list:list[CountyDemographics], current_field:str) -> list[CountyDemographics]:
    filtered_list = []
    for county in counties_list:
        if str(current_field[0]) == county.state:
            filtered_list.append(county)
    if not filtered_list:
        return []
    counties_list = filtered_list
    print(f'Filter: state == {current_field[0]} ({len(counties_list)} entries)')
    return counties_list

#function filter_gt will be used when current_operation == 'filter-gt'. It will take the parameters counties_list:list[CountyDemographics],
# current_field:list[str], and numeric_threshold:float. It will reduce the collection of entries to those for which the value in the
# current_field is greater-than the numeric_threshold. It will print "Filter: <field> gt <number> (xyz entries)" (where xyz is the number of
# remaining entries in the collection) to the terminal, and it will return the new filtered counties_list:list[str]

def filter_gt(counties_list:list[CountyDemographics], current_field:list[str], numeric_threshold:float)->list[CountyDemographics]:
    filtered_list = []
    for county in counties_list:
        if current_field[0].lower() == "education":
            if current_field[1] in county.education:
                percentage_b = county.education[current_field[1]]
                if percentage_b > numeric_threshold:
                    filtered_list.append(county)
        elif current_field[0].lower() == 'ethnicities':
            if current_field[1] in county.ethnicities:
                percentage_b = county.ethnicities[current_field[1]]
                if percentage_b > numeric_threshold:
                    filtered_list.append(county)
        elif current_field[0].lower() == "income":
            if current_field[1] in county.income:
                percentage_b = county.income['Persons Below Poverty Level']
                if percentage_b > numeric_threshold:
                    filtered_list.append(county)
        else:
            return print("error for filter-gt")

    counties_list = filtered_list
    print(f'Filter: {current_field[0]}.{current_field[1]} gt {numeric_threshold} ({len(counties_list)} entries)')
    return counties_list

#function filter_lt will be used when current_operation == 'filter-lt'. It will take the parameters counties_list:list[CountyDemographics],
# current_field:list[str], and numeric_threshold:float. It will reduce the collection of entries to those for which the value in the current_field
# is less-than the numeric_threshold. It will print "Filter: <field> lt <number> (xyz entries)" (where xyz is the number of remaining
# entries in the collection) to the terminal, and it will return the new filtered counties_list:list[str]

def filter_lt(counties_list:list[CountyDemographics], current_field:list[str], numeric_threshold:float)->list[CountyDemographics]:
    filtered_list = []
    for county in counties_list:
        if current_field[0].lower() == "education":
            if current_field[1] in county.education:
                percentage_a = county.education[current_field[1]]
                if percentage_a < numeric_threshold:
                    filtered_list.append(county)
        elif current_field[0].lower() == 'ethnicities':
            if current_field[1] in county.ethnicities:
                percentage_a = county.ethnicities[current_field[1]]
                if percentage_a < numeric_threshold:
                    filtered_list.append(county)
        elif current_field[0].lower() == "income":
            if current_field[1] in county.income:
                percentage_a = county.income[current_field[1]]
                if percentage_a < numeric_threshold:
                    filtered_list.append(county)
        else:
            return print("error for filter-lt")

    counties_list = filtered_list
    print(f'Filter: {current_field[0]}.{current_field[1]} lt {numeric_threshold} ({len(counties_list)} entries)')
    return counties_list

#function population_total will be used when current_operation == 'population-total'. It will take the parameters of counties_list:list[CountyDemographics]
# and dont_print:Bool(dont_print is used to avoid the population_total printing when this function is used inside the function percent. It will
# print (to the terminal) the total 2014 population across all current counties (not per county) as
# "2014 population: xyz" (where xyz is the population total). It will then return the total population as pop_total:int

def population_total(counties_list:list[CountyDemographics], dont_print=False)->int:
    pop_total = 0
    for county in counties_list:
        pop_total += county.population["2014 Population"]
    if not dont_print:
        print(f'2014 population: {pop_total}')
    return pop_total

#function population will be used when current_operation == 'population'. It will take the parameters of counties_list:list[CountyDemographics],
# current_field:list[str] and dont_print:Bool(dont_print is used to avoid the population printing when this function is used inside the function percent.
# It will compute the total 2014 subpopulation across all current counties (not per county). The current field is expected to be a
# percentage of the population for each entry, so this computation requires computing the subpopulation by entry. It will print the result of
# this computation (to the terminal) as "2014 <field> population: xyz" (where xyz is the computed total). It will then return the subpopulation
# as total:int

def population(counties_list:list[CountyDemographics], current_field:list[str], dont_print=False)->float:
    if current_field[0].lower() == 'education':
        total = 0
        for county in counties_list:
            if current_field[1] in county.education:
                total_in_county = (county.education[current_field[1]] / 100) * county.population["2014 Population"]
                total += total_in_county
    elif current_field[0].lower() == 'ethnicities':
        total = 0
        for county in counties_list:
            if current_field[1] in county.ethnicities:
                total_in_county = (county.ethnicities[current_field[1]] / 100) * county.population["2014 Population"]
                total += total_in_county
    elif current_field[0].lower() == 'income':
        total = 0
        for county in counties_list:
            if "Persons Below Poverty Level" in county.income:
                total_in_county = (county.income["Persons Below Poverty Level"] / 100) * county.population[
                    "2014 Population"]
                total += total_in_county
    else:
        print("An error occurred: Invalid field for population operation")

    if not dont_print:
        print(f'2014 {current_field[0]}.{current_field[1]} population: {total}')
    return total

#function percent will be called when current_operation = 'percent'. It will take the parameters of counties_list:list[CountyDemographics] and
# current_field:list[str]. It will print the percentage of the total population within the subpopulation specified by current_field
# as "2014 <field> percentage: xyz" (where xyz is this computed percentage). This operation is based on the previous population-total and
# population functions. It will then return the percentage with percent_of_total:int

def percent(counties_list:list[CountyDemographics], current_field:list[str])->float:
    total_sub_pop = population(counties_list, current_field, dont_print=True)
    total_pop = population_total(counties_list, dont_print=True)
    percent_of_total = (total_sub_pop/total_pop) * 100
    # Print "2014 <field> percentage: xyz" (where xyz is this computed percentage)
    print(f'2014 {current_field[0]}.{current_field[1]} percentage: {percent_of_total}')
    return percent_of_total


def main():

    data_set = build_data.get_data()
    operation_file = sys.argv[1]
    counties_list = data_set
    print(f'{len(counties_list)} records loaded')

    try:
        with open(operation_file, 'r') as file:
            line_number = 0
            for line in file:
                line_number += 1
                line_x = line.strip()
                try:
                    list_of_inputs = line_x.split(':')
                    current_operation = list_of_inputs[0]
                    if len(list_of_inputs) > 1:
                        current_field = list_of_inputs[1].strip()
                        current_field = current_field.split('.')
                    if len(list_of_inputs) > 2:
                        numeric_threshold = float(list_of_inputs[2])

                    #if-else statements to call the above functions:
                    if str(current_operation) == "display":
                        display(counties_list)
                    elif str(current_operation) == "filter-state":
                        counties_list = filter_state(counties_list, current_field)
                    elif str(current_operation) == "filter-gt":
                        counties_list = filter_gt(counties_list, current_field, numeric_threshold)
                    elif str(current_operation) == "filter-lt":
                        counties_list = filter_lt(counties_list, current_field, numeric_threshold)
                    elif str(current_operation) == "population-total":
                        population_total(counties_list)
                    elif str(current_operation) == "population":
                        population(counties_list, current_field)
                    elif str(current_operation) == "percent":
                        percent(counties_list, current_field)
                    else:
                        print(f'An error occurred on line {line_number} - operation invalid')

                except Exception as e:
                    print(f'An error occurred on line {line_number} :', e)

    except FileNotFoundError as e:
        print("An error occurred:", e)
main()
