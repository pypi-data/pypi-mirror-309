from tkinter import filedialog
from tkinter import *
from tkinter import simpledialog
import tkinter
import kspice
import networkx as nx
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


class _askTimeline(simpledialog.Dialog): 

    def __init__(self, root, title, timelines= []):
        self.timelines = timelines
        self.tl = IntVar(root)
        super().__init__(root, title)
    
    def body(self, master):


        tkinter.Label(master, text="Please select the timeline to run").pack()

        for i, timeline in enumerate(self.timelines):
            tkinter.Radiobutton(master, text = timeline.name, value=i, variable = self.tl, indicator = 0).pack()


        return master

    def apply(self):
        pass
        
class _askFiles(simpledialog.Dialog):

    def __init__(self, root, title, models, parameters, ics):
        self.models = models
        self.parameters = parameters
        self.ics = ics
        self.m = IntVar(root, 0)
        self.p = IntVar(root, 0)
        self.i = IntVar(root, 0)
        super().__init__(root, title)

    def body(self, master):

        

       

        tkinter.Label(master, text="Models").grid(column=0, row=0, sticky=tkinter.W, padx=5, pady=5)
        for i, model in enumerate(self.models):
            tkinter.Radiobutton(master, text=model, value=i, variable = self.m).grid(column=0, 
                                                                                                     row=1+i,
                                                                                                     sticky=tkinter.W,
                                                                                                     padx=5,
                                                                                                     pady=5)

        tkinter.Label(master, text="Parameters").grid(column=1, row=0, sticky=tkinter.W, padx=5, pady=5)        
        for i, param in enumerate(self.parameters):
            tkinter.Radiobutton(master, text=param, value=i, variable = self.p).grid(column=1, 
                                                                                                     row=1+i,
                                                                                                     sticky=tkinter.W,
                                                                                                     padx=5,
                                                                                                     pady=5)
        tkinter.Label(master, text="Initial Conditions").grid(column=2, row=0, sticky=tkinter.W, padx=5, pady=5)
        for i, ic in enumerate(self.ics):
            tkinter.Radiobutton(master, text=ic, value=i, variable = self.i).grid(column=2, 
                                                                                                     row=1+i,
                                                                                                     sticky=tkinter.W,
                                                                                                     padx=5,
                                                                                                     pady=5)

        return master

    def apply(self):
        pass
        
        
