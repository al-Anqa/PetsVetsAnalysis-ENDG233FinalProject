'''
ENDG233 Final Project
Pets Vets Analysis:
A project to look at the pet and veterinarian distributions across Calgary utilizing open-source data sets
By: Dylan Conley (30140483) and Ahmed Almousawi (30140399)

Modules required:
    matplotlib
    numpy
CSV files required:
    pets_data.csv
    communities_data.csv
    vets_data.csv
'''

import numpy as np
import matplotlib.pyplot as plt

class Neighbourhood:
    """A class used to create Neighbourhood objects.

        Attributes:
            name (str): String that represents the neighbourhood name
            population (int): Integer that represents the number of residents in a neighbourhood
            num_cats (str): String that represents the number of cats in a neighbourhood
            num_dogs (str): String that represents the number of dogs in a neighbourhood
            income (int): String that represents the median income in the neighbourhood
    """

    def __init__(self, name, population, num_cats, num_dogs, income):
        self.name = name
        self.population = population
        self.num_cats = num_cats
        self.num_dogs = num_dogs
        self.income = income

    def print_neighbourhood_info(self):
        print()
        print(f'Selected neighbourhood: {self.name}   Population: {self.population}   Average Income: {self.income}')
        print(f'\nPets Information:\nNumber of Cats in {self.name}: {self.num_cats:<6}Number of Cats per 100 people: {(self.num_cats / self.population) * 100:.2f}')
        print(f'Number of Dogs in {self.name}: {self.num_dogs:<6}Number of Dogs per 100 people: {(self.num_dogs / self.population) * 100:.2f}')
        print(f'Number of Pets in {self.name}: {self.num_dogs + self.num_cats:<6}Number of Pets per 100 people: {((self.num_dogs + self.num_cats)/ self.population) * 100:.2f}')
        print()

def main():
    '''Runs the bulk of the code
    Imports the data, uses a function to extract and convert information from the imports into more usable forms and then brings up the main menu

    parameters: none

    returns: none (The return statement is never reached. The program ends by using exit() which never causes a function to return to this function)
    
    '''
    pets_data = np.genfromtxt('pets_data.csv',  dtype=('U1000','U1000','U1000','U1000',int), delimiter=',', skip_header = True)

    communities_data = np.genfromtxt('communities_data.csv',  dtype=['U1000',int,int,int,int,int], delimiter=',', skip_header = True)

    vets_data = np.genfromtxt('vets_data.csv',  dtype=('U1000','U1000',int), delimiter=',', skip_header = True)

    initial_pet_calculations = run_initial_pet_calculations(pets_data, communities_data, vets_data)
    
    print('Welcome to a program examining the pet and veterinarian distributions across Calgary\n')

    main_menu(pets_data, communities_data, vets_data,initial_pet_calculations)

#Start of Program Calculations
def run_initial_pet_calculations(pets_data, communities_data, vets_data):
    '''Takes the imported data and runs several calculations with them.
    
    parameters:
    pets_data: Data directly imported from a csv file. A 1D array with rows of tuples. Within each tuple: 
        index 0: String. Date
        index 1: String. Community abbreviation
        index 2: String. Community
        index 3: String. Cats or dogs
        index 4: Int. Number of cats or dogs
    communities_data: Data directly imported from a csv file. A 1D array with rows of tuples. Within each tuple:
        index 0: String. Community
        index 1: Int. Median Household Income
        index 2: Int. Median Age
        index 3: Int. Population 2014
        index 4: Int. Dwellings 2014
        index 5: Int. City Quadrant (0 = NE, 1 = NW, 2= SW, 3 = SE)
    vets_data: Data directly imported from a csv file. A 1D array with rows of tuples. Within each tuple:
        index 0: String. Community
        index 1: String. Name of veterinarian
        index 2: Int. 24 hour clinic? (1 = True, 0 = False)
    
    returns:
    pets_registration: 2D array with information on number of cats/dogs/total pets in each community
        index 0: String. Community
        index 1: Int. Number of Cats
        index 2: Int. Number of Dogs
        index 3: Int. Number of Cats and Dogs
    cats_per_capita: Dict. Contains number of cats in each community divided by the population. Format is 'Community Name': Number of Cats (int)
    dogs_per_capita: Dict. Contains number of dogs in each community divided by the population. Format is 'Community Name': Number of Dogs (int)
    pets_per_capita: Dict. Contains number of pets in each community divided by the population. Format is 'Community Name': Number of pets (int)
    communitity_list: List. Contains all the communities in Calgary            
    NE_communities: List. Contains all the communities in the NE
    NW_communities: List. Contains all the communities in the NW
    SW_communities: List. Contains all the communities in the SW
    SE_communities: List. Contains all the communities in the SE
    pets_per_vet: Dict. Contains the number of pets for each community divided by the number of vets + 1. Format is 'Community Name': Pets in Community / (Vets + 1)
    '''

    # Community lists: creates lists of all communities, as well as the communities in each quadrant
    community_list, NE_communities, NW_communities, SW_communities, SE_communities = [], [], [], [], []
    for row in communities_data:                # Gets each tuple from the 1D array
        community_list.append(row[0])           # Adds the community name to community_list 
        if row[5] == 1:                         # Adds to NE if the final tuple value is 1
            NE_communities.append(row[0])
        elif row[5] == 2:                       # Adds to NW if the final tuple value is 2
            NW_communities.append(row[0])
        elif row[5] == 3:                       # Adds to SW if the final tuple value is 3
            SW_communities.append(row[0])
        elif row[5] == 4:                       # Adds to SE if the final tuple value is 4
            SE_communities.append(row[0])

    # Pets Registration: produces a strucured array pets_registration that contains the number of cats and dogs for each community
    
    pets_registration, combined_pets = [], []

    for row in pets_data:
        if row[0] == 'October 2021' and row[2] in community_list:       # Gets the most recent cats and dogs registration data from October 2021 and ensures that only communities that we have census data for are taken
            pets_registration.append(row[2])                            # Gets the community name and adds to list
            pets_registration.append(row[4])                            # Gets the # of cats/dogs and adds to list
    pets_registration = np.array(pets_registration)                     # Creates a 1D array from the list
    pets_registration = pets_registration.reshape((int(len(pets_registration)/4)), 4)   # Turns the 1D array into a 2D array with 4 columns and (1D Array Length / 4) Rows; current format is Community Name, Cats, Community Name, Dogs
    pets_registration = np.delete(pets_registration, 2, 1)              # Deletes the third column (repeat of communtity name)
    
    for row in pets_registration:
        combined_pets.append(int(row[1]) + int(row[2]))                 # Makes a consisting of the combined cats and dogs from each community

    pets_registration = np.c_[pets_registration, combined_pets]         # Adds the combined_pets list to the end of the array, overall formatting is community, cats, dogs, combined total
    pets_registration = list(zip(*pets_registration.T))                 # Turns it into a list so we can convert to a structured array
    
    dtp = np.dtype([('Name', 'U100'), ('Cats', '>i4'), ('Dogs', '>i4'), ('Total', '>i4')])      #Sets the datatype for each column of the structured array
    pets_registration = np.array(pets_registration, dtype=dtp)          # Creates a structured array

    # Cats/Dogs/Pets per Capita: Creates 3 dictionaries containing the number of cats, number of dogs, and total number of pets in each community using data from pets_registration
    cats_per_cap, dogs_per_cap, pets_per_cap = {}, {}, {}               
    index = 5                                                           # skips the first 5 rows of communities_data (Calgary-wide and Quadrant data)
    for row in pets_registration:                                       
        population = communities_data[index][3]
        cats_per_cap[row[0]] = row[1] / population                      # Gets the number of cats in a community and divides by population
        dogs_per_cap[row[0]] = row[2] / population                      # Gets the number of dogs in a community and divides by population
        pets_per_cap[row[0]] = row[3] / population                      # Gets the number of pets in a community and divides by population
        index += 1
    
    # Pets-per-Vet: gets the number of vets in each community and gives a dictionary containing the number of pets for each vet in the community
    pets_per_vet, vets_per_community, vets_per_community_plus_one = {}, {}, {}
    for community in pets_registration:                         
        vets_in_community = 0                                   # Default is 0 vets in a community
        for row in vets_data:                                   # Check for the community name in vets_data
            if community[0] == row[0]:                          # If the community name matches with the neighborhood the vet is located in
                vets_in_community += 1                          # Add it to the number of vets in community
        vets_per_community[community[0]] = vets_in_community    # Create dictionary with that value
        vets_per_community_plus_one[community[0]] = vets_per_community[community[0]] + 1    # Add one to find the hypothetical best place to open a vet and to prevent divide by 0 errors

        pets_per_vet[community[0]] = community[3] / vets_per_community_plus_one[community[0]]   # Create a third dictionary with the community name and the pet_per_vet value

    return pets_registration, cats_per_cap, dogs_per_cap, pets_per_cap, community_list, NE_communities, NW_communities, SW_communities, SE_communities, pets_per_vet

