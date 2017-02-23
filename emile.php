<?php


class Endpoint
{
	public $no;
	public $vanilla_time;
	public $caches;
	public $caches_time;
	public $videos;
	public $videos_request;
}

class Cache
{
	public $no;
	public $moved_videos;

	public function isfullfor($lenght)
	{
		$poid = 0;
		if (empty($this->moved_videos))
			return (FALSE);
		foreach ($this->moved_videos as $video_no) {
			$poid += $videos[$video_no];
		}
		$poid += $lenght;
		return ($poid > $GLOBALS['cache_size']);
	}
}

class Video
{
	public $no;
}

if (!isset($argv[1]))
{
	echo "Error in args\n";
	print_r($argv);
	exit();
}
$handle = @fopen($argv[1], "r");
if (!$handle)
{
	echo "Error in file";
	exit();
}

list($videos_nbr, $endpoints_nbr, $requests_desc, $cache_nbr, $GLOBALS['cache_size']) = explode(' ', fgets($handle));

$videos = explode(' ', fgets($handle));

$caches = array();
for ($i=0; $i < $cache_nbr; $i++) { 
	$cache = new Cache;
	$cache->no = $i;
	$cache->moved_videos = array();
	$caches[] = $cache;
}

//echo "Il y a $cache_nbr\n";

$endpoints = array();
for ($i=0; $i < $endpoints_nbr; $i++) { 

	$end = new Endpoint;
	$d = explode(' ', fgets($handle));
	$end->no = $i;
	$end->vanilla_time = $d[0];
	$end->caches = array();
	$end->caches_time = array();
	for ($y=0; $y < $d[1]; $y++) { 
		$e = explode(' ', fgets($handle));
		$end->caches[] = $e[0];
		$end->caches_time[] = $e[1];
	}
	$endpoints[] = $end;
}

while ($str = fgets($handle))
{
	$d = explode(' ', $str);
	$nbr_requests = $d[2]; // nbr request
	$video_no = $d[0]; // video_nbr
	$endpoints_nbr = $d[1]; // antpoint nbr

	$endpoints[$endpoints_nbr]->videos[] = $video_no;
	$endpoints[$endpoints_nbr]->videos_request[] = $nbr_requests;
}

function cmprequests($a, $b){
	return ($GLOBALS['last_endpoint']->videos_request[$a] > $GLOBALS['last_endpoint']->videos_request[$b]);
}
function cmpcaches($a, $b){
	return ($GLOBALS['last_endpoint']->caches_time[$a] > $GLOBALS['last_endpoint']->caches_time[$b]);
}

foreach ($endpoints as $endpoint) {
	$GLOBALS['last_endpoint'] = $endpoint;
	array_multisort($GLOBALS['last_endpoint']->videos_request, $GLOBALS['last_endpoint']->videos, SORT_DESC);
	array_multisort($GLOBALS['last_endpoint']->caches_time, $GLOBALS['last_endpoint']->caches, SORT_ASC);
	/*echo "******\n";
	print_r($GLOBALS['last_endpoint']->videos);
	print_r($GLOBALS['last_endpoint']->videos_request);
	print_r($GLOBALS['last_endpoint']->caches);
	print_r($GLOBALS['last_endpoint']->caches_time);
	echo "******\n";
	/*echo '******\n';
	print_r($endpoint->videos);
	print_r($endpoint->videos_request);
	echo '******\n';
	usort($endpoint->videos, "cmprequests");
	usort($endpoint->caches, "cmpcaches");*/
}


while (true) {
	$stop = true;
	foreach ($caches as $cache) {
		$best_endpoint = NULL;
		$best_endpoint_time;
		
		foreach ($endpoints as $endpoint) {
			if (count($endpoint->videos) == 0)
				continue;
			if (in_array($cache->no, $endpoint->caches))
			{
				//echo "aaa";
				//var_dum//p($videos[$endpoint->videos[0]]);
				if ($cache->isfullfor($videos[$endpoint->videos[0]]))
					continue;
				//echo "zazaza\n";
				$stop = false;
				// 1000  - 900 = 100
				$time = $endpoint->vanilla_time - $endpoint->caches_time[$endpoint->no];
				//var_dump($best_endpoint);
				if (is_null($best_endpoint) || $time < $best_endpoint)
				{
					//echo "LOOL";
					$best_endpoint = $endpoint;
					$best_endpoint_time = $time;
				}
			}
		}
		if ($best_endpoint && $best_endpoint->videos)
		{
			$cache->moved_videos[] = $best_endpoint->videos[0];
			array_shift($best_endpoint->videos);
			array_shift($best_endpoint->videos_request);
		}
	}
	if ($stop)
		break;
}


// Submission
$used_caches = 0;
$str = '';
foreach ($caches as $cache) {
	$used_caches++;
	$str .= $cache->no.' ';
	$i = 0;
	$limit = count($cache->moved_videos);
	foreach ($cache->moved_videos as $video) {
		if (++$i == $limit)
			$str .= $video;
		else
			$str .= $video.' ';
	}
	$str .= "\n";
}

echo $used_caches."\n";
echo $str;