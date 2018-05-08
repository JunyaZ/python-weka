import weka.core.jvm as jvm
import pandas as pd
import glob
import sys
import weka.core.packages as pkg
from weka.core.converters import Loader
import weka.core.converters as converters
from weka.attribute_selection import ASSearch, ASEvaluation, AttributeSelection
from weka.classifiers import Classifier
from weka.classifiers import Evaluation
from weka.core.classes import Random
from weka.classifiers import PredictionOutput, KernelClassifier, Kernel
import weka.core.packages as packages
# start JVM with packages
jvm.start(packages=True)
 
# package install
chisq_name = "EvolutionarySearch"
chisq_installed = False
for p in pkg.installed_packages():
    if p.name == chisq_name:
        chisq_installed = True
if not chisq_installed:
    pkg.install_package(chisq_name)
    print("pkg %s installed, please restart" % chisq_name)
    jvm.stop()
    sys.exit(1)
   
data_dir = "\\\\egr-1l11qd2\\CLS_lab\\Junya Zhao\\GWAS SNPs_2018\\random50_combo_Nonoverlap_\\"
globbed_files = glob.glob(data_dir +"*.csv")
for csv in globbed_files:
    data = converters.load_any_file(csv)
    data.class_is_last()
    search = ASSearch(classname="weka.attributeSelection.BestFirst", options=["-D","1","-N","10"])
    evaluator = ASEvaluation(classname="weka.attributeSelection.CfsSubsetEval", options=["-P","1","E","1"])
    attsel = AttributeSelection()
    attsel.folds(10)
    attsel.crossvalidation(True)
    attsel.seed(1)
    attsel.search(search)
    attsel.evaluator(evaluator)
    attsel.select_attributes(data)
    evl= Evaluation(data)
    print("# attributes: " + str(attsel.number_attributes_selected))
    print("attributes: " + str(attsel.selected_attributes))
    print("result string:\n" + attsel.results_string)
    print(evl)
    # write the report for each file 
    with open(f"{csv}._BestFirstreport.csv","a") as outfile:  
        outfile.write(attsel.results_string)
   # with open(f"{csv}._BestFirstlabel.csv","a") as output:
       # output.write(str(attsel.selected_attributes))
       # output.write(str(attsel.number_attributes_selected))

jvm.stop()