#Main menu
def main_menu(pets_data, communities_data, vets_data,initial_pet_calculations):
    '''Collects the users input to either see options related to pets, vets or to end the code. The pets or vets section will then be run if selected
    This function is designed to be run multiple times as it is an option to return to it from either the pets or vets menu
    
    parameters:
    pets_data: Data directly imported from a csv file. A 1D array with rows of tuples. Within each tuple: 
        index 0: String. Date
        index 1: String. Community abbreviation
        index 2: String. Community
        index 3: String. Cats or dogs
        index 4: Int. Number of cats or dogs
    communities_data: Data directly imported from a csv file. A 1D array with rows of tuples. Within each tuple:
        index 0: String. Community
        index 1: Int. Median Household Income
        index 2: Int. Median Age
        index 3: Int. Population 2014
        index 4: Int. Dwellings 2014
        index 5: Int. City Quadrant (0 = NE, 1 = NW, 2= SW, 3 = SE)
    vets_data: Data directly imported from a csv file. A 1D array with rows of tuples. Within each tuple:
        index 0: String. Community
        index 1: String. Name of veterinarian
        index 2: Int. 24 hour clinic? (1 = True, 0 = False)
    initial_pet_calculations: A tuple containing data that was extracted, modified and formatted from the orginal csv imports:
        index 0: 2D array. Col. 0 is all communities, Col. 1 is total cats, Col.2 is total dogs, Col.3 is total cats and dogs
        index 1: Dict. The keys are communities and the values are that communities cats per capita
        index 2: Dict. The keys are communities and the values are that communities dogs per capita
        index 3: Dict. The keys are communities and the values are that communities cats and dogs per capita
        index 4: List. Contains all the communities in Calgary            
        index 5: List. Contains all the communities in the NE
        index 6: List. Contains all the communities in the NW
        index 7: List. Contains all the communities in the SW
        index 8: List. Contains all the communities in the SE
        index 9: Dict. Contains the number of pets for each community divided by the number of vets + 1. Format is 'Community Name': Pets in Community / (Vets + 1)

    returns: none (The return statement is never reached. The program ends by using exit() which causes this function to never finish)
    '''
    print_main_menu() #Prints the input options to the user. They are inserted in various spots to always have the menu printed when the user enters this function
    while True:
        user_input = input()
        if user_input == 'Pets':
            pets_menu(pets_data, communities_data, initial_pet_calculations)
            print_main_menu()
        elif user_input == 'Vets':
            vets_menu(communities_data, vets_data, initial_pet_calculations)
            print_main_menu()
        elif user_input == 'End':
            exit() #Ends the code
        else: 
            print('That was an invalid entry. Please try again using one of the above options')
    
def print_main_menu():
    ''' A simple function that prints the main menu options.
    
    parameters: none
    returns: none
    
    '''
    print('This is the main menu. Please select one of the following options:\n')
    print('{selection_option:>4} : {reason}'.format(selection_option = 'Pets', reason = 'To learn more about the pet distribution in Calgary'))
    print('{selection_option:>4} : {reason}'.format(selection_option = 'Vets', reason = 'To learn more about the veterinarian distribution in Calgary'))
    print('{selection_option:>4} : {reason}'.format(selection_option = 'End', reason = 'To end the program'))
    return

#Vets menu
def vets_menu(communities_data, vets_data,initial_pet_calculations):
    '''Collects the users input which causes either a return to the main menu, end the program or to run a variety of different functions meant to manipulate and output information.
    This function is designed to be run multiple times as it is returned to after running each data manipulation or from the main menu multiple times
    
    parameters:
    pets_data: Data directly imported from a csv file. A 1D array with rows of tuples. Within each tuple: 
        index 0: String. Date
        index 1: String. Community abbreviation
        index 2: String. Community
        index 3: String. Cats or dogs
        index 4: Int. Number of cats or dogs
    communities_data: Data directly imported from a csv file. A 1D array with rows of tuples. Within each tuple:
        index 0: String. Community
        index 1: Int. Median Household Income
        index 2: Int. Median Age
        index 3: Int. Population 2014
        index 4: Int. Dwellings 2014
        index 5: Int. City Quadrant (0 = NE, 1 = NW, 2= SW, 3 = SE)
    vets_data: Data directly imported from a csv file. A 1D array with rows of tuples. Within each tuple:
        index 0: String. Community
        index 1: String. Name of veterinarian
        index 2: Int. 24 hour clinic? (1 = True, 0 = False)
    initial_pet_calculations: A tuple containing data that was extracted, modified and formatted from the orginal csv imports:
        index 0: 2D array. Col. 0 is all communities, Col. 1 is total cats, Col.2 is total dogs, Col.3 is total cats and dogs
        index 1: Dict. The keys are communities and the values are that communities cats per capita
        index 2: Dict. The keys are communities and the values are that communities dogs per capita
        index 3: Dict. The keys are communities and the values are that communities cats and dogs per capita
        index 4: List. Contains all the communities in Calgary            
        index 5: List. Contains all the communities in the NE
        index 6: List. Contains all the communities in the NW
        index 7: List. Contains all the communities in the SW
        index 8: List. Contains all the communities in the SE
        index 9: Dict. Contains the number of pets for each community divided by the number of vets + 1. Format is 'Community Name': Pets in Community / (Vets + 1)

    returns: none
    '''
    print()
    print_vets_menu() #Prints the input options to the user. They are inserted in various spots to always have the menu printed when the user enters this function
    while True:
        user_input = input()
        if user_input == 'Pets Per Vet':
            graph_community_vs_income_and_pets_per_vet(communities_data, initial_pet_calculations)
            print_vets_menu()
        elif user_input == 'Vets In Area': 
            vets_in_area(vets_data, initial_pet_calculations)
            print_vets_menu()
        elif user_input == 'Return':
            print()
            return #Brings user back to main menu
        elif user_input == 'End':
            exit() #Ends the code
        else:
            print('That was an invalid entry. Please try again using one of the above options')

