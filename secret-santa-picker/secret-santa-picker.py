import random
from typing import List
import copy
# import email_manager

class Participent:
    """
    Participent class:
    Define a participent in the secret santa game.
    """
    def __init__(self, name, email, DontPick: List[str]):
        self.name = name
        self.email = email
        self.DontPick = DontPick

    def __eq__(self, other):
        return self.name == other.name and self.email == other.email
    
    def __repr__(self) -> str:
        return f"Participent({self.name}, {self.email}, {[part for part in self.DontPick]})"

class SecretSantaGame:
    """
    Game instance takes participents and picks pairs.
    """
    def __init__(self, participents: List[Participent]):
        self.participents = participents
        self.pairs = [] # Pairs are tuples of (giver, receiver)

    def play_game(self, participent_list) -> bool:
        """
        Take participents and pick pairs.
        """
        retry_counter = 0
        # Make a copy of the participents list to draw from
        participents = copy.deepcopy(participent_list)
        for participent in participent_list:
            # Pick a random participent from the list
            receiver = random.choice(participents)
            # If the receiver is the same as the giver or the giver is in the receivers DontPick list, pick again
            while receiver == participent or receiver.name in participent.DontPick:
                # If there are no more valid participents to pick from, restart until a valid solution is reached
                # hat only has last person to draw, 
                # hat only has 1 person and it's on partipent's DontPick list,
                # hat has multiple left all in participents dont pick list,
                # hat has multiple left and it's the partipent and a person on their DontPick list
                if len(participents) == 1 \
                    or all(p.name in participent.DontPick for p in participents) \
                    or all(p.name in ([participent.name] + participent.DontPick) for p in participents):
                    # Inform user
                    print("No valid solution found. Restarting...")
                    # Clear the list of pairs
                    self.pairs = []
                    # Restart the game
                    return False
                retry_counter += 1
                # Redraw case
                receiver = random.choice(participents)
                if retry_counter > 100:
                    print("Too many retries. Restarting...")
                    self.pairs = []
                    return False
            # Add participents receiver to the DontPick list for subsequent games if applicable
            participent.DontPick.append(receiver.name)
            # Add participent to receivers DontPick list to try to avoid pairings
            receiver.DontPick.append(participent.name)
            # Add the pair to the list of pairs
            self.pairs.append((participent, receiver))
            # Remove the receiver from the list of participents
            participents.remove(receiver)
        return True

    def run(self, participent_list):
        """
        Run a dry run and print results to the console instead of sending emails.
        """
        solution_found = False
        retry_counter = 0
        while not solution_found:
            participent_copy = copy.deepcopy(participent_list)
            print("Looking for solution...")
            solution_found = self.play_game(participent_copy)
            retry_counter += 1
            if retry_counter > 100:
                print("Too many retries. Restarting...")
                SystemError("Unable to find a valid solution. Exiting...")
           
        print("Valid solution found!\n\n")
        self.participents = participent_copy
        for pair in self.pairs:
            print(f"{pair[0].name} is giving to {pair[1].name}")
        

if __name__ == "__main__":
    # Example usage

    # Create participents and add to list
    josh = Participent("josh", "josh.nj.lawrence@gmail.com", ["julee"])
    julee = Participent("julee", "josh.nj.lawrence@gmail.com", ["josh"])
    mike = Participent("mike", "josh.nj.lawrence@gmail.com", ["leslee"])
    leslee = Participent("leslee", "josh.nj.lawrence@gmail.com", ["mike"])
    kyle = Participent("kyle", "josh.nj.lawrence@gmail.com", ["rylan"])
    rylan = Participent("rylan", "josh.nj.lawrence@gmail.com", ["kyle"])
    mitchell = Participent("mitchell", "josh.nj.lawrence@gmail.com", ["lorin", "emilia"])
    lorin = Participent("lorin", "josh.nj.lawrence@gmail.com", ["mitchell", "emilia"])
    emilia = Participent("emilia", "josh.nj.lawrence@gmail.com", ["lorin", "mitchell"])
    participents = [josh, julee, mike, leslee, kyle, rylan, mitchell, lorin, emilia]

    # Create game instance
    secretsanta = SecretSantaGame(participents)
    # Play game
    print("\n\nSECRET SANTA DRAW")
    secretsanta.run(secretsanta.participents)

    print("\n\nBLUE BOX DRAW")
    bluebox = SecretSantaGame(secretsanta.participents[0:8])
    bluebox.run(bluebox.participents)

    # Send emails to participents