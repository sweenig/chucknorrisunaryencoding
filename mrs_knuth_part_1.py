import sys
from pprint import pformat
from typing import Dict, List, Tuple, Union

r_tuple = Union[Tuple[str,str],Tuple[str,str,str]]
a_key = Tuple[str,str,str,str,str]

debug = False

def log_msg(msg,debug=False):
    if debug:
        print(msg,file=sys.stderr)

class DLXCell:
    def __init__(self, title=None):
        self.prev_x = self
        self.next_x = self
        self.prev_y = self
        self.next_y = self

        self.col_header = None
        self.row_header = None

        # Only used for column and row headers.
        self.title = title

        # Size quickly identifies how many rows are in any particular column.
        self.size = 0

    def remove_x(self):
        self.prev_x.next_x = self.next_x
        self.next_x.prev_x = self.prev_x

    def remove_y(self):
        self.prev_y.next_y = self.next_y
        self.next_y.prev_y = self.prev_y

    def restore_x(self):
        self.prev_x.next_x = self
        self.next_x.prev_x = self

    def restore_y(self):
        self.prev_y.next_y = self
        self.next_y.prev_y = self

    def attach_horiz(self, other):
        n = self.prev_x
        other.prev_x = n
        n.next_x = other
        self.prev_x = other
        other.next_x = self

    def attach_vert(self, other):
        n = self.prev_y
        other.prev_y = n
        n.next_y = other
        self.prev_y = other
        other.next_y = self

    def remove_column(self):
        self.remove_x()
        node = self.next_y
        while node != self:
            node.remove_row()
            node = node.next_y

    def restore_column(self):
        node = self.prev_y
        while node != self:
            node.restore_row()
            node = node.prev_y
        self.restore_x()

    def remove_row(self):
        node = self.next_x
        while node != self:
            node.col_header.size -= 1
            node.remove_y()
            node = node.next_x

    def restore_row(self):
        node = self.prev_x
        while node != self:
            node.col_header.size += 1
            node.restore_y()
            node = node.prev_x

    def select(self):
        node = self
        while 1:
            node.remove_y()
            node.col_header.remove_column()
            node = node.next_x
            if node == self:
                break

    def unselect(self):
        node = self.prev_x
        while node != self:
            node.col_header.restore_column()
            node.restore_y()
            node = node.prev_x
        node.col_header.restore_column()
        node.restore_y()

