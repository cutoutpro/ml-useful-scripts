import cProfile
import pstats
import time
import os
from pathlib import Path


def profile(f):
  if os.getenv("PROFILING") is None:
    return f

  def _w(*args, **kws):
    profile = cProfile.Profile()
    profile.enable()
    result = f(*args, **kws)
    profile.disable()
    ps = pstats.Stats(profile).sort_stats('name')
    dump_path = Path(__file__).parent / 'logs' / \
        'profiles' / f'profile{time.time()}.pkl'
    ps.dump_stats(dump_path)
    print('profile saved at', dump_path)
    return result

  return _w


def read_profile(profile_path, redirect_to=None, filter='/app'):
  from io import StringIO
  if redirect_to is not None and isinstance(redirect_to, str):
    f = open(redirect_to, 'w')
    ps = pstats.Stats(profile_path, stream=f)
  elif isinstance(redirect_to, StringIO):
    ps = pstats.Stats(profile_path, stream=redirect_to)
  else:
    ps = pstats.Stats(profile_path)
  ps.sort_stats('cumulative').print_stats(filter)
  return redirect_to
  # ps.sort_stats('cumulative').print_stats('/app)


def to_csv_batch(profile_paths, filter='/app', savedir=None):
  import re
  import pandas
  from io import StringIO
  import os.path as osp
  summarys = {
      'ncalls': [],
      'tottime': [],
      'percall_1': [],
      'cumtime': [],
      'percall': [],
  }
  for profile_path in profile_paths:
    summary = {}
    tmp_io = read_profile(profile_path, StringIO(), filter=filter)
    tmp_io.seek(0)
    start = 0
    for line in tmp_io:
      if start and line.strip():
        ncalls, tottime, percall_1, cumtime, percall, key = re.split(
            ' +', line.strip())
        summary[key] = ncalls, tottime, percall_1, cumtime, percall
      if 'tottime' in line:
        start = 1
    for idx, k in enumerate(
        ('ncalls', 'tottime', 'percall_1', 'cumtime', 'percall')):
      summarys[k].append({key: summary[key][idx] for key in summary.keys()})
  dfs = dict([(i, pandas.DataFrame.from_records(summarys[i]))
              for i in ('ncalls', 'tottime', 'percall_1', 'cumtime', 'percall')
              ])
  if savedir is not None:
    for k, v in dfs.items():
      v.to_csv(osp.join(savedir, f'{k}.csv'))
  else:
    return dfs


def example():
  os.environ['PROFILING'] = "1"

  @profile
  def time_costing_func_with_many_steps():
    print('step1')
    print('step2')
    return

  # will log time cost each step in after running this func
  time_costing_func_with_many_steps()
