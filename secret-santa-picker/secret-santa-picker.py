import random
from typing import List
import copy
import email_manager

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
    def __init__(self, participents: List[Participent], _send_emails: bool = False):
        self.participents = participents
        self.pairs = [] # Pairs are tuples of (giver, receiver)
        self._send_emails = _send_emails # Specify weather or not run method should send emails to recipients
        self._names_drawn = False # Flag to indicate if names have been drawn

    def draw_names(self) -> bool:
        """
        Take participents and pick pairs.
        """
        retry_counter = 0
        # Make a copy of the participents list to draw from
        participents = copy.deepcopy(self.participents)
        participent_list = copy.deepcopy(self.participents)
        random.shuffle(participent_list)
        for participent in participent_list:
            receiver = random.choice(participents)
            # If the receiver is the same as the giver or the giver is in the receivers DontPick list, pick again
            while receiver == participent or receiver.name in participent.DontPick:
                # If there are no valid participents remaining to pick from, restart the game
                if len(participents) == 1 \
                    or all(p.name in participent.DontPick for p in participents) \
                    or all(p.name in ([participent.name] + participent.DontPick) for p in participents):
                    print("No valid solution found. Restarting...")
                    self.pairs = []
                    return False
                retry_counter += 1
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
        self.participents = participent_list
        return True

    def run(self):
        """
        Run a dry run and print results to the console instead of sending emails.
        """
        solution_found = False
        retry_counter = 0
        while not solution_found:
            solution_found = self.draw_names()
            retry_counter += 1
            if retry_counter > 100:
                SystemError("Unable to find a valid solution. Exiting...")
           
        print("Valid solution found!\n\n")
        

    def send_emails(self):
        """
        Send emails to participents with their assigned pair.
        """
        if not self._names_drawn:
            self.draw_names()
        for participent in self.participents:
            # Find the pair for the participent
            pair = [pair for pair in self.pairs if pair[0] == participent][0]
            # Send email to participent
            email_manager.send_email(participent.email, pair[1].name)

    def print_pairs(self):
        for pair in self.pairs:
            print(f"{pair[0].name} is giving to {pair[1].name}")

    def config_email(self):
        pass
        

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
    secretsanta.run()

    print("\n\nBLUE BOX DRAW")
    bluebox = SecretSantaGame(secretsanta.participents[0:8])
    bluebox.run()

    # Send emails to participents