class On_Off_Valve:
    
    def __init__(self, tag, model, app=False):  
        """Wrapper class for operating block-valves and motor-operated-valves in the Yggdrasil Engineering Simulator"""


        self.sim = model.sim
        self.tl = model.timeline
        
        if not app:

            applications = [x.name for x in self.tl.applications]
            
            if tag[0] in "DEFNS":
                app = "HuginA" if "HuginA" in applications else self._search_application_(tag)
            
            elif tag[0] in "ACVWYZ":
                app = "Munin" if "Munin" in applications else self._search_application_(tag)

            elif tag[0] in "G":
                app = "HuginB" if "HuginB" in applications else self._search_application_(tag)
            else:
                app = self._search_application_(tag)
        

        self.app = app
        
        if self.app:
            try:
                self.v = self.tl.get_block(app, tag)
            except:
                print("No valve with tag {} found in application {}".format(tag, self.app))
        else:
            print("No valve with tag {} found in any of the simulator applications".format(tag))
            self.v = False

        if self.v:
            if self.v.type not in ["MotorOperatedValve", "BlockValve", "LedaValve"]:
                print("Object is not a Leda-Valve, Motor-Operated_Valve or Block-Valve. Object is of type {}.\nNo further operations on object allowed.".format(self.v.type))
                self.v = False
    
    def _search_application_(self, tag):
        """ Returns the application name where tag can be found """
        for application in self.tl.applications:
            try:
                temp = self.tl.get_block(application.name, tag)
                print("{} found in application {}".format(tag, application.name))
                return application.name
                
            except:
                return False    
    
    def get_valve(self):
        """ Return the BlockValve object """
        return self.v
    

    def close(self):    
        """ Wrapper that closes the valve regardless of type """
        if self.v:
            if self.v.type == "MotorOperatedValve":
                self.tl.set_value(self.app, self.v.name + ":LocalClose", True)
            elif self.v.type == "BlockValve":
                self.tl.set_value(self.app, self.v.name + ":LocalInput", False)
            elif self.v.type == "LedaValve":
                self.tl.set_value(self.app, self.v.name + ":LocalControlSignalIn", 0, unit="%")
        else:
            print("Unvaild valve object")

    def open(self):
        """ Wrapper that open the valve regardless of type """
        if self.v:
            if self.v.type == "MotorOperatedValve":
                self.tl.set_value(self.app, self.v.name + ":LocalOpen", True)
            elif self.v.type == "BlockValve":
                self.tl.set_value(self.app, self.v.name + ":LocalInput", True)
            elif self.v.type == "LedaValve":
                self.tl.set_value(self.app, self.v.name + ":LocalControlSignalIn", 100, unit="%")
        else:
            print("Unvaild valve object")
            
    def get_pos(self):
        """ Wrapper that returns the stem position of the valve in percentage """
        if self.v:
            return self.tl.get_value(self.app, self.v.name + ":ValveStemPosition", unit="%")
        else:
            print("Unvaild valve object")
            
    def is_open(self):
        """ Wrapper that returns True if valve is defined as open """
        if self.v:
            return self.tl.get_value(self.app, self.v.name + ":IsDefinedOpen")
        else:
            print("Unvaild valve object")
            
    def is_closed(self):
        """ Wrapper that returns True if valve is defined as closed """
        if self.v:
            return self.tl.get_value(self.app, self.v.name + ":IsDefinedClosed")
        else:
            print("Unvaild valve object")        
    
class Motor_Heater:

    def __init__(self, tag, model, app=False):  
        """Wrapper class for operating motors and heaters in the Yggdrasil Engineering Simulator"""


        self.sim = model.sim
        self.tl = model.timeline
        
        if not app:

            applications = [x.name for x in self.tl.applications]
            
            if tag[0] in "DEFNS":
                app = "HuginA" if "HuginA" in applications else self._search_application_(tag)
            
            elif tag[0] in "ACVWYZ":
                app = "Munin" if "Munin" in applications else self._search_application_(tag)

            elif tag[0] in "G":
                app = "HuginB" if "HuginB" in applications else self._search_application_(tag)
            else:
                app = self._search_application_(tag)
        

        self.app = app
        
        if self.app:
            try:
                self.m = self.tl.get_block(app, tag)
            except:
                print("No motor with tag {} found in application {}".format(tag, self.app))
        else:
            print("No motor with tag {} found in any of the simulator applications".format(tag))
            self.m = False

        if self.m:
            if self.m.type not in ["ControlledAsynchronousMachine", "ControlledElectricHeater"]:
                print("Object is not a Motor or Heater. Object is of type {}.\nNo further operations on object allowed.".format(self.v.type))
                self.m = False

    def _search_application_(self, tag):
        """ Returns the application name where tag can be found """
        for application in self.tl.applications:
            try:
                temp = self.tl.get_block(application.name, tag)
                print("{} found in application {}".format(tag, application.name))
                return application.name
                
            except:
                return False       
    
    def start(self):
        
        """ Switch on the motor/element """
        if self.m:
            self.tl.set_value(self.app, self.m.name + ":LocalInput", True)
        else:
            print("Unvaild heater or motor object")   
    def stop(self):
        
        """ Switch off the motor/element """
        if self.m:
            self.tl.set_value(self.app, self.m.name + ":LocalInput", False)
        else:
            print("Unvaild heater or motor object")
    def is_on(self):
        """ Returns True if motor/element is switched on """
        return self.tl.get_value(self.app, self.m.name + ":LocalInput") == True
    def is_off(self):
        """ Returns True if motor/element is switched off """
        return self.tl.get_value(self.app, self.m.name + ":LocalInput") == False

