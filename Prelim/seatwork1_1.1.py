class RiverCrossing:
    def __init__(self, people, load, people_names):
        """
        Initialize the river crossing simulation.
        people: List of people's weights.
        load: The weight of the load.
        people_names: List of people's names corresponding to the weights.
        """
        self.people = people
        self.load = load
        self.load_name = "Supplies"

        # Map weights to names for clarity
        """Creates a dict to map weight of each person to their name
        by combining two the two lists
        """
        self.people_names = {weight: name for weight, name in zip(people, people_names)}

        self.side_a = people + [load]  # All people and load on side A
        self.side_b = []  # Side B starts empty
        self.boat = []  # Boat starts empty

    def get_lightest_pair(self, side):
        """
        Get the lightest pair of people whose total weight is <= 100kg.
        Returns a list of weights of the two lightest people.
        """
        for i in range(len(side)):
            for j in range(i + 1, len(side)):
                if side[i] + side[j] <= 100:
                    return [side[i], side[j]]
        return None  # Return None if no valid pair is found

    def get_heaviest_individual(self, side):
        """
        Get the heaviest individual from the given side.
        """
        return max(side)

    def move_people(self, people_to_move, from_side, to_side):
        """
        Move people from one side to the other.
        """
        for person in people_to_move:
            from_side.remove(person)
            to_side.append(person)

    def move_load(self, from_side, to_side):
        """
        Move the load if necessary.
        """
        if self.load in from_side:
            from_side.remove(self.load)
            to_side.append(self.load)

    def simulate_crossing(self):
        """
        Simulate the river crossing process and return the steps.
        """
        steps = []  # This will store the steps taken during the simulation

        # Continue until only the load is left on side A
        while len(self.side_a) > 1:
            # Record the state before the crossing
            """self.people_names looks up to the dict created earlier and finds the name of the person corresponding to the weight,
            then returns the name of the person. This line also checks if the weight corresponds to the load.
            """
            steps.append(f"Side A: {', '.join([self.people_names.get(p, self.load_name if p == self.load else str(p)) for p in self.side_a])}, Side B: {', '.join([self.people_names.get(p, self.load_name if p == self.load else str(p)) for p in self.side_b])}")

            # Sort people by weight for easier decision-making (lightest first)
            self.side_a.sort()

            # Step 1: Get the lightest pair of people that can cross without exceeding 100kg
            pair = self.get_lightest_pair(self.side_a)

            if pair:
                # If a valid pair is found, move them to the boat and cross
                self.move_people(pair, self.side_a, self.boat)
                # Record the action with names instead of weights
                steps.append(f"Crossing: {', '.join([self.people_names.get(p, self.load_name if p == self.load else str(p)) for p in pair])} cross to side B")
                self.move_people(pair, self.boat, self.side_b)

                # Step 2: After crossing, if side A is not empty, the lightest person on side B returns
                if self.side_a:
                    # Filter side B to consider only people (ignore load)
                    people_on_side_b = [p for p in self.side_b if p != self.load]
                    if people_on_side_b:
                        return_person = min(people_on_side_b)
                        # Record the return action
                        steps.append(f"{self.people_names.get(return_person, self.load_name if return_person == self.load else str(return_person))} returns to side A")
                        self.move_people([return_person], self.side_b, self.side_a)
            else:
                # If no valid pair found, send the heaviest individual
                heaviest = self.get_heaviest_individual(self.side_a)
                self.move_people([heaviest], self.side_a, self.boat)
                # Record the action with names instead of weights
                steps.append(f"Crossing: {self.people_names.get(heaviest, self.load_name if heaviest == self.load else str(heaviest))} cross to side B")
                self.move_people([heaviest], self.boat, self.side_b)

                # Step 2: After crossing, if side A is not empty, the lightest person on side B returns
                if self.side_a:
                    # Filter side B to consider only people (ignore load)
                    people_on_side_b = [p for p in self.side_b if p != self.load]
                    if people_on_side_b:
                        return_person = min(people_on_side_b)
                        # Record the return action
                        steps.append(f"{self.people_names.get(return_person, self.load_name if return_person == self.load else str(return_person))} returns to side A")
                        self.move_people([return_person], self.side_b, self.side_a)

            # Record the sides after the crossing
            steps.append(f"Side A: {', '.join([self.people_names.get(p, self.load_name if p == self.load else str(p)) for p in self.side_a])}, Side B: {', '.join([self.people_names.get(p, self.load_name if p == self.load else str(p)) for p in self.side_b])}")

        return steps


# Define the people, load, and their names
people = [90, 80, 60, 40]  # Weights of Roman, Verlyn, Lloyd, Robin
people_names = ["Roman", "Verlyn", "Lloyd", "Robin"]  # Corresponding names
load = 20  # Load (20kg)

# Initialize the river crossing simulation with names
river = RiverCrossing(people, load, people_names)

# Start the simulation and print the steps
steps = river.simulate_crossing()

# Print all the steps with detailed names
for step in steps:
    print(step)