def print_vets_menu():
    ''' A simple function that prints the vet menu options.
    
    parameters: none
    returns: none
    
    '''
    print('This is the veterinarian statistics menu. Please select one of the following options:\n')
    print('{selection_option:>12} : {reason}'.format(selection_option = 'Pets Per Vet', reason = 'To see a graph comparing the number of pets per veterinarian for different areas in Calgary'))
    print('{selection_option:>12} : {reason}'.format(selection_option = 'Vets In Area', reason = 'To learn more about the veterinarian services offered for different areas of Calgary'))        
    print('{selection_option:>12} : {reason}'.format(selection_option = 'Return', reason = 'To return to the main menu'))        
    print('{selection_option:>12} : {reason}'.format(selection_option = 'End', reason = 'To end the program'))
    return

#Pets menu
def pets_menu(pets_data, communities_data,initial_pet_calculations):
    '''Collects the users input which causes either a return to the main menu, end the program or to run a variety of different functions meant to manipulate and output information.
    This function is designed to be run multiple times as it is returned to after running each data manipulation or from the main menu multiple times
    
    parameters:
    pets_data: Data directly imported from a csv file. A 1D array with rows of tuples. Within each tuple: 
        index 0: String. Date
        index 1: String. Community abbreviation
        index 2: String. Community
        index 3: String. Cats or dogs
        index 4: Int. Number of cats or dogs
    communities_data: Data directly imported from a csv file. A 1D array with rows of tuples. Within each tuple:
        index 0: String. Community
        index 1: Int. Median Household Income
        index 2: Int. Median Age
        index 3: Int. Population 2014
        index 4: Int. Dwellings 2014
        index 5: Int. City Quadrant (0 = NE, 1 = NW, 2= SW, 3 = SE)
    vets_data: Data directly imported from a csv file. A 1D array with rows of tuples. Within each tuple:
        index 0: String. Community
        index 1: String. Name of veterinarian
        index 2: Int. 24 hour clinic? (1 = True, 0 = False)
    initial_pet_calculations: A tuple containing data that was extracted, modified and formatted from the orginal csv imports:
        index 0: 2D array. Col. 0 is all communities, Col. 1 is total cats, Col.2 is total dogs, Col.3 is total cats and dogs
        index 1: Dict. The keys are communities and the values are that communities cats per capita
        index 2: Dict. The keys are communities and the values are that communities dogs per capita
        index 3: Dict. The keys are communities and the values are that communities cats and dogs per capita
        index 4: List. Contains all the communities in Calgary            
        index 5: List. Contains all the communities in the NE
        index 6: List. Contains all the communities in the NW
        index 7: List. Contains all the communities in the SW
        index 8: List. Contains all the communities in the SE
        index 9: Dict. Contains the number of pets for each community divided by the number of vets + 1. Format is 'Community Name': Pets in Community / (Vets + 1)


    returns: none
    '''
    
    print()
    print_pets_menu() #Prints the input options to the user. They are inserted in various spots to always have the menu printed when the user enters this function
    while True:
        user_input = input()
        if user_input == 'Income':
            graph_income_vs_pets_by_capita(communities_data,initial_pet_calculations)
            print_pets_menu()
        elif user_input == 'Registration': 
            graph_time_vs_new_registration(pets_data, initial_pet_calculations)
            print_pets_menu()
        elif user_input == 'Total Pets':
            area_most_least_pets_total(initial_pet_calculations)
            print_pets_menu()
        elif user_input == 'Pets Per Capita':
            area_most_least_pets_capita(initial_pet_calculations)
            print_pets_menu()
        elif user_input == 'Area Info':
            area_info(communities_data, initial_pet_calculations)
            print_pets_menu()
        elif user_input == 'Return':
            print() 
            return #Brings the user back to the main menu
        elif user_input == 'End':
            exit() #Ends the code
        else:
            print('That was an invalid entry. Please try again using one of the above options')

def print_pets_menu():
    ''' A simple function that prints the pets_menu options.
    
    parameters: none
    returns: none
    
    '''
    print('This is the pet statistics menu. Please select one of the following options:\n')
    print('{selection_option:>15} : {reason}'.format(selection_option = 'Income', reason = 'To see a graph comparing income by community compared to pet ownership'))
    print('{selection_option:>15} : {reason}'.format(selection_option = 'Registration', reason = 'To see a graph comparing the change in pets for the last three years'))        
    print('{selection_option:>15} : {reason}'.format(selection_option = 'Total Pets', reason = 'To learn more about the areas in Calgary with the most or least pets'))
    print('{selection_option:>15} : {reason}'.format(selection_option = 'Pets Per Capita', reason = 'To learn more about the areas in Calgary with the most or least pets per capita'))
    print('{selection_option:>15} : {reason}'.format(selection_option = 'Area Info', reason = 'To see a variety of statistics related to pets within an area of Calgary'))
    print('{selection_option:>15} : {reason}'.format(selection_option = 'Return', reason = 'To return to the main menu'))        
    print('{selection_option:>15} : {reason}'.format(selection_option = 'End', reason = 'To end the program'))
    return