class PID:
    def __init__(self, tag, model, app=False):  
        """Wrapper class for operating PID controllers in the Yggdrasil Engineering Simulator"""


        self.sim = model.sim
        self.tl = model.timeline
        
        if not app:

            applications = [x.name for x in self.tl.applications]
            
            if tag[0] in "DEFNS":
                app = "HuginA" if "HuginA" in applications else self._search_application_(tag)
            
            elif tag[0] in "ACVWYZ":
                app = "Munin" if "Munin" in applications else self._search_application_(tag)

            elif tag[0] in "G":
                app = "HuginB" if "HuginB" in applications else self._search_application_(tag)
            else:
                app = self._search_application_(tag)
        

        self.app = app
        
        if self.app:
            try:
                self.c = self.tl.get_block(app, tag)
            except:
                print("No PID controller with tag {} found in application {}".format(tag, self.app))
        else:
            print("No PID controller with tag {} found in any of the simulator applications".format(tag))
            self.c = False

        if self.c:
            if self.c.type not in ["PidController"]:
                print("Object is not a PID Controller. Object is of type {}.\nNo further operations on object allowed.".format(self.v.type))
                self.c = False

    def _search_application_(self, tag):
        """ Returns the application name where tag can be found """
        for application in self.tl.applications:
            try:
                temp = self.tl.get_block(application.name, tag)
                print("{} found in application {}".format(tag, application.name))
                return application.name
                
            except:
                return False   
    
    def get_mode(self):
        """
        Returns text representation of the current mode
        """
        m = self.tl.get_value(self.app, self.c.name + ":Mode")
        if m == 0:
            return ("Auto")
        elif m == 1:
            return ("Manual")
        else: 
            return("External")
    
    def get_sp_selection(self):
        s = self.tl.get_value(self.app, self.c.name + ":SetpointSelection")
        if s == 0:
            return("Internal")
        else:
            return("External")

    def to_auto(self):
        """
        Set controller mode to Auto
        """
        self.tl.set_value(self.app, self.c.name + ":Mode", 0)

    def to_man(self):
        """
        Set controller mode to Manual
        """
        self.tl.set_value(self.app, self.c.name + ":Mode", 1)

    def to_external(self):
        """
        Set controller mode to External SP
        """
        self.tl.set_value(self.app, self.c.name + ":Mode", 2)        

    def set_output(self, out):
        """
        Change output of controller if controller is in manual mode
        """
        if self.get_mode() == "Manual":
            self.tl.set_value(self.app, self.c.name + ":ControllerOutput", out)
    def get_output(self):
        """
        Get output of controller
        """        
        return self.tl.get_value(self.app, self.c.name + ":ControllerOutput")

    def set_setpoint(self, sp):
        """
        Change internal setpoint of controller if controller is in manual or auto with internal setpoint selection
        """
        if self.get_mode() == "Manual" or (self.get_mode() == "Auto" and self.get_sp_selection() == "Internal"):
            self.tl.set_value(self.app, self.c.name + ":InternalSetpoint", sp)

