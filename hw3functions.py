import data
import build_data
import county_demographics
from data import CountyDemographics
import county_demographics


#Part 1
#population_total(list[CountyDemographics]) -> int
#Define a function named population_total with one parameter (of type list[CountyDemographics]),
# a list of county demographics objects (note that this is a parameter of the function and is not
# necessarily the full data set). This function must return the total 2014 Population across the
# set of counties in the provided list. If passed the full data set, then the expected result
# should be 318,857,056.

def population_total(lista:list[CountyDemographics])->int:
    total = 0
    for county in lista:
        total += county.population["2014 Population"]
    return total

#Part 2
#filter_by_state(list[CountyDemographics], str) -> list[CountyDemographics]
#Define a function named filter_by_state with two parameters, a list of county demographics
# objects and a two-letter state abbreviation. This function must return a list of county demographics
# objects from the input list that are within the specified state. If the provided key does not exist
# in the list, then the result should be the empty list. California, for example, has 58 counties
# (with a total 2014 population of 38802500), so the resulting list must include the 58 corresponding
# county demographics objects.

def filter_by_state(lista:list[CountyDemographics], state:str) -> list[CountyDemographics]:
    filtered_list = []
    for county in lista:
        if state == county.state:
            filtered_list.append(county)
    if not filtered_list:
        return []
    return filtered_list

#Part 3
#population_by_education(list[CountyDemographics], str) -> float
#Define a function named population_by_education with two parameters: a list of county demographics objects and the
# education key of interest (e.g., "Bachelor's Degree or Higher"). This function must return the total 2014
# sub-population across the set of counties in the provided list for the specified key of interest.
# For instance, if the input list contains only the example county above and the key is
# "Bachelor's Degree or Higher", the result will be 87,911.145. If the provided key does not exist,
# the result should be 0.

def population_by_education(lista:list[CountyDemographics], ed_key:str)->float:
    total = 0
    for county in lista:
        if ed_key in county.education:
            total_in_county = (county.education[ed_key] / 100) * county.population["2014 Population"]
            total += round(total_in_county)
    return total

#population_by_ethnicity(list[CountyDemographics], str) -> float
#Define a function named population_by_ethnicity with two parameters: a list of county demographics objects
# and the ethnicity key of interest (e.g., 'Two or More Races'). This function must return the total 2014
# sub-population across the set of counties in the provided list for the specified key of interest.
# If the provided key does not exist, the result should be 0.

def population_by_ethnicity(lista:list[CountyDemographics], ethnicity_key:str)->float:
    total = 0
    for county in lista:
        if ethnicity_key in county.ethnicities:
            total_in_county = (county.ethnicities[ethnicity_key] / 100) * county.population["2014 Population"]
            total += round(total_in_county)
    return total

#population_below_poverty_level(list[CountyDemographics]) -> float
#Define a function named population_below_poverty_level with one parameter: a list of county demographics objects.
# This function must return the total 2014 sub-population indicated by income key 'Persons Below Poverty Level'
# across the set of counties in the provided list for the specified key of interest.

def population_below_poverty_level(lista:list[CountyDemographics])->float:
    total = 0
    for county in lista:
        if "Persons Below Poverty Level" in county.income:
            total_in_county = (county.income["Persons Below Poverty Level"] / 100) * county.population["2014 Population"]
            total += round(total_in_county)
    return total

#Part 4
#percent_by_education(list[CountyDemographics], str) -> float
#Define a function named percent_by_education with two parameters: a list of county demographics objects and the
# education key of interest (e.g., "Bachelor's Degree or Higher"). This function must return the specified
# 2014 sub-population as a percentage of the total 2014 population across the set of counties in the provided
# list for the specified key of interest. This function can be defined using the corresponding functions from
# Parts 1 and 2. If the provided key does not exist, the result should be 0.
'''
def percent_by_education(lista:list[CountyDemographics], ed_key:str)->float:
    total = 0
    total_list_pop = population_total(lista)
    for county in lista:
        if ed_key in county.education:
            total_in_county = (county.education[ed_key] / 100) * county.population["2014 Population"]
            total += total_in_county
    percentage = (total/total_list_pop) * 100
    return round(percentage)
    '''


def percent_by_education(counties_list, demographic):
    total = 0
    total_list_pop = 0

    for county in counties_list:
        if demographic in county.education:
            total += county.education[demographic]

        total_list_pop += county.population.get("total", 0)  # Avoid missing population data

    if total_list_pop == 0:
        print(f"Warning: Total population is zero for demographic {demographic}. Returning 0%.")
        return 0  # Default to 0% if population is zero

    percentage = (total / total_list_pop) * 100
    return percentage

#percent_by_ethnicity(list[CountyDemographics], str) -> float
#Define a function named percent_by_ethnicity with two parameters: a list of county demographics objects and the
# ethnicity key of interest (e.g., 'Two or More Races'). This function must return the specified 2014
# sub-population as a percentage of the total 2014 population across the set of counties in the provided
# list for the specified key of interest. This function can be defined using the corresponding functions
# from Parts 1 and 2. If the provided key does not exist, the result should be 0.

'''
def percent_by_ethnicity(lista:list[CountyDemographics], ethnicity_key:str)->float:
    total = 0
    total_list_pop = population_total(lista)
    for county in lista:
        if ethnicity_key in county.ethnicities:
            total_in_county = (county.ethnicities[ethnicity_key] / 100) * county.population["2014 Population"]
            total += total_in_county
    percentage = (total/total_list_pop) * 100
    return round(percentage)
    
'''