#Functions called from the vets menu
def graph_community_vs_income_and_pets_per_vet(communities_data, initial_pet_calculations):
    '''This functions takes pet per capita and income data and compares it on the same graph

    parameters: 
    communities_data: Data directly imported from a csv file. A 1D array with rows of tuples. The relevant indexes within the tuple are:
        index 0: String. Community
        index 1: Int. Median Household Income
    initial_pet_calculations: A tuple containing data that was extracted, modified and formatted from the orginal csv imports. The relevant index within the tuple is:
        index 9: Dict. Contains the number of pets for each community divided by the number of vets + 1. Format is 'Community Name': Pets in Community / (Vets + 1)

    returns: none
    '''
    #Creates a dictionary pairing community with community income. It uses communities data which includes Calgary and quadrants so those are removed
    all_communities_income = {}
    for row in communities_data:
        all_communities_income[row[0]] = row[1]
    all_communities_income.pop('NE')
    all_communities_income.pop('NW')
    all_communities_income.pop('SE')
    all_communities_income.pop('SW')
    all_communities_income.pop('Calgary')

    #A dictionary pairing community with the amount of cats and dogs per veterinarian
    all_communities_cats_dogs_vet = initial_pet_calculations[9] 

    #Sorts the dictionary so that in both dictionary's are ordered from lowest community to highest community income
    all_communities_sorted = {}
    all_communities_cats_dogs_vet_sorted = {}
    income_sorted = sorted(all_communities_income.values()) #Creates an iterable of the incomes in order from smallest to biggest
    for sorted_income in income_sorted: 
        for community, income in all_communities_income.items():
            if income == sorted_income:
                all_communities_sorted[community] = income #Creates a sorted community with income dictionary
                for community_unsorted, pets in all_communities_cats_dogs_vet.items():
                    if community == community_unsorted:
                        all_communities_cats_dogs_vet_sorted[community] = pets #Creates a sorted community with pets per vet dictionary

    income_x_axis_labels = list(all_communities_sorted.keys())
    #Generates an order of numbers starting at 1 that has the same amount of numbers as the number of communities
    income_x_axis_points = []
    for i in range(len(income_x_axis_labels)):
        income_x_axis_points.append(i+1)

    fig = plt.figure()

    #Two subplots will be created on top of each other to have two sets of data with different values on the same plot
    ax1 = fig.add_subplot(111)
    #Plots cat, dog points
    ax1.plot(income_x_axis_points, all_communities_cats_dogs_vet_sorted.values(), 'bo', label='Total Cats and Dogs Per Veterinarian') # Graphs all coordinates
    ax1.set_ylabel('Pets per Vetrinarians if a New Vetrinarian Opened in Each Community', color='blue')
    #Changes the labels from numbers to communities and formats them
    plt.xticks(income_x_axis_points, income_x_axis_labels, fontsize=6, rotation = 90)
    plt.grid()
    #Creates a second axis along the y-axis that has a shared x axis
    ax2 = ax1.twinx()
    #Plots income points
    ax2.plot(income_x_axis_points, all_communities_sorted.values(), 'go', label='Average Household Income') # Graphs all coordinates
    ax2.set_ylabel('Average Income for Each Community', color='green')

    #Creates a title
    plt.title('Pets per Vetrinarian and Income for Each Community')      

    #Adds x-axis title
    ax1.set_xlabel('Communities')

    #Used to set the lower and upped bounds for the display of the x-axis
    plt.xlim(0, len(income_x_axis_points)+1)  

    #Explains graph
    plt.figtext(0.5, 0.01, "This graph is designed to identify the best locations to start a new veterinarian practice.\nThe left y-axis is designed to demonstrate where there would be a large market of pets.\nThe right y-axis demonstrates which communities have more money to pay for veterinarian services", ha="center", fontsize=7)

    #Allows for slightly better viewing of the graph and ensures the x-title can be seen
    plt.tight_layout()

    #Shows graph
    plt.show()    

    print('You are now being returned to the vet statistics menu')   

    return

def vets_in_area(vets_data, initial_pet_calculations):
    '''This function collects the user input and then outputs any veternarians in the area specified by the user. The veternarians are sorted by 24 hours vs not

    parameters:
    vets_data: Data directly imported from a csv file. A 1D array with rows of tuples. Within each tuple:
        index 0: String. Community
        index 1: String. Name of veterinarian
        index 2: Int. 24 hour clinic? (1 = True, 0 = False)    
    initial_pet_calculations: A tuple containing data that was extracted, modified and formatted from the orginal csv imports. The relevant parts used are:
        index 4: List. Contains all the communities in Calgary            
        index 5: List. Contains all the communities in the NE
        index 6: List. Contains all the communities in the NW
        index 7: List. Contains all the communities in the SW
        index 8: List. Contains all the communities in the SE
    
    returns: none
    '''
    #Generates lists from the parameters that may be called upon
    community_list = initial_pet_calculations[4]
    northwest_communities = initial_pet_calculations[6]
    southwest_communities = initial_pet_calculations[7]
    northeast_communities = initial_pet_calculations[5]
    southeast_communities = initial_pet_calculations[8]

    print('This is the veterinarian info menu. Please type in the community or quadrant you would like to learn more about. If you need to see the options you can enter please type Details')
    
    #This section loops until a valid input is entered. The user is given the option to see all the selection options otherwise it takes an input and sets the selected_community_list to a correct value
    while True:
        area = input()
        if area == 'Details':
            for index,item in enumerate(community_list):
                if index + 2 <= len(community_list): #Causes it to go through every element except the last in this if statement
                    print('{}, '.format(item), end='') #Prints the area followed by a comma and a space
                else:                                #For the last element just prints the element with a comma or space
                    print(item)
            continue
        elif area == 'Calgary':
            selcted_community_list = community_list  #The valid communities is set to a list of all communities in Calgary
            break
        elif area == 'NE':
            selcted_community_list = northeast_communities #The valid communities is set to a list of the communities in North-East Calgary
            break
        elif area == 'NW':
            selcted_community_list = northwest_communities #The valid communities is set to a list of the communities in North-West Calgary
            break
        elif area == 'SW':
            selcted_community_list = southwest_communities #The valid communities is set to a list of the communities in South-West Calgary
            break
        elif area == 'SE':
            selcted_community_list = southeast_communities #The valid communities is set to a list of the communities in South-East Calgary
            break
        elif area in community_list:
            selcted_community_list = [area] #The valid communities is set to just the community specified
            break
        else:
            print('That was an invalid entry. Please try again or enter Details to see the options')

    #Sets up two variable to indicate whether there was any valid vets for each category
    at_least_one_hours_24 = False
    at_least_one_non_24_hours = False

    for row in vets_data:
        if row[0] in selcted_community_list and row[2] == 1 and at_least_one_hours_24 == False: #Only runs if the community is within one of the selected communities and it is the first 24 hours facility in the area
            print()
            print('Vets in {} that currently have 24 hour services:'.format(area))
            print(row[1])
            at_least_one_hours_24 = True #Changed to indicate that there is at least one 24 hours clinic in the area
        elif row[0] in selcted_community_list and row[2] == 1 and at_least_one_hours_24 == True: #Only runs if the community is within one of the selected communities and it is the second or greater 24 hours facility in the area
            print(row[1])
    for row in vets_data:
        if row[0] in selcted_community_list and row[2] == 0 and at_least_one_hours_24 == True and at_least_one_non_24_hours == False: #Only runs if the community is within the one of the selected communities, there was at least one 24 hour clinic found and it is the first not 24 hour clinic in the area
            print()
            print('Vets in {} that are not 24 hours:'.format(area))
            print(row[1])
            at_least_one_non_24_hours = True #Changed to indicate that there is at least one non-24 hours clinic in the area
        elif row[0] in selcted_community_list and row[2] == 0 and at_least_one_hours_24 == False and at_least_one_non_24_hours == False: #Only runs if the community is within the one of the selected communities, there were no 24 hour clinics found and it is the first not 24 hour clinic in the area
            print()
            print('There are no 24 hour clinics in this area')
            print()
            print('Vets in {} that are not 24 hours:'.format(area))
            print(row[1])
            at_least_one_non_24_hours = True #Changed to indicate that there is at least one non-24 hours clinic in the area
        elif row[0] in selcted_community_list and row[2] == 0 and at_least_one_non_24_hours == True: #Only runs if the community is within the one of the selected communities and it is the second or greaterr non-24 hours facility in the area
            print(row[1])
    if at_least_one_non_24_hours == False and at_least_one_hours_24 == False: #Only runs if there is no clinics at all in the area
        print()
        print('There are no veterinarian clinics in this area')
    elif at_least_one_non_24_hours == False: #Only runs if there were 24 hour clinics but no non-24 hour clinics
        print()
        print('There are only 24 hour clinics in this area')
    print()
    return

