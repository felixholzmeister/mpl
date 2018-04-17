# <imports>
from otree.api import Currency as c
from otree.constants import BaseConstants
# </imports>


# ******************************************************************************************************************** #
# *** CLASS CONSTANTS *** #
# ******************************************************************************************************************** #
class Constants(BaseConstants):

    # ---------------------------------------------------------------------------------------------------------------- #
    # --- Task-specific Settings --- #
    # ---------------------------------------------------------------------------------------------------------------- #

    # lottery payoffs
    # "high" and "low" outcomes (in currency units set in settings.py) of "lottery A" and "lottery B"
    # note that payoffs are identical for all choices and only probabilities of "high" and "low" outcomes change
    lottery_a_hi = 2.00
    lottery_a_lo = 1.60
    lottery_b_hi = 3.85
    lottery_b_lo = 0.10

    # number of binary choices between "lottery A" and "lottery B"
    # note that the number of choices determines the probabilities of high and low outcomes of lotteries "A" and "B"
    # for <num_choices = X>, the probability of outcome "high" is 1/X for the first choice, 2/X for the second, etc.
    num_choices = 10

    # include 'certain' choice (** only applies if <variation_type = 'probability'> **)
    # if <certain_choice = True>, the binary choice with probability of the outcome "high" being equal to 1 is included
    # if <certain_choice = False>, the list only contains (<num_choices> - 1) binary decision pairs
    # note, however, that the probability of outcome "high" is set by <num_choices>, not (<num_choices> - 1), though
    # i.e., if <certain_choice = False>, the last choice implies a probability of (X - 1)/X (given <num_choices = X>)
    certain_choice = True

    # ---------------------------------------------------------------------------------------------------------------- #
    # --- Overall Settings and Appearance --- #
    # ---------------------------------------------------------------------------------------------------------------- #

    # show each lottery pair on a separate page
    # if <one_choice_per_page = True>, each single binary choice between lottery "A" and "B" is shown on a separate page
    # if <one_choice_per_page = False>, all <num_choices> choices are displayed in a table on one page
    one_choice_per_page = False

    # order choices between lottery pairs randomly
    # if <random_order = True>, the ordering of binary decisions is randomized for display
    # if <random_order = False>, binary choices are listed in ascending order of the probability of the "high" outcome
    random_order = False

    # enforce consistency, i.e. only allow for a single switching point
    # if <enforce_consistency = True>, all options "A" above a selected option "A" are automatically selected
    # similarly, all options "B" below a selected option "B" are automatically checked, implying consistent choices
    # note that <enforce_consistency> is only implemented if <one_choice_per_page = False> and <random_order = False>
    enforce_consistency = False

    # depict probabilities as percentage numbers
    # if <percentage = True>, the probability of outcome "high" will be displayed as percentage number
    # if <percentage = False>, the probabilities will be displayed as fractions, i.e. "1/X", "2/X", etc.
    percentage = False

    # show small pie charts for each lottery
    # if <small_pies = True>, a pie chart depicting the probabilities of outcomes is rendered next to each lottery
    # if <small_pies = False>, no graphical representation of probabilities is displayed
    small_pies = True

    # display lotteries in terms of large pie charts
    # if <large_pies = True>, lotteries are depicted as pie charts; if <large_pies = False> lotteries are list items
    # note that <large_pies = True> only affects the task's appearance if <one_choice_per_page = True>
    large_pies = True

    # show progress bar
    # if <progress_bar = True> and <one_choice_per_page = True>, a progress bar is rendered
    # if <progress_bar = False>, no information with respect to the advance within the task is displayed
    # the progress bar graphically depicts the advance within the task in terms of how many decision have been made
    # further, information in terms of "page x out of <num_choices>" (with x denoting the current choice) is provided
    progress_bar = True

    # show instructions page
    # if <instructions = True>, a separate template "Instructions.html" is rendered prior to the task
    # if <instructions = False>, the task starts immediately (e.g. in case of printed instructions)
    instructions = True

    # show results page summarizing the task's outcome including payoff information
    # if <results = True>, a separate page containing all relevant information is displayed after finishing the task
    # if <results = False>, the template "Decision.html" will not be rendered
    results = True

    # ---------------------------------------------------------------------------------------------------------------- #
    # --- oTree Settings (Don't Modify) --- #
    # ---------------------------------------------------------------------------------------------------------------- #

    name_in_url = 'mpl'
    players_per_group = None

    if one_choice_per_page:
        if certain_choice:
            num_rounds = num_choices
        else:
            num_rounds = num_choices - 1
    else:
        num_rounds = 1
