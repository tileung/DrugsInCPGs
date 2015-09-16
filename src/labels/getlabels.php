<?php
# 
# get drug labels from mesh, nci-t, rxnorm, drugbank, ndf-rt, chebi
#

$fresh = false;
if(array_search("fresh",$argv)) $fresh = true;

$dbs = array(
	"mesh" => "getMESHFromAberOWL",
	"ncit" => "getNCITFromAberOWL",
//	"rxnorm" => "getRXNORMFromAberOWL",
	"drugbank" => "getDrugBankFromBio2RDF",
	"ndfrt" => "getNDFRTFromSource",
	"chebi" => "getCHEBIFromAberOWL"
);
// atc

$found = array();
$result_file = "labels.tab";
$fp = fopen($result_file,"w");
foreach($dbs AS $db) {
	echo "processing $db ";
	$labels = $db();
	foreach( explode("\n",$labels) AS $r) {
		$a = explode("\t",$r);
		$id = $a[0];
		$label = strtolower($a[1]);
		$type = 'label';
		if(isset($a[2])) $type = $a[2];
		$l = filterLabel($label);
		if($l) {
			if(!isset($found[$l])) {
				$found[$l] = '';
				fwrite($fp, "$id\t$label\t$type\n");
	}}}
	echo "\n";
}
fclose($fp);



function filterLabel($label)
{
	if(!isset($label) or strlen($label) < 3 or strlen($label) > 50) return '';
	
	$a = $label[0];
	$b = $label[1];
	$chars = array('(','[','{','-',"'",',');
	foreach($chars AS $char) {
		if($a == $char or $b==$char) return '';
	}
	return $label;
}

function getCHEBIFromAberOWL()
{
	$categories = array('role',"'organic molecule'");
	global $fresh;
	$results['result'] = array();
	
	$file = "drug.labels.chebi.json";
	if(!file_exists($file) or $fresh) {
		echo "downloading CHEBI from AberOWL ... ";
		$buf ='';
		foreach($categories AS $cat) {
			echo $cat." ";
			$url = "http://aber-owl.net/service/api/runQuery.groovy?type=subeq&query=".urlencode($cat)."&ontology=CHEBI&labels=true";
			$buf = file_get_contents($url);
			$result = json_decode($buf, true);
			$results['result'] = array_merge($results['result'], $result['result']);
		}
		file_put_contents($file,json_encode($results));
		echo " done.".PHP_EOL;
	}
	$buf = file_get_contents($file);
	$result = json_decode($buf, true);
	$labels = getLabelsFromAberOWLResult($result, array("label","synonym") );
	return $labels;
}


function getDrugBankFromBio2RDF()
{
	global $fresh;
	$file = "drug.labels.drugbank.tab";
	if(!file_exists($file) or $fresh) {
		echo "downloading DrugBank from Bio2RDF ..";
		$sparql = "PREFIX dv: <http://bio2rdf.org/drugbank_vocabulary:>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX bv: <http://bio2rdf.org/bio2rdf_vocabulary:>
SELECT distinct str(?id) str(?label) str(?p)
{
  ?drug a dv:Drug.
  ?drug bv:identifier ?id .
  {
    ?drug ?p ?label . FILTER (?p = dct:title)
  } UNION {
    ?drug ?p ?s . ?s dct:title ?label . FILTER(?p = dv:synonym)
  } UNION {
    ?drug ?p ?b . ?b dct:title ?label . FILTER(?p = dv:brand)
  }
} ";
		$url = "http://dumontierlab-dev1.stanford.edu:13053/sparql?query=".urlencode($sparql)."&format=text/tab-separated-values";
		$buf = file_get_contents($url);
		file_put_contents($file,str_replace('"','', substr($buf, strpos($buf,"\n")+1)));
		echo "done.".PHP_EOL;
	}
	$labels = file_get_contents($file);
	return $labels;
}

function getNDFRTFromSource()
{
	global $fresh;
	$file = "drug.labels.ndfrt.tab";
	if(!file_exists($file) or $fresh) {
		echo "downloading NDFRT from Source ..";
		$url = "http://evs.nci.nih.gov/ftp1/NDF-RT/NDF-RT.txt";
		$buf = file_get_contents($url);
		file_put_contents($file,$buf);
		echo "done.".PHP_EOL;
	}
	$labels = '';
	$fp = fopen($file,"r");
	while($l = fgets($fp)) {
		$a = explode("\t",$l);
		$id = $a[0];
		$label = trim($a[1]);
		if($label[0] == '[') {
			$label = substr($label, strpos($label,"]")+2);
		}
		$labels .= "$id\t$label\tlabel\n";
	}
	fclose($fp);
	return $labels;
}

