/**
 * A simple tool to validate triples against SHACL shapes.
 *
 * Synopsis: java -cp $CLASSPATH testShacl shapes.ttl data.ttl
 *
 * Note that the CLASSPATH needs to include:
 * <ul>
 *  <li>SHACL library (https://github.com/TopQuadrant/shacl)</li>
 *  <li>Apache Jena (https://jena.apache.org/)</li>
 * </ul>
 *
 * @author      Gaurav Vaidya <gaurav@ggvaidya.com>
 * @version     0.1
 */

import org.apache.jena.rdf.model.*;
import org.apache.jena.vocabulary.*;
import org.apache.jena.util.*;
import org.apache.jena.query.*;
import org.topbraid.shacl.arq.*;
import org.topbraid.shacl.util.*;
import org.topbraid.shacl.model.*;
import org.topbraid.spin.arq.*;
import org.topbraid.spin.util.*;
import org.topbraid.spin.progress.*;
import org.topbraid.shacl.constraints.*;
import org.topbraid.shacl.vocabulary.*;
import java.io.*;
import java.net.*;
import java.util.*;

/**
 * A command-line tool to test whether a given XML file conforms to
 * a set of SHACL shapes in a given Turtle file.
 */
public class testShacl {

    /**
     * Version string.
     */
    public static final String Version = "0.1";

    /**
     * Check command line arguments, load files as Jena models,
     * then pass them on to {@link #testSHACLModel(Model, Model)}.
     */ 
    public static void main(String[] args) {
        // Count the command line arguments.
        if(args.length == 1) {
            if(args[0].equalsIgnoreCase("--version")) {
                System.out.println("testShacl " + testShacl.Version);
                System.exit(0);
            } else if(args[0].equalsIgnoreCase("--help")) {
                System.out.println("testShacl shapes.ttl data.xml");
                System.out.println(" - shapes.ttl: SHACL shapes to test (as a Turtle file)");
                System.out.println(" - data.xml: data to validate (as RDF/XML)");
                System.exit(0);
            }
        } 
        
        if(args.length != 2) {
            System.err.println("Two arguments required: the path to the SHACL shapes to test (as a Turtle file) and the path to the data to test (as an RDF file).");

            System.exit(1);
        }

        Model shapesModel = JenaUtil.createMemoryModel();
        Model dataModel = JenaUtil.createMemoryModel();
        try {
            // Load shapes file.
            String shapesFilename = args[0];
            shapesModel.read(
                new FileInputStream(new File(shapesFilename)),
                null,
                FileUtils.langTurtle
            );
            
            // Load data file.
            String dataFilename = args[1];
            dataModel.read(
                new FileInputStream(new File(dataFilename)),
                null,
                FileUtils.langXML
            );
        } catch(IOException e) {
            System.err.println("Could not read file: " + e);
            System.exit(1);
        }

        // Validate the model from the data file against
        // the shapes in the shapes file.
        Model results = validateSHACL(shapesModel, dataModel);

        // Note that if validation fails entirely, we'll still
        // end up with zero triples in the results model -- which
        // will look like successful validation!
        if(results.size() == 0) {
            // System.err.println("Validation passed successfully.");
            System.exit(0);
        } else {
            System.err.println("Validation failed.\n");

            // If this is the only output to System.out, we can 
            // read System.out as Turtle.
            System.out.println(ModelPrinter.get().print(results));

            System.exit(1);
        }
    }

    /**
     * Validate a SHACL model against the provided data.
     */
    public static Model validateSHACL(Model shapesModel, Model dataModel) {

        // Validation can't proceed without core SHACL definitions
        // from 'shacl.ttl' and 'dash.ttl'.
        Model coreSHACLModel = JenaUtil.createMemoryModel();
        try {
            shapesModel.read(
                new FileInputStream(new File("dash.ttl")),
                null,
                FileUtils.langTurtle
            );
            shapesModel.read(
                new FileInputStream(new File("shacl.ttl")),
                null,
                FileUtils.langTurtle
            );
        } catch(IOException e) {
            throw new RuntimeException("Could not load 'shacl.ttl' and 'dash.ttl': " + e);
        }

        // Register any SHACL functions we have.
        SHACLFunctions.registerFunctions(shapesModel);

        // System.err.println(ModelPrinter.get().print(completeShapesModel));

        // Create a dataset containing both the shapes model and the data model.
        URI shapesGraphURI = URI.create("urn:x-shacl-shapes-graph:" + UUID.randomUUID().toString());
        Dataset dataset = ARQFactory.get().getDataset(dataModel);
        dataset.addNamedModel(shapesGraphURI.toString(), shapesModel);

        // System.err.println(ModelPrinter.get().print(dataModel));

        // Validate this dataset.
        Model results;
        try {
            results = ModelConstraintValidator.get().validateModel(
                dataset,
                shapesGraphURI,
                null,
                true,
                null,
                null 
            );
        } catch(InterruptedException e) {
            throw new RuntimeException("Impossible code branch: it should be impossible to interrupt model validation without providing a progress monitor.");
        }

        return results;
    }
}
