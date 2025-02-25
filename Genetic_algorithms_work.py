import time 
import random
import statistics



#RESTRICT ALL INPUT CALLS TO INTEGERS

def get_int_input(prompt):
    """Prompt the user until they enter a valid integer"""
    while True:
        try:
            #Take input and attempt to convert it to an integer
            user_input = int(input(prompt))
            return user_input # Return the integer
        except ValueError:
            print("Invalid input! Please enter a valid integer.") 


# CONSTANTS (weights in grams):

# - PROJECT GOAL

#Target weight for the rats population. 
#The simulation aims to evolve rats until their average weight reaches this goal.
GOAL = get_int_input("Set your goal by entering your desired weight\n-->  ")


# - INITIAL POPULATION SETUP

#The initial number of rats in this population
NUM_RATS = get_int_input("What is your initial number of rats?\n--> ")

#The minimum starting weight of a rat in grams
INITIAL_MIN_WT = get_int_input("Enter the weight of the lightest rat of your initial sample\n--> ")

INITIAL_MAX_WT = get_int_input("Enter the weight of the heaviest rat of your initial sample\n--> ")

#The most common starting weight of a rat in grams.
INITIAL_MODE_WT = get_int_input("Enter the current weight mode in your sample\n--> ")

#Define a special funtion that restricts input to floats
#Input must consist of floats with a predefined number of decimal values
def get_float_input_dec(prompt, default_value, decimals):
    """Prompt the user to enter a float, defaulting to 0.01 if no input is provided
    Restrict input to 2 decimal places."""
    
    while True: 
        user_input = input(f"{prompt} (default: {default_value})")

        if user_input == "":
            print(f"Using default value: {default_value}")
            return round(default_value, decimals)
        
        try:
            user_input = float(user_input)
            user_input = round(user_input, decimals)
            return user_input
        except ValueError:
            print("Please enter a valid input")


# - MUTATION PARAMETERS

#Collecting input using the previously created funtions
#The probability of a mutation occurring per rat.
MUTATE_ODDS = get_float_input_dec("Enter mutation odds (To use the default value of 0.01, enter an empty\n string by simply pressing 'ENTER')\n--> ", 0.01, 2)

#The minimum factor by which a mutation can vary the weight.
MUTATE_MIN = get_float_input_dec("Enter the minimum mutation factor ratio\n--> ", 0.5, 1)
#The maximum factor by which a mutation can vary the weight
MUTATE_MAX = get_float_input_dec("Enter the maximum mutation factor ratio\n--> ", 1.2, 1)
#The number of offsrping produced by breeding cycle
LITTER_SIZE = get_int_input("What is the litter size? (maximum offspring per birthgiving)\n--> ")
#The number of breeding cycles per year
LITTERS_PER_YEAR = get_int_input("What is the maximum number of litters per year?\n--> ")
#The maximum number of generations the simulation will run before stopping.
GENERATION_LIMIT = get_int_input("How many generations (cycles) would you like this simulation to run?\n--> ")


if NUM_RATS % 2 != 0: #The modulo operator (%) returs the remainder of the division of NUM_RATS by 2.
    NUM_RATS += 1 #If the remainder is different than zero, then NUM_RATS is uneven, hence the program
                  #will then sum + 1 to NUM_RATS, forcing always an even input.





#Statistics part 





def populate(NUM_RATS, INITIAL_MIN_WT, INITIAL_MAX_WT,INITIAL_MODE_WT ):
    """Initialize a population with a triangular distribution of weights"""
    return[int(random.triangular(INITIAL_MIN_WT, INITIAL_MAX_WT, INITIAL_MODE_WT))\
           for i in range(NUM_RATS)]


def fitness(population, goal):
    """Measure population fitness by comparing it's average individual's weight to the desired weight"""
    ave = statistics.mean(population)
    return ave / goal

def select(population, to_retain):
    """Cull a population to retain only a specified number of individuals"""
    sorted_population = sorted(population)
    to_retain_by_sex = to_retain //2
    
    #Assumption 1 - The population is evenly divided between males and females.
    members_per_sex = len(sorted_population) // 2

    #Assumption 2 - No female rat is heavier than a male rat 
    #Take all elements from the start of sorted_population up to (but not including) members_per_sex.
    females = sorted_population[:members_per_sex]
    #Take all elements from members_per_sex onward until the end of serted_population.

    males = sorted_population[members_per_sex:]

    #Create two tuples with the culled males and females from the sorted population
    selected_females = females[-to_retain_by_sex:]
    selected_males = males[-to_retain_by_sex:]
    return selected_males, selected_females

def breed(males, females, litter_size):
    """Crossover genes among members (weights) of a population."""
    random.shuffle(males)
    random.shuffle(females)
    children = []
    for male, female in zip(males, females):
        for child in range(litter_size):
            child = random.randint(female, male)
            children.append(child)
    return children 

def mutate(children, mutate_odds, mutate_min, mutate_max):
    """Randomly alter rat weights using input odds & fractional changes."""
    for index, rat in enumerate(children):
        if mutate_odds >= random.random():
            children[index] = round(rat * random.uniform(mutate_min,
                                                         mutate_max))
    return children

def main():
    """Initialize population, select, breed, and mutate, display results"""
    generations = 0
    parents = populate(NUM_RATS, INITIAL_MIN_WT, INITIAL_MAX_WT,
                       INITIAL_MODE_WT)                 
    print(f"initial population weights = {parents}")
    popl_fitness = fitness(parents, GOAL)
    print(f"initial popualtion fitness = {popl_fitness}")
    print(f"number to retain = {NUM_RATS}")

    ave_wt = []

    #While the GOAL weight hasn't yet been met and we haven't yet run all the generations predefined
    while popl_fitness < 1 and generations < GENERATION_LIMIT:   
        generations += 1          
        selected_males, selected_females = select(parents, NUM_RATS)
        children = breed(selected_males, selected_females, LITTER_SIZE)
        children = mutate(children, MUTATE_ODDS, MUTATE_MIN, MUTATE_MAX)
        parents = selected_males + selected_females + children
        popl_fitness = fitness(parents, GOAL)
        print("Generation {} fitness = {:.4f}".format(generations,
                                                      popl_fitness))

    ave_wt.append(int(statistics.mean(parents)))
    generations += 1
    print(f"average weight per generation = {ave_wt}")
    print(f"\nnumber of generations = {generations-1}")
    print(f"number of years = {int(generations/LITTERS_PER_YEAR)}")

if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    duration = end_time - start_time
    print(f"\nRuntime for this program was {duration} seconds")

    


    




    