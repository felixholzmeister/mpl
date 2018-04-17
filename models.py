from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from mpl.config import *
import random
from random import randrange


author = 'Felix Holzmeister'

doc = """
Multiple price list task as proposed by Holt/Laury (2002), American Economic Review 92(5).
"""


# ******************************************************************************************************************** #
# *** CLASS SUBSESSION
# ******************************************************************************************************************** #
class Subsession(BaseSubsession):

    def creating_session(self):
        if self.round_number == 1:

            n = Constants.num_choices
            for p in self.get_players():

                # create list of lottery indices
                # ----------------------------------------------------------------------------------------------------
                indices = [j for j in range(1, n)]
                indices.append(n) if Constants.certain_choice else None

                # create list of probabilities
                # ----------------------------------------------------------------------------------------------------
                if Constants.percentage:
                    probabilities = [
                        "{0:.2f}".format(k / n * 100) + "%"
                        for k in indices
                    ]
                else:
                    probabilities = [
                        str(k) + "/" + str(n)
                        for k in indices
                    ]

                # create list corresponding to form_field variables including all choices
                # ----------------------------------------------------------------------------------------------------
                form_fields = ['choice_' + str(k) for k in indices]

                # create list of choices
                # ----------------------------------------------------------------------------------------------------
                p.participant.vars['mpl_choices'] = list(
                    zip(indices, form_fields, probabilities)
                )

                # randomly determine index/choice of binary decision to pay
                # ----------------------------------------------------------------------------------------------------
                p.participant.vars['mpl_index_to_pay'] = random.choice(indices)
                p.participant.vars['mpl_choice_to_pay'] = 'choice_' + str(p.participant.vars['mpl_index_to_pay'])

                # randomize order of lotteries if <random_order = True>
                # ----------------------------------------------------------------------------------------------------
                if Constants.random_order:
                    random.shuffle(p.participant.vars['mpl_choices'])

                # initiate list for choices made
                # ----------------------------------------------------------------------------------------------------
                p.participant.vars['mpl_choices_made'] = [None for j in range(1, n + 1)]

            # generate random switching point for PlayerBot in tests.py
            # --------------------------------------------------------------------------------------------------------
            for participant in self.session.get_participants():
                participant.vars['mpl_switching_point'] = random.randint(1, n)


# ******************************************************************************************************************** #
# *** CLASS GROUP
# ******************************************************************************************************************** #
class Group(BaseGroup):
    pass


# ******************************************************************************************************************** #
# *** CLASS PLAYER
# ******************************************************************************************************************** #
class Player(BasePlayer):

    # add model fields to class player
    # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    if Constants.certain_choice:
        for j in range(1, Constants.num_choices + 1):
            locals()['choice_' + str(j)] = models.StringField()
        del j
    else:
        for j in range(1, Constants.num_choices):
            locals()['choice_' + str(j)] = models.StringField()
        del j

    random_draw = models.IntegerField()
    choice_to_pay = models.StringField()
    option_to_pay = models.StringField()
    inconsistent = models.IntegerField()
    switching_row = models.IntegerField()

    # set player's payoff
    # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def set_payoffs(self):

        # random draw to determine whether to pay the "high" or "low" outcome of the randomly picked lottery
        # ------------------------------------------------------------------------------------------------------------
        self.random_draw = randrange(1, len(self.participant.vars['mpl_choices']))

        # set <choice_to_pay> to participant.var['choice_to_pay'] determined creating_session
        # ------------------------------------------------------------------------------------------------------------
        self.choice_to_pay = self.participant.vars['mpl_choice_to_pay']

        # elicit whether lottery "A" or "B" was chosen for the respective choice
        # ------------------------------------------------------------------------------------------------------------
        self.option_to_pay = getattr(self, self.choice_to_pay)

        # set player's payoff
        # ------------------------------------------------------------------------------------------------------------
        if self.option_to_pay == 'A':
            if self.random_draw <= self.participant.vars['mpl_index_to_pay']:
                self.payoff = Constants.lottery_a_hi
            else:
                self.payoff = Constants.lottery_a_lo
        else:
            if self.random_draw <= self.participant.vars['mpl_index_to_pay']:
                self.payoff = Constants.lottery_b_hi
            else:
                self.payoff = Constants.lottery_b_lo

        # set payoff as global variable
        # ------------------------------------------------------------------------------------------------------------
        self.participant.vars['mpl_payoff'] = self.payoff

    # determine consistency
    # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def set_consistency(self):

        n = Constants.num_choices

        # replace A's by 1's and B's by 0's
        self.participant.vars['mpl_choices_made'] = [
            1 if j == 'A' else 0 for j in self.participant.vars['mpl_choices_made']
        ]

        # check for multiple switching behavior
        for j in range(1, n):
            choices = self.participant.vars['mpl_choices_made']
            self.inconsistent = 1 if choices[j] > choices[j - 1] else 0
            if self.inconsistent == 1:
                break

    # determine switching row
    # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def set_switching_row(self):

        # set switching point to row number of first 'B' choice
        if self.inconsistent == 0:
            self.switching_row = sum(self.participant.vars['mpl_choices_made']) + 1