class Choke:
    def __init__(self, tag, model, app=False):  
        """Wrapper class for operating Choke objects in the Yggdrasil Engineering Simulator"""


        self.sim = model.sim
        self.tl = model.timeline
        
        if not app:

            applications = [x.name for x in self.tl.applications]
            
            if tag[0] in "DEFNS":
                app = "HuginA" if "HuginA" in applications else self._search_application_(tag)
            
            elif tag[0] in "ACVWYZ":
                app = "Munin" if "Munin" in applications else self._search_application_(tag)

            elif tag[0] in "G":
                app = "HuginB" if "HuginB" in applications else self._search_application_(tag)
            else:
                app = self._search_application_(tag)
        

        self.app = app
        
        if self.app:
            try:
                self.c = self.tl.get_block(app, tag)
            except:
                print("No choke with tag {} found in application {}".format(tag, self.app))
        else:
            print("No choke with tag {} found in any of the simulator applications".format(tag))
            self.c = False

        if self.c:
            if self.c.type not in ["ControlValve", "LedaValve"]:
                print("Object is not a Control Valve. Object is of type {}.\nNo further operations on object allowed.".format(self.c.type))
                self.c = False

    def _search_application_(self, tag):
        """ Returns the application name where tag can be found """
        for application in self.tl.applications:
            try:
                temp = self.tl.get_block(application.name, tag)
                print("{} found in application {}".format(tag, application.name))
                return application.name
                
            except:
                return False       
    
    def move_to(self, pos):
        """
        Wrapper that moves a choke object to a desired position.  
        If LocalControlSignalIn is connected from an external source, the choke will be set in Manual Mode
        """
        connections = self.tl.get_block(self.app, self.c.name).input_connections
        if len(connections) > 0:
            for conn in connections:
                if "LocalControlSignalIn" in str(conn):
                    self.direct_control()
        self.tl.set_value(self.app, self.c.name + ":LocalControlSignalIn", pos, unit="%")
        self.tl.set_value(self.app, self.c.name + ":TargetPosition", pos, unit="%")

    def direct_control(self):
        """
        Set object in manual mode
        """
        self.tl.set_value(self.app, self.c.name + ":InputSwitch",2)

    def reset_control(self):
        """
        If object has defined connection to LocalControlSignalIn, set mode to Local
        """
        connections = self.tl.get_block(self.app, self.c.name).input_connections
        if len(connections) > 0:
            for conn in connections:
                if "LocalControlSignalIn" in str(conn):
                    self.tl.set_value(self.app, self.c.name + ":InputSwitch", 0)      
    
    def get_pos(self):
        return self.tl.get_value(self.app, self.c.name + ":ValveStemPosition", unit="%")

class Transmitter:
    def __init__(self, tag, model, app=False):  
        """Wrapper class for reading transmitter objects in the Yggdrasil Engineering Simulator"""


        self.sim = model.sim
        self.tl = model.timeline
        
        if not app:

            applications = [x.name for x in self.tl.applications]
            
            if tag[0] in "DEFNS":
                app = "HuginA" if "HuginA" in applications else self._search_application_(tag)
            
            elif tag[0] in "ACVWYZ":
                app = "Munin" if "Munin" in applications else self._search_application_(tag)

            elif tag[0] in "G":
                app = "HuginB" if "HuginB" in applications else self._search_application_(tag)
            else:
                app = self._search_application_(tag)
        

        self.app = app
        
        if self.app:
            try:
                self.t = self.tl.get_block(app, tag)
            except:
                print("No transmitter with tag {} found in application {}".format(tag, self.app))
        else:
            print("No transmitter with tag {} found in any of the simulator applications".format(tag))
            self.t = False

        if self.t:
            if self.t.type not in ["AlarmTransmitter"]:
                print("Object is not a Transmitter. Object is of type {}.\nNo further operations on object allowed.".format(self.t.type))
                self.t = False

    def _search_application_(self, tag):
        """ Returns the application name where tag can be found """
        for application in self.tl.applications:
            try:
                temp = self.tl.get_block(application.name, tag)
                print("{} found in application {}".format(tag, application.name))
                return application.name
                
            except:
                return False   
    def get_value(self, unit):
        return self.tl.get_value(self.app, self.t.name + ":MeasuredValue", unit=unit)