class AlgorithmXSolver():
    # R - a list of requirements. The __init__() method converts R to a dictionary, but R must
    #     originally be passed in as a simple list of requirements. Each requirement is a tuple
    #     of values that uniquely identify that requirement from all other requirements.
    #
    # A - must be passed in as a dictionary - keys are actions, values are lists of covered requirements
    #
    # O - list of optional requirements. They can be covered, but they never cause failure.
    #     Optional requirements are important because if they get covered, no other action can 
    #     also cover that same requirement. Also referred to as "at-most-one-time constraints".
    #
    def __init__(self, R: list, A: dict, O: list = []):
        self.A = A
        self.R = R + list(O)
        self.O = set(O)

        # The list of actions (rows) that produce the current path through the matrix.
        self.solution = []
        self.solution_count = 0
        
        # A history can be added to a subclass to allow Algorithm X to handle "multiplicity".
        # In the basic Solver, nothing is ever put into the history. A subclass can override
        # the _process_row_selection() method to add history in cases of multiplicity. 
        self.history = [set()]

        # For the basic Algorithm X Solver, all solutions are always valid. However, a subclass
        # can add functionality to check solutions as they are being built to steer away from
        # invalid solutions. The basic Algorithm X Solver never modifies this attribute.
        self.solution_is_valid = True

        # Create a column in the matrix for every requirement.
        self.matrix_root = DLXCell()
        self.matrix_root.size = 10000000
        self.matrix_root.title = 'root'
        
        self.col_headers = [DLXCell(requirement) for requirement in self.R]

        # Row headers are never attached to the rest of the DLX matrix. They are only used 
        # currently to keep track of the action associated with each row.
        self.row_headers = {action:DLXCell(action) for action in self.A}

        self.R = {requirement:self.col_headers[i] for i, requirement in enumerate(self.R)}

        for i in range(len(self.col_headers)):
            self.matrix_root.attach_horiz(self.col_headers[i])

        # Create a row in the matrix for every action.
        for action in self.A:
            previous_cell = None
            for requirement in A[action]:
                next_cell = DLXCell()
                next_cell.col_header = self.R[requirement]
                next_cell.row_header = self.row_headers[action]
                next_cell.col_header.attach_vert(next_cell)
                next_cell.col_header.size += 1
                
                if previous_cell:
                    previous_cell.attach_horiz(next_cell)
                else:
                    previous_cell = next_cell


    def solve(self):
        
        # Algorithm X Step 1:
        #
        # Choose the column (requirement) with the best value for "sort criteria". For
        # the basic implementation of sort criteria, Algorithm X always chooses the column
        # covered by the fewest number of actions. Optional requirements are not eligible 
        # for this step.
        best_column = self.matrix_root
        best_value  = 'root'
        
        node = self.matrix_root.next_x
        while node != self.matrix_root:
            
            # Optional requirements (at-most-one-time constraints) are never chosen as best.
            if node.title not in self.O:
                
                # Get the sort criteria for this requirement (column).
                value = self._requirement_sort_criteria(node)
                if best_column == self.matrix_root or value < best_value:
                    best_column = node
                    best_value  = value
                node = node.next_x

            else:

                # Optional requirements stop the search for the best column.
                node = self.matrix_root
            
        if best_column == self.matrix_root:
            self._process_solution()
            if self.solution_is_valid:
                self.solution_count += 1
                yield self.solution
        else:

            # Build a list of all actions (rows) that cover the chosen requirement (column).
            actions = []
            node = best_column.next_y
            while node != best_column:
                actions.append(node)
                node = node.next_y

            # The next step is to loop through all possible actions. To prepare for this,
            # a new level of history is created. The history for this new level starts out
            # as a complete copy of the most recent history.
            self.history.append(self.history[-1].copy())    
                
            # Loop through the possible actions sorted by the given sort criteria. A basic
            # Algorithm X implementation does not provide sort criteria. Actions are tried
            # in the order they happen to occur in the matrix.
            for node in sorted(actions, key=lambda n:self._action_sort_criteria(n.row_header)):
                self.select(node=node)
                if self.solution_is_valid:
                    for s in self.solve():
                        yield s
                self.deselect(node=node)

                # All backtracking results in going back to a solution that is valid.
                self.solution_is_valid = True

            self.history.pop()

    # Algorithm X Step 4 - Details:
    #
    # The select method updates the matrix when a row is selected as part of a solution.
    # Other rows that satisfy overlapping requirements need to be deleted and in the end,
    # all columns satisfied by the selected row get removed from the matrix.
    def select(self, node):

        node.select()
        self.solution.append(node.row_header.title)
        self._process_row_selection(node.row_header.title)


    # Algorithm X Step 4 - Clean Up:
    #
    # The select() method selects a row as part of the solution being explored. Eventually that
    # exploration ends and it is time to move on to the next row (action). Before moving on,
    # the matrix and the partial solution need to be restored to their prior states.
    def deselect(self, node):

        node.unselect()
        self.solution.pop()
        self._process_row_deselection(node.row_header.title)


    # In cases of multiplicity, this method can be used to ask Algorithm X to remember that
    # it has already tried certain things. For instance, if Emma wants two music lessons per
    # week, trying to put her first lesson on Monday at 8am is no different than trying to put
    # her second lesson on Monday at 8am. See my Algorithm X Playground for more details, 
    # specifically Mrs. Knuth - Part III.
    def _remember(self, item_to_remember: tuple) -> None:
        if item_to_remember in self.history[-1]:
            self.solution_is_valid = False
        else:
            self.history[-1].add((item_to_remember))

        
    # In some cases it may be beneficial to have Algorithm X try certain paths through the matrix.
    # This can be the case when there is reason to believe certain actions have a better chance than
    # other actions at producing complete paths through the matrix. The method included here does
    # nothing, but can be overridden to influence the order in which Algorithm X tries rows (actions) 
    # that cover some particular column.
    def _action_sort_criteria(self, row_header: DLXCell):
        return 0
    

    # In some cases it may be beneficial to have Algorithm X try covering certain requirements
    # before others as it looks for paths through the matrix. The default is to sort the requirements
    # by how many actions cover each requirement, but in some cases there might be several 
    # requirements covered by the same number of actions. By overriding this method, the
    # Algorithm X Solver can be directed to break ties a certain way or consider another way
    # of prioritizing the requirements.
    def _requirement_sort_criteria(self, col_header: DLXCell):
        return col_header.size
    
    
    # The following method can be overridden by a subclass to add logic to perform more detailed solution
    # checking if invalid paths are possible through the matrix. Some problems have requirements that
    # cannot be captured in the basic requirements list passed into the __init__() method. For instance,
    # a solution might only be valid if it fits certain parameters that can only be checked at intermediate
    # steps. In a case like that, this method can be overridden to add the functionality necessary to 
    # check the solution.
    #
    # If the subclass logic results in an invalid solution, the 'solution_is_valid' attribute should be set
    # to False instructing Algorithm X to stop progressing down this path in the matrix.
    def _process_row_selection(self, row):
        pass


    # This method can be overridden by a subclass to add logic to perform more detailed solution
    # checking if invalid paths are possible through the matrix. This method goes hand-in-hand with the
    # _process_row_selection() method above to "undo" what was done above.
    def _process_row_deselection(self, row):
        pass


    # This method can be overridden to instruct Algorithm X to do something every time a solution is found.
    # For instance, Algorithm X might be looking for the best solution or maybe each solution must be
    # validated in some way. In either case, the solution_is_valid attribute can be set to False
    # if the current solution should not be considered valid and should not be generated.
    def _process_solution(self):
        pass