function getRXNORMFromAberOWL()
{
	$ctx = stream_context_create(array('http' => array('timeout' => 10000)));
	
	global $fresh;
	$file = "drug.labels.rxnorm.json";
	if(!file_exists($file) or $fresh) {
		echo "downloading RXNORM from AberOWL ..";
		$url = "http://aber-owl.net/service/api/runQuery.groovy?type=subeq&query=%3Chttp://www.w3.org/2002/07/owl%23Thing%3E&ontology=RXNORM";
		$buf = file_get_contents($url,0,$ctx);
		file_put_contents($file,$buf);
		echo "done.".PHP_EOL;
	}
	$buf = file_get_contents($file);
	$result = json_decode($buf, true);
	print_r($result);exit;
	$labels = getLabelsFromAberOWLResult($result, array("synonym"));
	return $labels;
}


function getNCITFromAberOWL()
{
	global $fresh;
	$file = "drug.labels.ncit.json";
	if(!file_exists($file) or $fresh) {
		echo "downloading NCIT from AberOWL ..";
		$url = "http://aber-owl.net/service/api/runQuery.groovy?type=subeq&query=%27drug,%20food,%20chemical%20or%20biomedical%20material%27&ontology=NCIT&labels=true";
		$buf = file_get_contents($url);
		file_put_contents($file,$buf);
		echo "done.".PHP_EOL;
	}
	$buf = file_get_contents($file);
	$result = json_decode($buf, true);
	$labels = getLabelsFromAberOWLResult($result, array("preferred_name","full_syn"));
	return $labels;
}

function getMESHFromAberOWL()
{
	$categories = array('chemical actions and uses','pharmaceutical preparations','organic chemicals','polycyclic compounds');
	global $fresh;
	$results['result'] = array();
	
	$file = "drug.labels.mesh.json";
	if(!file_exists($file) or $fresh) {
		echo "downloading MESH from AberOWL ... ";
		$buf ='';
		foreach($categories AS $cat) {
			echo $cat." ";
			$url = "http://aber-owl.net/service/api/runQuery.groovy?type=subeq&query='".urlencode($cat)."'&ontology=RH-MESH&labels=true";
			$buf = file_get_contents($url);
			$result = json_decode($buf, true);
			$results['result'] = array_merge($results['result'], $result['result']);
		}
		file_put_contents($file,json_encode($results));
		echo " done.".PHP_EOL;
	}
	$buf = file_get_contents($file);
	$result = json_decode($buf, true);
	$labels = getLabelsFromAberOWLResult($result, array("label") );
	return $labels;
}

function getNDFRTFromAberOWL()
{
	$categories = array('Therapeutic Categories','Pharmaceutical Preparations','Chemical Ingredients');
	global $fresh;
	$results['result'] = array();
	
	$file = "drug.labels.ndfrt.json";
	if(!file_exists($file) or $fresh) {
		echo "downloading NDFRT from AberOWL ... ";
		$buf ='';
		foreach($categories AS $cat) {
			echo $cat." ";
			$url = "http://aber-owl.net/service/api/runQuery.groovy?type=subeq&query='".urlencode($cat)."'&ontology=NDF-RT&labels=true";
			$buf = file_get_contents($url);
			$result = json_decode($buf, true);
			$results['result'] = array_merge($results['result'], $result['result']);
		}
		file_put_contents($file,json_encode($results));
		echo " done.".PHP_EOL;
	}
	$buf = file_get_contents($file);
	$result = json_decode($buf, true);
	$labels = getLabelsFromAberOWLResult($result, array("label") );
	return $labels;
}



function getLabelsFromAberOWLResult($result, $fields = null)
{
	$buf = '';
	foreach($result['result'] AS $o) {
		$id = $o['owlClass'];
		if(isset($fields)) {
			foreach($fields AS $field) {
				if(isset($o[$field])) {
					foreach($o[$field] AS $v) {
						$f = filterLabel($v);
						if($f) 
							$buf .= "$id\t$v\t$field\n";
					}
				}
			}
		}
	}
	return $buf;
}


function profileFields($result)
{
	$all = array();
	foreach($result['result'] AS $o) {
		$keys = array_keys($o);
		$all = array_merge($all,$keys);
		$all= array_unique($all);
	}
	print_r($all);
}