class YggLCS:
    """
    Wrapper for creating a simulator object.  
    Will invoke GUI elements for choosing model, timeline and timeline-files.
    """
    def __init__(self, run = False):
        """
        Initialise a Yggdrasil LCS object.  
        Optional "run" parameter will call "run" on timeline after initialization if True
        """

        root = Tk()
        root.withdraw()

        self.model = filedialog.askdirectory(**{"title":"Please select model directory"})
        self.sim = kspice.Simulator(self.model)
        self.tl = _askTimeline(root, "Timelines", self.sim.timelines).tl.get()
        self.timeline = self.sim.timelines[self.tl]
        self.timeline.activate()
        files = _askFiles(root, "Files", self.timeline.models, self.timeline.parameters, self.timeline.initial_conditions)
        self.model = files.m.get()
        self.parameter = files.p.get()
        self.ic = files.i.get()
        self.timeline.load(self.timeline.models[self.model], self.timeline.parameters[self.parameter], self.timeline.initial_conditions[self.ic])
        self.timeline.initialize()
        if run:
            self.timeline.run()

    def get_timeline(self):
        """
        Returns the active timeline object
        """
        return self.timeline
    
    def on_off_valve(self, tag, app=False):
        """
        Creates and returns a on-off valve object
        """
        return On_Off_Valve(tag, self, app)

    def motor_heater(self, tag, app=False):
        """
        Creates and returns an electrical element, used for heaters and motors
        """
        return Motor_Heater(tag, self, app)

    def pid(self, tag, app=False):
        """
        Creates and returns a PID controller
        """
        return PID(tag, self, app)
    
    def choke(self, tag, app=False):
        """        
        Creates and returns a choke object
        """
        return Choke(tag, self, app)

    def transmitter(self, tag, app=False):
        """
        Creates and returns an AlarmTransmitter object
        """
        return Transmitter(tag, self, app)
    
    def run(self):
        self.timeline.run()
    def pause(self):
        self.timeline.pause()
    def close_project(self):
        self.sim.close_project()

class Sequence:
    """
    Sequencer object.  Consists of a collection of Step objects.
    Constructor requires the globals() dictionary from calling module as second argument.  
    Optional inhibit conditions is a list with conditions in the form of function references.
    """

    def __init__(self, name, glob, sim, inhibit_conditions=[], verbose = False):
        self.glob = glob
        self.steps = []
        self.inhibits = inhibit_conditions
        self.name = name
        self.sim = sim
        self.verbose = verbose

    def check_inhibits(self):
        """ Inhibit conditions must all evaluate to False to allow sequence to start"""
        ret = True
        if len(self.inhibits) > 0:            
            for inhibit in self.inhibits:
                if inhibit():
                    print("Inhibit condition prevents sequence start of " + self.name + ": " + str(inhibit))
                    ret = False
        return ret
    
    def start(self):
        """
        Executes the sequence, Step by Step according to Step configuration and logic
        """

        print("\n*** Starting Sequence. Name: {}, number of Steps: {} ***".format(self.name, len(self.steps)))

        if self.check_inhibits():
            self.steps.sort()

            # Step 1 is the always the first step in a sequence.  Following steps dictated by Step property and logic.
            step = self.steps[0] 
            while True:
                if self.verbose:
                    print("Executing step {}".format(step.number), end="...") 
                if step.check_conditions():
                    #print("Conditions all ok", end="...")                
                    step.execute_actions()
                    if self.verbose:
                        print("Executing {} action(s)".format(len(step.st)), end="...")
                    start = self.sim.timeline.model_time
                    while not step.check_trans():
                        time.sleep(1)
                        end = self.sim.timeline.model_time
                        if (end-start).seconds > step.tmax:
                            raise Exception("Step timeout in step number {}".format(step.number))
                if self.verbose:
                    print("Step {} executed successfully.".format(step.number))
                if step.next:
                    step = self.glob[step.next()]
                else:
                    print("*** Sequence {} finished ***".format(self.name))
                    break
        else:
            raise Exception("Sequence cannot be started due to inhibit conditions")
        return self.name

    def add_step(self, step):
        self.steps.append(step)

    def add_steps(self, steps):
        for step in steps:
            self.add_step(step)

