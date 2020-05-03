# 6.00 Problem Set 8
#
# Name:
# Collaborators:
# Time:


import numpy
import random
import pylab
from ps7 import *
#
# PROBLEM 1
#
class ResistantVirus(SimpleVirus):

    """
    Representation of a virus which can have drug resistance.
    """

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):

        """

        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)
        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'grimpex',False}, means that this virus
        particle is resistant to neither guttagonol nor grimpex.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.

        """
        # TODO
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb
        self.resistances = resistances
        self.mutProb = mutProb


    def isResistantTo(self, drug):

        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in Patient to determine how many virus
        particles have resistance to a drug.

        drug: The drug (a string)
        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        # TODO
        return self.resistances[drug]


    def reproduce(self, popDensity, activeDrugs):

        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient class.

        If the virus particle is not resistant to any drug in activeDrugs,
        then it does not reproduce. Otherwise, the virus particle reproduces
        with probability:

        self.maxBirthProb * (1 - popDensity).

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent).

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.

        For example, if a virus particle is resistant to guttagonol but not
        grimpex, and `self.mutProb` is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        grimpex and a 90% chance that the offspring will not be resistant to
        grimpex.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """
        # TODO
        new_resistances = {}
        resistance_check = []
        if len(activeDrugs) == 0:
            pass
        else:
            for drug in activeDrugs:
                resistance_check.append(self.isResistantTo(drug))
            if True not in resistance_check:
                raise NoChildException
        repProb = self.maxBirthProb * (1 - popDensity)
        if random.random() >= repProb:
            raise NoChildException

        #Now virus is going to reproduce
        for resistance in self.resistances:
            if self.resistances[resistance] == True:
                if random.random() < self.mutProb:
                    new_resistances[resistance] = False
                else:
                    new_resistances[resistance] = True
            if self.resistances[resistance] == False:
                if random.random() >= self.mutProb:
                    new_resistances[resistance] = False
                else:
                    new_resistances[resistance] = True

        return ResistantVirus(self.maxBirthProb, self.clearProb, \
            new_resistances, self.mutProb)

# drugs = ['a', 'b', 'c']
# resistances = {'a': True, 'b': False, 'c': False}
# maxBirthProb = 0.1
# mutProb = 0.1
# clearProb = 0.05

# RV1 = ResistantVirus(maxBirthProb, clearProb, resistances, mutProb)
# print RV1.reproduce(2, drugs)

class Patient(SimplePatient):

    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the  maximum virus population for this patient (an integer)
        """
        self.viruses = viruses
        self.maxPop = maxPop
        self.drugs = []
        # TODO


    def addPrescription(self, newDrug):

        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: list of drugs being administered to a patient is updated
        """
        # TODO
        # should not allow one drug being added to the list multiple times
        if newDrug not in self.drugs:
            self.drugs.append(newDrug)


    def getPrescriptions(self):

        """
        Returns the drugs that are being administered to this patient.
        returns: The list of drug names (strings) being administered to this
        patient.
        """
        return self.drugs
        # TODO

    def checkResistances(self, virus, drugs):
        """
        test virus to see if it is resistant to all the drugs
        drugs: list of strings
        virus: instance of virus
        """
        for drug in drugs:
            if not virus.isResistantTo(drug):
                return False
        return True

    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'grimpex'])

        returns: the population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        num_resistant = 0
        for virus in self.viruses:
            if self.checkResistances(virus, drugResist):
                num_resistant += 1
        return num_resistant
        # TODO



    def update(self):

        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly
        - The current population density is calculated. This population density
          value is used until the next call to update().
        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient.
          The listof drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: the total virus population at the end of the update (an
        integer)
        """
        # TODO
        viruses_after_doesClear = []
        for virus in self.viruses:
            if not virus.doesClear():
                viruses_after_doesClear.append(virus)
        pop_density = float(len(viruses_after_doesClear)) / float(self.maxPop)
        viruses_after_reproduce = []
        for virus in viruses_after_doesClear:
            viruses_after_reproduce.append(virus)
            try:
                new_virus = virus.reproduce(pop_density, self.drugs)
                viruses_after_reproduce.append(new_virus)
            except NoChildException:
                continue
        self.viruses = viruses_after_reproduce
        return len(self.viruses)



#
# PROBLEM 2
#

def simulationWithDrug():

    """

    Runs simulations and plots graphs for problem 4.
    Instantiates a patient, runs a simulation for 150 timesteps, adds
    guttagonol, and runs the simulation for an additional 150 timesteps.
    total virus population vs. time and guttagonol-resistant virus population
    vs. time are plotted
    """
    # TODO
    viruses = []
    gutt_resist_pop = []
    for n in range(100):
        viruses.append(ResistantVirus(0.1, 0.05, {'guttagonol': False}, 0.005))
    P1 = Patient(viruses, 1000)


    virus_population = [100]
    for t in range(150):
        virus_population.append(P1.update())
        gutt_resist_pop.append(P1.getResistPop(['guttagonol']))
    P1.addPrescription('guttagonol')
    for t in range(150):
        virus_population.append(P1.update())
        gutt_resist_pop.append(P1.getResistPop(['guttagonol']))

    plt1 = pylab.figure(1)
    pylab.plot(virus_population)
    pylab.xlabel("Time")
    pylab.ylabel("Viruses in Patient")
    pylab.title("Total Viruses in Patient vs Time")

    plt2 = pylab.figure(2)
    pylab.plot(gutt_resist_pop)
    pylab.xlabel("Time")
    pylab.ylabel("Guttagonol Resistant Viruses in Patient")
    pylab.title("Total Guttagonol Resistant Viruses in Patient vs Time")

    pylab.show()

simulationWithDrug()




#
# PROBLEM 3
#

def simulationDelayedTreatment():

    """
    Runs simulations and make histograms for problem 5.
    Runs multiple simulations to show the relationship between delayed treatment
    and patient outcome.
    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).
    """

    # TODO

#
# PROBLEM 4
#

def simulationTwoDrugsDelayedTreatment():

    """
    Runs simulations and make histograms for problem 6.
    Runs multiple simulations to show the relationship between administration
    of multiple drugs and patient outcome.

    Histograms of final total virus populations are displayed for lag times of
    150, 75, 0 timesteps between adding drugs (followed by an additional 150
    timesteps of simulation).
    """

    # TODO



#
# PROBLEM 5
#

def simulationTwoDrugsVirusPopulations():

    """

    Run simulations and plot graphs examining the relationship between
    administration of multiple drugs and patient outcome.
    Plots of total and drug-resistant viruses vs. time are made for a
    simulation with a 300 time step delay between administering the 2 drugs and
    a simulations for which drugs are administered simultaneously.

    """
    #TODO