#Functions called from the pets menu
def graph_income_vs_pets_by_capita(communities_data, initial_pet_calculations):
    '''This function takes cats and dogs and income by community and graphs it
    The x-axis is the communities ordered from poorest to richest
    The x-axis is three lines, one for cats, one for dogs, one for cats and dogs. It displays all points as well as a line of best fit

    parameters:
    communities_data: Data directly imported from a csv file. A 1D array with rows of tuples. The relevant indexes within the tuple are:
        index 0: String. Community
        index 1: Int. Median Household Income    
    initial_pet_calculations: A tuple containing data that was extracted, modified and formatted from the orginal csv imports. The relevant parts of it used are:
        index 1: Dict. The keys are communities and the values are that communities cats per capita
        index 2: Dict. The keys are communities and the values are that communities dogs per capita
        index 3: Dict. The keys are communities and the values are that communities cats and dogs per capita
    
    returns: none
    '''
    # Generates a dictionary pairing just communities with their average income using the dataset all_communities_income
    all_communities_income = {}
    for row in communities_data:
        all_communities_income[row[0]] = row[1]
    all_communities_income.pop('NE') #Communities_data also has quadrants and city so they are removed
    all_communities_income.pop('NW')
    all_communities_income.pop('SE')
    all_communities_income.pop('SW')
    all_communities_income.pop('Calgary')

    #Dictionaries pairing communities with their pets by capita
    all_communities_cats_dogs = initial_pet_calculations[3] 
    all_communities_cats = initial_pet_calculations[1]
    all_communities_dogs = initial_pet_calculations[2]

    #This part pulls the income values, sorts them and then matches the communities back up with the incomes
    all_communities_sorted = {}
    income_sorted = sorted(all_communities_income.values())
    for sorted_income in income_sorted:
        for community, income in all_communities_income.items():
            if income == sorted_income:
                all_communities_sorted[community] = income

    #A list of the communities that has been sorted poorest to richest
    income_x_axis_labels = list(all_communities_sorted.keys())

    #Generates an order of numbers starting at 1 that has the same amount of numbers as the number of communities
    income_x_axis_points = []
    for i in range(len(income_x_axis_labels)):
        income_x_axis_points.append(i+1)

    #Creates the three y-axis data sets that are pet populations listed in order
    cats_dogs_y_axis = []
    cats_y_axis = []
    dogs_y_axis = []
    for community_sorted in all_communities_sorted.keys(): #Looks at the sorted communities
        for community, population in all_communities_cats_dogs.items():
            if community_sorted == community:              #If the sorted community matches the key in the dict pairing community with cats and dogs
                cats_dogs_y_axis.append(population * 100)  #The corresponding animal population is then added to the list. Multiplied by 100 to convert from per 1 person to per 100 people
    for community_sorted in all_communities_sorted.keys(): #Repeats for just cats and then just dogs
        for community,population in all_communities_cats.items():
            if community_sorted == community:
                cats_y_axis.append(population * 100)
    for community_sorted in all_communities_sorted.keys():
        for community,population in all_communities_dogs.items():
            if community_sorted == community:
                dogs_y_axis.append(population * 100)

    #Graphs
    FIGURE1 = 1

    plt.figure(FIGURE1)

    #Converted to numpys to fit np.polyfit() requirements
    income_x_axis_points_numpy = np.array(income_x_axis_points)
    cats_dogs_y_axis_numpy = np.array(cats_dogs_y_axis)    
    cats_y_axis_numpy = np.array(cats_y_axis)    
    dogs_y_axis_numpy = np.array(dogs_y_axis)    

    # Graphs cats and dogs. np.polyfit() takes the x-points and y-points and returns a line of best fit as a1, b1, c1 in the form y=ax^2+bx+c. That line is then graphed as well as the points themselves
    a1, b1, c1 = np.polyfit(income_x_axis_points_numpy, cats_dogs_y_axis_numpy, 2)
    plt.plot(income_x_axis_points_numpy, income_x_axis_points_numpy * income_x_axis_points_numpy * a1 + income_x_axis_points_numpy * b1 + c1, 'b')
    plt.plot(income_x_axis_points, cats_dogs_y_axis, 'bo', label='Cats and Dogs per 100 People')
    
    # Graphs cats. np.polyfit() takes the x-points and y-points and returns a line of best fit as a2, b2, c2 in the form y=ax^2+bx+c. That line is then graphed as well as the points themselves
    a2, b2, c2 = np.polyfit(income_x_axis_points_numpy, cats_y_axis_numpy, 2)
    plt.plot(income_x_axis_points_numpy, income_x_axis_points_numpy * income_x_axis_points_numpy * a2 + income_x_axis_points_numpy * b2 + c2, 'g')
    plt.plot(income_x_axis_points, cats_y_axis, 'go', label='Total Cat per 100 Peoples')
    
    # Graphs dogs. np.polyfit() takes the x-points and y-points and returns a line of best fit as a3, b3, c3 in the form y=ax^2+bx+c. That line is then graphed as well as the points themselves
    a3, b3, c3 = np.polyfit(income_x_axis_points_numpy, dogs_y_axis_numpy, 2)
    plt.plot(income_x_axis_points_numpy, income_x_axis_points_numpy * income_x_axis_points_numpy * a3 + income_x_axis_points_numpy * b3 + c3, 'r')
    plt.plot(income_x_axis_points, dogs_y_axis, 'ro', label='Total Dogs per 100 People')

    #Creates titles and a legend
    plt.title('Pet Ownership Compared to Income')      
    plt.xlabel('Communities (Ordered from lowest average income to highest)')
    plt.ylabel('Number of pets per 100 people')
    plt.legend(shadow=True)

    #Modifies x-axis labels 
    plt.xticks(income_x_axis_points, income_x_axis_labels) #Used to display the community name instead of an integer
    plt.xticks(rotation=90, fontsize=6) #Used to rotate the labels vertically and reduce their size to allow to accomodate for the cramped space
    plt.xlim(0, len(income_x_axis_points)+1)  #Used to set the lower and upped bounds for the display of the x-axis

    #Gives gridlines
    plt.grid()

    #Allows for slightly better viewing of the graph and ensures the x-title can be seen
    plt.tight_layout()

    #Shows graph
    plt.show()    

    print('You are now being returned to the pet statistics menu')

    return

