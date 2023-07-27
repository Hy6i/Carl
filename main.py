# This file is for strategy
from util.objects import *
from util.routines import *
from util.tools import find_hits


class Bot(GoslingAgent):
    debug_text = ''  # A variable to store debug information

    def run(self):
        self.print_debug()  # Print debug information if needed

        # Check if an intent is set for the bot, execute it, and return
        if self.get_intent() is not None:
            self.debug_intent()
            return

        # Calculate distances to opponent's goal and friend's goal
        d1 = abs(self.ball.location.y - self.foe_goal.location.y)
        d2 = abs(self.me.location.y - self.foe_goal.location.y)

        # Check if bot is in front of the ball
        is_in_front_of_ball = d1 > d2

        if self.kickoff_flag:
            # If it's a kickoff, set the intent to kickoff and return
            self.set_intent(kickoff())
            return

        if is_in_front_of_ball:
            # If bot is in front of the ball, retreat to friend's goal
            self.set_intent(goto(self.friend_goal.location))
            self.debug_text = 'Retreating'
            return

        # Default intent: Set the intent to shoot at opponent's goal
        self.set_intent(short_shot(self.foe_goal.location))

        # Define target locations for finding hits
        targets = {
            'at_opponent_goal': (self.foe_goal.left_post, self.foe_goal.right_post),
            'away_from_our_net': (self.friend_goal.right_post, self.friend_goal.left_post)
        }

        # Find potential hits at opponent's goal and away from our net
        hits = find_hits(self, targets)
        if len(hits['at_opponent_goal']) > 0:
            # Set the intent to hit at opponent's goal
            self.set_intent(hits['at_opponent_goal'][0])
            return
        if len(hits['away_from_our_net']) > 0:
            # Set the intent to hit away from our net
            self.set_intent(hits['away_from_our_net'][0])
            return

        # If the bot has enough boost, set the intent to shoot at opponent's goal
        if self.me.boost > 97:
            self.set_intent(short_shot(self.foe_goal.location))
            self.debug_text = 'Shooting'
            return

        # If no better options available, go to the closest large boost pad
        closest_boost = self.get_closest_large_boost()
        if closest_boost is not None:
            self.set_intent(goto(closest_boost.location))
            self.debug_text = 'Getting Boost'
            return
