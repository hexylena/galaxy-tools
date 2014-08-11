<?
// Taken from http://goessner.net/articles/JsonPath/
require_once('json.php');      // JSON parser
require_once('jsonpath-0.8.1.php');  // JSONPath evaluator

$json = implode('', file($argv[1]));
//$should_use_path = ("PATH" === $argv[3]);
$parser = new Services_JSON(SERVICES_JSON_LOOSE_TYPE);
$o = $parser->decode($json);

$jp_args = array($o, $argv[2]);
//if($should_use_path){
        //array_push($jp_args, array("resultType" => "PATH"));
//}

$match = call_user_func_array('jsonPath', $jp_args);
$res = $parser->encode($match);
print "$res\n";

?>