class MrsKnuthPartISolver(AlgorithmXSolver):
    def __init__(self,requirements:list,actions:dict):
        super().__init__(requirements, actions)

def parse_schedule(schedule:list)->Dict[str,List[str]]:
    """
    Function to parse the schedules into structured data.
    It takes the input line, which has already been split into a list.
    It outputs a dictionary where the days are the keys and each day
    has a list of available hours. Since the teacher's schedule and 
    the students' schedules all follow this format, this can be used
    for all the schedules.
    e.g.:
    M 10 11 1 2 3 4 Tu W 10 11 1 2 3 4 Th F -> 
    {
      'M': ['10', '11', '1', '2', '3', '4'],
      'Tu': [],
      'W': ['10', '11', '1', '2', '3', '4']
      'Th': [],
      'F': [],
    }
    """
    return_schedule = {}
    day = None
    for e in schedule: # look through each element
        try:
            int(e) # see if it's a day or an hour
            is_day = False # it's not a day, so it's an hour
        except ValueError: is_day = True # we couldn't convert it to an integer, so it's a day
        if is_day:
            return_schedule[e] = [] # start the list to contain the available hours for today
            day = e # save this day until we reach the next day
        else: return_schedule[day].append(e) # add the hour to the day's list of available hours
    return return_schedule

