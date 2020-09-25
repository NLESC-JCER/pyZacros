from copy import deepcopy

from .Species import *
from .SpeciesList import SpeciesList


class Cluster:

    def __init__(self, site_types: list,
                 species: SpeciesList,
                 gas_species: SpeciesList = SpeciesList(),
                 neighboring: list = None,
                 multiplicity: int = 1,
                 cluster_energy: float = 0.000):
        """
        Creates a new Cluster object

        :parm site_types: list
        :parm neighboring: list
        :parm species: list
        :parm multiplicity: int
        :parm cluster_energy: float
        """
        self.site_types = site_types                  # e.g. [ "f", "f" ]
        self.neighboring = neighboring                # e.g. [ (1,2) ]
        self.species = species                        # e.g. [ Species("H*",1), Species("H*",1) ]
        self.gas_species = gas_species                # e.g. [ Species("H2") ]
        self.multiplicity = multiplicity              # e.g. 2
        self.cluster_energy = cluster_energy          # Units eV

        self.sites = len(site_types)

        if( sum([s.denticity for s in self.species]) != self.sites ):
            msg  = "### ERROR ### Cluster.__init__.\n"
            msg += "Inconsistent dimensions for species or site_types\n"
            raise NameError(msg)

        self.__label = None
        self.__updateLabel()

        self.__mass = 0.0

        for item in species:
            self.__mass += item.mass()

        for item in gas_species:
            self.__mass += item.mass()


    def __len__( self ) -> int:
        """
        Returns the number of species inside the cluster
        """
        return len(self.species)


    def __eq__( self, other ):
        """
        Returns True if both objects have the same label. Otherwise returns False
        """
        if( self.__label == other.__label ):
            return True
        else:
            return False


    def __hash__(self):
        """
        Returns a hash based on the label
        """
        return hash(self.__label)


    def __updateLabel( self ):
        """
        Updates the attribute 'label'
        """
        self.__label = ""
        for i in range(len(self.species)):
            self.__label += self.species[i].symbol+"-"
            for j in range(self.species[i].denticity):
                self.__label += self.site_types[i]
                if(j != self.species[i].denticity-1):
                    self.__label += "-"
            if(i != len(self.species)-1):
                self.__label += ","

        if(len(self.gas_species) > 0):
            self.__label += ":"

        for i in range(len(self.gas_species)):
            self.__label += self.gas_species[i].symbol
            if(i != len(self.gas_species)-1):
                self.__label += ","

        if self.neighboring is not None:
            if(len(self.neighboring) > 0):
                self.__label += ":"

        # For neighboring nodes are sorted
        if self.neighboring is not None:
            for i in range(len(self.neighboring)):
                lNeighboring = list(self.neighboring[i])
                lNeighboring.sort()
                self.__label += str(tuple(lNeighboring)).replace(" ", "")
                if( i != len(self.neighboring)-1):
                    self.__label += ","


    def label( self ) -> str:
        """
        Returns the label of the cluster
        """
        if( self.label is None ):
            self.__updateLabel()

        return self.__label


    def __str__( self ) -> str:
        """
        Translates the object to a string
        """
        output  = "cluster " + self.__label +"\n"

        if( len(self.gas_species) != 0 ):
            output += "  # gas_species "
            for i in range(len(self.gas_species)):
                output += self.gas_species[i].symbol
                if( i != len(self.gas_species)-1 ):
                    output += " "
            output += "\n"

        if( self.sites != 0 ):
            output += "  sites " + str(self.sites)+"\n"

            if self.neighboring is not None and len(self.neighboring) > 0:
                output += "  neighboring "
                for i in range(len(self.neighboring)):
                    output += str(self.neighboring[i][0])+"-"+str(self.neighboring[i][1])
                    if( i != len(self.neighboring)-1 ):
                        output += " "
                output += "\n"

            output += "  lattice_state"+"\n"
            for i in range(len(self.species)):
                for j in range(self.species[i].denticity):
                    output += "    "+str(i+1)+" "+self.species[i].symbol+" "+str(j+1)+"\n"

            output += "  site_types "
            for i in range(len(self.site_types)):
                output += str(self.site_types[i])
                if( i != len(self.site_types)-1 ):
                    output += " "
            output += "\n"

            output += "  graph_multiplicity "+str(self.multiplicity)+"\n"

        output += "  cluster_eng "+("%.8f"%self.cluster_energy)+"\n"
        output += "end_cluster"

        return output


    def mass( self ) -> float:
        """
        Returns the mass of the cluster in Da
        """
        return self.__mass


    def simplify( self ) -> Cluster:
        """
        Returns a new cluster where empty sites and gas species are removed.
        In case the cluster is fully empty None is returned
        """
        newCluster = deepcopy(self)

        idSitesToRemove = []
        for i in range(newCluster.sites):
            if( newCluster.species[i] == Species("*") ):
                idSitesToRemove.append(i)

        if( len(idSitesToRemove) == newCluster.sites ):
            return None

        newCluster.sites = newCluster.sites - len(idSitesToRemove)
        for id in idSitesToRemove:
            newCluster.site_types.pop( id )
            newCluster.species.pop( id )

        if( newCluster.neighboring is not None and len(newCluster.neighboring) > 0 ):
            idPairsToRemove = []
            for id in idSitesToRemove:
                for i,pair in enumerate(self.neighboring):
                    print(id+1, pair[0], pair[1])
                    if( id+1 == pair[0] or id+1 == pair[1] ):
                        idPairsToRemove.append(i)

            for id in idPairsToRemove:
                newCluster.neighboring.pop( id )

        newCluster.gas_species = []

        newCluster.__updateLabel()

        return newCluster