class Step:
    """
    A Sequence Step object.  Constructor takes Step configuration in the form of a dictionary.  
    Required fields in dictionary:
        number: The step number. 
        conditions: A list of conditions in the form of function references, all must be evaluated to True for the step to execute
        actions: A list of actions in the form of function references, all will be executed simultaniously
        transitions: A list of transition conditions in the form of function references.  All must be evaluated to True for the step to finish.
        tmax: The maximum number of seconds the step can take, measured in simulator time.
        next: The name of the next Step variable in string format.  Will be evaluated in runtime to find the correct object.
    """
    def __init__(self, config):
        self.failed = False
        self.number = config["number"]
        self.cond = config["conditions"]
        self.st = config["actions"]
        self.trans = config["transitions"]
        self.tmax = config["tmax"]
        self.next = config["next"]

    def conditions(self):
        """
        Returns the list of condition function references
        """
        return self.cond

    def check_conditions(self):
        """
        All conditions must evaluate to True to continue
        """
        for cond in self.cond:
            
            if not cond():
                raise Exception("Condition not met: " + str(cond))
                return False
        return True
    def execute_actions(self):
        """
        Executes all actions
        """
        for st in self.st:
            st()

    def check_trans(self):
        """
        All transitions must evaluate to True to continue.
        """
        ret = True
        for trans in self.trans:
            if not trans():
                ret = False
        return ret

    def StepAction(self):
        """
        Returns the list of Step Actions
        """
        return self.st

    def transition(self):
        """
        Returns the list of Step Transitions
        """
        return self.trans

    def onFail(self):
        """
        To be implemented.  What to do on Step failure (conditions or transitions).  For now Exceptions are raised directly.
        """
        return False

    def __lt__(self, other):
        """
        To allow sorting
        """
        return self.number < other.number

    def __eq__(self, other):
        """
        To allow sorting
        """
        return self.number == other.number


class Admin:

    """
    Creates an Administration sequence.  
    Arguments:
        sequences: A list of Sequence objects
        edges: A list of tuples dictating the dependencies between sequences.
        glob: a copy of the globals dictionary from calling module
        sim: a reference to the YggLCS simulator object from calling module
    """

    def __init__(self, sequences, edges, glob, sim):
        self.seq = {}
        for s in sequences:
            self.seq[s.name] = s
        # Initialise first step (START)
        start = Step({
            "number": 1,
            "conditions": [],
            "actions": [],
            "transitions": [],
            "tmax": 2,
            "next": None
        })
        start_seq = Sequence("START", 
               glob,
               sim,
               []
               )
        start_seq.add_step(start)
        self.seq["START"] = start_seq

        #Initialize the last step (END)
        end = Sequence("END", 
               glob,
               sim,
               []
               )
        end.add_step(start)
        self.seq["END"] = end
        
        self.edges = edges

        # Create a directed graph
        self.G = nx.DiGraph()
        # Create the nodes and connect the edges
        self.G.add_edges_from(edges)


    def start(self):
        """
        Starts the admin sequence execution
        """
        self.execute_tasks(self.G, self.seq)



    def start_sequence(self, seq, name):
        """
        Helper function to start a sequence and return the name of the sequence that was started.
        """
        seq.start()
        return name





# Execute the tasks based on the dependency graph
    def execute_tasks(self, graph, seq_objects):
        """
        Function that starts all the sequences which has no parent or whos parent has completed. 
        Parallel sequences are started in separate pseudo threads to enable paralell execution. 
        Edges in directed graph dicated when a sequence can be started.
        """
        # Find the start tasks (those that have no predecessors)
        initial_tasks = [n for n in graph.nodes if graph.in_degree(n) == 0]
    
        # Initialize an executor for parallel task execution
        with ThreadPoolExecutor() as executor:
            # Track futures
            task_futures = {}
    
            # Start initial tasks
            for task_name in initial_tasks:
                
                task_futures[task_name] = executor.submit(self.start_sequence, seq_objects[task_name], task_name)
    
            # As each task finishes, check if we can start dependent tasks
            while task_futures:
                for future in as_completed(task_futures.values()):
                    task_name = future.result()  # Get the result (task name)
                    
                    if task_name is None:
                        raise ValueError("Error: Task returned None!")
    
                    # Check if task has successors
                    if task_name in graph:
                        successors = list(graph.successors(task_name))
                        for successor in successors:
                            # Check if all predecessors of the successor have finished
                            predecessors = list(graph.predecessors(successor))
                            if all(p in task_futures and task_futures[p].done() for p in predecessors):
                                # Start successor task
                                
                                task_futures[successor] = executor.submit(self.start_sequence, seq_objects[successor], successor)
    
                    # Remove completed task from tracking
                    if task_name in task_futures:
                        del task_futures[task_name]