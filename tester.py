import sys
import time

CACHES_SIZE = 0
VIDEO_SIZES = []

def get_input(fd):
    lines = []
    for line in fd.readlines():
        lines.append(line.rstrip())
    return lines

def split_line(line):
    return [c for c in line]

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

def parse_result(result_lines):
    results = []
    for line in result_lines:
        results.append(line.split(' '))
    return results

def check_size(results, cache_size, video_size):
    for cache in results:
        cache_sum = 0
        for video_id in cache[1::]:
            cache_sum += video_size[int(video_id)]
        if cache_sum > cache_size:
            return False
    return True

def get_score(endpoints, results):
    sum_score = 0
    all_requests = 0
    for endpoint in endpoints:
        for video_id, request_nb in endpoint['videos']:
            all_requests += request_nb
            max_score = request_nb * endpoint['data_center_latency']
            time_score = endpoint['data_center_latency']
            for cache_id, timeresp in endpoint['caches']:
                for result in results:
                    if result[0] == str(cache_id) and str(video_id) in result[1::]:
                        if timeresp < time_score:
                            time_score = timeresp
            score = request_nb * time_score
            sum_score += abs(score - max_score)
    return (sum_score*1000) / all_requests


def app_run():
    with open(sys.argv[1], "r") as fd:
        input = get_input(fd)

    with open(sys.argv[2], "r") as fd:
        results = get_input(fd)

    results.pop(0)
    results = parse_result(results)

    videos_nb, endpoint_nb, request_nb, caches_nb, caches_size = input.pop(0).split(' ')
    CACHES_SIZE = int(caches_size)
    for size in input.pop(0).split(' '):
        VIDEO_SIZES.append(int(size))

    if check_size(results, CACHES_SIZE, VIDEO_SIZES) == False:
        raise Exception("Error cache size exceeded")
    endpoints = parse_endpoints_and_requests(input, int(endpoint_nb), int(request_nb))
    print("Score: %d" % int(get_score(endpoints, results)))


if __name__ == "__main__":
    try:
        if len(sys.argv) == 3:
            try:
                app_run()
            except Exception as e:
                print(e)
    except OSError as e:
        print("Error %s" % e)