def graph_time_vs_new_registration(pets_data, initial_pet_calculations):
    '''Collects the user's input to determine which communities in Calgary to look at. Once found it generates the number of pets for each month for that area.
    That data is then converted to find the change in pets for each month and then graphed.

    parameters:
    pets_data: Data directly imported from a csv file. A 1D array with rows of tuples. The relvant indexes within each tuple is: 
        index 0: String. Date
        index 2: String. Community
        index 3: String. Cats or dogs
        index 4: Int. Number of cats or dogs
    initial_pet_calculations: A tuple containing data that was extracted, modified and formatted from the orginal csv imports. The relvant indexes within each tuple is: 
        index 4: List. Contains all the communities in Calgary            
        index 5: List. Contains all the communities in the NE
        index 6: List. Contains all the communities in the NW
        index 7: List. Contains all the communities in the SW
        index 8: List. Contains all the communities in the SE

    returns: none
    '''
    community_list = initial_pet_calculations[4]
    northwest_communities = initial_pet_calculations[6]
    southwest_communities = initial_pet_calculations[7]
    northeast_communities = initial_pet_calculations[5]
    southeast_communities = initial_pet_calculations[8]

    print('Please type in the community or quadrant you would like to learn more about. If you need to see the options you can enter please type Details')
    
    #This section loops until a valid input is entered. The user is given the option to see all the selection options otherwise it takes an input and sets the selected_community_list to a correct value
    while True:
        area = input()
        if area == 'Details':
            for index,item in enumerate(community_list):
                if index + 2 <= len(community_list): #Causes it to go through every element except the last in this if statement
                    print('{}, '.format(item), end='') #Prints the area followed by a comma and a space
                else:                                #For the last element just prints the element with a comma or space
                    print(item)
            print('Please type in the community or quadrant you would like to learn more about. If you need to see the options you can enter please type Details')
            continue
        elif area == 'Calgary':
            selcted_community_list = community_list  #The valid communities is set to a list of all communities in Calgary
            break
        elif area == 'NE':
            selcted_community_list = northeast_communities #The valid communities is set to a list of the communities in North-East Calgary
            break
        elif area == 'NW':
            selcted_community_list = northwest_communities #The valid communities is set to a list of the communities in North-West Calgary
            break
        elif area == 'SW':
            selcted_community_list = southwest_communities #The valid communities is set to a list of the communities in South-West Calgary
            break
        elif area == 'SE':
            selcted_community_list = southeast_communities #The valid communities is set to a list of the communities in South-East Calgary
            break
        elif area in community_list:
            selcted_community_list = [area] #The valid communities is set to just the community specified
            break
        else:
            print('That was an invalid entry. Please try again or enter Details to see the options')

    months_list = [] 
    for row in reversed(pets_data): #Creates a list of the all the months in the data set from oldest to newest
        if row[0] not in months_list: 
            months_list.append(row[0])
    
    dates_with_cats, dates_with_dogs, dates_with_cats_and_dogs = {}, {}, {}

    #This section creates 3 dictionaries pairing date with animal population at that date
    #This section deals with there not being any information provided for a specific month and community by instead inserting a numpy NaN value. The significance of a NaN value is it will be skipped over when graphing without an error message
    for date in months_list:
        cats = False #cats and dogs are both indicators as to whether at least one cat/dog data point has been found for that date
        dogs = False
        cats_value = 0 #cats_value and dogs_value are used to track the cats and dogs in order to sum them together for total cats and dogs
        dogs_value = 0
        for row in reversed(pets_data): #Goes through the data oldest date to newest
            if date == row[0] and row[2] in selcted_community_list and row[3] == 'CATS': #If the date is correct, it's a community we want and for cats it evaluates true
                if date in dates_with_cats: #If already in dictionary, the value is added
                    dates_with_cats[date] = dates_with_cats[date] + row[4]
                    cats_value += row[4]
                else:                       #If not in dictionary, the value is created and cats is changed to True
                    dates_with_cats[date] = row[4]
                    cats_value = row[4]
                    cats = True
            if date == row[0] and row[2] in selcted_community_list and row[3] == 'DOGS': #If the date is correct, it's a community we want and for dogs it evaluates true
                if date in dates_with_dogs: #If already in dictionary, the value is added
                    dates_with_dogs[date] = dates_with_dogs[date] + row[4]
                    dogs_value += row[4]
                else:                       #If not in dictionary, the value is created and dogs is changed to True
                    dates_with_dogs[date] = row[4]
                    dogs_value = row[4]
                    dogs = True
        if cats == False: #If no cat value for the specified communities and month then set to Nan
            dates_with_cats[date] = np.NaN
        if dogs == False: #If no dog value for the specified communities and month then set to Nan
            dates_with_dogs[date] = np.NaN
        if dogs == False or cats == False: #If no cat or dog value for the specified communities and month then set to Nan
            dates_with_cats_and_dogs[date] = np.NaN
        else:                              #If both cats and dogs are valid then it is summed and added to cats_and_dogs
            dates_with_cats_and_dogs[date] = cats_value + dogs_value

    #Creates lists to be used to find change in pets
    dates_list_sorted = list(dates_with_cats.keys())
    cats_sorted_by_date = list(dates_with_cats.values())
    dogs_sorted_by_date = list(dates_with_dogs.values())
    cats_and_dogs_sorted_by_date = list(dates_with_cats_and_dogs.values())

    delta_cats = []
    first_value = True
    for value in reversed(cats_sorted_by_date): #Goes through the dates from newest to oldest
        if first_value == True:  #If first value, assigns nothing, instead saves temporary value to be used to find change in for value 2
            temp = value
            first_value = False
        else:                    #If not first value, takes the last value and subtracts the current value to find the change in pets
            delta_cats.append(temp-value)
            temp = value
    delta_cats.reverse() #Reversed to have it be from oldest to newest
    
    delta_dogs = [] #Repeated for dogs
    first_value = True
    for value in reversed(dogs_sorted_by_date):
        if first_value == True:
            temp = value
            first_value = False
        else:
            delta_dogs.append(temp-value)
            temp = value
    delta_dogs.reverse()
    
    delta_cats_dogs = [] #Repeated for cats and dogs
    first_value = True
    for value in reversed(cats_and_dogs_sorted_by_date):
        if first_value == True:
            temp = value
            first_value = False
        else:
            delta_cats_dogs.append(temp-value)
            temp = value
    delta_cats_dogs.reverse()

    dates_list_sorted.pop() # With finding change in, the most recent month can not be found so that value is removed

    dates_x_axis_points = [] #Creates a list of numbers starting from 1 designed to correspond to the dates. Necesarry in order to graph
    for i in range(len(dates_list_sorted)):
        dates_x_axis_points.append(i + 1)
    

    #Graphs
    FIGURE1 = 1

    plt.figure(FIGURE1)

    #Graphs all 3 lines
    plt.plot(dates_x_axis_points, delta_cats_dogs, 'bo--', label='Cats and Dogs')
    
    plt.plot(dates_x_axis_points, delta_cats, 'go--', label='Cats')

    plt.plot(dates_x_axis_points, delta_dogs, 'ro--', label='Dogs')

    #Creates titles and a legend
    if area in ['NE', 'NW', 'SW', 'SE']:
        title = 'Change in Pet Ownership Over 3 Years in the ' + area
    else:
        title = 'Change in Pet Ownership Over 3 Years in ' + area
    plt.title(title)      
    plt.xlabel('Month')
    plt.ylabel('Number of pets')
    plt.legend(shadow=True)

    #Modifies x-axis labels 
    plt.xticks(dates_x_axis_points, dates_list_sorted) #Used to display the community name instead of an integer
    plt.xticks(rotation=45, fontsize=8, ha='right') #Used to rotate the labels vertically and reduce their size to allow to accomodate for the cramped space
    plt.xlim(0, len(dates_x_axis_points)+1)  #Used to set the lower and upped bounds for the display of the x-axis

    #Allows for slightly better viewing of the graph and ensures the x-title can be seen
    plt.tight_layout()

    #Shows graph
    plt.show()    

    print('You are now being returned to the pet statistics menu')

    return

