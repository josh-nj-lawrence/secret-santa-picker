import random
from typing import List
import copy
import sys
sys.path.append("..")
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
        self._names_drawn = True
        return True

    def run(self):
        """
        Run the secret santa game.
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
            #TODO config instance emailer
            email_manager.send_email(participent.email, pair[1].name)

    def print_pairs(self):
        for pair in self.pairs:
            print(f"{pair[0].name} is giving to {pair[1].name}")

    def config_email(self):
        pass
        

if __name__ == "__main__":
    # Example usage

    # Create participents and add to list
    Josh = Participent("Josh", "josh.nj.lawrence@gmail.com", ["Julee"])
    Julee = Participent("Julee", None, ["Josh"])
    Mike = Participent("Mike", None, ["Leslee"])
    Leslee = Participent("Leslee", None, ["Mike"])
    Kyle = Participent("Kyle", None, ["Rylan"])
    Rylan = Participent("Rylan", None, ["Kyle"])
    Mitchell = Participent("Mitchell", None, ["Lorin", "Emilia"])
    Lorin = Participent("Lorin", None, ["Mitchell", "Emilia"])
    Emilia = Participent("Emilia", None, ["Lorin", "Mitchell"])
    participents = [Josh, Julee, Mike, Leslee, Kyle, Rylan, Mitchell, Lorin, Emilia]
    # Create game instance
    secretsanta = SecretSantaGame(participents)
    # Play game
    secretsanta.run()
    bluebox_participents = [p for p in secretsanta.participents if p != Emilia]
    bluebox = SecretSantaGame(bluebox_participents)
    bluebox.run()

    # Send emails to participents
    emailer = email_manager.EmailManager()
    pwd = input("Enter app password: ")
    emailer.config("josh.nj.lawrence@gmail.com", pwd)

    for participent in participents:
        print("MSG TO {name}".format(name=participent.name.upper()))
        if participent != Emilia:
            blue_box_recipient = [pair[1].name for pair in bluebox.pairs if pair[0] == participent][0]
        secret_santa_recipient = [pair[1].name for pair in secretsanta.pairs if pair[0] == participent][0]
        sub = "Minniti Secret Santa & BlueBox!!!!"
        msg = """Hello {name},\n\nWith Christmas apporaching, the following message will provide you with all relevant information for this year's gift exchange!\n\nThis year we will be continuing the Blue Box tradition, in addition to this we will run a concurrent secret santa gift exchange.\n\nThe rules of Blue Box are as follows: buy your selected recipient a gift whose total is closest in price (including tax) to this year and fits in the box.\nThis year we will be considering the closest value, even if it goes past the target value of $20.23.\n\nThe rules for our secret santa exchange are simply buy your recipient a present close to the price limit. This year the limit is $75.\n\nThe following should include your allocated recipients for this years exchanges:\n\nYou've been assigned {blue_box_recipient} for blue box and {secret_santa_recipient} for secret santa.\n\nCan't wait to celebrate with you all! See you at Christmas!""".format(name=participent.name, blue_box_recipient=blue_box_recipient, secret_santa_recipient=secret_santa_recipient)
        if participent.name == "Emilia":
            msg = """Hello {name},\n\nWith Christmas apporaching, the following message will provide you with all relevant information for this year's gift exchange!\n\nThis year we will be continuing the Blue Box tradition, in addition to this we will run a concurrent secret santa gift exchange.\n\nThe rules of Blue Box are as follows: buy your selected recipient a gift whose total is closest in price (including tax) to this year and fits in the box.\nThis year we will be considering the closest value, even if it goes past the target value of $20.23.\n\nThe rules for our secret santa exchange are simply buy your recipient a present close to the price limit. This year the limit is $75.\n\nThe following should include your allocated recipients for this years exchanges:\n\nYou've been assigned {secret_santa_recipient} for secret santa.\n\nCan't wait to celebrate with you all! See you at Christmas!""".format(name=participent.name, secret_santa_recipient=secret_santa_recipient)
        
        #emailer.send_email(participent.email, msg)
        #print("\n\n\n"+msg)
        emailer.send_email(participent.email, sub, msg)