from .ElementaryReaction import *

class Mechanism(list):

    def __str__( self ) -> str:
        """
        Translates the object to a string
        """
        output = "mechanism"+"\n"
        for i in range(len(self)):
            output += str(self[i])
            if( i != len(self)-1 ):
                output += "\n"
        output += "\n"
        output += "end_mechanism"

        return output


    @staticmethod
    def test():
        """
        Tests the main methods of the object
        """
        print( "---------------------------------------------------" )
        print( ">>> Testing Mechanism class" )
        print( "---------------------------------------------------" )

        s0 = Species( "*" )      # Empty adsorption site
        s1 = Species( "H*", 1 )  # H adsorbed with dentation 1
        s2 = Species( "H2*", 1 ) # H2 adsorbed with dentation 1
        s3 = Species( "H2*", 2 ) # H2 adsorbed with dentation 2

        myCluster1 = Cluster( "H*(f)-H*(f)",
                                site_types=( "f", "f" ),
                                neighboring=[ (1,2) ],
                                species=( s1, s1 ),
                                multiplicity=2,
                                energy=0.1 )   #TODO energy --> cluster_energy

        myCluster2 = Cluster( "H2*(f)-*(f)",
                                site_types=( "f", "f" ),
                                neighboring=[ (1,2) ],
                                species=( s2, s0 ),
                                multiplicity=2,
                                energy=0.1 )

        myCluster3 = Cluster( "H2*(f,f)",
                                site_types=( "f", "f" ),
                                neighboring=[ (1,2) ],
                                species=( s3, s3 ),
                                multiplicity=2,
                                energy=0.1 )

        myReaction1 = ElementaryReaction( "H*(f)-H*(f)<-->H2*(f)-*(f)",
                                            site_types=( "f", "f" ),
                                            neighboring=[ (1,2) ],
                                            initial=myCluster1,
                                            final=myCluster2,
                                            reversible=True,
                                            pre_expon=1e+13,
                                            pe_ratio=0.676,
                                            activation_energy = 0.2 )

        myReaction2 = ElementaryReaction( "H2*(f,f)<-->H2*(f)-*(f)",
                                            site_types=( "f", "f" ),
                                            neighboring=[ (1,2) ],
                                            initial=myCluster3,
                                            final=myCluster2,
                                            reversible=True,
                                            pre_expon=1e+13,
                                            pe_ratio=0.676,
                                            activation_energy = 0.2 )

        myMechanism = Mechanism()
        myMechanism.append( myReaction1 )
        myMechanism.append( myReaction2 )

        print( myMechanism )

        output = str(myMechanism)
        expectedOutput = """\
mechanism
reversible_step H*(f)-H*(f)<-->H2*(f)-*(f)
  sites 2
  neighboring 1-2
  initial
    1 H* 1
    2 H* 1
  final
    1 H2* 1
    2 * 1
  site_types f f
  pre_expon 1.000000e+13
  pe_ratio 0.676
  activ_eng 0.2
end_step
reversible_step H2*(f,f)<-->H2*(f)-*(f)
  sites 2
  neighboring 1-2
  initial
    1 H2* 1
    2 H2* 1
  final
    1 H2* 1
    2 * 1
  site_types f f
  pre_expon 1.000000e+13
  pe_ratio 0.676
  activ_eng 0.2
end_step
end_mechanism\
"""
        assert( output == expectedOutput )