def area_most_least_pets_total(initial_pet_calculations):
    '''This function allows the user to select cat, dog or both and quadrant of city.
       This then causes the program to print out the three most animal populated communities and three least populated communities.
       The user is then given the choice to exit the function or do another selection.

       This specific funtion generates the necesarry data for pets, calls upon a function to determine the user's selection, converts that to an array and then uses a second function to determine and print the max and mins.
    
       parameters:
    initial_pet_calculations: A tuple containing data that was extracted, modified and formatted from the orginal csv imports. The relevant parts used are:
        index 0: 2D array. Col. 0 is all communities, Col. 1 is total cats, Col.2 is total dogs, Col.3 is total cats and dogs           
        index 5: List. Contains all the communities in the NE
        index 6: List. Contains all the communities in the NW
        index 7: List. Contains all the communities in the SW
        index 8: List. Contains all the communities in the SE

       returns: none
    '''
    #Converts 2-D array to three dictionaries that pair all communities with their cats, dogs, and cats and dogs combined
    all_pets_data = initial_pet_calculations[0]
    all_communities_cats, all_communities_dogs, all_communities_cats_dogs = {}, {}, {}
    for row in all_pets_data:
        all_communities_cats[row[0]] = row[1]
        all_communities_dogs[row[0]] = row[2]
        all_communities_cats_dogs[row[0]] = row[3]
    
    #Following part runs infinitely until user chooses to exit
    while True:
        #Runs function that returns a dictionary with the only the area of Calgary the user specifies and the number per community for the type of pet the user specifies. Also returns what that quadrant is and the pet
        valid_communities_dict, area, animal = most_least_pets_step_1(all_communities_cats, all_communities_dogs, all_communities_cats_dogs, initial_pet_calculations)

        #Creates array of just the valid animal population sizes based on a dictionary involving communities and pet numbers
        num_of_pets_array = np.fromiter(valid_communities_dict.values(), dtype=int)
        
        #Runs function that uses the the num_of_pets_array and valid_communities_dict to generally determine the 3 highest and lowest pet populations for within the dictionary
        most_least_pets_step_2(num_of_pets_array, valid_communities_dict, area, animal , '')
    
        #Either ends this section of the code or repeats whole thing
        print('\nPlease type Return to use other parts of the program otherwise hit enter to learn more about the minimum and maximum number of pets for communities in Calgary')
        if input() == 'Return':
            return

def area_most_least_pets_capita(initial_pet_calculations):
    '''This function allows the user to select cat, dog or both and quadrant of city.
       This then causes the program to print out the three most animal populated communities and three least populated communities per capita.
       The user is then given the choice to exit the function or do another selection.

       This specific funtion generates the necesarry data for pets, calls upon a function to determine the user's selection, converts that to an array and then uses a second function to determine and print the max and mins.
    
       parameters:
    initial_pet_calculations: A tuple containing data that was extracted, modified and formatted from the orginal csv imports. The relevant parts used are:
        index 1: Dict. The keys are communities and the values are that communities cats per capita
        index 2: Dict. The keys are communities and the values are that communities dogs per capita
        index 3: Dict. The keys are communities and the values are that communities cats and dogs per capita           
        index 5: List. Contains all the communities in the NE
        index 6: List. Contains all the communities in the NW
        index 7: List. Contains all the communities in the SW
        index 8: List. Contains all the communities in the SE

       returns: none
    '''
    #Creates three dictionaries that pair all communities with their cats, dogs, and cats and dogs combined per capita
    all_communities_cats_dogs = initial_pet_calculations[3] 
    all_communities_cats = initial_pet_calculations[1]
    all_communities_dogs = initial_pet_calculations[2]

    while True:    
        #Runs function that returns a dictionary with the only the area of Calgary the user specifies and the number per community for the type of pet the user specifies. Also returns what that quadrant is and the pet        
        valid_communities_dict, area, animal = most_least_pets_step_1(all_communities_cats, all_communities_dogs, all_communities_cats_dogs, initial_pet_calculations)
    
        #Creates array of just the valid animal population sizes per capita based on a dictionary involving communities and pet numbers
        num_of_pets_array = np.fromiter(valid_communities_dict.values(), dtype=float)
        
        #Runs function that uses the the num_of_pets_array and valid_communities_dict to generally determine the 3 highest and lowest pet populations per capita for within the dictionary
        most_least_pets_step_2(num_of_pets_array, valid_communities_dict, area, animal , ' per capita')
        
        #Either ends this section of the code or repeats whole thing
        print('\nPlease type Return to use other parts of the program otherwise hit enter to learn more about the minimum and maximum number of pets for communities in Calgary')
        if input() == 'Return':
            return

def area_info(communities_data, initial_pet_calculations):
    '''Takes in a user input for a community, checks if its valid and, if so, creates a Neighbourhood object.
    Then, the function prints it using the print_neighbourhood_info()
    
    parameters:
    communities_data: Data directly imported from a csv file. A 1D array with rows of tuples. Within each tuple:
        index 0: String. Community
        index 1: Int. Median Household Income
        index 3: Int. Population 2014
    initial_pet_calculations: A tuple containing data that was extracted, modified and formatted from the orginal csv imports. The relevant parts used are:
        index 0: 2D array. Col. 0 is all communities, Col. 1 is total cats, Col.2 is total dogs, Col.3 is total cats and dogs

    returns: none
    '''
    pets_registration, communities = initial_pet_calculations[0], communities_data  
    community_list = [community[0] for community in communities[5:]]    #Creates a list of valid communities for inputs

    print('This is the pet information menu.', end= ' ')                #Prints the name of the menu you're on    
    while True:
        print('Please type in the community you would like to learn more about. If you need to see the options you can enter, please type Details')
        requested_community = str(input())                              #Get a community input from the user
        if requested_community in community_list:                       #Checks if it exists in our list of valid inputs
            break
        elif requested_community == 'Details':                          #Prints all valid inputs
            for index,item in enumerate(community_list):
                if index + 2 <= len(community_list):                    #Causes it to go through every element except the last in this if statement
                    print('{}, '.format(item), end='')                  #Prints the area followed by a comma and a space
                else:                                                   #For the last element just prints the element with a comma or space
                    print(item)
        else:
             print('That was an invalid entry. Please try again or enter Details to see the options')
        
    for row in pets_registration:                                       #Get each set in the structured array
        for community in communities:                                   #Get each set in the strucured array                                   
            if community[0] == row[0] and community[0] == requested_community:  #Finds the rows where the community names match with the requested community
                requested_community = Neighbourhood(row[0], community[3], row[1], row[2], community[1])     #Creates a Neighbourhood object with the selected values
                requested_community.print_neighbourhood_info()          #Uses the print_neighbourhood_info() function (inside Neighbourhood class) to print the pet information
    return

