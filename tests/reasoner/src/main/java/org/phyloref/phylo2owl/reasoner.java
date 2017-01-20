/**
 * A program to invoke a reasoner over an input ontology.
 *
 * Synopsis: java -jar reasoner.jar tree.owl phylorefs.omn
 *
 * @author      Gaurav Vaidya <gaurav@ggvaidya.com>
 * @version     0.1
 */

package org.phyloref.phylo2owl;

import org.semanticweb.owlapi.*;
import org.semanticweb.owlapi.io.*;
import org.semanticweb.owlapi.model.*;
import org.semanticweb.owlapi.apibinding.*;
import org.semanticweb.HermiT.*;
import org.coode.owlapi.manchesterowlsyntax.*;
import java.io.*;
import java.util.*;

/**
 * A command-line tool to reason over an input ontology.
 */
public class reasoner {

    /**
     * Version string.
     */
    public static final String Version = "0.1";

    /**
     * Check command line arguments, load files as Jena models,
     * then pass them on to {@link #getIndividualsByClass(OWLOntology)}.
     */ 
    public static void main(String[] args) {
        if(args.length > 2) {
            // We only support up to two arguments.
            System.err.println("Invalid number of arguments: ontology filename and phyloreference filename required.");
            System.exit(1);

        } else if(args.length == 0 || args.length == 1) {
            // There are few single-word command line options:
            if(args.length == 1) {
                if(args[0].equalsIgnoreCase("--version")) {
                    // --version: Display the version number.
                    System.err.println("reasoner " + reasoner.Version);
                    System.exit(1);

                } else {
		    if(!args[0].equalsIgnoreCase("--help")) {
                        // Unless the user asks for --help, we display
                        // an error message on a single argument.
                        System.err.println("Error: argument '" + args[0] + "' not understood.\n");
                    }
                }
            }

            // Display command line options.
            System.err.println("reasoner input.owl phylorefs.omn");
            System.err.println(" - input.owl: Ontology to reasoner over.");
            System.err.println(" - phylorefs.omn: Phyloreferences to test.");

            System.exit(1);
        } else {

            // Two arguments: args[0] contains the tree as an OWL ontology, 
            // while args[1] is the phyloreference as an OWL ontology.
            String treeFileName = args[0];
            String phylorefsFileName = args[1];

            File fTree = new File(treeFileName);
            File fPhylorefs = new File(phylorefsFileName);

            if(!fTree.canRead()) {
                System.err.println("File '" + treeFileName + "' could not be read.");
                System.exit(1);
            }

            if(!fPhylorefs.canRead()) {
                System.err.println("File '" + phylorefsFileName + "' could not be read.");
                System.exit(1);
            }

            // If run in interactive mode, re-run the inferences when the user
            // hits enter.
            String filter = "";
            Console console = System.console();
            boolean repeat = false;

            do {
                // Reason over the tree and phyloreferences.
                // This produces a set of OWL classes and the
                // individuals they are linked to.
                Map<OWLClass, Set<OWLNamedIndividual>> results;

                try {
                    results = getIndividualsByClass(fTree, fPhylorefs);
                } catch(OWLException e) {
                    System.err.println("Error (OWL): " + e);
                    System.exit(1);
                    return;
                } catch(IOException e) {
                    System.err.println("Error (reading input file): " + e);
                    System.exit(1);
                    return;
                }

                // Produce output as n-triples. We simply assert that every
                // individual is rdf:type-d to its corresponding class.
                for(OWLClass cl: results.keySet()) {
                    for(OWLNamedIndividual ind: results.get(cl)) {
                        String triple = "<" + ind.getIRI() + "> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <" + cl.getIRI() + "> .";
                        if(filter.equals("") || triple.toLowerCase().contains(filter.toLowerCase()))
                            System.out.println(triple);
                    }
                }

                if(console != null) {
                    repeat = true;
                    filter = console.readLine("Enter text to filter on or 'exit' to exit: ");

                    if(filter.equalsIgnoreCase("exit"))
                        repeat = false;
                    else
                        System.out.println("\n=== Filtering on '" + filter + "' ===");
                }
            } while(repeat);
        } 
    }

    /**
     * Reasons over the input tree (as an OWL ontology), combined with
     * the phyloreferences (as a separate input). That way, the OWL ontology
     * can be built directly from the phylogeny, while the phyloreferences
     * can be stored and manipulated separately.
     */
    public static Map<OWLClass, Set<OWLNamedIndividual>> getIndividualsByClass(File fTree, File fPhylorefs) throws OWLException, IOException {
        Map results = new HashMap<OWLClass, Set<OWLNamedIndividual>>();
        OWLOntologyManager manager = OWLManager.createOWLOntologyManager();

        // Since our Phyloreferencing ontology hasn't been published,
        // we redirect its IRI to the real URI here. We can fix this
        // once we publish that ontology.
        manager.addIRIMapper(new OWLOntologyIRIMapper() {
            public IRI getDocumentIRI(IRI ontologyIRI) {
                if(ontologyIRI.equals(IRI.create("http://phyloinformatics.net/phyloref.owl"))) {
                    return IRI.create("https://raw.githubusercontent.com/hlapp/phyloref/master/phyloref.owl");
                }

                return null;
            }
        });

        // Load the tree as an OWL ontology.
        OWLOntology ontology = manager.loadOntologyFromOntologyDocument(fTree);

        // Load the phyloreferences.
        OWLParser parser = new ManchesterOWLSyntaxParserFactory().createParser(manager);
        parser.parse(new FileDocumentSource(fPhylorefs), ontology);

        // Reason over it.
        Reasoner hermit = new Reasoner(ontology);

        // Store the sets of individuals belonging to each class in a data
        // structure and return it.
        for(OWLClass clazz: ontology.getClassesInSignature()) {
            results.put(clazz, hermit.getInstances(clazz, false).getFlattened());
        }

        return results;
    }
}
