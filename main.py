import sys

def get_input(fd):
    lines = []
    for line in fd.readlines():
        lines.append(line.rstrip())
    return lines

def split_line(line):
    return [c for c in line]

def cache_from_endpoints(endpoints):
  caches = {}
  for endpoint in endpoints:
    for (cache_id, cache_latency) in endpoints['caches']:
      if not cache_id in caches:
        caches[cache_id] = {}
      for (video_id, video_requests) in endpoints['videos']:
        if not video_id in caches[cache_id]['video_requests']:
          caches[cache_id]['video_requests'][video_id] = {}
        caches[cache_id]['video_requests'][video_id][endpoint_id] = video_requests * (endpoints['data_center_latency'] - cache_latency)
  return caches

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

def app_run():
    fd = open(sys.argv[1], "r")
    input = get_input(fd)

    videos_nb, endpoint_nb, request_nb, caches_nb, caches_size = input.pop(0).split(' ')
    videos_sizes = input.pop(0).split(' ')
    endpoints = parse_endpoints_and_requests(input, int(endpoint_nb), int(request_nb))

    import ipdb; ipdb.set_trace()
    caches = caches_from_endpoints(endpoints)

    fd.close()

if __name__ == "__main__":
    try:
        if len(sys.argv) == 2:
            app_run()
    except OSError as e:
        print("Error %s" % e)
