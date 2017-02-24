import sys
import time
import functools
import operator

FUNCTIONS_TIMES = {}
CACHES_SIZE = 0
VIDEO_SIZES = []

def timeit(func):
    @functools.wraps(func)
    def newfunc(*args, **kwargs):
        startTime = time.time()
        ret = func(*args, **kwargs)
        elapsedTime = time.time() - startTime
        if func.__name__ in FUNCTIONS_TIMES.keys():
            FUNCTIONS_TIMES[func.__name__] += elapsedTime
        else:
            FUNCTIONS_TIMES[func.__name__] = elapsedTime
        return ret
    return newfunc


@timeit
def get_input(fd):
    lines = []
    for line in fd.readlines():
        lines.append(line.rstrip())
    return lines

@timeit
def split_line(line):
    return [c for c in line]


@timeit
def caches_from_endpoints(endpoints):
    caches = {}
    for endpoint in endpoints:
        for (cache_id, cache_latency) in endpoint['caches']:
            if not cache_id in caches:
                caches[cache_id] = {'video_requests': {}, 'used_size': 0, 'cached_videos': []}
            for (video_id, video_requests) in endpoint['videos']:
                if not video_id in caches[cache_id]['video_requests']:
                    caches[cache_id]['video_requests'][video_id] = {}
                caches[cache_id]['video_requests'][video_id][endpoints.index(endpoint)] = video_requests * (
                endpoint['data_center_latency'] - cache_latency)
    return caches

@timeit
def compute_video_score(cache_score_dict):
    sum_score = 0
    for score in cache_score_dict.values():
        sum_score += score
    return sum_score

@timeit
def get_video_max_id_from_cache(cache):
    current_id = 0
    current_max_score = 0
    for video_id, cache_dict in cache['video_requests'].items():
        video_score = compute_video_score(cache_dict)
        if video_score > current_max_score:
            current_id = video_id
            current_max_score = video_score
    return current_id

@timeit
def best_cache_for_vid(caches, video_id):
    max = (0, 0)
    for c_id, cache in caches.items():
        if video_id in cache['video_requests'].keys():
            score = compute_video_score(cache['video_requests'][video_id])
            if score > max[1]:
                max = (c_id, score)
    return max[0]

@timeit
def parse_endpoint(latency, caches_numbers, input):
    endpoint = {'caches': [], 'videos': [], 'data_center_latency': latency}
    for i in range(0, caches_numbers):
        cache_id, cache_latency = input.pop(0).split(' ')
        endpoint['caches'].append((int(cache_id), int(cache_latency)))
    return endpoint

@timeit
def parse_endpoints_and_requests(input, endpoint_nb, request_nb):
    endpoints = []

    for i in range(0, (int(endpoint_nb))):
        latency, caches_numbers = input.pop(0).split(' ')
        if int(caches_numbers) > 0:
            endpoints.append(parse_endpoint(int(latency), int(caches_numbers), input))
        else:
            endpoints.append({'caches': [], 'videos': [], 'data_center_latency': int(latency)})
    for k in range(0, int(request_nb)):
        video_id, endpoint_id, requests = input.pop(0).split(' ')
        endpoints[int(endpoint_id)]['videos'].append((int(video_id), int(requests)))
    return endpoints

@timeit
def cache_video(caches, cache_id, video_id, caches_size):
    endpoints = caches[cache_id]['video_requests'][video_id]
    del caches[cache_id]['video_requests'][video_id]
    if caches[cache_id]['used_size'] + VIDEO_SIZES[video_id] > caches_size:
        return
    caches[cache_id]['cached_videos'].append(str(video_id))
    caches[cache_id]['used_size'] += VIDEO_SIZES[video_id]
    for cache in caches.values():
        for ep in endpoints:
            if video_id in cache['video_requests'] and ep in cache['video_requests'][video_id]:
                del cache['video_requests'][video_id][ep]
                if len(cache['video_requests'][video_id]) == 0:
                    del cache['video_requests'][video_id]

def print_result(caches):
    print (len(caches))
    for cache_id, data in caches.items():
        print ("%s %s" % (cache_id, " ".join(data['cached_videos'])))

def print_total_times():
    sorted_function_times = sorted(FUNCTIONS_TIMES.items(), key=operator.itemgetter(1))
    for func_name, timetotal in sorted_function_times:
        percent_on_time = (timetotal / (FUNCTIONS_TIMES["app_run"] / 100))
        print('function [{}] finished in {} ms {}% of total program time.'.format(func_name, int(timetotal * 1000), int(percent_on_time)), file=sys.stderr)

@timeit
def app_run():

    with open(sys.argv[1], "r") as fd:
        input = get_input(fd)

    videos_nb, endpoint_nb, request_nb, caches_nb, caches_size = input.pop(0).split(' ')
    CACHES_SIZE = int(caches_size)
    for size in input.pop(0).split(' '):
        VIDEO_SIZES.append(int(size))
    endpoints = parse_endpoints_and_requests(input, int(endpoint_nb), int(request_nb))
    caches = caches_from_endpoints(endpoints)

    for c_id, cache in caches.items():
        while len(cache['video_requests']) > 0:
            video_id = get_video_max_id_from_cache(cache)
            cache_id = best_cache_for_vid(caches, video_id)
            cache_video(caches, cache_id, video_id, int(caches_size))
    print_result(caches)


if __name__ == "__main__":
    try:
        if len(sys.argv) == 2:
            app_run()
            print_total_times()
    except OSError as e:
        print("Error %s" % e)