def build_solver_matrix(teacher_schedule:dict, student_schedules:Dict[str,Dict[str,List[str]]])->Tuple[
        List[r_tuple],
        Dict[a_key,List[r_tuple]]
    ]:
    """
    This function builds the requirements and action files for this problem given the teacher's schedule
    and the students' schedules. It returns the requirements list, which is a list of requirement
    tuples and also returns the actions dictionary, which has for keys the tuple of actions and for 
    values the list of requirements satisfied by that action.
    """
    requirements = []
    actions = {}
    # parse teacher schedule
    for day,hours in teacher_schedule.items(): # each day in the teacher's schdule might have an opening
        for hour in hours: # each hour might have an opening
            requirements.append(('slot filled', day, hour)) # if the hour has an opening, it must eventually be scheduled
    # parse student schedules
    for student,schedule in student_schedules.items(): # each student plays at least one instrument
        requirements.append(('student scheduled',student)) # each student needs an appointment
        for instrument, days in schedule.items(): # drill into the details of the student's needs
            for day,hours in days.items(): # loop through the student's schedule
                if len(hours) > 0: # if the student has availability
                    if ('instrument on day', day, instrument) not in requirements: # if the day doesn't already have the student's instrument
                        requirements.append(('instrument on day', day, instrument)) # let's add it as a requirement
                for hour in hours: # looking through the student's availability on that day
                    if hour in teacher_schedule[day]: # if the student's availability intersects the teacher's availability
                        action = ('place student',student,instrument,day,hour) # it's possible to put the student in that slot, let's add it as an action
                        requirements_filled = [ # if the student were placed in that slot
                            ('student scheduled', student), # the student would have a slot
                            ('slot filled',day,hour), # the slot would be scheduled
                            ('instrument on day', day,instrument) # the instrument would be taught that day
                        ]
                        actions[action] = requirements_filled # combine into the complete action and add to the actions
    log_msg("Requirements\n" + pformat(requirements) + "\n")
    log_msg("Actions:\n" + pformat(actions) + "\n")
    return (requirements,actions)

# process input
teacher_schedule = parse_schedule(input().split()) # split the schedule and parse it into structured data
log_msg(f"Teacher schedule: {pformat(teacher_schedule)}")
student_count = int(input()) # get the count of students (needed so we know how many input lines to expect)
log_msg(f"Students requesting lessons: {student_count}")
student_input = [input() for _ in range(student_count)] # receive the student schedule input
student_schedules = {}
for s in student_input:
    name, instrument, *schedule = s.split()
    student_schedules.setdefault(name, {})[instrument] = parse_schedule(schedule) # build the student schedule as structured data
    log_msg(f"Parsed {name}'s ({instrument}) schedule: {schedule}->{student_schedules[name][instrument]}")
log_msg(f"Student schedules:\n{pformat(student_schedules)}")

# Solve using AlgorithmX
solver = MrsKnuthPartISolver(*build_solver_matrix(teacher_schedule,student_schedules)) # build the solver
solutions = {}
for solution in solver.solve():
    for _, name, instrument, day, hour in solution: # split out the actions in the solution
        log_msg(f"Schedule {name} for a {instrument} less on {day} at {hour}")
        if int(hour) in solutions: solutions[int(hour)][day] = f"{name}/{instrument}" # this is the first appointment for this hour of the day
        else: solutions[int(hour)] = {day:f"{name}/{instrument}"} # we already have an appointment at this hour (though for a different day), so add it intead of replacing

log_msg(f"Solutions:\n" + pformat(solutions))

# Output the solution
answer = "       Monday        Tuesday       Wednesday       Thursday        Friday"
for row in [8,9,10,11,"LUNCH",1,2,3,4]: # these are the possible hours of the day
    answer += "\n" # start a new row in the answer
    if row == "LUNCH": answer += ((" " * 10 + "LUNCH") * 5)[3:] # if it's lunch, mark it for lunch
    else:
        answer += f"{row:>2}" # output the hour of the day at the beginning of the row
        for day in teacher_schedule.keys(): # fill out each day of the teacher's schedule
            if row in solutions and day in solutions[row]: # if the solution involves a student at this hour on this day
                    answer += f" {solutions[row][day]:^14}" # insert the student and it's instrument
            else: answer += " " + "-" * 14 # nothing is scheduled, make it empty
        answer = answer.rstrip() # make sure this row doesn't contain any trailing spaces
answer = answer.rstrip() # make sure the answer doesn't have a trailing newline
print(answer) # output the answer