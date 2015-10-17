<?php
# 
# get indications from sider	
#

$fresh = false;
if(array_search("fresh",$argv)) $fresh = true;

$dbs = array(
	"sider" => "getIndicationsFromSIDERBio2RDF"
);
$cpgindications = getCPGIndications();

$found = array();
$result_file = "indications.tab";
$fp = fopen($result_file,"w");
foreach($dbs AS $db) {
	echo "processing $db ";
	$indications = $db();

	$list = explode("\n",$indications);
	foreach($list AS $l) {
		$a = explode("\t",$l);
		$drug = substr($a[1], strpos($a[1], "drugbank:")+9);
		$cui = substr($a[3], strpos($a[3], "umls:")+5);
		$indication_drugs[ $cui ][$drug] = '';
	}
	$buf = '';
	foreach($cpgindications AS $cpg_indication => $v) {
		if(isset($indication_drugs[  $cpg_indication ])) {
			$drugs = $indication_drugs [$cpg_indication];
			foreach($drugs AS $drug => $v) {
				$buf .= "$cpg_indication\t$drug\n";				
			}
		};
		
	}
	
	fwrite($fp, $buf);
	echo "\n";
}
fclose($fp);




function getIndicationsFromSIDERBio2RDF()
{
	global $fresh;
	$file = "drug.indications.sider.tab";
	if(!file_exists($file) or $fresh) {
		echo "getting SIDER Indications from Bio2RDF ..";
		$sparql = "PREFIX sv: <http://bio2rdf.org/sider_vocabulary:>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX dv: <http://bio2rdf.org/drugbank_vocabulary:>
PREFIX dct: <http://purl.org/dc/terms/>
SELECT ?pc ?dbdrug str(?dbdrug_label) ?indication
{ ?dia a sv:Drug-Indication-Association; sv:drug ?drug; sv:indication ?indication; sv:provenance \"NLP_indication\"^^xsd:string . ?drug sv:x-pubchem.compound ?pc .
  ?dbdrug ?p ?pc .
  ?dbdrug a dv:Drug; ?p ?pc; dct:title ?dbdrug_label .  
} ";
		$url = "http://localhost:8890/sparql?query=".urlencode($sparql)."&format=text/tab-separated-values";
		$buf = file_get_contents($url);
		file_put_contents($file,str_replace('"','', substr($buf, strpos($buf,"\n")+1)));
		echo "done.".PHP_EOL;
	}
	$results = file_get_contents($file);
	return $results;
}

function getCPGIndications()
{
	$filename = "MedicareCDW_CUIs.tab";
	$fp = fopen($filename,"r");
	while($l = fgets($fp)) {
		$a = explode("\t",trim($l));
		list($icd9,$cui,$cat,$disease) = $a;
		$list[$cui] = '';
	}
	return $list;	
}