#Functions called from most_least_pets_total or most_least_pets_capita
def most_least_pets_step_1(all_communities_cats, all_communities_dogs, all_communities_cats_dogs, initial_pet_calculations):
    '''This function is designed to take the users input for quadrant and type of pet and check if it is a valid input.
    If valid, it will select one of the dictionaries that are passed into the function and modify it to match the user's input.
    
    parameters:
    all_communities_cats: A dictionary with communities as the key and either total cat population or cats per capita specific to each community
    all_communities_dogs: A dictionary with communities as the key and either total dog population or dogs per capita specific to each community    
    all_communities_cats_dogs: A dictionary with communities as the key and either total cat and dog population or cats and dogs per capita specific to each community
    initial_pet_calculations: A tuple containing data that was extracted, modified and formatted from the orginal csv imports. The relevant parts used are:       
        index 5: List. Contains all the communities in the NE
        index 6: List. Contains all the communities in the NW
        index 7: List. Contains all the communities in the SW
        index 8: List. Contains all the communities in the SE

    returns:
    A tuple with multiple pieces of data. 
        index 0: Dict. Contains only the communities the user wants as keys and the corresponding value for cats, dogs or cats and dogs based on what the user specifies
        index 1: String. Contains either NE, NW, SE, SW or Calgary dependent on what the user selected
        index 2: String. Contains either Cats, Dogs or Cats and Dogs dependent on what the user selected

    '''
    #Generates the list of communities for each quadrant
    northwest_communities = initial_pet_calculations[6]
    southwest_communities = initial_pet_calculations[7]
    northeast_communities = initial_pet_calculations[5]
    southeast_communities = initial_pet_calculations[8]

    
    #Gathers input to determine animal to look into. Prints out a menu, requests input. If valid it sets all_communities_with_selected_pet_type to that pets dictionary otherwise prompts user to re-enter input
    print('\nPlease select whether you would like to learn more about cats, dogs, or total cats and dogs within Calgary')
    print('{selection_option:>13} : {reason}'.format(selection_option = 'Cats', reason = 'To learn more about the most and least cats'))
    print('{selection_option:>13} : {reason}'.format(selection_option = 'Dogs', reason = 'To learn more about the most and least dogs'))
    print('{selection_option:>13} : {reason}'.format(selection_option = 'Cats and Dogs', reason = 'To learn more about the most and least cats and dogs'))
    while True:
        animal = input()
        if animal == 'Cats':
            all_communities_with_selected_pet_type = all_communities_cats
            break
        elif animal == 'Dogs':
            all_communities_with_selected_pet_type = all_communities_dogs
            break
        elif animal == 'Cats and Dogs':
            all_communities_with_selected_pet_type = all_communities_cats_dogs
            break
        else: 
            print('That was an invalid entry. Please try again using one of the above options')
    
    #Gathers input to determine where in Calgary. Prints out a menu, requests input. If valid it sets adds only the pairs from all_communities_with_selected_pet_type to valid_communities_dict if the community in the pair is within that area of Calgary otherwise prompts user to re-enter input
    print('\nPlease select whether where in Calgary you would like to learn more about this pet')
    print('{selection_option:>7} : {reason}'.format(selection_option = 'Calgary', reason = 'To learn more about the pets in all of Calgary'))
    print('{selection_option:>7} : {reason}'.format(selection_option = 'NE', reason = 'To learn more about the pets in the North-East'))
    print('{selection_option:>7} : {reason}'.format(selection_option = 'NW', reason = 'To learn more about the pets in the North-West'))
    print('{selection_option:>7} : {reason}'.format(selection_option = 'SW', reason = 'To learn more about the pets in the South-West'))
    print('{selection_option:>7} : {reason}'.format(selection_option = 'SE', reason = 'To learn more about the pets in the South-East'))
    while True:
        area = input()
        if area == 'Calgary':
            valid_communities_dict = all_communities_with_selected_pet_type
            break
        elif area == 'NE':
            valid_communities_dict = {}
            for community,pets in all_communities_with_selected_pet_type.items():
                if community in northeast_communities:
                    valid_communities_dict[community] = pets
            break
        elif area == 'NW':
            valid_communities_dict = {}
            for community,pets in all_communities_with_selected_pet_type.items():
                if community in northwest_communities:
                    valid_communities_dict[community] = pets
            break
        elif area == 'SW':
            valid_communities_dict = {}
            for community,pets in all_communities_with_selected_pet_type.items():
                if community in southwest_communities:
                    valid_communities_dict[community] = pets
            break
        elif area == 'SE':
            valid_communities_dict = {}
            for community,pets in all_communities_with_selected_pet_type.items():
                if community in southeast_communities:
                    valid_communities_dict[community] = pets
            break
        else: 
            print('That was an invalid entry. Please try again using one of the above options')
    return valid_communities_dict, area, animal

def most_least_pets_step_2(num_of_pets_array, valid_communities_dict, area, animal, capita_vs_sum):
    '''This function is designed to take the users input for quadrant and type of pet and check if it is a valid input.
    If valid, it will select one of the dictionaries that are passed into the function and modify it to match the user's input.
    
    parameters:
    num_of_pets_array: A 1D array that contains all the pet populations in the same order as valid_communities dict. Int if called from most_least_pets_total, float if called from most_least_pets_capita
    valid_communities_dict: A dictionary that has a set of communities as keys and then their corresponding pet populations as values
    area: A string that contains either NE, NW, SE, SW or Calgary dependent on what the user selected
    animal: A string that contains either Cats, Dogs or Cats and Dogs depenent on what the user selected
    capita_vs_sum: A string used to determine whether this function is called from most_least_pets_total or most_least_pets_capita. It is blank for most_lest_pets_total but says ' per capita' for most_least_pets_capita

    returns: none
    '''

    #Finds top three max's
    print('The communities in the {} with the most {}{}:'.format(area, animal.lower(), capita_vs_sum)) #Specifies the area and the pet the program looks at and indicates if it is per capita

    number_max_found = 0
    #Creates an array that can be modified without impacting the original
    num_of_pets_array_finding_max = np.copy(num_of_pets_array)

    #Runs until 3 or more communities are found and printed    
    while number_max_found < 3:
        index = -1
        #Finds max in current set of data
        num_of_pets_max = np.amax(num_of_pets_array_finding_max)
        for community, max in valid_communities_dict.items():
            index += 1
            if max == num_of_pets_max:
                number_max_found += 1
                #Once max is found, prints it out with the community and animal. If this is for the per capita function that is specified and the max is multiplied 100 to set it to per 100 people
                if capita_vs_sum == ' per capita':
                    print('{} with {:.2f} {} per 100 people'.format(community, max * 100, animal))
                else:
                    print('{} with {} {}'.format(community, max, animal))
                #The array is modified such that the max found is replaced with -1. Therefore a new number will now be the max when this section loops
                num_of_pets_array_finding_max = np.where(num_of_pets_array_finding_max == max, -1, num_of_pets_array_finding_max)
        
    #Find bottom three min's
    print('\nThe communities in the {} with the least {}{}:'.format(area, animal.lower(), capita_vs_sum))
    
    number_min_found = 0
    #Creates an array that can be modified without impacting the original
    num_of_pets_array_finding_min = np.copy(num_of_pets_array)

    #Runs until 3 or more communities are found and printed    
    while number_min_found < 3:
        index = -1
        #Finds min in current set of data
        num_of_pets_min= np.amin(num_of_pets_array_finding_min)
        for community, min in valid_communities_dict.items():
            index += 1
            if min == num_of_pets_min:
                number_min_found += 1
                #Once min is found, prints it out with the community and animal. If this is for the per capita function that is specified and the min is multiplied 100 to set it to per 100 people
                if capita_vs_sum == ' per capita':
                    print('{} with {:.2f} {} per 100 people'.format(community, min * 100, animal))
                else:
                    print('{} with {} {}'.format(community, min, animal))
                #The array is modified such that the min found is replaced with 10000000. Therefore a new number will now be the min when this section loops
                num_of_pets_array_finding_min = np.where(num_of_pets_array_finding_min == min, 10000000, num_of_pets_array_finding_min)
    return 

#Starts running the code
if __name__ == '__main__':
    main()
    