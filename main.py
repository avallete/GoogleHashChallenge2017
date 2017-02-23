import sys

CACHES_SIZE = 0
VIDEOS_SIZES = []

def get_input(fd):
    lines = []
    for line in fd.readlines():
        lines.append(line.rstrip())
    return lines


def split_line(line):
    return [c for c in line]


def caches_from_endpoints(endpoints):
    caches = {}
    for endpoint in endpoints:
        for (cache_id, cache_latency) in endpoint['caches']:
            if not cache_id in caches:
                caches[cache_id] = {'video_requests': {}}
            for (video_id, video_requests) in endpoint['videos']:
                if not video_id in caches[cache_id]['video_requests']:
                    caches[cache_id]['video_requests'][video_id] = {}
                caches[cache_id]['video_requests'][video_id][endpoints.index(endpoint)] = video_requests * (
                endpoint['data_center_latency'] - cache_latency)
    return caches

def compute_video_score(cache_score_dict):
    sum_score = 0
    for score in cache_score_dict.values():
        sum_score += score
    return sum_score

def get_video_max_id_from_cache(cache):
    current_id = 0
    current_max_score = 0
    for video_id, cache_dict in cache['video_requests'].items():
        video_score = compute_video_score(cache_dict)
        if video_score > current_max_score:
            current_id = video_id
            current_max_score = video_score
    return current_id

def best_cache_for_vid(caches, video_id):
    max = (0, 0)
    for cache in caches:
        if cache['video_requests'][video_id]:
            score = compute_video_score(cache['video_requests'][video_id])
            if score > max[1]:
                max = (caches.index(cache), score)
    return max[0];

def parse_endpoint(latency, caches_numbers, input):
    endpoint = {'caches': [], 'videos': [], 'data_center_latency': latency}
    for i in range(0, caches_numbers):
        cache_id, cache_latency = input.pop(0).split(' ')
        endpoint['caches'].append((int(cache_id), int(cache_latency)))
    return endpoint


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

def cache_video(caches, cache_id, video_id):
    del caches[cache_id]['video_requests'][video_id]
    if caches[cache_id]['used_size'] + VIDEO_SIZES[video_id] > CACHES_SIZE:
        return
    caches[cache_id]['cached_videos'].append(video_id)
    caches[cache_id]['used_size'] += VIDEO_SIZES[video_id]
    # reduce score on other caches

def app_run():
    fd = open(sys.argv[1], "r")
    input = get_input(fd)

    videos_nb, endpoint_nb, request_nb, caches_nb, caches_size = input.pop(0).split(' ')
    CACHES_SIZE = int(caches_size)
    for size in input.pop(0).split(' '):
        VIDEOS_SIZES.append(int(size))
    endpoints = parse_endpoints_and_requests(input, int(endpoint_nb), int(request_nb))

    caches = caches_from_endpoints(endpoints)
    fd.close()


if __name__ == "__main__":
    try:
        if len(sys.argv) == 2:
            app_run()
    except OSError as e:
        print("Error %s" % e)
