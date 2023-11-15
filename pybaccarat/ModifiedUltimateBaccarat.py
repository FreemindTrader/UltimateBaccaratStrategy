import readchar
from colorama import Fore
from colorama import Style
from pybaccarat.baccaratsystems import BaccSys


class ModifiedUltimate(BaccSys):

    def __init__(self):
        '''!
        TBD
        '''

        self.last_actual_outcome = ""
        self.current_state = 0
        self.last_bet_on = ""
        self.last_amt_bet = 0
        self.registry_count = 0

        self.initial_money = 0
        self.base_bet = 300
        self.last_bet_unit = 0

        # money management portion of the system
        self.bank_roll_unit = 20
        self.total_bank_roll_unit = 80
        self.bet_limit_min_unit = 5
        self.bet_limit_max_unit = 7
        self.target_profit_unit = 8
        self.loss_limit_unit = self.bank_roll_unit
        self.max_loss_per_shoe = self.loss_limit_unit * self.base_bet

        self.played_hands = 0
        self.bet_units = 1

        self.busted = False

        self.cum_won = 0

        super(ModifiedUltimate, self).__init__()

    def deposit_money(self, to_deposit ):
        self.initial_money += to_deposit
        return self.initial_money



    def backup_states(self):
        self.last_amt_bet = self.amt_bet
        self.last_bet_on = self.bet_on
        self.last_bet_unit = self.bet_units


    def get_strategy_string(self):
        output = "NO BET"
        winloss = ""
        if self.last_WLT == "W":
            winloss = "W "
        elif self.last_WLT == "L":
            winloss = "X "
        elif self.last_WLT == "T":
            winloss = "T "

        if self.last_bet_unit > 0:
            if self.registry_count > 0:
                if self.last_WLT == "W":
                    output = f"{Fore.CYAN}" + "{0} {1}{2}{3}-{4} ".format(winloss, self.current_state, self.last_bet_on, self.last_bet_unit, self.registry_count ) + f"{Style.RESET_ALL}"
                elif self.last_WLT == "L":
                    output = f"{Fore.RED}" + "{0} {1}{2}{3}-{4} ".format(winloss, self.current_state, self.last_bet_on, self.last_bet_unit, self.registry_count ) + f"{Style.RESET_ALL}"
                elif self.last_WLT == "T":
                    output = f"{Fore.WHITE}" + "{0} {1}{2}{3}-{4} ".format(winloss, self.current_state, self.last_bet_on,
                                                                          self.last_bet_unit,
                                                                          self.registry_count) + f"{Style.RESET_ALL}"
            else:
                if (self.last_WLT == "W"):
                    output = f"{Fore.GREEN} C " + "{0}{1}{2}".format(self.current_state, self.last_bet_on, self.last_bet_unit )+ f"{Style.RESET_ALL}"
                elif (self.last_WLT == "T"):
                    output = f"{Fore.GREEN} T " + "{0}{1}{2}".format(self.current_state, self.last_bet_on,
                                                                     self.last_bet_unit) + f"{Style.RESET_ALL}"


        if self.busted:
            return f"{Fore.RED}!!!! FUCKED FOR THIS SHOE !!!"+ f"{Style.RESET_ALL}"

        return output

    def update_registry(self):
        if self.last_WLT == "W":
            self.win_update_registry()
        elif self.last_WLT == "L":
            self.loss_update_registry()

    def loss_update_registry(self):
        if self.registry_count == 0:
            self.registry_count = self.last_bet_unit + 1
        else:
            self.registry_count += self.last_bet_unit

    def win_update_registry(self):
        if self.registry_count > 0:
            self.registry_count -= self.last_bet_unit



    def bet_one_unit_after_loss(self, new_state ):

        if ( new_state == 1 or new_state == 3):
            self.bet_on = self.opposite_side(self.last_bet_on)
        elif (new_state == 2 or new_state == 4):
            self.bet_on = self.last_bet_on

        self.current_state = new_state

        if self.will_exceed_loss_limit():
            self.current_state = 0
            self.bet_on = ""
            self.bet_units = 0
            self.amt_bet = 0
            self.busted = True
        else:
            self.current_state = new_state
            self.bet_units = 1
            self.amt_bet = self.base_bet * self.bet_units

    def rebet_the_same(self, same_state):
        self.current_state = same_state
        self.bet_on = self.last_bet_on
        self.amt_bet = self.last_amt_bet

    def process_state1(self):
        if self.last_WLT == "W":
            self.win_start_coup(1)

        elif self.last_WLT == "T":
            self.rebet_the_same(1)

        elif self.last_WLT == "L":
            self.bet_one_unit_after_loss(2)

        self.backup_states()


    def process_state2(self):
        if self.last_WLT == "W":
            self.win_start_coup(1)

        elif self.last_WLT == "T":
            self.rebet_the_same(2)

        elif self.last_WLT == "L":
            self.bet_one_unit_after_loss(3)

        self.backup_states()

    def process_state3(self):
        if self.last_WLT == "W":
            self.win_start_coup(1)

        elif self.last_WLT == "T":
            self.rebet_the_same(3)

        elif self.last_WLT == "L":
            self.bet_one_unit_after_loss(4)

        self.backup_states()


    def process_state4(self):
        if self.last_WLT == "W":
            self.win_start_coup(3)
        elif self.last_WLT == "T":
            self.rebet_the_same(4)
        else:
            self.bet_one_unit_after_loss(1)

        self.backup_states()


    def hand_pre(self):
        '''!
        Ultimate Baccarat Strategy rules:
        1. if board 2 last entry is in row 1, play chop else play same
        2. overrides rule 1. If 4+ in a row on board 0, play same
        '''
        parent_ret = super(Ultimate, self).hand_pre()

        if self.last_actual_outcome != "":
            if self.current_state == 0:
                self.current_state = 1

                self.bet_on = self.opposite_side(self.last_actual_outcome)
                self.bet_units = 1
                self.amt_bet = self.base_bet * self.bet_units

                self.backup_states()

            elif self.current_state == 1:
                self.process_state1()
            elif self.current_state == 2:
                self.process_state2()
            elif self.current_state == 3:
                self.process_state3()
            elif self.current_state == 4:
                self.process_state4()

        #
        return ""

    def hand_post(self, win, win_diff, p_hand, b_hand):
        if ( win[0] != "T"):
            self.last_actual_outcome = win[0]

        if ( self.busted != True ):
            parent_ret = super(Ultimate, self).hand_post(win, win_diff,p_hand,b_hand)
            self.update_registry()
            return self.get_strategy_string()

        if self.busted:
            return f"{Fore.RED}!!!! FUCKED FOR THIS SHOE !!!"+ f"{Style.RESET_ALL}"

        return ""

    def end_shoe(self):
        seq2 = ""
        for i in self.WLseq:
            for j in i:
                seq2 += "0123456789abcdefghij"[j]
            seq2 += " "
        return "Won = %d, Lost = %d, Tie = %d, Money = %+.2f, Sequence = %s" % ( self.won, self.lost,self.tied,self.money,seq2)


    def will_exceed_loss_limit(self):
        potential_loss = self.money - self.base_bet

        if (abs(potential_loss) > self.max_loss_per_shoe):
            return True

        return False


    def try_coup_when_in_red(self, whats_left):
        # here we are already losing
        if (abs(whats_left) < self.max_loss_per_shoe):
            '''
                Since we are lossing, I need to be specifically careful about doubling the loss
                1) I need to code something that doesn't go again the RUN trend
                2) Even if I wanna bet again the trend, I cannot do the whole registry_count.
            '''
            self.amt_bet = self.base_bet * self.registry_count
            self.bet_units = self.registry_count
        else:
            ''' 
                Since we have exceed the max loss limit for the current shoe, 
                We will have to quit betting
            '''
            if (abs(self.money) >= self.max_loss_per_shoe):
                self.bet_on = ""
                self.bet_units = 0
                self.amt_bet = 0
                self.busted = True
                return False
            else:
                '''
                    Whatever money we can use, we will only bet close to the limit
                '''
                margin_left = self.max_loss_per_shoe - abs(self.money)
                left_unit = int(margin_left / self.base_bet)

                if (left_unit > 0):
                    self.bet_units = left_unit
                    self.amt_bet = left_unit * self.base_bet
                    return True
                else:
                    self.bet_on = ""
                    self.bet_units = 0
                    self.amt_bet = 0
                    self.busted = True
                    return False

    '''
        Majority of the betting logic is in the 
    '''
    def win_start_coup(self, new_state ):

        if ( self.current_state == 1 or self.current_state == 3):
            self.bet_on = self.opposite_side(self.last_bet_on)
        elif (self.current_state == 2 or self.current_state == 4):
            self.bet_on = self.last_bet_on

        self.current_state = new_state

        if self.registry_count > 0:

            '''
                If we fail this coup, will our loss be greter than the max_loss_per_shoe
                we might have already have some loss in the previous hands, if we loss this coup, will we be down more than allowed. 
                    We have to calculated that here.
            '''

            whats_left = self.money - self.registry_count * self.base_bet

            # we are still winning
            if ( whats_left > 0 ):
                self.amt_bet = self.base_bet * self.registry_count
                self.bet_units = self.registry_count
            else:
                self.try_coup_when_in_red( whats_left)
        else:
            self.bet_units = 1
            self.amt_bet = self.base_bet * self.bet_units


        return True