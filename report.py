#!/usr/bin/env python3
# 
# Reports what you are spending your time on
# 
# Copyright (c) 2019 Johannes Buchner
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import os
import datetime
from collections import Counter
import re
import json

dir = os.path.expanduser('~/.local/share/activitytracker/')

def load_patterns():
	patterns = []
	for line in open(dir + 'classes'):
		if line.startswith('#'): continue	
		if line.strip() == '': continue	
		activity_class, pattern = line.strip().split('\t', 1)
		patterns.append((activity_class, re.compile(pattern)))
	return patterns

patterns = load_patterns()
classes = sorted({activity_class for activity_class, _ in patterns})

def find_matching_pattern(title):
	for pattern_class, pattern in patterns:	
		if pattern.search(title) is not None:
			return pattern_class
	

t0 = datetime.datetime.now()


def read_classes():
	#lastt = None
	lastclass = None
	lasttitle = None

	for line in open(dir + 'log'):
		try:
			item = json.loads(line.strip())
		except json.decoder.JSONDecodeError:
			#print("Issue parsing line '%s'" % line.strip())
			continue
		t, nevents, title = item.get('timestamp'), item.get('nevents',1), item.get('windowname','') + ' :: ' + item.get('exe','')

		t = datetime.datetime.fromtimestamp(t)
		
		if nevents < 1:
			continue
		
		#if lastt is not None and (t - lastt).days > 7:
		#	continue

		#lastt = t
		if lasttitle is not None and title == lasttitle:
			activity_class = lastclass
		else:
			activity_class = find_matching_pattern(title)
		
		if activity_class is None:
			activity_class = 'unclassified'
		
		yield item, t, title, activity_class
		
		lasttitle, lastclass = title, activity_class


# we want each row to be a 30 minute window
# and compute the fraction of time spent on each category
# and plot over time

def read_buckets():
	lastbucket = None
	currentcounter = Counter()
	knowncounter = Counter()
	unknowncounter = Counter()

	for item, time, title, activity_class in read_classes():
		startofyear = datetime.date(year=time.year,month=1,day=1)
		startofday = datetime.datetime(year=time.year,month=time.month,day=time.day,hour=0,minute=0,second=0, tzinfo=time.tzinfo)
		timebucket = (
			time.year, 
			(time.date() - startofyear).days,
			int((time - startofday).total_seconds() / 60 / 15),
		)
		#print(time, time.tzinfo, timebucket)
		if lastbucket is None or lastbucket != timebucket:
			if lastbucket is not None:
				yield lastbucket, currentcounter, knowncounter, unknowncounter
			currentcounter = Counter()
			knowncounter = Counter()
			unknowncounter = Counter()
		
		if activity_class == 'unclassified':
			unknowncounter[title] += 1
		else:
			knowncounter[title] += 1
		currentcounter[activity_class] += 1
		lastbucket = timebucket
	
	if lastbucket is not None:
		yield lastbucket, currentcounter, knowncounter, unknowncounter

def fmt(c,s):
	if c > s * 3 / 4:
		return '===='
	elif c > s * 2 / 4:
		return '=== '
	elif c > s * 1 / 4:
		return '==  '
	elif c > s * 1 / 10:
		return '=   '
	else:
		return '    '

print('DDD HH %s' % (' '.join(['%-4s' % c[:4] for c in classes])))
lastbucket = None
for bucket, counter, knowns, unknowns in read_buckets():
	s = sum(counter.values())
	u = ''
	if unknowns:
		mostcommon, nunknown = unknowns.most_common(1)[0]
		if nunknown * 10 > s or True:
			u = ' | %.2f%%: %s' % (nunknown * 100 / s, mostcommon)
	else:
		mostcommon, n = knowns.most_common(1)[0]
		u = ' | %.2f%%: %s' % (n * 100 / s, mostcommon)
	
	if lastbucket is not None and bucket[1] != lastbucket[1]:
		print()
	print('%3d %2d %s%s' % (bucket[1], bucket[2]//4, ' '.join([fmt(counter[c], s) for c in classes]), u))
	lastbucket = bucket
		
	