def percent_by_ethnicity(counties_list, demographic):
    total = 0
    total_list_pop = 0

    for county in counties_list:
        if demographic in county.ethnicities:
            total += county.ethnicities[demographic]

        # Access the total population from the county's population dictionary
        total_list_pop += county.population.get("total", 0)  # Use "total" or adjust based on your data

    # Check for zero population to avoid division by zero
    if total_list_pop == 0:
        print(f"Warning: Total population is zero for demographic {demographic}. Returning 0%.")
        return 0  # Return 0% if the population is zero

    # Calculate the percentage
    percentage = (total / total_list_pop) * 100
    return percentage


#percent_below_poverty_level(list[CountyDemographics]) -> float
#Define a function named percent_by_education with one parameter: a list of county demographics objects.
# This function must return the 2014 sub-population indicated by income key 'Persons Below Poverty Level'
# as a percentage of the total 2014 population across the set of counties in the provided list for the specified
# key of interest. This function can be defined using the corresponding functions from Parts 1 and 2.

'''
def percent_below_poverty_level(lista:list[CountyDemographics])->float:
    total = 0
    total_list_pop = population_total(lista)
    for county in lista:
        if "Persons Below Poverty Level" in county.income:
            total_in_county = (county.income["Persons Below Poverty Level"] / 100) * county.population[
                "2014 Population"]
            total += round(total_in_county)
    percentage = (total / total_list_pop) * 100
    return round(percentage)
    
'''


def percent_below_poverty_level(counties_list):
    total = 0
    total_list_pop = 0

    for county in counties_list:
        # Ensure that 'below_poverty_level' exists in the county
        if hasattr(county, 'below_poverty_level'):  # Check if the attribute exists
            total += county.below_poverty_level
        else:
            print(f"Warning: {county.county} does not have 'below_poverty_level' data")

        total_list_pop += county.population.get("total", 0)  # Same check for population

    # Check for zero population to avoid division by zero
    if total_list_pop == 0:
        print("Warning: Total population is zero for below poverty level. Returning 0%.")
        return 0

    # Calculate the percentage
    percentage = (total / total_list_pop) * 100
    return percentage

#Part 5
#education_greater_than(list[CountyDemographics], str, float) -> list[CountyDemographics]
#education_less_than(list[CountyDemographics], str, float) -> list[CountyDemographics]
#Define two functions, education_greater_than and education_less_than, each taking three parameters:
# a list of county demographics objects, the education key of interest, and a numeric threshold value.
# This function must return a list of all county demographics objects for which the value for the specified
# key is greater than or less than (as appropriate by function name) the specified threshold value.
# For instance, we might want to find all counties in which the "Bachelor's Degree or Higher" population is
# greater than 60 percent.

def education_greater_than(lista:list[CountyDemographics], ed_key:str, numeric_threshold:float)->list[CountyDemographics]:
    result_list = []
    for county in lista:
        if ed_key in county.education:
            percentage = county.education[ed_key]
            if percentage > numeric_threshold:
                result_list.append(county)
    return result_list

def education_less_than(lista:list[CountyDemographics], ed_key:str, numeric_threshold:float)->list[CountyDemographics]:
    result_list = []
    for county in lista:
        if ed_key in county.education:
            percentage = county.education[ed_key]
            if percentage < numeric_threshold:
                result_list.append(county)
    return result_list

#ethnicity_greater_than(list[CountyDemographics], str, float) -> list[CountyDemographics]
#ethnicity_less_than(list[CountyDemographics], str, float) -> list[CountyDemographics]
#Define two functions, ethnicity_greater_than and ethnicity_less_than, each taking three parameters: a list of
# county demographics objects, the ethnicity key of interest, and a numeric threshold value.
# This function must return a list of all county demographics objects for which the value for the
# specified key is greater than or less than (as appropriate by function name) the specified threshold value.
# For instance, we might want to find all counties in which the 'Hispanic or Latino' population is greater
# than 30 percent.

def ethnicity_greater_than(lista:list[CountyDemographics], ethnicity_key:str, numeric_threshold:float)->list[CountyDemographics]:
    result_list = []
    for county in lista:
        if ethnicity_key in county.ethnicities:
            percentage = county.ethnicities[ethnicity_key]
            if percentage > numeric_threshold:
                result_list.append(county)
    return result_list

def ethnicity_less_than(lista:list[CountyDemographics], ethnicity_key:str, numeric_threshold:float)->list[CountyDemographics]:
    result_list = []
    for county in lista:
        if ethnicity_key in county.ethnicities:
            percentage = county.ethnicities[ethnicity_key]
            if percentage < numeric_threshold:
                result_list.append(county)
    return result_list

#below_poverty_level_greater_than(list[CountyDemographics], float) -> list[CountyDemographics]
#below_poverty_level_less_than(list[CountyDemographics], float) -> list[CountyDemographics]
#Define two functions, below_poverty_level_greater_than and below_poverty_level_less_than,
# each taking two parameters: a list of county demographics objects and a numeric threshold value.
# This function must return a list of all county demographics objects for which the value for key
# 'Persons Below Poverty Level' is greater than or less than (as appropriate by function name) the
# specified threshold value. For instance, we might want to find all counties in which the population below
# the poverty level is greater than 30 percent.

def below_poverty_level_greater_than(lista:list[CountyDemographics], numeric_threshold:float)->list[CountyDemographics]:
    total = 0
    result_list = []
    for county in lista:
        if 'Persons Below Poverty Level' in county.income:
            percentage = county.income['Persons Below Poverty Level']
            if percentage > numeric_threshold:
                result_list.append(county)
    return result_list

def below_poverty_level_less_than(lista:list[CountyDemographics], numeric_threshold:float)->list[CountyDemographics]:
    total = 0
    result_list = []
    for county in lista:
        if 'Persons Below Poverty Level' in county.income:
            percentage = county.income['Persons Below Poverty Level']
            if percentage < numeric_threshold:
                result_list.append(county)
    return result_list
